#!/usr/bin/env python3
"""Deterministic Factory/BMAD companion evaluator and bounded transactions."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


PLUGIN_VERSION = "0.3.11"
BMAD_VERSION = "6.10.0"
SNAPSHOT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}")
RESERVED_SNAPSHOT_IDS = frozenset({"latest", "receipts", "install-receipts"})
SNAPSHOT_MANIFEST_MODE = 0o644
SOLUTION_CONTEXT_SCHEMA_VERSION = 2
SOLUTION_CONTEXT_TYPE = "SOLUTION_CONTEXT"
EVIDENCE_ONLY = "EVIDENCE_ONLY"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
ADAPTER_ROOT = PLUGIN_ROOT / "assets" / "project-adapter"
if not ADAPTER_ROOT.is_dir():
    ADAPTER_ROOT = PLUGIN_ROOT / "project-adapter"
BMAD_MANIFESTS = (
    Path("_bmad/_config/manifest.yaml"),
    Path("_bmad/_config/manifest.yml"),
    Path("_bmad/manifest.yaml"),
)


def _load_policy():
    sys.dont_write_bytecode = True
    path = Path(__file__).with_name("conductor_bmad_policy.py")
    spec = importlib.util.spec_from_file_location("conductor_bmad_policy", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load policy: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


policy = _load_policy()
SUPPORTED_BMAD_SKILLS = policy.SUPPORTED_BMAD_SKILLS
SUPPORTED_TEA_SKILLS = policy.SUPPORTED_TEA_SKILLS
ALLOWED_WORKFLOWS = {
    *policy.ALLOWED_UPSTREAM_WORKFLOWS,
    *(name.removeprefix("bmad-") for name in policy.ALLOWED_UPSTREAM_WORKFLOWS),
}
SOLUTION_CONTEXT_ONLY_PROMOTION = {"architecture", "spec"}
policy_classify = policy.policy_classify
assess_bmad_layout = policy.assess_bmad_layout
enforcement_activation = policy.enforcement_activation
hook_decision = policy.hook_decision
capability_audit = policy.capability_audit
reconcile_brownfield = policy.reconcile_brownfield
policy_lint = policy.policy_lint


class CompanionError(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def plan_id(value: dict[str, Any]) -> str:
    return digest_bytes(canonical(value))


def direct_inventory(directory: Path) -> dict[str, dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    for path in directory.iterdir():
        metadata = path.lstat()
        record: dict[str, Any] = {"mode": stat.S_IMODE(metadata.st_mode)}
        if stat.S_ISREG(metadata.st_mode):
            record.update(kind="file", sha256=digest_file(path))
        elif stat.S_ISLNK(metadata.st_mode):
            record.update(kind="symlink", target=os.readlink(path))
        elif stat.S_ISDIR(metadata.st_mode):
            record.update(kind="directory")
        else:
            record.update(kind="other")
        inventory[path.name] = record
    return dict(sorted(inventory.items()))


def snapshot_inventory(snapshot: Path, artifact_name: str) -> dict[str, dict[str, Any]]:
    if snapshot.is_symlink() or not snapshot.is_dir():
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    inventory = direct_inventory(snapshot)
    expected = {"SNAPSHOT_MANIFEST.json", artifact_name}
    if set(inventory) != expected or any(record["kind"] != "file" for record in inventory.values()):
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    if inventory["SNAPSHOT_MANIFEST.json"]["mode"] != SNAPSHOT_MANIFEST_MODE:
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    return inventory


def recursive_file_inventory(directory: Path, *, prefix: str = "") -> dict[str, dict[str, Any]]:
    if directory.is_symlink() or not directory.is_dir():
        raise CompanionError("CONDUCTOR_BMAD_SOURCE_MISSING")
    inventory: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.rglob("*")):
        metadata = path.lstat()
        relative = path.relative_to(directory).as_posix()
        if stat.S_ISDIR(metadata.st_mode):
            continue
        if not stat.S_ISREG(metadata.st_mode):
            raise CompanionError("CONDUCTOR_BMAD_SYMLINK_REJECTED" if stat.S_ISLNK(metadata.st_mode) else "CONDUCTOR_BMAD_SOURCE_TYPE_INVALID", relative)
        destination = f"{prefix}/{relative}" if prefix else relative
        inventory[destination] = {
            "mode": stat.S_IMODE(metadata.st_mode),
            "sha256": digest_file(path),
            "source_path": relative,
            "source_sha256": digest_file(path),
        }
    if not inventory:
        raise CompanionError("CONDUCTOR_BMAD_SOURCE_EMPTY")
    return inventory


def solution_snapshot_inventory(snapshot: Path, artifacts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if snapshot.is_symlink() or not snapshot.is_dir() or not isinstance(artifacts, dict) or not artifacts:
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    actual: dict[str, dict[str, Any]] = {}
    for path in sorted(snapshot.rglob("*")):
        metadata = path.lstat()
        relative = path.relative_to(snapshot).as_posix()
        if stat.S_ISDIR(metadata.st_mode):
            continue
        if not stat.S_ISREG(metadata.st_mode):
            raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
        actual[relative] = {"kind": "file", "mode": stat.S_IMODE(metadata.st_mode), "sha256": digest_file(path)}
    expected_paths = {"SNAPSHOT_MANIFEST.json", *artifacts}
    if set(actual) != expected_paths or actual["SNAPSHOT_MANIFEST.json"]["mode"] != SNAPSHOT_MANIFEST_MODE:
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    for name, expected in artifacts.items():
        if not isinstance(name, str) or not isinstance(expected, dict):
            raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or path.parts[:1] != ("content",):
            raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
        record = actual[name]
        if record["mode"] != expected.get("mode") or record["sha256"] != expected.get("sha256"):
            raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
    return actual


def result(state: str, code: str, action: str, **details: Any) -> dict[str, Any]:
    return {
        "state": state,
        "reason_code": code,
        **details,
        "next_legal_action": action,
        "mutations": details.pop("mutations", []) if "mutations" in details else [],
    }


def safe_relative(root: Path, value: str, *, prefix: Path | None = None) -> tuple[Path, Path]:
    root = root.resolve()
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise CompanionError("CONDUCTOR_BMAD_PATH_INVALID", value)
    candidate = root / relative
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise CompanionError("CONDUCTOR_BMAD_SYMLINK_REJECTED", relative.as_posix())
    resolved = candidate.resolve(strict=False)
    try:
        normalized = resolved.relative_to(root)
    except ValueError as error:
        raise CompanionError("CONDUCTOR_BMAD_PATH_ESCAPE", value) from error
    if prefix is not None and normalized.parts[: len(prefix.parts)] != prefix.parts:
        raise CompanionError("CONDUCTOR_BMAD_PATH_PREFIX_INVALID", value)
    return candidate, normalized


def bmad_manifest_path(root: Path) -> Path | None:
    found = [root / item for item in BMAD_MANIFESTS if (root / item).is_file()]
    if len(found) > 1:
        raise CompanionError("CONDUCTOR_BMAD_MANIFEST_AMBIGUOUS")
    return found[0] if found else None


def parse_modules(path: Path) -> dict[str, str]:
    modules: dict[str, str] = {}
    current: str | None = None
    in_modules = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith((" ", "-")):
            in_modules = line.strip() == "modules:"
        if not in_modules:
            continue
        name = re.match(r"\s*-\s+name:\s*['\"]?([^'\"#\s]+)", line)
        version = re.match(r"\s+version:\s*['\"]?([^'\"#\s]+)", line)
        if name:
            current = name.group(1)
            if current in modules:
                raise CompanionError("CONDUCTOR_BMAD_MODULE_DUPLICATE", current)
            modules[current] = "unknown"
        elif version and current:
            modules[current] = version.group(1)
    if not modules:
        raise CompanionError("CONDUCTOR_BMAD_MODULES_UNREADABLE")
    return modules


def conductor_state(root: Path) -> tuple[bool, bool]:
    factory = (root / "docs/Conductor/ARCHITECTURE.md").is_file() and (root / "scripts/conductorctl").is_file()
    partial = (root / "docs/Conductor").exists() and not factory
    return factory, partial


def bmad_state(root: Path) -> tuple[bool, bool, Path | None]:
    layout = assess_bmad_layout(root)
    manifest_value = layout["canonical_manifest"]
    manifest = root / manifest_value if isinstance(manifest_value, str) else None
    present = layout["state"] == "canonical_root"
    partial = not layout["safe"]
    return present, partial, manifest


def meaningful_entries(root: Path) -> list[str]:
    if not root.exists():
        return []
    ignored = {".git", ".claude"}
    return sorted(item.name for item in root.iterdir() if item.name not in ignored)


def doctor(root: Path, harness: str) -> dict[str, Any]:
    root = root.resolve()
    factory, conductor_partial = conductor_state(root)
    layout = assess_bmad_layout(root)
    bmad, bmad_partial, manifest = bmad_state(root)
    non_canonical = policy.non_canonical_bmad_layouts(root)
    evidence = {
        "root": str(root), "harness": harness, "conductor_present": factory,
        "bmad_present": bmad, "bmad_manifest": str(manifest.relative_to(root)) if manifest else None,
        "bmad_layout": layout,
    }
    if bmad_partial:
        action = (
            "repair_or_remove_partial_state_with_human_review"
            if layout["reason_code"] == "CONDUCTOR_BMAD_PARTIAL_STATE"
            else "review_zero_write_remediation_preview"
        )
        return result(
            "BLOCKED",
            "CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT",
            action,
            evidence={
                **evidence,
                "layout_reason_code": layout["reason_code"],
                "non_canonical_bmad_layouts": non_canonical,
            },
        )
    if conductor_partial:
        return result("BLOCKED", "CONDUCTOR_BMAD_PARTIAL_STATE", "repair_or_remove_partial_state_with_human_review", evidence=evidence)
    if factory and bmad:
        return result("BOTH_PRESENT", "CONDUCTOR_BMAD_BOTH_PRESENT", "run_factory_bmad_audit", evidence=evidence)
    if factory:
        return result("CONDUCTOR_ONLY", "CONDUCTOR_BMAD_FACTORY_ONLY", "preview_pinned_bmad_bootstrap", evidence=evidence)
    if bmad:
        return result("BMAD_ONLY", "CONDUCTOR_BMAD_BMAD_ONLY", "run_factory_brownfield_preview", evidence=evidence)
    entries = meaningful_entries(root)
    if entries:
        return result("NEITHER_BROWNFIELD", "CONDUCTOR_BMAD_NEITHER_BROWNFIELD", "run_factory_brownfield_preview", evidence={**evidence, "meaningful_entries": entries})
    return result("NEITHER_GREENFIELD", "CONDUCTOR_BMAD_NEITHER_GREENFIELD", "run_factory_greenfield_preview", evidence=evidence)


def module_audit(root: Path, harness: str, route: str | None = None) -> dict[str, Any]:
    payload = capability_audit(root, harness, route)
    payload["classifications"] = payload["module_classifications"]
    if payload["state"] == "READY":
        payload["classifications"] = {
            name: ("OPTIONAL_STAGE_F_EVIDENCE_ONLY" if name == "tea" else "UPSTREAM_CAPABILITY_ONLY")
            for name in payload["modules"]
        }
    return payload


def tree_inventory(root: Path) -> dict[str, str]:
    inventory: dict[str, str] = {}
    if not root.exists():
        return inventory
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        if relative.parts in {(".claude",), (".claude", "hooks")}:
            continue
        if relative.parts[:3] == (".claude", "hooks", ".state"):
            continue
        key = relative.as_posix()
        if path.is_symlink():
            inventory[key] = f"symlink:{os.readlink(path)}"
        elif path.is_dir():
            inventory[key] = "directory"
        elif path.is_file():
            inventory[key] = f"file:{digest_file(path)}"
        else:
            inventory[key] = "other"
    return inventory


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))


def canonical_workflow(value: str) -> str:
    return value.removeprefix("bmad-")


def bootstrap_plan(root: Path, harness: str) -> dict[str, Any]:
    root = root.resolve()
    if harness != "claude":
        raise CompanionError("CONDUCTOR_BMAD_CODEX_BOOTSTRAP_UNSUPPORTED", "The pinned installer targets Claude Code. Use an existing reviewed Core/BMM installation for the Codex guarded MCP route.")
    state = doctor(root, harness)
    if state["state"] != "CONDUCTOR_ONLY":
        raise CompanionError("CONDUCTOR_BMAD_BOOTSTRAP_STATE_INVALID", state["state"])
    command = [
        "npx", "--yes", f"bmad-method@{BMAD_VERSION}", "install",
        "--directory", str(root), "--modules", "bmm", "--tools", "claude-code", "--yes",
    ]
    plan = {
        "schema_version": 1, "operation": "bootstrap", "plugin_version": PLUGIN_VERSION,
        "target": str(root), "command": command, "modules": ["core", "bmm"],
        "tool": "claude-code", "excluded_modules": ["bmad-loop", "tea"],
        "allowed_prefixes": ["_bmad", "_bmad-output", ".claude/commands", ".claude/skills", "docs/upstream/bmad/install-receipts"],
        "allowed_container_paths": [".claude"],
        "pre_inventory_sha256": digest_bytes(canonical(tree_inventory(root))),
    }
    return {**plan, "plan_id": plan_id(plan)}


def bootstrap(root: Path, harness: str, approval: str | None) -> dict[str, Any]:
    root = root.resolve()
    try:
        plan = bootstrap_plan(root, harness)
    except CompanionError as error:
        return result("BLOCKED", error.code, "run_factory_bmad_doctor", detail=error.detail)
    if approval is None:
        return result("PLAN_READY", "CONDUCTOR_BMAD_BOOTSTRAP_PLAN_READY", "review_and_exactly_approve_plan", plan=plan)
    if approval != plan["plan_id"]:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", "review_current_plan", plan=plan)
    before = tree_inventory(root)
    completed = subprocess.run(plan["command"], cwd=root, text=True, capture_output=True, shell=False)
    after = tree_inventory(root)
    changes = changed_paths(before, after)
    allowed = tuple(plan["allowed_prefixes"])
    containers = set(plan["allowed_container_paths"])
    unexpected = [
        path for path in changes
        if path not in containers and not any(path == prefix or path.startswith(prefix + "/") for prefix in allowed)
    ]
    receipt_dir = root / "docs/upstream/bmad/install-receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipt_dir / f"{plan['plan_id']}.json"
    audit = module_audit(root, harness)
    outcome = "APPLIED" if completed.returncode == 0 and not unexpected and audit["state"] == "READY" else "BLOCKED"
    payload = {
        "schema_version": 1, "operation": "bootstrap", "plan_id": plan["plan_id"],
        "outcome": outcome, "return_code": completed.returncode, "changed_paths": changes,
        "unexpected_paths": unexpected, "stdout_sha256": digest_bytes(completed.stdout.encode()),
        "stderr_sha256": digest_bytes(completed.stderr.encode()), "audit": audit,
    }
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if outcome != "APPLIED":
        return result("BLOCKED", "CONDUCTOR_BMAD_BOOTSTRAP_POST_AUDIT_FAILED", "inspect_receipt_and_recover_manually", receipt=receipt.relative_to(root).as_posix(), unexpected_paths=unexpected, mutations=changes)
    return result("APPLIED", "CONDUCTOR_BMAD_BOOTSTRAP_APPLIED", "restart_claude_then_run_factory_bmad_doctor", target=str(root), receipt=receipt.relative_to(root).as_posix(), mutations=changes)


def parse_companion_list(value: str) -> list[str]:
    if not value.startswith("[") or not value.endswith("]"):
        raise ValueError("Expected a YAML flow list")
    inner = value[1:-1].strip()
    if not inner:
        return []
    result = []
    for token in inner.split(","):
        token = token.strip()
        if token[:1] in {"'", '\"'}:
            if len(token) < 2 or token[-1] != token[0]:
                raise ValueError("Unmatched quote")
            token = token[1:-1]
        if not token or not re.fullmatch(r"[A-Za-z0-9_./ -]+", token):
            raise ValueError("Expected a plain relative companion path")
        result.append(token)
    return result


def repository_companions(root: Path, values: list[str]) -> list[str]:
    """An exact opt-in list, never a repository-wide source permission."""
    paths = []
    for value in values:
        path = Path(value)
        if (not value or path.as_posix() != value or path.is_absolute()
                or any(part.startswith(".") for part in path.parts)
                or any(c in value for c in "\\\n\r:#?*[]{}") or path.suffix.lower() != ".md"):
            raise CompanionError("CONDUCTOR_BMAD_REPO_COMPANION_INVALID", value)
        safe, relative = safe_relative(root, value)
        if relative.is_relative_to(policy.output_directory(root)) or not safe.exists() or not stat.S_ISREG(safe.lstat().st_mode):
            raise CompanionError("CONDUCTOR_BMAD_REPO_COMPANION_INVALID", value)
        paths.append(relative.as_posix())
    if len(paths) != len(set(paths)):
        raise CompanionError("CONDUCTOR_BMAD_REPO_COMPANION_INVALID", "Duplicate permission")
    return sorted(paths)


def spec_package_inventory(root: Path, selection: Path, repo_companions: list[str] | None = None) -> dict[str, dict[str, Any]]:
    """Freeze the explicit Spec closure while preserving output-relative paths."""
    permitted = set(repository_companions(root, repo_companions or []))
    output = root / policy.output_directory(root)
    source_base = root if permitted else output
    used = set()
    spec = selection / "SPEC.md" if selection.is_dir() else selection
    if spec.name != "SPEC.md" or not spec.is_file():
        raise CompanionError("CONDUCTOR_BMAD_SPEC_REQUIRED")
    pending = [spec]
    memlog = spec.parent / ".memlog.md"
    if memlog.exists() or memlog.is_symlink():
        pending.append(memlog)
    inventory = {}
    while pending:
        path = pending.pop()
        try:
            relative = path.relative_to(source_base)
        except ValueError as error:
            raise CompanionError("CONDUCTOR_BMAD_COMPANION_ESCAPE", str(path)) from error
        repo_path = path.relative_to(root).as_posix()
        if not path.is_relative_to(output):
            if repo_path not in permitted:
                raise CompanionError("CONDUCTOR_BMAD_COMPANION_ESCAPE", repo_path)
            used.add(repo_path)
        safe, _ = safe_relative(root, repo_path)
        if not safe.exists() or not stat.S_ISREG(safe.lstat().st_mode):
            raise CompanionError("CONDUCTOR_BMAD_COMPANION_MISSING", relative.as_posix())
        name = "content/" + relative.as_posix()
        if name in inventory:
            continue
        if path.name == "SPEC.md":
            log = path.parent / ".memlog.md"
            if log.exists() or log.is_symlink():
                pending.append(log)
        digest = digest_file(safe)
        inventory[name] = {"mode": stat.S_IMODE(safe.stat().st_mode), "sha256": digest,
                           "source_path": relative.as_posix(), "source_sha256": digest}
        if path.suffix.lower() != ".md" or path.name == ".memlog.md":
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        lines = text.splitlines()[1:]
        try:
            end = lines.index("---")
        except ValueError as error:
            raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID", "Frontmatter must end on a delimiter line") from error
        lines = lines[:end]
        refs = []; found = False; collecting = False
        for line in lines:
            key = re.match(r"^(?:companions|\"companions\"|'companions'):\s*(.*?)\s*$", line)
            if key:
                if found:
                    raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID")
                found = True; collecting = True
                value = key[1]
                if value:
                    try:
                        refs = parse_companion_list(value)
                    except ValueError as error:
                        raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID", "Use a list of plain relative paths") from error
                    collecting = False
            elif collecting and re.match(r"^\s*- ", line):
                try:
                    refs.extend(parse_companion_list("[" + line.strip()[2:].strip() + "]"))
                except ValueError as error:
                    raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID") from error
            elif re.search(r"(?:companions['\"]?\s*:|^\s*<<\s*:)", line):
                raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID", "Unsupported companion mapping or YAML merge")
            elif collecting and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
                collecting = False
            elif collecting and line.strip() and not line.lstrip().startswith("#"):
                raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID")
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
            raise CompanionError("CONDUCTOR_BMAD_COMPANIONS_INVALID")
        for ref in refs:
            if Path(ref).is_absolute() or any(c in ref for c in "\\\n\r:#?*[]{}"):
                raise CompanionError("CONDUCTOR_BMAD_COMPANION_ESCAPE", ref)
            candidates = set()
            for base in (path.parent, root / policy.active_bmad_root(root).parent):
                # Normalize .. lexically, then reject every symlink before reading.
                candidate = Path(os.path.abspath(base / ref))
                if not candidate.is_relative_to(root):
                    continue
                # Opt-in mode must not resolve an ambiguous reference by filtering
                # out its unapproved interpretation. Count paths before granting reads.
                if not permitted and not candidate.is_relative_to(output):
                    continue
                # Check the unnormalised path too: link/../file must not hide a link.
                cursor = base
                for part in Path(ref).parts:
                    cursor = cursor.parent if part == ".." else cursor / part
                    if cursor.is_symlink():
                        raise CompanionError("CONDUCTOR_BMAD_SYMLINK_REJECTED", ref)
                if candidate.exists() or candidate.is_symlink():
                    safe_relative(root, candidate.relative_to(root).as_posix())
                    candidates.add(candidate)
            if len(candidates) != 1:
                raise CompanionError("CONDUCTOR_BMAD_COMPANION_AMBIGUOUS" if candidates else "CONDUCTOR_BMAD_COMPANION_MISSING", ref)
            pending.extend(candidates)
    if used != permitted:
        raise CompanionError("CONDUCTOR_BMAD_REPO_COMPANION_UNUSED", ", ".join(sorted(permitted - used)))
    return dict(sorted(inventory.items()))


def promotion_plan(
    root: Path,
    source_value: str,
    snapshot_id: str,
    workflow: str,
    reviewer: str,
    review_ref: str,
    review_qualifier: str | None = None,
    *,
    evidence_type: str | None = None,
    authority: str | None = None,
    plan_identity: str | None = None,
    supersedes_snapshot_id: str | None = None,
    supersedes_sha256: str | None = None,
    repo_companions: list[str] | None = None,
    git_binding: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    permitted = repository_companions(root, repo_companions or [])
    if (permitted and evidence_type != SOLUTION_CONTEXT_TYPE) or (git_binding and not permitted):
        raise CompanionError("CONDUCTOR_BMAD_PROMOTION_ARGUMENTS_INVALID")
    if workflow not in ALLOWED_WORKFLOWS:
        raise CompanionError("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", workflow)
    workflow = canonical_workflow(workflow)
    if workflow in SOLUTION_CONTEXT_ONLY_PROMOTION and evidence_type != SOLUTION_CONTEXT_TYPE:
        raise CompanionError("CONDUCTOR_BMAD_SOLUTION_CONTEXT_REQUIRED", workflow)
    if not SNAPSHOT_RE.fullmatch(snapshot_id):
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_ID_INVALID", snapshot_id)
    if snapshot_id.casefold() in RESERVED_SNAPSHOT_IDS:
        raise CompanionError("CONDUCTOR_BMAD_SNAPSHOT_ID_RESERVED", snapshot_id)
    if policy.installed_bmad_version(root) == "6.12.1-next.0" and not policy.assess_bmad_layout(root)["safe"]:
        raise CompanionError("CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT")
    source, relative = safe_relative(root, source_value, prefix=policy.output_directory(root))
    if not reviewer.strip() or not review_ref.strip():
        raise CompanionError("CONDUCTOR_BMAD_REVIEW_EVIDENCE_INVALID")
    qualifier = review_qualifier.strip() if review_qualifier is not None else None
    if review_qualifier is not None and (not qualifier or len(qualifier) > 500):
        raise CompanionError("CONDUCTOR_BMAD_REVIEW_EVIDENCE_INVALID")
    destination = root / "docs/upstream/bmad" / snapshot_id
    if evidence_type is not None:
        if evidence_type != SOLUTION_CONTEXT_TYPE:
            raise CompanionError("CONDUCTOR_BMAD_EVIDENCE_TYPE_INVALID", evidence_type)
        if authority != EVIDENCE_ONLY:
            raise CompanionError("CONDUCTOR_BMAD_AUTHORITY_INVALID", authority or "")
        if not isinstance(plan_identity, str) or not plan_identity.strip() or len(plan_identity.strip()) > 200:
            raise CompanionError("CONDUCTOR_BMAD_PLAN_IDENTITY_INVALID")
        spec_package = policy.installed_bmad_version(root) == "6.12.1-next.0" and (source.name == "SPEC.md" or (source / "SPEC.md").is_file())
        if (not source.is_dir() and not spec_package) or source.is_symlink():
            raise CompanionError("CONDUCTOR_BMAD_SOURCE_TYPE_INVALID", source_value)
        if (supersedes_snapshot_id is None) != (supersedes_sha256 is None):
            raise CompanionError("CONDUCTOR_BMAD_SUPERSESSION_INVALID")
        supersedes = None
        if supersedes_snapshot_id is not None:
            if not SNAPSHOT_RE.fullmatch(supersedes_snapshot_id) or supersedes_snapshot_id.casefold() in RESERVED_SNAPSHOT_IDS or supersedes_snapshot_id == snapshot_id:
                raise CompanionError("CONDUCTOR_BMAD_SUPERSESSION_INVALID")
            if not isinstance(supersedes_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", supersedes_sha256):
                raise CompanionError("CONDUCTOR_BMAD_SUPERSESSION_INVALID")
            prior_manifest = root / "docs/upstream/bmad" / supersedes_snapshot_id / "SNAPSHOT_MANIFEST.json"
            try:
                prior = json.loads(prior_manifest.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as error:
                raise CompanionError("CONDUCTOR_BMAD_SUPERSESSION_INVALID") from error
            if not isinstance(prior, dict) or prior.get("aggregate_sha256") != supersedes_sha256:
                raise CompanionError("CONDUCTOR_BMAD_SUPERSESSION_INVALID")
            supersedes = {"snapshot_id": supersedes_snapshot_id, "aggregate_sha256": supersedes_sha256}
        if permitted and not spec_package:
            raise CompanionError("CONDUCTOR_BMAD_SPEC_REQUIRED")
        artifacts = spec_package_inventory(root, source, permitted) if spec_package else recursive_file_inventory(source, prefix="content")
        base = {
            "schema_version": SOLUTION_CONTEXT_SCHEMA_VERSION,
            "operation": "promote",
            "plugin_version": PLUGIN_VERSION,
            "policy_version": policy.POLICY_VERSION,
            "evidence_type": SOLUTION_CONTEXT_TYPE,
            "authority": EVIDENCE_ONLY,
            "source": relative.as_posix(),
            "source_artifacts": artifacts,
            "source_aggregate_sha256": digest_bytes(canonical(artifacts)),
            "snapshot_id": snapshot_id,
            "destination": destination.relative_to(root).as_posix(),
            "workflow": workflow,
            "plan_identity": plan_identity.strip(),
            "reviewer": reviewer.strip(),
            "review_reference": review_ref.strip(),
        }
        if spec_package:
            base["source_base"] = policy.output_directory(root).as_posix()
        if permitted:
            base["source_base"] = "."
            companions = {"output_root": policy.output_directory(root).as_posix(),
                          "selected_source": relative.as_posix(), "paths": permitted}
            if git_binding:
                # Approval covers committed content and its commit, so a descendant checkout needs no new approval.
                try:
                    companions.update(binding="git", **policy.git_approval_context(root, [a["source_path"] for a in artifacts.values()]))
                except ValueError as error:
                    code, _, detail = str(error).partition(":")
                    raise CompanionError(code, detail) from error
            else:
                companions["target_root"] = str(root)
            base["repository_companions"] = companions
        if policy.installed_bmad_version(root) == "6.12.1-next.0":
            base["bmad_version"] = "6.12.1-next.0"
        if supersedes is not None:
            base["supersedes"] = supersedes
        if qualifier is not None:
            base["review_qualifier"] = qualifier
        return {**base, "plan_id": plan_id(base)}
    if authority is not None or plan_identity is not None or supersedes_snapshot_id is not None or supersedes_sha256 is not None:
        raise CompanionError("CONDUCTOR_BMAD_PROMOTION_ARGUMENTS_INVALID")
    if not source.is_file():
        raise CompanionError("CONDUCTOR_BMAD_SOURCE_MISSING", source_value)
    artifact_name = "artifact" + (source.suffix or ".txt")
    base = {
        "schema_version": 1, "operation": "promote", "plugin_version": PLUGIN_VERSION,
        "source": relative.as_posix(), "source_sha256": digest_file(source),
        "source_mode": stat.S_IMODE(source.lstat().st_mode),
        "snapshot_id": snapshot_id, "destination": destination.relative_to(root).as_posix(),
        "artifact_name": artifact_name, "workflow": workflow,
        "reviewer": reviewer.strip(), "review_reference": review_ref.strip(),
    }
    if qualifier is not None:
        base["review_qualifier"] = qualifier
    return {**base, "plan_id": plan_id(base)}


def snapshot_manifest(plan: dict[str, Any]) -> dict[str, Any]:
    if plan.get("schema_version") == SOLUTION_CONTEXT_SCHEMA_VERSION:
        core = {
            "schema_version": SOLUTION_CONTEXT_SCHEMA_VERSION,
            "snapshot_id": plan["snapshot_id"],
            "evidence_type": SOLUTION_CONTEXT_TYPE,
            "authority": EVIDENCE_ONLY,
            "policy_version": plan["policy_version"],
            "artifacts": plan["source_artifacts"],
            "review": {"decision": "APPROVED", "reviewer": plan["reviewer"], "reference": plan["review_reference"]},
            "provenance": {
                "system": "BMAD",
                "bmad_version": plan.get("bmad_version", BMAD_VERSION),
                "workflow": plan["workflow"],
                "promotion_plan_id": plan["plan_id"],
                "plan_identity": plan["plan_identity"],
                "source_root": plan.get("source_base", plan["source"]),
                "source_aggregate_sha256": plan["source_aggregate_sha256"],
            },
        }
        if "repository_companions" in plan:
            core["provenance"]["repository_companions"] = plan["repository_companions"]
        if "supersedes" in plan:
            core["supersedes"] = plan["supersedes"]
        if "review_qualifier" in plan:
            core["review"]["qualifier"] = plan["review_qualifier"]
        return {**core, "aggregate_sha256": digest_bytes(canonical(core))}
    core = {
        "schema_version": 1, "snapshot_id": plan["snapshot_id"],
        "artifact": {"path": plan["artifact_name"], "mode": plan["source_mode"], "sha256": plan["source_sha256"], "source_path": plan["source"], "source_sha256": plan["source_sha256"]},
        "review": {"decision": "APPROVED", "reviewer": plan["reviewer"], "reference": plan["review_reference"]},
        "provenance": {"system": "BMAD", "bmad_version": BMAD_VERSION, "workflow": plan["workflow"], "promotion_plan_id": plan["plan_id"]},
    }
    if "review_qualifier" in plan:
        core["review"]["qualifier"] = plan["review_qualifier"]
    return {**core, "aggregate_sha256": digest_bytes(canonical(core))}


def promote(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = root.resolve()
    try:
        plan = promotion_plan(
            root, args.source, args.snapshot_id, args.workflow, args.reviewer, args.review_ref,
            getattr(args, "review_qualifier", None),
            evidence_type=getattr(args, "evidence_type", None),
            authority=getattr(args, "authority", None),
            plan_identity=getattr(args, "plan_identity", None),
            supersedes_snapshot_id=getattr(args, "supersedes_snapshot_id", None),
            supersedes_sha256=getattr(args, "supersedes_sha256", None),
            repo_companions=getattr(args, "repo_companion", None),
            git_binding=getattr(args, "git_binding", False),
        )
    except CompanionError as error:
        return result("BLOCKED", error.code, "correct_promotion_request", detail=error.detail)
    destination = root / plan["destination"]
    manifest = snapshot_manifest(plan)
    if destination.exists():
        existing_manifest = destination / "SNAPSHOT_MANIFEST.json"
        if not destination.is_symlink():
            try:
                existing = json.loads(existing_manifest.read_text(encoding="utf-8"))
                inventory = solution_snapshot_inventory(destination, manifest["artifacts"]) if plan["schema_version"] == SOLUTION_CONTEXT_SCHEMA_VERSION else snapshot_inventory(destination, plan["artifact_name"])
            except (OSError, UnicodeError, json.JSONDecodeError):
                existing = None
                inventory = {}
            except CompanionError:
                existing = None
                inventory = {}
            exact_inventory = plan["schema_version"] == SOLUTION_CONTEXT_SCHEMA_VERSION or (
                inventory.get(plan["artifact_name"], {}).get("sha256") == plan["source_sha256"]
                and inventory.get(plan["artifact_name"], {}).get("mode") == plan["source_mode"]
            )
            if existing == manifest and exact_inventory:
                return result("REUSABLE", "CONDUCTOR_BMAD_SNAPSHOT_REUSABLE", "cite_snapshot_id_and_digest", snapshot_id=plan["snapshot_id"], aggregate_sha256=manifest["aggregate_sha256"])
        return result("BLOCKED", "CONDUCTOR_BMAD_SNAPSHOT_IMMUTABLE_CONFLICT", "choose_new_snapshot_id_or_review_existing")
    if args.approve_plan is None:
        return result("PLAN_READY", "CONDUCTOR_BMAD_PROMOTION_PLAN_READY", "review_and_exactly_approve_plan", plan={**plan, "aggregate_sha256": manifest["aggregate_sha256"]})
    if args.approve_plan != plan["plan_id"]:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", "review_current_plan", plan=plan)
    source = root / plan["source"]
    if plan["schema_version"] == SOLUTION_CONTEXT_SCHEMA_VERSION:
        try:
            source_current = spec_package_inventory(root, source, plan.get("repository_companions", {}).get("paths")) if "source_base" in plan else recursive_file_inventory(source, prefix="content")
        except CompanionError:
            source_current = {}
        source_stale = source_current != plan["source_artifacts"]
    else:
        source_stale = digest_file(source) != plan["source_sha256"]
    if source_stale:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_STALE", "regenerate_promotion_plan")
    parent = destination.parent
    parent.mkdir(parents=True, exist_ok=True)
    temporary = parent / f".tmp-{plan['plan_id']}"
    if temporary.exists():
        return result("BLOCKED", "CONDUCTOR_BMAD_PARTIAL_TRANSACTION", "inspect_partial_transaction")
    temporary.mkdir()
    if plan["schema_version"] == SOLUTION_CONTEXT_SCHEMA_VERSION:
        for name, artifact in plan["source_artifacts"].items():
            artifact_path = temporary / name
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile((root / plan.get("source_base", plan["source"])) / artifact["source_path"], artifact_path)
            artifact_path.chmod(artifact["mode"])
    else:
        artifact_path = temporary / plan["artifact_name"]
        shutil.copyfile(source, artifact_path)
        artifact_path.chmod(plan["source_mode"])
    manifest_path = temporary / "SNAPSHOT_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path.chmod(SNAPSHOT_MANIFEST_MODE)
    os.replace(temporary, destination)
    receipts = parent / "receipts"
    receipts.mkdir(exist_ok=True)
    receipt_path = receipts / f"promotion-{plan['plan_id']}.json"
    files = solution_snapshot_inventory(destination, manifest["artifacts"]) if plan["schema_version"] == SOLUTION_CONTEXT_SCHEMA_VERSION else snapshot_inventory(destination, plan["artifact_name"])
    receipt = {"schema_version": plan["schema_version"], "operation": "promotion", "plan_id": plan["plan_id"], "snapshot_id": plan["snapshot_id"], "snapshot_path": plan["destination"], "aggregate_sha256": manifest["aggregate_sha256"], "created_files": files, "outcome": "APPLIED"}
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result("APPLIED", "CONDUCTOR_BMAD_PROMOTION_APPLIED", "cite_snapshot_id_and_digest", snapshot_id=plan["snapshot_id"], aggregate_sha256=manifest["aggregate_sha256"], receipt=receipt_path.relative_to(root).as_posix(), mutations=sorted([f"{plan['destination']}/{name}" for name in files] + [receipt_path.relative_to(root).as_posix()]))


def rollback_plan(root: Path, receipt_value: str) -> tuple[dict[str, Any], Path, Path]:
    root = root.resolve()
    receipt_path, relative = safe_relative(root, receipt_value, prefix=Path("docs/upstream/bmad/receipts"))
    if not receipt_path.is_file():
        raise CompanionError("CONDUCTOR_BMAD_RECEIPT_MISSING")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CompanionError("CONDUCTOR_BMAD_RECEIPT_INVALID") from error
    snapshot_value = receipt.get("snapshot_path")
    files = receipt.get("created_files")
    if not isinstance(snapshot_value, str) or not isinstance(files, dict):
        raise CompanionError("CONDUCTOR_BMAD_RECEIPT_INVALID")
    snapshot, _ = safe_relative(root, snapshot_value, prefix=Path("docs/upstream/bmad"))
    if not snapshot.is_dir() or snapshot.is_symlink():
        raise CompanionError("CONDUCTOR_BMAD_ROLLBACK_STATE_INVALID")
    try:
        manifest = json.loads((snapshot / "SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
        if isinstance(manifest, dict) and manifest.get("schema_version") == SOLUTION_CONTEXT_SCHEMA_VERSION:
            actual = solution_snapshot_inventory(snapshot, manifest.get("artifacts"))
        else:
            artifact = manifest.get("artifact", {}) if isinstance(manifest, dict) else {}
            artifact_name = artifact.get("path") if isinstance(artifact, dict) else None
            actual = snapshot_inventory(snapshot, artifact_name) if isinstance(artifact_name, str) else {}
    except (OSError, UnicodeError, json.JSONDecodeError, CompanionError):
        actual = {}
    if actual != files:
        raise CompanionError("CONDUCTOR_BMAD_ROLLBACK_DIGEST_MISMATCH")
    plan = {"schema_version": 1, "operation": "rollback", "receipt": relative.as_posix(), "receipt_sha256": digest_file(receipt_path), "snapshot_path": snapshot_value, "created_files": files}
    return {**plan, "plan_id": plan_id(plan)}, receipt_path, snapshot


def rollback(root: Path, receipt_value: str, approval: str | None) -> dict[str, Any]:
    root = root.resolve()
    try:
        plan, receipt_path, snapshot = rollback_plan(root, receipt_value)
    except CompanionError as error:
        return result("BLOCKED", error.code, "inspect_snapshot_and_receipt_manually")
    if approval is None:
        return result("PLAN_READY", "CONDUCTOR_BMAD_ROLLBACK_PLAN_READY", "review_and_exactly_approve_plan", plan=plan)
    if approval != plan["plan_id"]:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", "review_current_plan", plan=plan)
    shutil.rmtree(snapshot)
    rollback_receipt = receipt_path.with_name(f"rollback-{plan['plan_id']}.json")
    rollback_receipt.write_text(json.dumps({"schema_version": 1, "operation": "rollback", "plan_id": plan["plan_id"], "source_receipt": plan["receipt"], "outcome": "APPLIED"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result("APPLIED", "CONDUCTOR_BMAD_ROLLBACK_APPLIED", "retain_receipts_for_audit", receipt=rollback_receipt.relative_to(root).as_posix(), mutations=[plan["snapshot_path"], rollback_receipt.relative_to(root).as_posix()])


def verify_checkout(root: Path, snapshot_id: str, run_id: str | None = None) -> dict[str, Any]:
    """Local, zero-write check that this checkout still holds what a human approved; grants nothing."""
    root = root.resolve()
    if not SNAPSHOT_RE.fullmatch(snapshot_id) or snapshot_id.casefold() in RESERVED_SNAPSHOT_IDS:
        return result("BLOCKED", "CONDUCTOR_BMAD_SNAPSHOT_ID_INVALID", "correct_snapshot_id")
    snapshot = root / "docs/upstream/bmad" / snapshot_id
    manifest_path = snapshot / "SNAPSHOT_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        core = {key: value for key, value in manifest.items() if key != "aggregate_sha256"}
        if manifest.get("schema_version") != SOLUTION_CONTEXT_SCHEMA_VERSION or digest_bytes(canonical(core)) != manifest.get("aggregate_sha256"):
            raise CompanionError("CONDUCTOR_BMAD_MANIFEST_HASH_MISMATCH")
        solution_snapshot_inventory(snapshot, manifest["artifacts"])
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError, KeyError) as error:
        return result("BLOCKED", "CONDUCTOR_BMAD_SNAPSHOT_MISSING", "promote_or_restore_snapshot", detail=str(error))
    except CompanionError as error:
        return result("BLOCKED", error.code, "restore_exact_snapshot_bytes_or_repromote")
    companions = manifest.get("provenance", {}).get("repository_companions")
    identity = {"snapshot_id": snapshot_id, "aggregate_sha256": manifest["aggregate_sha256"]}
    if not isinstance(companions, dict) or companions.get("binding") != "git":
        # Root-bound and legacy snapshots keep their original contract unchanged.
        bound_here = isinstance(companions, dict) and companions.get("target_root") == str(root)
        if isinstance(companions, dict) and not bound_here:
            return result("BLOCKED", "CONDUCTOR_BMAD_SNAPSHOT_ROOT_BOUND_ELSEWHERE", "repromote_with_git_binding_or_use_original_checkout", **identity)
        binding = "root" if bound_here else "path"
    else:
        problem = policy.git_checkout_problem(root, companions, manifest["artifacts"])
        if problem is not None and problem["reason_code"] == "CONDUCTOR_BMAD_CHECKOUT_INPUTS_CHANGED":
            # Reviewers see what changed against the approved bytes, not only which file.
            frozen = {a["source_path"]: snapshot / name for name, a in manifest["artifacts"].items()}
            problem["diff"] = {path: "".join(list(difflib.unified_diff(
                frozen[path].read_text(encoding="utf-8").splitlines(keepends=True),
                (root / path).read_text(encoding="utf-8").splitlines(keepends=True) if (root / path).is_file() else [],
                f"approved/{path}", f"current/{path}"))[:200]) for path in problem["changed"]}
        if problem is not None:
            action = "promote_superseding_snapshot_for_review" if problem["reason_code"] == "CONDUCTOR_BMAD_CHECKOUT_INPUTS_CHANGED" else "rebase_on_a_descendant_of_the_approval_commit"
            return result("BLOCKED", problem.pop("reason_code"), action, **identity, **problem)
        binding = "git"
    if run_id is not None:
        run_root = root / "docs/Conductor/runs" / run_id
        try:
            intent_path = run_root / "intent_pack.json"
            intent = json.loads(intent_path.read_text(encoding="utf-8"))
            lock = json.loads((run_root / "countersign/INTENT_LOCK.json").read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            return result("BLOCKED", "CONDUCTOR_BMAD_CHECKOUT_RUN_UNREADABLE", "lock_intent_before_verifying", detail=str(error), **identity)
        cited = {"kind": "upstream_snapshot", "ref": manifest_path.relative_to(root).as_posix(), "sha256": digest_file(manifest_path)}
        if cited not in intent.get("sources", []):
            return result("BLOCKED", "CONDUCTOR_BMAD_CHECKOUT_SNAPSHOT_NOT_CITED", "cite_snapshot_in_intent_and_relock", **identity)
        if lock.get("decision") != "GO" or lock.get("subject_sha256") != digest_file(intent_path):
            return result("BLOCKED", "CONDUCTOR_BMAD_CHECKOUT_INTENT_STALE", "obtain_current_intent_lock", **identity)
    return result("VERIFIED", "CONDUCTOR_BMAD_CHECKOUT_VERIFIED", "continue_under_existing_approval", binding=binding, **identity)


def intake_sources() -> dict[Path, Path]:
    return {
        Path("docs/adapters/bmad/BMAD_POLICY.md"): ADAPTER_ROOT / "BMAD_POLICY.md",
        Path("docs/adapters/bmad/RAW_BRIEF_TEMPLATE.md"): ADAPTER_ROOT / "RAW_BRIEF_TEMPLATE.md",
        Path("docs/Conductor/PROJECT_PREFLIGHT.json"): ADAPTER_ROOT / "PROJECT_PREFLIGHT.json",
        Path("scripts/conductor_project_preflight"): ADAPTER_ROOT / "conductor_project_preflight",
        Path("scripts/conductor_bmad_policy_lint"): ADAPTER_ROOT / "conductor_bmad_policy_lint",
        Path("scripts/conductor_bmad_policy.py"): Path(__file__).with_name("conductor_bmad_policy.py"),
        Path("scripts/conductor_bmad_6121.json"): Path(__file__).with_name("conductor_bmad_6121.json"),
    }


def intake_generated(audit: dict[str, Any]) -> dict[Path, bytes]:
    audit_record = {
        "schema_version": 1,
        "policy_version": audit["policy_version"],
        "status": audit["state"],
        # The retained record is repository policy coverage, shared by both hosts.
        # Keep the existing wire identity; current invocation readiness is not persisted here.
        "reason_code": "CONDUCTOR_BMAD_POLICY_OK",
        "installation_version": audit["installation_version"],
        "modules": audit["modules"],
        "module_classifications": audit["module_classifications"],
        "capabilities": audit["capabilities"],
        "coverage_sha256": audit["coverage_sha256"],
        "uncovered_capabilities": audit["uncovered_capabilities"],
        "missing_capabilities": audit["missing_capabilities"],
    }
    return {
        Path("docs/adapters/bmad/CAPABILITY_AUDIT.json"): json.dumps(audit_record, indent=2, sort_keys=True).encode() + b"\n",
        Path("docs/adapters/bmad/BMAD_RECONCILIATION.json"): json.dumps(audit["reconciliation"], indent=2, sort_keys=True).encode() + b"\n",
    }


def intake(root: Path, harness: str, approval: str | None) -> dict[str, Any]:
    root = root.resolve()
    audit = module_audit(root, harness)
    if audit["state"] != "READY":
        return result("BLOCKED", "CONDUCTOR_BMAD_INTAKE_AUDIT_REQUIRED", "resolve_factory_bmad_audit", audit=audit)
    files = []
    conflicts = []
    generated = intake_generated(audit)
    reconciliation_target = root / "docs/adapters/bmad/BMAD_RECONCILIATION.json"
    if reconciliation_target.is_file() and not reconciliation_target.is_symlink():
        generated[Path("docs/adapters/bmad/BMAD_RECONCILIATION.json")] = reconciliation_target.read_bytes()
    for destination, source in intake_sources().items():
        if not source.is_file():
            return result("BLOCKED", "CONDUCTOR_BMAD_PACKAGE_INCOMPLETE", "repair_companion_package")
        target = root / destination
        action = "create"
        if target.exists():
            action = "present" if target.is_file() and not target.is_symlink() and digest_file(target) == digest_file(source) else "conflict"
        if action == "conflict":
            conflicts.append(destination.as_posix())
        executable = destination in {
            Path("scripts/conductor_project_preflight"),
            Path("scripts/conductor_bmad_policy_lint"),
        }
        files.append({"path": destination.as_posix(), "action": action, "sha256": digest_file(source), "executable": executable})
    for destination, content in generated.items():
        target = root / destination
        action = "create"
        if target.exists():
            action = "present" if target.is_file() and not target.is_symlink() and target.read_bytes() == content else "conflict"
        if action == "conflict":
            conflicts.append(destination.as_posix())
        files.append({"path": destination.as_posix(), "action": action, "sha256": digest_bytes(content), "executable": False})
    if conflicts:
        return result("BLOCKED", "CONDUCTOR_BMAD_INTAKE_CONFLICT", "reconcile_user_owned_files", conflicts=conflicts)
    base = {"schema_version": 1, "operation": "intake", "plugin_version": PLUGIN_VERSION, "target": str(root), "files": files}
    plan = {**base, "plan_id": plan_id(base)}
    creates = [item for item in files if item["action"] == "create"]
    if not creates:
        return result("READY", "CONDUCTOR_BMAD_INTAKE_CURRENT", "draft_raw_brief_from_template")
    if approval is None:
        return result("PLAN_READY", "CONDUCTOR_BMAD_INTAKE_PLAN_READY", "review_and_exactly_approve_plan", plan=plan)
    if approval != plan["plan_id"]:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", "review_current_plan", plan=plan)
    mutations = []
    for item in creates:
        destination = root / item["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        relative = Path(item["path"])
        if relative in generated:
            destination.write_bytes(generated[relative])
        else:
            shutil.copyfile(intake_sources()[relative], destination)
        if item["executable"]:
            destination.chmod(0o755)
        mutations.append(item["path"])
    receipt_dir = root / "docs/adapters/bmad/receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipt_dir / f"intake-{plan['plan_id']}.json"
    receipt.write_text(json.dumps({"schema_version": 1, "operation": "intake", "plan_id": plan["plan_id"], "outcome": "APPLIED", "created_files": mutations}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mutations.append(receipt.relative_to(root).as_posix())
    return result("APPLIED", "CONDUCTOR_BMAD_INTAKE_APPLIED", "draft_raw_brief_from_template", receipt=receipt.relative_to(root).as_posix(), mutations=mutations)


def _contract_asset_root() -> Path:
    """Packaged plugins carry the contracts under assets/project-adapter; the authored source tree keeps
    them at docs/adapters/bmad (the published contract), two levels above plugin-src/conductor-bmad."""
    if (ADAPTER_ROOT / "contracts").is_dir():
        return ADAPTER_ROOT
    return PLUGIN_ROOT.parent.parent / "docs" / "adapters" / "bmad"


def contract_sources() -> dict[Path, Path]:
    """Inert adapter contract files: schemas, lane policy, authority policy. No authority, no enforcement change."""
    assets = _contract_asset_root()
    return {
        Path("docs/adapters/bmad/contracts/bmad_adapter_config.schema.json"): assets / "contracts" / "bmad_adapter_config.schema.json",
        Path("docs/adapters/bmad/contracts/lane_policy.schema.json"): assets / "contracts" / "lane_policy.schema.json",
        Path("docs/adapters/bmad/lane_policy.json"): assets / "lane_policy.json",
        Path("docs/adapters/bmad/BMAD_POLICY.md"): ADAPTER_ROOT / "BMAD_POLICY.md",
    }


def seed_contracts(root: Path, approval: str | None) -> dict[str, Any]:
    """Preview or apply the inert contract seed. Does not depend on the capability audit."""
    root = root.resolve()
    if policy.git_root(root) is None:
        return result("BLOCKED", "CONDUCTOR_BMAD_SEED_NO_GIT", "run_inside_a_git_worktree")
    files: list[dict[str, Any]] = []
    conflicts: list[str] = []
    for destination, source in contract_sources().items():
        if not source.is_file():
            return result("BLOCKED", "CONDUCTOR_BMAD_PACKAGE_INCOMPLETE", "repair_companion_package", missing=source.name)
        target = root / destination
        action = "create"
        if target.exists() or target.is_symlink():
            action = "present" if target.is_file() and not target.is_symlink() and digest_file(target) == digest_file(source) else "conflict"
        if action == "conflict":
            conflicts.append(destination.as_posix())
        files.append({"path": destination.as_posix(), "action": action, "sha256": digest_file(source), "executable": False})
    if conflicts:
        return result("BLOCKED", "CONDUCTOR_BMAD_SEED_CONFLICT", "reconcile_user_owned_files", conflicts=conflicts, files=files)
    base = {"schema_version": 1, "operation": "seed-contracts", "plugin_version": PLUGIN_VERSION, "target": str(root), "files": files}
    plan = {**base, "plan_id": plan_id(base)}
    creates = [item for item in files if item["action"] == "create"]
    if not creates:
        return result("READY", "CONDUCTOR_BMAD_SEED_CURRENT", "run_contract_lint_intent")
    if approval is None:
        return result("PLAN_READY", "CONDUCTOR_BMAD_SEED_PLAN_READY", "review_and_exactly_approve_plan", plan=plan)
    if approval != plan["plan_id"]:
        return result("BLOCKED", "CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", "review_current_plan", plan=plan)
    mutations: list[str] = []
    for item in creates:
        destination = root / item["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(contract_sources()[Path(item["path"])], destination)
        mutations.append(item["path"])
    receipt_dir = root / "docs/adapters/bmad/receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt = receipt_dir / f"seed-contracts-{plan['plan_id']}.json"
    receipt.write_text(json.dumps({"schema_version": 1, "operation": "seed-contracts", "plan_id": plan["plan_id"], "outcome": "APPLIED", "created_files": mutations}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    mutations.append(receipt.relative_to(root).as_posix())
    return result("APPLIED", "CONDUCTOR_BMAD_SEED_APPLIED", "run_contract_lint_intent", receipt=receipt.relative_to(root).as_posix(), mutations=mutations)


def concise(payload: dict[str, Any]) -> str:
    lines = [f"Factory BMAD: {payload['state']}", f"Reason: {payload['reason_code']}"]
    evidence = payload.get("evidence")
    if isinstance(evidence, dict):
        lines.append(f"Factory: {'present' if evidence.get('conductor_present') else 'absent'}; BMAD: {'present' if evidence.get('bmad_present') else 'absent'}")
    target = payload.get("target")
    if not target and isinstance(payload.get("plan"), dict):
        target = payload["plan"].get("target") or payload["plan"].get("destination")
    if target:
        lines.append(f"Target: {target}")
    if payload.get("plan"):
        plan = payload["plan"]
        lines.append(f"Approval Plan ID: {plan['plan_id']}")
        if plan.get("operation") == "bootstrap" and plan.get("pre_inventory_sha256"):
            lines.append(f"Pre-inventory SHA-256: {plan['pre_inventory_sha256']}")
    if payload.get("receipt"):
        lines.append(f"Receipt: {payload['receipt']}")
    changes = payload.get("mutations")
    if isinstance(changes, list):
        lines.append(f"Changes: {len(changes)}")
    elif isinstance(payload.get("plan"), dict) and isinstance(payload["plan"].get("files"), list):
        lines.append(f"Changes: {len(payload['plan']['files'])} planned")
    else:
        lines.append("Changes: 0")
    lines.append(f"Next: {payload['next_legal_action']}")
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    root.add_argument("--root", default=".")
    root.add_argument("--json", action="store_true")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("doctor", "audit", "policy-lint"):
        command = sub.add_parser(name)
        command.add_argument("--harness", choices=("claude", "codex"), default="claude")
        if name != "doctor":
            command.add_argument("--route", choices=("native", "guarded-mcp"))
    sub.add_parser("hook")
    bootstrap_parser = sub.add_parser("bootstrap")
    bootstrap_parser.add_argument("--harness", choices=("claude", "codex"), default="claude")
    bootstrap_parser.add_argument("--approve-plan")
    promote_parser = sub.add_parser("promote")
    promote_parser.add_argument("--source", required=True)
    promote_parser.add_argument("--repo-companion", action="append", default=[], metavar="PATH", help="Exact repository-relative Markdown companion outside BMAD output; repeatable, Spec closure only")
    promote_parser.add_argument("--snapshot-id", required=True)
    promote_parser.add_argument("--workflow", required=True)
    promote_parser.add_argument("--reviewer", required=True)
    promote_parser.add_argument("--review-ref", required=True)
    promote_parser.add_argument("--review-qualifier")
    promote_parser.add_argument("--evidence-type", choices=(SOLUTION_CONTEXT_TYPE,))
    promote_parser.add_argument("--authority", choices=(EVIDENCE_ONLY,))
    promote_parser.add_argument("--plan-identity")
    promote_parser.add_argument("--supersedes-snapshot-id")
    promote_parser.add_argument("--supersedes-sha256")
    promote_parser.add_argument("--git-binding", action="store_true", help="With --repo-companion: bind approval to committed content and its commit instead of this checkout's path")
    promote_parser.add_argument("--approve-plan")
    verify_parser = sub.add_parser("verify-checkout", help="Check that this checkout holds an approved snapshot's exact inputs on a compatible base")
    verify_parser.add_argument("--snapshot-id", required=True)
    verify_parser.add_argument("--run", help="Also require this run's locked Intent Pack to cite the snapshot")
    for name in ("automation-capture", "automation-compare"):
        automation_parser = sub.add_parser(name, help="Open (capture) or close and prove (compare) a governed automation write window")
        automation_parser.add_argument("--run", required=True)
    intake_parser = sub.add_parser("intake")
    intake_parser.add_argument("--harness", choices=("claude", "codex"), default="claude")
    intake_parser.add_argument("--approve-plan")
    seed_parser = sub.add_parser("seed-contracts")
    seed_parser.add_argument("--approve-plan")
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("--receipt", required=True)
    rollback_parser.add_argument("--approve-plan")
    return root


def main() -> int:
    args = parser().parse_args()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", args.root) if args.command == "hook" else args.root).resolve()
    try:
        if args.command == "doctor":
            payload = doctor(root, args.harness)
        elif args.command == "audit":
            payload = module_audit(root, args.harness, args.route)
        elif args.command == "policy-lint":
            payload = policy_lint(root, args.harness, args.route)
        elif args.command == "hook":
            try:
                hook_input = json.load(sys.stdin)
            except (UnicodeError, json.JSONDecodeError):
                if enforcement_activation(root)["active"]:
                    print("CONDUCTOR_BMAD_HOOK_INPUT_INVALID: malformed hook JSON", file=sys.stderr)
                    return 2
                hook_input = {}
            if not isinstance(hook_input, dict):
                if enforcement_activation(root)["active"]:
                    print("CONDUCTOR_BMAD_HOOK_INPUT_INVALID: hook input must be an object", file=sys.stderr)
                    return 2
                hook_input = {}
            decision = hook_decision(root, hook_input)
            print(json.dumps(decision or {}, sort_keys=True))
            return 0
        elif args.command == "bootstrap":
            payload = bootstrap(root, args.harness, args.approve_plan)
        elif args.command == "promote":
            payload = promote(root, args)
        elif args.command == "intake":
            payload = intake(root, args.harness, args.approve_plan)
        elif args.command == "seed-contracts":
            payload = seed_contracts(root, args.approve_plan)
        elif args.command == "verify-checkout":
            payload = verify_checkout(root, args.snapshot_id, args.run)
        elif args.command == "automation-capture":
            payload = policy.automation_capture(root, args.run)
        elif args.command == "automation-compare":
            payload = policy.automation_compare(root, args.run)
        else:
            payload = rollback(root, args.receipt, args.approve_plan)
    except (OSError, UnicodeError, subprocess.SubprocessError) as error:
        payload = result("BLOCKED", "CONDUCTOR_BMAD_IO_FAILURE", "inspect_error_and_retry_safely", detail=str(error))
    print(json.dumps(payload, indent=2, sort_keys=True) if args.json else concise(payload))
    return 0 if payload["state"] not in {"BLOCKED", "FAIL"} else 2


if __name__ == "__main__":
    sys.exit(main())
