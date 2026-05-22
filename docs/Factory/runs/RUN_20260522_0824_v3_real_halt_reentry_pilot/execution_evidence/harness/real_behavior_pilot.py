#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


RUN_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = RUN_ROOT / "execution_evidence"


def main() -> int:
    halt_result = run_failed_command_halt()
    valid_reentry = run_reentry_case("reentry_valid", source_revision="intent-v2", cursor_revision="intent-v2")
    stale_reentry = run_reentry_case("reentry_stale_cursor", source_revision="intent-v2", cursor_revision="intent-v1")

    assertions = [
        halt_result["halted"] is True,
        halt_result["command_returncode"] != 0,
        halt_result["continuation_executed"] is False,
        halt_result["continuation_marker_exists"] is False,
        valid_reentry["resume_allowed"] is True,
        valid_reentry["halted"] is False,
        stale_reentry["resume_allowed"] is False,
        stale_reentry["halted"] is True,
    ]

    summary = {
        "pilot": "v3_real_halt_reentry",
        "status": "PASS" if all(assertions) else "FAIL",
        "halt_failed_command": halt_result,
        "reentry_valid": valid_reentry,
        "reentry_stale_cursor": stale_reentry,
    }
    write_json(EVIDENCE_DIR / "pilot_summary.json", summary)
    write_summary(summary)
    return 0 if all(assertions) else 1


def run_failed_command_halt() -> dict[str, Any]:
    case_dir = EVIDENCE_DIR / "halt_failed_command"
    case_dir.mkdir(parents=True, exist_ok=True)
    continuation_marker = case_dir / "CONTINUED_AFTER_FAILURE"
    if continuation_marker.exists():
        continuation_marker.unlink()

    command = ["bash", "-lc", "printf 'halt pilot command failed as intended\\n'; exit 7"]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    halted = completed.returncode != 0

    continuation_executed = False
    if not halted:
        continuation_marker.write_text("continuation ran\n", encoding="utf-8")
        continuation_executed = True

    result = {
        "case": "halt_failed_command",
        "command": " ".join(command),
        "command_returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "halted": halted,
        "halt_reason": "halt_on_failure command exited nonzero" if halted else "",
        "continuation_executed": continuation_executed,
        "continuation_marker_exists": continuation_marker.exists(),
    }
    write_json(case_dir / "result.json", result)
    return result


def run_reentry_case(case_name: str, *, source_revision: str, cursor_revision: str) -> dict[str, Any]:
    case_dir = EVIDENCE_DIR / case_name
    case_dir.mkdir(parents=True, exist_ok=True)

    source_state = {
        "artifact": "pack/intent.md",
        "mission_status": "interrupted",
        "source_revision": source_revision,
        "authority": "authored_factory_artifact",
    }
    derived_cursor = {
        "resume_target": "pack/intent.md",
        "cursor_revision": cursor_revision,
        "authority": "derived_resume_cursor",
    }

    write_json(case_dir / "source_state.json", source_state)
    write_json(case_dir / "derived_cursor.json", derived_cursor)

    revisions_match = source_state["source_revision"] == derived_cursor["cursor_revision"]
    result = {
        "case": case_name,
        "source_revision": source_state["source_revision"],
        "cursor_revision": derived_cursor["cursor_revision"],
        "source_authority": source_state["authority"],
        "cursor_authority": derived_cursor["authority"],
        "resume_allowed": revisions_match,
        "halted": not revisions_match,
        "halt_reason": "" if revisions_match else "derived cursor conflicts with authored source artifact",
        "resume_source": "authored_factory_artifact" if revisions_match else "",
    }
    write_json(case_dir / "result.json", result)
    return result


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_summary(summary: dict[str, Any]) -> None:
    lines = [
        "# Real Halt And Reentry Pilot Summary",
        "",
        f"- Status: {summary['status']}",
        f"- Failed-command halted: {summary['halt_failed_command']['halted']}",
        f"- Continuation marker exists: {summary['halt_failed_command']['continuation_marker_exists']}",
        f"- Valid reentry allowed: {summary['reentry_valid']['resume_allowed']}",
        f"- Stale cursor halted: {summary['reentry_stale_cursor']['halted']}",
        "",
        "This evidence is run-local and does not promote Factory v3.",
    ]
    (EVIDENCE_DIR / "PILOT_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
