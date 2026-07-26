#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "mission_cursor_lint: FAIL - $1" >&2
  exit 1
}

require_nonempty_file() {
  local path="$1"
  [[ -s "$path" ]] || fail "required file missing or empty: $path"
}

MISSION_ID="${1:-}"
CURSOR_PATH="${2:-}"

[[ -n "$MISSION_ID" ]] || fail "usage: bash scripts/mission_cursor_lint.sh <MISSION_ID> [cursor_path]"

MISSION_ROOT="docs/Factory/missions/$MISSION_ID"
CURSOR_PATH="${CURSOR_PATH:-$MISSION_ROOT/MISSION_CURSOR.json}"
MANIFEST="$MISSION_ROOT/MISSION_MANIFEST.md"
CHECKPOINT="$MISSION_ROOT/MISSION_CHECKPOINT.md"
RECALL="$MISSION_ROOT/MISSION_CONTEXT_RECALL_REPORT.md"

require_nonempty_file "$CURSOR_PATH"
require_nonempty_file "$MANIFEST"
require_nonempty_file "$CHECKPOINT"
require_nonempty_file "$RECALL"

python3 - "$MISSION_ID" "$CURSOR_PATH" "$MANIFEST" "$CHECKPOINT" "$RECALL" <<'PY'
import hashlib
import json
import pathlib
import re
import sys

mission_id, cursor_path, manifest_path, checkpoint_path, recall_path = sys.argv[1:]
cursor_file = pathlib.Path(cursor_path)
manifest_file = pathlib.Path(manifest_path)
checkpoint_file = pathlib.Path(checkpoint_path)
recall_file = pathlib.Path(recall_path)

ALLOWED_MISSION_LIFECYCLES = {
    "MISSION_PLANNING",
    "MISSION_READY_FOR_CHECKPOINT",
    "MISSION_AUTHORIZED",
    "MISSION_EXECUTING",
    "MISSION_HALTED",
    "MISSION_COMPLETED",
}

ALLOWED_UNIT_STATUSES = {
    "planned",
    "running",
    "pack_complete",
    "closed_go",
    "failed",
    "skipped",
    "planning_signal",
}

ALLOWED_ACTIONS = {
    "read_mission_artifacts",
    "read_current_unit_pack",
    "initialize_unit_factory_run",
    "run_mission_lint",
    "run_unit_validator",
    "execute_unit_micro_sprint",
    "update_unit_handoff",
    "update_manifest_from_unit_evidence",
    "advance_to_next_unit",
    "await_human_checkpoint",
    "halt",
}

ACTION_ALLOWED_STATUSES = {
    "read_mission_artifacts": ALLOWED_UNIT_STATUSES,
    "read_current_unit_pack": {"planned", "running", "planning_signal"},
    "initialize_unit_factory_run": {"planned", "planning_signal"},
    "run_mission_lint": {"planned", "running"},
    "run_unit_validator": {"running"},
    "execute_unit_micro_sprint": {"running"},
    "update_unit_handoff": {"running"},
    "update_manifest_from_unit_evidence": {"running", "pack_complete", "closed_go", "failed", "skipped"},
    "advance_to_next_unit": {"pack_complete", "closed_go", "skipped"},
    "await_human_checkpoint": {"planned", "pack_complete", "planning_signal"},
    "halt": ALLOWED_UNIT_STATUSES,
}

EXECUTION_ACTIONS = {"execute_unit_micro_sprint"}


