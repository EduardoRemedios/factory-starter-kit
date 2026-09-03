#!/usr/bin/env python3
"""Validate and record schema-locked Factory execution closeout evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


SCHEMA = "factory.execution-closeout.v1"
CLOSEOUT_NAME = "EXECUTION_CLOSEOUT.json"
OUTCOME_RULES = {
    "REVIEW_READY": (
        "FACTORY_EXECUTION_REVIEW_READY",
        "review_the_retained_clean_worktree",
    ),
    "NO_GO": (
        "FACTORY_EXECUTION_NO_GO",
        "review_failed_verification_evidence",
    ),
    "BLOCKED": (
        "FACTORY_EXECUTION_BLOCKED",
        "resolve_the_recorded_blocker",
    ),
}
RESULT_STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}
TOP_LEVEL_KEYS = {
    "schema",
    "run_id",
    "sprint_id",
    "execution_mode",
    "outcome",
    "reason_code",
    "next_legal_action",
    "authority_grants",
    "pack_manifest",
    "execution_authorization",
    "micro_sprints",
    "verification_manifest",
    "completed_micro_sprints",
    "verification_results",
    "retained_evidence",
}
REFERENCE_KEYS = {"path", "sha256"}
RESULT_KEYS = {"id", "status", "evidence_path", "sha256", "blocker"}
EVIDENCE_KEYS = {"id", "path", "sha256"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]{1,63}$")
RUN_ID_RE = re.compile(r"^RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+$")


class ExecutionCloseoutError(ValueError):
    def __init__(self, reason_code: str, detail: str):
        super().__init__(detail)
        self.reason_code = reason_code
        self.detail = detail


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(reason_code: str, detail: str) -> None:
    raise ExecutionCloseoutError(reason_code, detail)


def exact_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", f"{label}_keys")
    return value


def unique_strings(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or not all(isinstance(item, str) and item for item in value)
        or len(value) != len(set(value))
    ):
        fail("FACTORY_EXECUTION_CLOSEOUT_DUPLICATE_ID", label)
    return value


def safe_run_root(root: Path, run_id: str) -> Path:
    if not RUN_ID_RE.fullmatch(run_id):
        fail("FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH", "run_id")
    cursor = root.resolve()
    for part in ("docs", "Factory", "runs", run_id):
        cursor = cursor / part
        if cursor.is_symlink():
            fail("FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH", "run_root")
    if not cursor.is_dir():
        fail("FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH", "run_root")
    return cursor


def safe_file(root: Path, relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        fail("FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH", label)
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        fail("FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH", label)
    resolved_root = root.resolve()
    unresolved = root / candidate
    cursor = resolved_root
    for part in candidate.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            fail("FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH", label)
    resolved = unresolved.resolve()
    if resolved == resolved_root or resolved_root not in resolved.parents:
        fail("FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH", label)
    if not resolved.is_file() or resolved.is_symlink():
        fail("FACTORY_EXECUTION_CLOSEOUT_EVIDENCE_MISSING", f"{label}:{relative}")
    return resolved


def validate_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", f"{label}_sha256")
    return value


def validate_reference(
    root: Path,
    value: Any,
    *,
    label: str,
    expected_path: str | None = None,
) -> Path:
    reference = exact_object(value, REFERENCE_KEYS, label)
    if expected_path is not None and reference["path"] != expected_path:
        fail("FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH", label)
    path = safe_file(root, reference["path"], label)
    expected = validate_digest(reference["sha256"], label)
    if sha256_file(path) != expected:
        fail("FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH", label)
    return path


def parse_verification_ids(path: Path) -> list[str]:
    ids = [
        line.split(":", 1)[1].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("  - id:")
    ]
    if not ids or len(ids) != len(set(ids)) or not all(ID_RE.fullmatch(item) for item in ids):
        fail("FACTORY_EXECUTION_CLOSEOUT_VERIFICATION_MANIFEST_INVALID", "check_ids")
    return ids


def parse_micro_sprint_ids(path: Path) -> list[str]:
    ids = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^## (MS-[0-9]{2})(?:\s|$)", line)
        if match:
            ids.append(match.group(1))
    if not ids or len(ids) != len(set(ids)):
        fail("FACTORY_EXECUTION_CLOSEOUT_MICRO_SPRINT_MISMATCH", "planned_ids")
    return ids


def load_closeout(path: Path) -> dict[str, Any]:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", f"duplicate_key:{key}")
            value[key] = item
        return value

    try:
        if path.stat().st_size > 1024 * 1024:
            fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "oversize")
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError) as error:
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "json")
        raise AssertionError from error
    return exact_object(value, TOP_LEVEL_KEYS, "closeout")


def validate_authorization_reference(
    run_root: Path, value: Any, *, recorded: bool
) -> None:
    reference = exact_object(value, REFERENCE_KEYS, "execution_authorization")
    if reference["path"] != "EXECUTION_AUTHORIZATION.md":
        fail("FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH", "execution_authorization")
    expected = validate_digest(reference["sha256"], "execution_authorization")
    live = run_root / "EXECUTION_AUTHORIZATION.md"
    if not recorded or live.is_symlink() or live.exists():
        path = safe_file(run_root, "EXECUTION_AUTHORIZATION.md", "execution_authorization")
        if sha256_file(path) != expected:
            fail("FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH", "execution_authorization")
        return
    # A recorded closeout may outlive control archival: accept a byte-identical
    # archived authorization (e.g. MS05_EXECUTION_AUTHORIZATION.md) at run root.
    for candidate in sorted(run_root.iterdir()):
        if (
            candidate.name.endswith("_EXECUTION_AUTHORIZATION.md")
            and not candidate.is_symlink()
            and candidate.is_file()
            and sha256_file(candidate) == expected
        ):
            return
    fail("FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH", "execution_authorization_archived")


def validate_closeout(
    root: Path, run_id: str, value: dict[str, Any], *, recorded: bool = False
) -> dict[str, Any]:
    root = root.resolve()
    value = exact_object(value, TOP_LEVEL_KEYS, "closeout")
    run_root = safe_run_root(root, run_id)
    if value["schema"] != SCHEMA:
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "schema")
    if value["run_id"] != run_id:
        fail("FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH", "run_id")
    sprint_path = run_root / "SPRINT_ID.txt"
    if not sprint_path.is_file() or value["sprint_id"] != sprint_path.read_text(encoding="utf-8").strip():
        fail("FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH", "sprint_id")
    mode_path = run_root / "EXECUTION_MODE.txt"
    # Recording demands live EXECUTION_ENABLED; a recorded closeout stays valid
    # after the run is restored to PLANNING_ONLY.
    allowed_modes = {"EXECUTION_ENABLED", "PLANNING_ONLY"} if recorded else {"EXECUTION_ENABLED"}
    if (
        not mode_path.is_file()
        or mode_path.read_text(encoding="utf-8").strip() not in allowed_modes
        or value["execution_mode"] != "EXECUTION_ENABLED"
    ):
        fail("FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH", "execution_mode")
    outcome = value["outcome"]
    if outcome not in OUTCOME_RULES:
        fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", "outcome")
    reason_code, next_action = OUTCOME_RULES[outcome]
    if value["reason_code"] != reason_code or value["next_legal_action"] != next_action:
        fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", "outcome_mapping")
    if value["authority_grants"] != []:
        fail("FACTORY_EXECUTION_CLOSEOUT_AUTHORITY_VIOLATION", "authority_grants")

    validate_reference(
        run_root,
        value["pack_manifest"],
        label="pack_manifest",
        expected_path="pack/PACK_MANIFEST.md",
    )
    validate_authorization_reference(
        run_root, value["execution_authorization"], recorded=recorded
    )
    micro_path = validate_reference(
        run_root,
        value["micro_sprints"],
        label="micro_sprints",
        expected_path="pack/micro_sprints.md",
    )
    manifest_path = validate_reference(
        run_root,
        value["verification_manifest"],
        label="verification_manifest",
        expected_path="pack/verification_manifest.yaml",
    )

    planned_micro_sprints = parse_micro_sprint_ids(micro_path)
    completed = unique_strings(value["completed_micro_sprints"], "completed_micro_sprints")
    if completed != planned_micro_sprints:
        fail("FACTORY_EXECUTION_CLOSEOUT_MICRO_SPRINT_MISMATCH", "completed_micro_sprints")

    expected_checks = parse_verification_ids(manifest_path)
    results = value["verification_results"]
    if not isinstance(results, list):
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "verification_results")
    result_ids: list[str] = []
    non_passing = 0
    for index, item in enumerate(results):
        result_item = exact_object(item, RESULT_KEYS, f"verification_result_{index}")
        check_id = result_item["id"]
        if not isinstance(check_id, str) or not ID_RE.fullmatch(check_id):
            fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "verification_id")
        result_ids.append(check_id)
        status = result_item["status"]
        if status not in RESULT_STATUSES:
            fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "verification_status")
        evidence_path = safe_file(root, result_item["evidence_path"], f"verification:{check_id}")
        expected_digest = validate_digest(result_item["sha256"], f"verification:{check_id}")
        if sha256_file(evidence_path) != expected_digest:
            fail("FACTORY_EXECUTION_CLOSEOUT_EVIDENCE_DIGEST_MISMATCH", check_id)
        blocker = result_item["blocker"]
        if status == "PASS" and blocker is not None:
            fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", check_id)
        if status != "PASS":
            non_passing += 1
            if not isinstance(blocker, str) or not blocker.strip():
                fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", check_id)
    if len(result_ids) != len(set(result_ids)):
        fail("FACTORY_EXECUTION_CLOSEOUT_DUPLICATE_ID", "verification_results")
    if result_ids != expected_checks:
        fail("FACTORY_EXECUTION_CLOSEOUT_VERIFICATION_COVERAGE_MISMATCH", "verification_results")
    if outcome == "REVIEW_READY" and non_passing:
        fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", "review_ready_requires_all_pass")
    if outcome != "REVIEW_READY" and not non_passing:
        fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", "negative_requires_blocker")
    if outcome == "REVIEW_READY" and any(item["status"] == "NOT_RUN" for item in results):
        fail("FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION", "not_run")

    retained = value["retained_evidence"]
    if not isinstance(retained, list) or not retained:
        fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "retained_evidence")
    retained_ids: list[str] = []
    retained_paths: list[str] = []
    for index, item in enumerate(retained):
        evidence = exact_object(item, EVIDENCE_KEYS, f"retained_evidence_{index}")
        if not isinstance(evidence["id"], str) or not ID_RE.fullmatch(evidence["id"]):
            fail("FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", "retained_evidence_id")
        retained_ids.append(evidence["id"])
        retained_paths.append(evidence["path"])
        evidence_path = safe_file(root, evidence["path"], f"retained:{evidence['id']}")
        expected_digest = validate_digest(evidence["sha256"], f"retained:{evidence['id']}")
        if sha256_file(evidence_path) != expected_digest:
            fail("FACTORY_EXECUTION_CLOSEOUT_EVIDENCE_DIGEST_MISMATCH", evidence["id"])
    if len(retained_ids) != len(set(retained_ids)) or len(retained_paths) != len(set(retained_paths)):
        fail("FACTORY_EXECUTION_CLOSEOUT_DUPLICATE_ID", "retained_evidence")

    return {
        "schema": SCHEMA,
        "run_id": run_id,
        "sprint_id": value["sprint_id"],
        "outcome": outcome,
        "reason_code": reason_code,
        "next_legal_action": next_action,
        "completed_micro_sprints": planned_micro_sprints,
        "verification_check_ids": expected_checks,
        "verification_result_count": len(results),
        "retained_evidence_count": len(retained),
    }


def validate_closeout_file(root: Path, run_id: str) -> dict[str, Any]:
    path = safe_run_root(root, run_id) / CLOSEOUT_NAME
    if not path.is_file() or path.is_symlink():
        fail("FACTORY_EXECUTION_CLOSEOUT_MISSING", CLOSEOUT_NAME)
    value = load_closeout(path)
    validated = validate_closeout(root, run_id, value, recorded=True)
    return {**validated, "path": path.relative_to(root.resolve()).as_posix(), "sha256": sha256_file(path)}


def record_closeout(root: Path, run_id: str, input_path: Path) -> dict[str, Any]:
    root = root.resolve()
    resolved_input = input_path.resolve()
    if not resolved_input.is_file() or resolved_input.is_symlink():
        fail("FACTORY_EXECUTION_CLOSEOUT_INPUT_MISSING", str(input_path))
    value = load_closeout(resolved_input)
    validated = validate_closeout(root, run_id, value)
    target = safe_run_root(root, run_id) / CLOSEOUT_NAME
    canonical = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if target.exists():
        if not target.is_file() or target.is_symlink() or target.read_bytes() != canonical:
            fail("FACTORY_EXECUTION_CLOSEOUT_EXISTS", CLOSEOUT_NAME)
        mutations: list[str] = []
    else:
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(canonical)
        os.replace(temporary, target)
        mutations = [target.relative_to(root).as_posix()]
    return {
        **validated,
        "path": target.relative_to(root).as_posix(),
        "sha256": sha256_file(target),
        "mutations": mutations,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="factory-execution-closeout")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--root", required=True)
    validate.add_argument("--run", required=True)
    validate.add_argument("--json", action="store_true")
    record = subparsers.add_parser("record")
    record.add_argument("--root", required=True)
    record.add_argument("--run", required=True)
    record.add_argument("--input", required=True)
    record.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "validate":
            payload = validate_closeout_file(Path(args.root), args.run)
        else:
            payload = record_closeout(Path(args.root), args.run, Path(args.input))
    except ExecutionCloseoutError as error:
        payload = {"status": "FAIL", "reason_code": error.reason_code, "detail": error.detail, "mutations": []}
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
