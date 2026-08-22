#!/usr/bin/env python3
"""Fail-closed, zero-Claude preflight for Factory-BMAD live verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_JOURNEYS = {"greenfield", "brownfield-neither", "brownfield-bmad"}
SHA256 = re.compile(r"[0-9a-f]{64}")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def verdict_digest(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    unsigned.pop("verdict_sha256", None)
    return hashlib.sha256(canonical(unsigned)).hexdigest()


def paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def has_symlink_component(path: Path) -> bool:
    cursor = Path(path.anchor)
    for part in path.parts[1:]:
        cursor /= part
        if cursor.exists() and cursor.is_symlink():
            return True
    return False


def load_preimages(values: list[str], expected_roles: set[str], reasons: list[str]) -> dict[str, dict[str, Any]]:
    preimages: dict[str, dict[str, Any]] = {}
    for raw in values:
        role, separator, value = raw.partition("=")
        path = Path(value)
        if not separator or role in preimages or path.is_symlink() or not path.is_file():
            reasons.append("FACTORY_BMAD_PROTECTED_PREIMAGE_INVALID")
            continue
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            reasons.append("FACTORY_BMAD_PROTECTED_PREIMAGE_INVALID")
            continue
        entries = manifest.get("entries")
        valid = (
            manifest.get("schema_version") == 1
            and isinstance(entries, list)
            and manifest.get("entry_count") == len(entries)
            and isinstance(manifest.get("root"), str)
            and Path(manifest["root"]).is_absolute()
            and isinstance(manifest.get("aggregate_sha256"), str)
            and SHA256.fullmatch(manifest["aggregate_sha256"]) is not None
        )
        if not valid:
            reasons.append("FACTORY_BMAD_PROTECTED_PREIMAGE_INVALID")
            continue
        preimages[role] = {
            "path": str(path.resolve(strict=False)),
            "root": str(Path(manifest["root"]).resolve(strict=False)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "aggregate_sha256": manifest["aggregate_sha256"],
            "entry_count": manifest["entry_count"],
        }
    if set(preimages) != expected_roles:
        reasons.append("FACTORY_BMAD_PROTECTED_PREIMAGE_INVALID")
    return preimages


def validate_candidate(candidate: Path, release: str, reasons: list[str]) -> None:
    manifests = (
        candidate / "plugin-src/factory/manifest.json",
        candidate / "plugin-src/factory-bmad/manifest.json",
        candidate / ".claude-plugin/marketplace.json",
    )
    try:
        factory = json.loads(manifests[0].read_text(encoding="utf-8"))
        companion = json.loads(manifests[1].read_text(encoding="utf-8"))
        marketplace = json.loads(manifests[2].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        reasons.append("FACTORY_BMAD_CANDIDATE_RELEASE_INVALID")
        return
    versions = {factory.get("version"), companion.get("version")}
    versions.update(item.get("version") for item in marketplace.get("plugins", []))
    if versions != {release} or companion.get("factory_dependency") != f"~{release}":
        reasons.append("FACTORY_BMAD_CANDIDATE_RELEASE_INVALID")


def validate_source_coupling(path: Path, reasons: list[str]) -> str:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        reasons.append("FACTORY_BMAD_SOURCE_COUPLING_INVALID")
        return ""
    candidates = value.get("live_verifier_candidates")
    if not isinstance(candidates, list) or not candidates:
        reasons.append("FACTORY_BMAD_SOURCE_COUPLING_INVALID")
        return hashlib.sha256(path.read_bytes()).hexdigest()
    stale_values = ("0.2." + "1", "0.2." + "2", "2.1." + "218")
    for relative in candidates:
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts or not candidate.is_file():
            reasons.append("FACTORY_BMAD_SOURCE_COUPLING_INVALID")
            continue
        if candidate.parts[0] != "tests":
            text = candidate.read_text(encoding="utf-8", errors="ignore")
            if any(stale in text for stale in stale_values):
                reasons.append("FACTORY_BMAD_STALE_LIVE_LITERAL")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_verdict(output: Path, value: dict[str, Any]) -> None:
    if output.exists() or output.is_symlink():
        raise RuntimeError("FACTORY_BMAD_PREFLIGHT_EVIDENCE_EXISTS")
    output.parent.mkdir(parents=True, exist_ok=True)
    value["verdict_sha256"] = verdict_digest(value)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")


def check(args: argparse.Namespace) -> int:
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    reasons: list[str] = []
    if args.release_version != "0.2.4" or args.bmad_version != contract.get("bmad_version"):
        reasons.append("FACTORY_BMAD_VERSION_CONTRACT_INVALID")
    binary = args.claude_bin.resolve(strict=False)
    if not binary.is_file() or not os.access(binary, os.X_OK):
        reasons.append("FACTORY_BMAD_CLAUDE_BINARY_INVALID")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", args.observed_version):
        reasons.append("FACTORY_BMAD_CLAUDE_VERSION_INVALID")
    elif not args.observed_version.startswith(args.supported_version_prefix):
        reasons.append("FACTORY_BMAD_CLAUDE_VERSION_UNSUPPORTED")
    if args.permission_mode != "dontAsk" or args.permission_rule != contract["permission_rule"]:
        reasons.append("FACTORY_BMAD_PERMISSION_RULE_INVALID")
    if args.permission_rule in contract.get("rejected_permission_rules", []):
        reasons.append("FACTORY_BMAD_PERMISSION_RULE_INVALID")
    if contract.get("cleanup_policy") != "forbidden":
        reasons.append("FACTORY_BMAD_CLEANUP_POLICY_INVALID")

    journeys: dict[str, Path] = {}
    for raw in args.journey_root:
        name, separator, value = raw.partition("=")
        if not separator or name in journeys:
            reasons.append("FACTORY_BMAD_JOURNEY_ROOT_INVALID")
            continue
        journeys[name] = Path(value)
    if set(journeys) != EXPECTED_JOURNEYS:
        reasons.append("FACTORY_BMAD_JOURNEY_ROOT_INVALID")

    raw_roots = {
        "config": args.config_root,
        "evidence": args.evidence_root,
        "candidate": args.candidate_root,
        **{f"journey:{name}": path for name, path in journeys.items()},
    }
    for name, path in raw_roots.items():
        if has_symlink_component(path.absolute()):
            reasons.append(f"FACTORY_BMAD_ROOT_SYMLINK:{name}")
    roots = {name: path.resolve(strict=False) for name, path in raw_roots.items()}
    if not roots["candidate"].is_dir() or roots["candidate"].is_symlink():
        reasons.append("FACTORY_BMAD_CANDIDATE_ROOT_INVALID")
    else:
        validate_candidate(roots["candidate"], args.release_version, reasons)
    for name, path in roots.items():
        if name != "candidate" and (path.exists() or path.is_symlink()):
            reasons.append(f"FACTORY_BMAD_ROOT_NOT_ABSENT:{name}")
    expected_roles = set(contract.get("protected_root_roles", []))
    preimages = load_preimages(args.protected_preimage, expected_roles, reasons)
    roots.update(
        {
            f"protected:{role}": Path(preimage["root"])
            for role, preimage in preimages.items()
        }
    )
    names = sorted(roots)
    for index, left_name in enumerate(names):
        for right_name in names[index + 1 :]:
            if paths_overlap(roots[left_name], roots[right_name]):
                reasons.append("FACTORY_BMAD_ROOT_OVERLAP")
    evidence_root = roots["evidence"]
    output = args.output.resolve(strict=False)
    try:
        output.relative_to(evidence_root)
    except ValueError:
        reasons.append("FACTORY_BMAD_EVIDENCE_PATH_ESCAPE")

    source_coupling_sha256 = validate_source_coupling(args.source_coupling, reasons)

    value = {
        "schema_version": 1,
        "state": "BLOCKED" if reasons else "PASS",
        "reason_codes": sorted(set(reasons)),
        "claude_binary": str(binary),
        "observed_version": args.observed_version,
        "supported_version_prefix": args.supported_version_prefix,
        "release_version": args.release_version,
        "bmad_version": args.bmad_version,
        "permission_mode": args.permission_mode,
        "permission_rule": args.permission_rule,
        "contract_sha256": hashlib.sha256(args.contract.read_bytes()).hexdigest(),
        "source_coupling_sha256": source_coupling_sha256,
        "roots": {name: str(path) for name, path in sorted(roots.items())},
        "protected_preimages": preimages,
        "claude_invocations": 0,
        "cleanup_performed": False,
    }
    try:
        write_verdict(args.output, value)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps({"state": value["state"], "reason_codes": value["reason_codes"], "verdict_sha256": value["verdict_sha256"]}, sort_keys=True))
    return 1 if reasons else 0


def verify(args: argparse.Namespace) -> int:
    path = args.verify_verdict
    if path.is_symlink() or not path.is_file():
        print("FACTORY_BMAD_PREFLIGHT_EVIDENCE_INVALID", file=sys.stderr)
        return 2
    value = json.loads(path.read_text(encoding="utf-8"))
    actual = verdict_digest(value)
    roots = value.get("roots", {})
    expected_values = {
        "claude_binary": str(args.expected_claude_bin.resolve(strict=False)),
        "permission_rule": args.expected_permission_rule,
        "release_version": args.expected_release_version,
    }
    expected_roots = {
        "config": str(args.expected_config_root.resolve(strict=False)),
        "evidence": str(args.expected_evidence_root.resolve(strict=False)),
        "candidate": str(args.expected_candidate_root.resolve(strict=False)),
    }
    live_root = str(args.expected_live_root.resolve(strict=False))
    journey_roots = {roots.get(f"journey:{name}") for name in EXPECTED_JOURNEYS}
    mismatch = (
        value.get("state") != "PASS"
        or value.get("verdict_sha256") != actual
        or actual != args.expected_verdict_sha256
        or any(value.get(name) != expected for name, expected in expected_values.items())
        or any(roots.get(name) != expected for name, expected in expected_roots.items())
        or live_root not in journey_roots
    )
    if mismatch:
        print("FACTORY_BMAD_PREFLIGHT_EVIDENCE_MISMATCH", file=sys.stderr)
        return 2
    print(json.dumps({"state": "PASS", "verdict_sha256": actual}, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--verify-verdict", type=Path)
    value.add_argument("--expected-verdict-sha256")
    value.add_argument("--expected-claude-bin", type=Path)
    value.add_argument("--expected-config-root", type=Path)
    value.add_argument("--expected-evidence-root", type=Path)
    value.add_argument("--expected-candidate-root", type=Path)
    value.add_argument("--expected-live-root", type=Path)
    value.add_argument("--expected-permission-rule")
    value.add_argument("--expected-release-version")
    value.add_argument("--contract", type=Path)
    value.add_argument("--claude-bin", type=Path)
    value.add_argument("--observed-version")
    value.add_argument("--supported-version-prefix")
    value.add_argument("--permission-mode")
    value.add_argument("--permission-rule")
    value.add_argument("--release-version")
    value.add_argument("--bmad-version")
    value.add_argument("--config-root", type=Path)
    value.add_argument("--evidence-root", type=Path)
    value.add_argument("--candidate-root", type=Path)
    value.add_argument("--source-coupling", type=Path)
    value.add_argument("--protected-preimage", action="append", default=[])
    value.add_argument("--journey-root", action="append", default=[])
    value.add_argument("--output", type=Path)
    return value


def main() -> int:
    args = parser().parse_args()
    if args.verify_verdict is not None:
        required = (
            args.expected_verdict_sha256,
            args.expected_claude_bin,
            args.expected_config_root,
            args.expected_evidence_root,
            args.expected_candidate_root,
            args.expected_live_root,
            args.expected_permission_rule,
            args.expected_release_version,
        )
        if any(item is None for item in required):
            return 2
        return verify(args)
    required = (args.contract, args.claude_bin, args.observed_version, args.supported_version_prefix, args.permission_mode, args.permission_rule, args.release_version, args.bmad_version, args.config_root, args.evidence_root, args.candidate_root, args.source_coupling, args.output)
    if any(item is None for item in required):
        return 2
    return check(args)


if __name__ == "__main__":
    raise SystemExit(main())