def fail(message: str) -> None:
    print(f"mission_cursor_lint: FAIL - {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text()
    except UnicodeDecodeError as exc:
        fail(f"could not read text file {path}: {exc}")


def file_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def clean(text: str) -> str:
    text = re.sub(r"`", "", text)
    text = re.sub(r"\*\*", "", text)
    return " ".join(text.split()).strip()


def normalize_status(value: str) -> str:
    raw = clean(value).lower()
    if "planning_signal" in raw:
        return "planning_signal"
    if "closed (go)" in raw or raw == "closed_go":
        return "closed_go"
    if raw == "pack_complete" or raw == "completed":
        return "pack_complete"
    if raw in {"planned", "pending"}:
        return "planned"
    if raw == "running":
        return "running"
    if raw == "failed":
        return "failed"
    if raw == "skipped" or "not executed" in raw:
        return "skipped"
    return raw


def parse_checkpoint_decision(text: str) -> str | None:
    match = re.search(r"^- Decision:\s*(GO|NO-GO)\s*$", text, re.M)
    return match.group(1) if match else None


def parse_manifest_units(text: str) -> list[dict[str, object]]:
    if "## Ordered Mission Units" not in text:
        fail("MISSION_MANIFEST.md missing '## Ordered Mission Units'")
    section_match = re.search(r"^## Ordered Mission Units\s*\n(?P<body>.*?)(?=^## |\Z)", text, re.S | re.M)
    if not section_match:
        fail("could not parse ordered mission units section")
    table_lines = [line.rstrip() for line in section_match.group("body").splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        fail("ordered mission units table is missing header, delimiter, or rows")

    headers = split_row(table_lines[0])
    header_index = {header: idx for idx, header in enumerate(headers)}
    for required in ("Order", "RUN_ID", "SPRINT_ID", "Pack Path"):
        if required not in header_index:
            fail(f"ordered mission units table missing required column: {required}")
    status_header = next((header for header in headers if header.startswith("Status")), None)
    if status_header is None:
        fail("ordered mission units table missing Status column")

    units = []
    for row_line in table_lines[2:]:
        cells = split_row(row_line)
        if len(cells) != len(headers):
            fail(f"malformed ordered mission units row: {row_line}")
        order_match = re.search(r"\d+", cells[header_index["Order"]])
        if not order_match:
            fail(f"could not parse unit order from row: {row_line}")
        run_id_match = re.search(r"RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+", cells[header_index["RUN_ID"]])
        sprint_id_match = re.search(
            r"(?:SPRINT_\d{8}_\d{3}|[A-Z0-9]+(?:[A-Z0-9_-]*[A-Z0-9])?-\d{2})",
            cells[header_index["SPRINT_ID"]],
        )
        pack_path_match = re.search(
            r"docs/Factory/runs/RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+/pack",
            cells[header_index["Pack Path"]],
        )
        status = normalize_status(cells[headers.index(status_header)])
        units.append(
            {
                "order": int(order_match.group(0)),
                "unit_id": clean(cells[header_index["Unit ID"]]) if "Unit ID" in header_index else None,
                "run_id": run_id_match.group(0) if run_id_match else None,
                "sprint_id": sprint_id_match.group(0) if sprint_id_match else None,
                "pack_path": pack_path_match.group(0) if pack_path_match else None,
                "status": status,
                "raw_status": clean(cells[headers.index(status_header)]),
            }
        )
    if [unit["order"] for unit in units] != sorted(unit["order"] for unit in units):
        fail("mission unit ordering is not strictly increasing")
    return units


try:
    cursor = json.loads(read_text(cursor_file))
except json.JSONDecodeError as exc:
    fail(f"MISSION_CURSOR.json is not valid JSON: {exc}")

manifest = read_text(manifest_file)
checkpoint = read_text(checkpoint_file)
recall = read_text(recall_file)

if cursor.get("schema_version") != 1:
    fail("schema_version must be 1")
if cursor.get("cursor_kind") != "derived_resume_cursor":
    fail("cursor_kind must be derived_resume_cursor")
if cursor.get("mission_id") != mission_id:
    fail(f"cursor mission_id does not match requested mission: {cursor.get('mission_id')} != {mission_id}")
if mission_id not in manifest:
    fail("MISSION_MANIFEST.md does not mention the requested mission id")
if mission_id not in checkpoint:
    fail("MISSION_CHECKPOINT.md does not mention the requested mission id")

mission_lifecycle = cursor.get("mission_lifecycle")
if mission_lifecycle not in ALLOWED_MISSION_LIFECYCLES:
    fail(f"invalid mission_lifecycle: {mission_lifecycle}")

checkpoint_decision = parse_checkpoint_decision(checkpoint)
if checkpoint_decision not in {"GO", "NO-GO"}:
    fail("MISSION_CHECKPOINT.md missing explicit '- Decision: GO' or '- Decision: NO-GO' line")
if cursor.get("checkpoint_decision") != checkpoint_decision:
    fail("cursor checkpoint_decision does not match MISSION_CHECKPOINT.md")

unit_status = normalize_status(str(cursor.get("current_unit_status", "")))
if unit_status not in ALLOWED_UNIT_STATUSES:
    fail(f"invalid current_unit_status: {cursor.get('current_unit_status')}")

next_action = cursor.get("next_legal_action")
if next_action not in ALLOWED_ACTIONS:
    fail(f"invalid next_legal_action: {next_action}")
if unit_status not in ACTION_ALLOWED_STATUSES[next_action]:
    fail(f"next_legal_action '{next_action}' is not valid for current_unit_status '{unit_status}'")

halt_required = cursor.get("halt_required")
if not isinstance(halt_required, bool):
    fail("halt_required must be a boolean")
if halt_required:
    if next_action != "halt":
        fail("halt_required=true requires next_legal_action=halt")
    if not cursor.get("halt_reason"):
        fail("halt_required=true requires halt_reason")
else:
    if next_action == "halt":
        fail("next_legal_action=halt requires halt_required=true")

execution_mode = cursor.get("execution_mode")
if execution_mode not in {"PLANNING_ONLY", "EXECUTION_ENABLED"}:
    fail(f"invalid execution_mode: {execution_mode}")
if next_action in EXECUTION_ACTIONS and execution_mode != "EXECUTION_ENABLED":
    fail(f"{next_action} requires EXECUTION_ENABLED")
if next_action in EXECUTION_ACTIONS and checkpoint_decision != "GO":
    fail(f"{next_action} requires mission checkpoint GO")

if "Coverage Verdict: WEAK" in recall and not halt_required:
    fail("MISSION_CONTEXT_RECALL_REPORT.md records WEAK coverage and cursor is not halted")

scope_text = "\n".join((manifest, checkpoint, recall))
if re.search(r"(?is)(unresolved[^\n]*\[SCOPE EXPANSION\]|\[SCOPE EXPANSION\][^\n]*unresolved)", scope_text) and not halt_required:
    fail("mission artifacts record unresolved [SCOPE EXPANSION] and cursor is not halted")

source_artifacts = cursor.get("source_artifacts")
fingerprints = cursor.get("source_artifact_fingerprints")
if not isinstance(source_artifacts, list) or not source_artifacts:
    fail("source_artifacts must be a non-empty list")
if not isinstance(fingerprints, dict) or not fingerprints:
    fail("source_artifact_fingerprints must be a non-empty object")

required_sources = {str(manifest_file), str(checkpoint_file), str(recall_file)}
missing_sources = sorted(required_sources - set(source_artifacts))
if missing_sources:
    fail(f"source_artifacts missing required mission sources: {', '.join(missing_sources)}")

for artifact in source_artifacts:
    if not isinstance(artifact, str):
        fail("source_artifacts entries must be strings")
    artifact_path = pathlib.Path(artifact)
    if artifact_path.is_absolute():
        fail(f"source artifact must be repository-relative: {artifact}")
    if not artifact_path.is_file() or artifact_path.stat().st_size == 0:
        fail(f"source artifact missing or empty: {artifact}")
    expected_digest = fingerprints.get(artifact)
    if not isinstance(expected_digest, str) or not expected_digest.startswith("sha256:"):
        fail(f"source_artifact_fingerprints missing sha256 digest for {artifact}")
    actual_digest = file_sha256(artifact_path)
    if expected_digest != actual_digest:
        fail(f"source artifact fingerprint mismatch for {artifact}")

units = parse_manifest_units(manifest)
current_unit = cursor.get("current_unit")
if not isinstance(current_unit, dict):
    fail("current_unit must be an object")
current_order = current_unit.get("order")
if not isinstance(current_order, int):
    fail("current_unit.order must be an integer")
manifest_unit = next((unit for unit in units if unit["order"] == current_order), None)
if manifest_unit is None:
    fail(f"current_unit.order not found in manifest: {current_order}")
if manifest_unit["status"] != unit_status:
    fail(
        "cursor current_unit_status does not match manifest "
        f"(cursor={unit_status}, manifest={manifest_unit['raw_status']})"
    )

for key in ("unit_id", "run_id", "sprint_id", "pack_path"):
    cursor_value = current_unit.get(key)
    manifest_value = manifest_unit.get(key)
    if cursor_value is None:
        continue
    if manifest_value is not None and cursor_value != manifest_value:
        fail(f"cursor current_unit.{key} does not match manifest ({cursor_value} != {manifest_value})")

run_id = current_unit.get("run_id") or manifest_unit.get("run_id")
if run_id:
    exec_mode_path = pathlib.Path("docs") / "Factory" / "runs" / str(run_id) / "EXECUTION_MODE.txt"
    if exec_mode_path.is_file():
        actual_mode = exec_mode_path.read_text().strip()
        if actual_mode != execution_mode:
            fail(f"cursor execution_mode does not match {exec_mode_path}: {execution_mode} != {actual_mode}")
    elif next_action not in {"initialize_unit_factory_run", "await_human_checkpoint", "halt"}:
        fail(f"current unit run root has no EXECUTION_MODE.txt: {exec_mode_path}")

pack_path = current_unit.get("pack_path") or manifest_unit.get("pack_path")
if next_action == "read_current_unit_pack":
    if not pack_path:
        fail("read_current_unit_pack requires current_unit.pack_path")
    if not pathlib.Path(str(pack_path)).is_dir():
        fail(f"current unit pack path does not exist: {pack_path}")

validator = cursor.get("last_non_cursor_validator")
if next_action != "halt":
    if not isinstance(validator, dict):
        fail("last_non_cursor_validator must be an object when cursor is not halted")
    validator_name = validator.get("name")
    validator_status = validator.get("status")
    validator_artifact = validator.get("artifact_path")
    if validator_name == "mission_cursor_lint":
        fail("last_non_cursor_validator must not be mission_cursor_lint")
    if validator_status != "PASS":
        fail("last_non_cursor_validator.status must be PASS when cursor is not halted")
    if not isinstance(validator_artifact, str):
        fail("last_non_cursor_validator.artifact_path must be a string")
    validator_path = pathlib.Path(validator_artifact)
    if not validator_path.is_file() or validator_path.stat().st_size == 0:
        fail(f"last non-cursor validator artifact missing or empty: {validator_artifact}")
    expected_digest = fingerprints.get(validator_artifact)
    if expected_digest is not None and expected_digest != file_sha256(validator_path):
        fail(f"last non-cursor validator fingerprint mismatch for {validator_artifact}")

if mission_lifecycle in {"MISSION_HALTED", "MISSION_COMPLETED"} and not halt_required:
    if next_action not in {"read_mission_artifacts", "halt"}:
        fail(f"{mission_lifecycle} only allows read_mission_artifacts or halted cursor action")

print("mission_cursor_lint: PASS")
print(
    "mission_cursor_lint: "
    f"mission_id={mission_id} lifecycle={mission_lifecycle} "
    f"unit_order={current_order} unit_status={unit_status} next_action={next_action}"
)
PY
