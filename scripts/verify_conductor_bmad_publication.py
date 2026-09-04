#!/usr/bin/env python3
"""Build and verify an exact public companion delta without touching source Git state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path


FORBIDDEN_PREFIXES = ("artifacts/", "docs/Conductor/runs/")
PUBLIC_PREFIXES = (
    "docs/adapters/bmad/", "plugin-src/conductor-bmad/",
    "plugins/conductor-bmad/", "plugins/conductor-bmad-claude/",
)
PUBLIC_EXACT = {
    ".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json",
    "docs/CHANGELOG.md", "docs/PROJECT_STATE.md", "docs/ROADMAP.md",
    "scripts/build_conductor_plugins.py", "scripts/build_conductor_bmad_plugins.py",
    "scripts/verify_conductor_bmad_publication.py",
    "plugins/conductor/payload/OWNERSHIP.json",
    "plugins/conductor-claude/payload/OWNERSHIP.json",
    "plugins/conductor/payload/docs/CHANGELOG.md",
    "plugins/conductor/payload/docs/PROJECT_STATE.md",
    "plugins/conductor/payload/docs/ROADMAP.md",
    "plugins/conductor-claude/payload/docs/CHANGELOG.md",
    "plugins/conductor-claude/payload/docs/PROJECT_STATE.md",
    "plugins/conductor-claude/payload/docs/ROADMAP.md",
}
PRIVACY_RULES = {
    "local_home": re.compile(r"/Users/[^/\s]+/"),
    "customer": re.compile(r"Symphony|AuditEdge|website_sales", re.I),
    "enterprise_profile": re.compile(r"Claude Enterprise", re.I),
    "private_key": re.compile(r"BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY"),
    "token": re.compile(r"(?:sk-|gh[pousr]_)[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),
}
VOLATILE_REF_PREFIX = "refs/codex/turn-diffs/"
PRIVACY_EXCEPTIONS = (
    ("scripts/verify_conductor_bmad_publication.py", "local_home", "/Users/[^/", "Privacy-rule definition only."),
    ("scripts/verify_conductor_bmad_publication.py", "local_home", "/Users/person/", "Exact negative-fixture definition only."),
    ("scripts/verify_conductor_bmad_publication.py", "customer", "Symphony", "Privacy-rule definition only."),
    ("scripts/verify_conductor_bmad_publication.py", "customer", "AuditEdge", "Privacy-rule definition only."),
    ("scripts/verify_conductor_bmad_publication.py", "customer", "website_sales", "Privacy-rule definition only."),
    ("scripts/verify_conductor_bmad_publication.py", "enterprise_profile", "Claude Enterprise", "Privacy-rule definition only."),
    ("tests/test_conductor_bmad_docs_privacy.py", "customer", "Symphony", "Negative privacy-test fixture only."),
    ("tests/test_conductor_bmad_docs_privacy.py", "customer", "AuditEdge", "Negative privacy-test fixture only."),
    ("tests/test_conductor_bmad_docs_privacy.py", "customer", "website_sales", "Negative privacy-test fixture only."),
    ("tests/test_conductor_bmad_docs_privacy.py", "enterprise_profile", "Claude Enterprise", "Negative privacy-test fixture only."),
    ("tests/test_conductor_bmad_publication.py", "local_home", "/Users/person/", "Negative privacy-test fixture only."),
    ("tests/test_conductor_bmad_publication.py", "customer", "AuditEdge", "Negative privacy-test fixture only."),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def public_path(path: str) -> bool:
    return (
        path in PUBLIC_EXACT
        or path.startswith(PUBLIC_PREFIXES)
        or (path.startswith("scripts/verify_conductor_bmad_") and path.endswith(".sh"))
        or (path.startswith("tests/test_conductor_bmad_") and path.endswith(".py"))
    ) and not path.startswith(FORBIDDEN_PREFIXES)


def changed(root: Path) -> list[str]:
    tracked = git(root, "diff", "--name-only").splitlines()
    untracked = git(root, "ls-files", "--others", "--exclude-standard").splitlines()
    return sorted(set(tracked + untracked))


def base_bytes(root: Path, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"], cwd=root, capture_output=True
    )
    return result.stdout if result.returncode == 0 else None


def scan_privacy(path: str, data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return ["non_utf8"]
    allowed = {
        (rule_id, literal)
        for exception_path, rule_id, literal, _ in PRIVACY_EXCEPTIONS
        if exception_path == path
    }
    violations = []
    for name, rule in PRIVACY_RULES.items():
        if any((name, match.group(0)) not in allowed for match in rule.finditer(text)):
            violations.append(name)
    return violations


def exception_records(paths: set[str]) -> list[dict[str, str]]:
    records = []
    for path, rule_id, literal, rationale in PRIVACY_EXCEPTIONS:
        if path not in paths:
            continue
        text = Path(path).read_text()
        if literal not in {match.group(0) for match in PRIVACY_RULES[rule_id].finditer(text)}:
            raise RuntimeError(f"stale privacy exception: {path}:{rule_id}:{literal}")
        records.append({"path": path, "rule_id": rule_id, "literal": literal, "rationale": rationale})
    return records


def build_manifest(root: Path, output: Path) -> dict[str, object]:
    entries = []
    unclassified = []
    for relative in changed(root):
        if relative.startswith(FORBIDDEN_PREFIXES):
            continue
        if not public_path(relative):
            unclassified.append(relative)
            continue
        path = root / relative
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise RuntimeError(f"non-regular public path: {relative}")
        data = path.read_bytes()
        violations = scan_privacy(relative, data)
        if violations:
            raise RuntimeError(f"privacy violation {relative}: {violations}")
        previous = base_bytes(root, relative)
        entries.append({
            "operation": "MODIFY" if previous is not None else "ADD",
            "path": relative,
            "kind": "file",
            "mode": stat.S_IMODE(metadata.st_mode),
            "source_sha256": sha(data),
            "base_sha256": sha(previous) if previous is not None else None,
            "classification": "PUBLIC_CANONICAL" if relative.startswith("docs/") or "/payload/docs/" in relative else "PUBLIC_PRODUCT",
        })
    if unclassified:
        raise RuntimeError("unclassified candidate paths: " + ", ".join(unclassified))
    core = {
        "schema": "conductor.publication-manifest.v1",
        "base_commit": git(root, "rev-parse", "HEAD").strip(),
        "entries": entries,
        "privacy_exceptions": exception_records({item["path"] for item in entries}),
        "authority_grants": [],
    }
    payload = {**core, "aggregate_sha256": sha(json.dumps(core, sort_keys=True, separators=(",", ":")).encode())}
    write(output, payload)
    return payload


def validate_manifest(root: Path, manifest: dict[str, object], contract: dict[str, object] | None = None) -> None:
    if manifest.get("schema") != "conductor.publication-manifest.v1" or manifest.get("authority_grants") != []:
        raise RuntimeError("manifest identity or authority invalid")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("manifest entries invalid")
    paths = [item.get("path") for item in entries if isinstance(item, dict)]
    if len(paths) != len(entries) or len(set(paths)) != len(paths) or len({str(p).lower() for p in paths}) != len(paths):
        raise RuntimeError("duplicate or case-colliding path")
    if manifest.get("privacy_exceptions") != exception_records(set(paths)):
        raise RuntimeError("privacy exceptions are not exact path+rule+literal records")
    if manifest.get("base_commit") != git(root, "rev-parse", "HEAD").strip():
        raise RuntimeError("manifest base commit is stale")
    if contract is not None:
        if contract.get("schema_version") != 1 or contract.get("authority_grants") != []:
            raise RuntimeError("publication contract invalid")
        if set(contract.get("forbidden_prefixes", [])) != set(FORBIDDEN_PREFIXES):
            raise RuntimeError("publication contract prefix policy mismatch")
    for item in entries:
        path = item["path"]
        if item.get("operation") not in {"ADD", "MODIFY"} or item.get("kind") != "file" or not public_path(path):
            raise RuntimeError(f"invalid manifest entry: {path}")
        if contract is not None:
            required = set(contract.get("required_fields", []))
            if not required.issubset(item) or item["operation"] not in contract.get("allowed_operations", []) or item["kind"] not in contract.get("allowed_kinds", []) or item.get("classification") not in contract.get("allowed_classifications", []):
                raise RuntimeError(f"contract violation: {path}")
        source = root / path
        if source.is_symlink() or not source.is_file() or sha(source.read_bytes()) != item.get("source_sha256") or stat.S_IMODE(source.stat().st_mode) != item.get("mode"):
            raise RuntimeError(f"stale source: {path}")
        violations = scan_privacy(path, source.read_bytes())
        if violations:
            raise RuntimeError(f"privacy violation {path}: {violations}")
        previous = base_bytes(root, path)
        expected = sha(previous) if previous is not None else None
        if expected != item.get("base_sha256"):
            raise RuntimeError(f"stale base preimage: {path}")
    core = {key: value for key, value in manifest.items() if key != "aggregate_sha256"}
    if sha(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()) != manifest.get("aggregate_sha256"):
        raise RuntimeError("manifest aggregate invalid")


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise RuntimeError("JSON object required")
    return value


def parse_refs(records: list[str]) -> dict[str, str]:
    parsed = {}
    for record in records:
        object_id, separator, ref = record.partition(" ")
        invalid_character = any(
            character.isspace() or ord(character) < 32 or character in "~^:?*[\\"
            for character in ref
        )
        if (
            not separator
            or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id)
            or not ref.startswith("refs/")
            or ref.endswith(("/", "."))
            or "//" in ref
            or ".." in ref
            or "@{" in ref
            or invalid_character
        ):
            raise RuntimeError(f"invalid ref record: {record!r}")
        if ref in parsed:
            raise RuntimeError(f"duplicate ref record: {ref}")
        parsed[ref] = object_id
    return parsed


def partition_refs(refs: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    volatile = {
        ref: object_id
        for ref, object_id in refs.items()
        if ref.startswith(VOLATILE_REF_PREFIX)
    }
    stable = {ref: object_id for ref, object_id in refs.items() if ref not in volatile}
    return stable, volatile


def ref_aggregate(refs: dict[str, str]) -> str:
    return sha(json.dumps(refs, sort_keys=True, separators=(",", ":")).encode())


def volatile_disclosure(before: dict[str, str], after: dict[str, str]) -> dict[str, object]:
    added = [
        {"ref": ref, "object_id": after[ref]}
        for ref in sorted(after.keys() - before.keys())
    ]
    removed = [
        {"ref": ref, "object_id": before[ref]}
        for ref in sorted(before.keys() - after.keys())
    ]
    changed = [
        {"ref": ref, "before": before[ref], "after": after[ref]}
        for ref in sorted(before.keys() & after.keys())
        if before[ref] != after[ref]
    ]
    return {
        "prefix": VOLATILE_REF_PREFIX,
        "before_count": len(before),
        "after_count": len(after),
        "added": added,
        "removed": removed,
        "changed": changed,
        "before_sha256": ref_aggregate(before),
        "after_sha256": ref_aggregate(after),
    }


def source_identity_snapshot(root: Path) -> dict[str, object]:
    return {
        "schema": "conductor.publication-baseline.v1",
        "head": git(root, "rev-parse", "HEAD").strip(),
        "branch": git(root, "branch", "--show-current").strip(),
        "remotes": git(root, "remote", "-v").splitlines(),
        "refs": git(root, "for-each-ref", "--format=%(objectname) %(refname)").splitlines(),
    }


def protected_inventory(root: Path, prefixes: tuple[str, ...], excluded: set[str] | None = None) -> dict[str, dict[str, object]]:
    excluded = excluded or set()
    records: dict[str, dict[str, object]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if relative in excluded or not any(relative == prefix.rstrip("/") or relative.startswith(prefix) for prefix in prefixes):
            continue
        metadata = path.lstat()
        record: dict[str, object] = {
            "path": relative,
            "mode": stat.S_IMODE(metadata.st_mode),
        }
        if stat.S_ISREG(metadata.st_mode):
            record.update(kind="file", sha256_or_symlink_target=sha(path.read_bytes()))
        elif stat.S_ISLNK(metadata.st_mode):
            record.update(kind="symlink", sha256_or_symlink_target=os.readlink(path))
        else:
            continue
        records[relative] = record
    return records


def baseline_protected_inventory(baseline: dict[str, object], prefixes: tuple[str, ...], excluded: set[str]) -> dict[str, dict[str, object]]:
    entries = baseline.get("entries")
    if not isinstance(entries, dict):
        raise RuntimeError("publication baseline entries invalid")
    records: dict[str, dict[str, object]] = {}
    for path, source in entries.items():
        if not isinstance(path, str) or path in excluded or not any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in prefixes):
            continue
        if not isinstance(source, dict) or source.get("kind") not in {"file", "symlink"} or not isinstance(source.get("mode"), int) or not isinstance(source.get("sha256"), str):
            raise RuntimeError(f"publication baseline record invalid: {path}")
        records[path] = {
            "path": path,
            "kind": source["kind"],
            "mode": source["mode"],
            "sha256_or_symlink_target": source["sha256"],
        }
    return records


def require_inventory_equal(expected: dict[str, dict[str, object]], actual: dict[str, dict[str, object]]) -> None:
    if expected != actual:
        changed = sorted(path for path in expected.keys() | actual.keys() if expected.get(path) != actual.get(path))
        raise RuntimeError("protected inventory drift: " + ", ".join(changed))


def validate_source_identity(root: Path, baseline: dict[str, object]) -> dict[str, object]:
    if baseline.get("schema") != "conductor.publication-baseline.v1":
        raise RuntimeError("publication baseline invalid")
    current = source_identity_snapshot(root)
    if current["head"] != baseline.get("head"):
        raise RuntimeError("source head drift")
    if current["branch"] != baseline.get("branch"):
        raise RuntimeError("source branch drift")
    if current["remotes"] != baseline.get("remotes"):
        raise RuntimeError("source remote drift")
    baseline_records = baseline.get("refs")
    if not isinstance(baseline_records, list) or not all(isinstance(item, str) for item in baseline_records):
        raise RuntimeError("publication baseline refs invalid")
    baseline_stable, baseline_volatile = partition_refs(parse_refs(baseline_records))
    current_stable, current_volatile = partition_refs(parse_refs(current["refs"]))
    if baseline_stable != current_stable:
        changed_refs = sorted(
            ref
            for ref in baseline_stable.keys() | current_stable.keys()
            if baseline_stable.get(ref) != current_stable.get(ref)
        )
        raise RuntimeError("stable refs changed: " + ", ".join(changed_refs))
    if git(root, "diff", "--cached", "--name-only", "-z"):
        raise RuntimeError("source index is not empty")
    return {
        "stable_ref_count": len(current_stable),
        "stable_refs_sha256": ref_aggregate(current_stable),
        "volatile_refs": volatile_disclosure(baseline_volatile, current_volatile),
    }


def materialize(root: Path, manifest: dict[str, object], baseline: dict[str, object], output: Path) -> dict[str, object]:
    identity = validate_source_identity(root, baseline)
    validate_manifest(root, manifest)
    candidate = Path(tempfile.mkdtemp(prefix="factory-publication-candidate-"))
    git(root, "worktree", "add", "--detach", str(candidate), manifest["base_commit"])
    for item in manifest["entries"]:
        destination = candidate / item["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / item["path"], destination)
        destination.chmod(item["mode"])
        git(candidate, "add", "--", item["path"])
    staged = sorted(git(candidate, "diff", "--cached", "--name-only").splitlines())
    expected = sorted(item["path"] for item in manifest["entries"])
    if staged != expected:
        raise RuntimeError("staged path mismatch")
    statuses = git(candidate, "diff", "--cached", "--name-status").splitlines()
    expected_statuses = sorted(f"{'A' if item['operation'] == 'ADD' else 'M'}\t{item['path']}" for item in manifest["entries"])
    if sorted(statuses) != expected_statuses:
        raise RuntimeError("staged operation mismatch")
    for item in manifest["entries"]:
        blob = subprocess.run(["git", "show", f":{item['path']}"], cwd=candidate, capture_output=True, check=True).stdout
        mode = git(candidate, "ls-files", "-s", "--", item["path"]).split()[0]
        expected_mode = "100755" if item["mode"] & stat.S_IXUSR else "100644"
        if sha(blob) != item["source_sha256"] or mode != expected_mode:
            raise RuntimeError(f"staged blob mismatch: {item['path']}")
    git(candidate, "-c", "user.name=Factory Verification", "-c", "user.email=factory@example.invalid", "commit", "-m", "test-only publication candidate")
    commit = git(candidate, "rev-parse", "HEAD").strip()
    payload = {"schema": "conductor.publication-candidate.v1", "worktree": str(candidate), "commit": commit, "base_commit": manifest["base_commit"], "manifest_sha256": manifest["aggregate_sha256"], "public_paths": sorted(item["path"] for item in manifest["entries"]), "source_identity": identity, "authority_grants": []}
    write(output, payload)
    return payload


def validate_candidate(candidate: dict[str, object]) -> tuple[Path, str]:
    required = {"schema", "worktree", "commit", "base_commit", "manifest_sha256", "public_paths", "source_identity", "authority_grants"}
    if set(candidate) != required or candidate.get("schema") != "conductor.publication-candidate.v1" or candidate.get("authority_grants") != []:
        raise RuntimeError("candidate schema invalid")
    commit = candidate.get("commit")
    source_value = candidate.get("worktree")
    public_paths = candidate.get("public_paths")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise RuntimeError("candidate commit invalid")
    if not isinstance(source_value, str) or not Path(source_value).is_absolute():
        raise RuntimeError("candidate worktree path invalid")
    source = Path(source_value)
    if source.is_symlink() or not source.is_dir() or not (source / ".git").exists():
        raise RuntimeError("candidate worktree path invalid")
    if not isinstance(public_paths, list) or not all(isinstance(path, str) and public_path(path) for path in public_paths) or public_paths != sorted(set(public_paths)):
        raise RuntimeError("candidate public paths invalid")
    if git(source, "rev-parse", "HEAD").strip() != commit:
        raise RuntimeError("candidate worktree HEAD mismatch")
    return source, commit


def require_clean_clone(clone: Path, commit: str) -> None:
    if git(clone, "rev-parse", "HEAD").strip() != commit:
        raise RuntimeError("clone HEAD mismatch")
    if git(clone, "status", "--porcelain=v1", "-z"):
        raise RuntimeError("clone worktree is not clean")


def verify_clone(candidate: dict[str, object], commands: list[list[str]] | None = None) -> dict[str, object]:
    source, commit = validate_candidate(candidate)
    clone = Path(tempfile.mkdtemp(prefix="factory-publication-clone-"))
    subprocess.run(["git", "clone", "--quiet", "--no-local", str(source), str(clone)], check=True)
    if git(clone, "rev-parse", "HEAD").strip() != commit:
        raise RuntimeError("clone HEAD mismatch")
    commands = commands if commands is not None else [
        ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"],
        ["python3", "scripts/build_conductor_plugins.py", "--check"],
        ["python3", "scripts/build_conductor_bmad_plugins.py", "--check"],
        ["bash", "scripts/knowledge_lint.sh"],
        ["git", "diff", "--check"],
    ]
    for command in commands:
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        subprocess.run(command, cwd=clone, check=True, env=environment)
    require_clean_clone(clone, commit)
    return {"status": "PASS", "clone": str(clone), "commit": commit, "final_status": "EMPTY_PORCELAIN_V1_Z"}


def closeout_check(root: Path, baseline: dict[str, object], candidate: dict[str, object]) -> dict[str, object]:
    identity = validate_source_identity(root, baseline)
    _, commit = validate_candidate(candidate)
    protected = ("plugin-src/conductor-bmad/", "plugins/conductor-bmad/", "plugins/conductor-bmad-claude/", "artifacts/verification/conductor_bmad_release_gate_repair/", "docs/Conductor/runs/RUN_20260811_0839_factory_bmad_release_gate_repair/")
    excluded = set(candidate["public_paths"])
    before = baseline_protected_inventory(baseline, protected, excluded)
    after = protected_inventory(root, protected, excluded)
    require_inventory_equal(before, after)
    return {"source_identity": identity, "candidate_commit": commit, "protected_record_count": len(after), "authority_grants": []}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build-manifest"); build.add_argument("--output", required=True)
    check = sub.add_parser("manifest"); check.add_argument("--manifest", required=True); check.add_argument("--contract")
    preview = sub.add_parser("preview"); preview.add_argument("--manifest", required=True); preview.add_argument("--baseline")
    make = sub.add_parser("materialize"); make.add_argument("--manifest", required=True); make.add_argument("--baseline"); make.add_argument("--output", required=True)
    clone = sub.add_parser("verify-clone"); clone.add_argument("--candidate", required=True)
    final = sub.add_parser("closeout"); final.add_argument("--baseline", required=True); final.add_argument("--candidate", required=True)
    args = parser.parse_args(); root = Path.cwd().resolve()
    if args.command == "build-manifest":
        value = build_manifest(root, Path(args.output)); state = "MANIFEST_READY"
    elif args.command in {"manifest", "preview"}:
        value = load(Path(args.manifest))
        contract = load(Path(args.contract)) if args.command == "manifest" and args.contract else None
        if args.command == "preview":
            identity = validate_source_identity(root, load(Path(args.baseline)))
        validate_manifest(root, value, contract)
        if args.command == "preview":
            value = {**value, "source_identity": identity}
        state = "PASS" if args.command == "manifest" else "PLAN_READY"
    elif args.command == "materialize":
        value = materialize(root, load(Path(args.manifest)), load(Path(args.baseline)), Path(args.output)); state = "PASS"
    elif args.command == "verify-clone":
        value = verify_clone(load(Path(args.candidate))); state = "PASS"
    else:
        value = closeout_check(root, load(Path(args.baseline)), load(Path(args.candidate))); state = "PASS"
    print(json.dumps({"state": state, **value}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
