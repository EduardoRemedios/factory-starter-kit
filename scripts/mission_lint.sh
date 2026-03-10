#!/usr/bin/env bash
set -euo pipefail

# Factory Starter Kit — Mission Continuity Lint
#
# This validates mission continuity from authored mission docs and
# referenced run artifacts. It intentionally does not maintain a second
# mission-state file.
#
# Adapt the project-state checks if your repo uses different canonical
# state docs or naming conventions.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "mission_lint: FAIL - $1" >&2
  exit 1
}

require_nonempty_file() {
  local path="$1"
  [[ -s "$path" ]] || fail "required file missing or empty: $path"
}

MISSION_ID="${1:-}"
[[ -n "$MISSION_ID" ]] || fail "usage: bash scripts/mission_lint.sh <MISSION_ID>"

MANIFEST="docs/Factory/missions/$MISSION_ID/MISSION_MANIFEST.md"
CHECKPOINT="docs/Factory/missions/$MISSION_ID/MISSION_CHECKPOINT.md"

require_nonempty_file "$MANIFEST"
require_nonempty_file "$CHECKPOINT"

python3 - "$MISSION_ID" "$MANIFEST" "$CHECKPOINT" <<'PY'
import pathlib
import re
import sys

mission_id, manifest_path, checkpoint_path = sys.argv[1:]
manifest = pathlib.Path(manifest_path).read_text()
checkpoint = pathlib.Path(checkpoint_path).read_text()
root = pathlib.Path(".")


def fail(message: str) -> None:
    print(f"mission_lint: FAIL - {message}", file=sys.stderr)
    raise SystemExit(1)


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
    if raw in {"pack_complete", "completed"}:
        return "pack_complete"
    if raw in {"planned", "pending"}:
        return "planned"
    if raw in {"running", "failed", "skipped"}:
        return raw
    return raw


if "## Ordered Mission Units" not in manifest:
    fail("MISSION_MANIFEST.md missing '## Ordered Mission Units'")

if not re.search(r"Decision:\s*GO", checkpoint):
    fail("MISSION_CHECKPOINT.md missing explicit GO decision")

section_match = re.search(r"^## Ordered Mission Units\s*\n(?P<body>.*?)(?=^## |\Z)", manifest, re.S | re.M)
if not section_match:
    fail("could not parse ordered mission units section")

table_lines = [line.rstrip() for line in section_match.group("body").splitlines() if line.strip().startswith("|")]
if len(table_lines) < 3:
    fail("ordered mission units table is incomplete")

headers = split_row(table_lines[0])
header_index = {header: idx for idx, header in enumerate(headers)}
status_header = next((h for h in headers if h.startswith("Status")), None)
if status_header is None:
    fail("ordered mission units table missing Status column")

required_headers = ("Order", "RUN_ID", "SPRINT_ID", "Pack Path")
for header in required_headers:
    if header not in header_index:
        fail(f"ordered mission units table missing required column: {header}")

units = []
for line in table_lines[2:]:
    cells = split_row(line)
    if len(cells) != len(headers):
        fail(f"malformed mission row: {line}")
    order_match = re.search(r"\d+", cells[header_index["Order"]])
    if not order_match:
        fail(f"could not parse order in row: {line}")
    run_id_match = re.search(r"RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+", cells[header_index["RUN_ID"]])
    sprint_id_match = re.search(r"(?:SPRINT_\d{8}_\d{3}|[A-Z0-9]+(?:[A-Z0-9_-]*[A-Z0-9])?-\d{2})", cells[header_index["SPRINT_ID"]])
    pack_path_match = re.search(r"docs/Factory/runs/RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+/pack", cells[header_index["Pack Path"]])
    units.append(
        {
            "order": int(order_match.group(0)),
            "run_id": run_id_match.group(0) if run_id_match else None,
            "sprint_id": sprint_id_match.group(0) if sprint_id_match else None,
            "pack_path": pack_path_match.group(0) if pack_path_match else None,
            "status": normalize_status(cells[headers.index(status_header)]),
        }
    )

terminal = {"pack_complete", "closed_go"}
for unit in units:
    if unit["status"] not in terminal:
        continue
    if not unit["run_id"] or not unit["pack_path"]:
        fail(f"terminal mission unit missing run or pack path metadata: order={unit['order']}")
    expected_pack = f"docs/Factory/runs/{unit['run_id']}/pack"
    if unit["pack_path"] != expected_pack:
        fail(f"pack path mismatch for order={unit['order']}: expected {expected_pack}")
    for relpath in ("PACK_AUDIT_REPORT.md", "HANDOFF/HANDOFF_STAGE_I2.md"):
        path = root / expected_pack / relpath
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"missing required pack evidence for order={unit['order']}: {path}")
    if unit["status"] == "closed_go":
        human_go = root / "docs" / "Factory" / "runs" / unit["run_id"] / "HUMAN_GO.txt"
        if not human_go.is_file() or human_go.stat().st_size == 0:
            fail(f"closed_go unit missing HUMAN_GO evidence: order={unit['order']}")

next_planned = next((unit for unit in units if unit["status"] == "planned"), None)
if next_planned:
    predecessor_index = units.index(next_planned) - 1
    if predecessor_index >= 0:
        predecessor = units[predecessor_index]
        if predecessor["status"] not in terminal:
            fail(f"next planned unit order={next_planned['order']} does not follow a terminal predecessor")

closed_go_units = [unit for unit in units if unit["status"] == "closed_go"]
if closed_go_units:
    latest = max(closed_go_units, key=lambda item: item["order"])
    for doc in ("docs/PROJECT_STATE.md", "docs/ROADMAP.md", "docs/CHANGELOG.md"):
        text = (root / doc).read_text()
        if latest["sprint_id"] and latest["sprint_id"] in text:
            continue
        if latest["run_id"] and latest["run_id"] in text:
            continue
        fail(f"canonical state doc missing latest closed_go reference ({latest['sprint_id'] or latest['run_id']}): {doc}")

print("mission_lint: PASS")
print(f"mission_lint: mission_id={mission_id} units={len(units)} closed_go={len(closed_go_units)}")
PY
