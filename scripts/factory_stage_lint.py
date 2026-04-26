from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class FactoryStageLintError(Exception):
    """Raised when stage-lint cannot resolve the requested run or stage."""


STAGES = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "I2")
CYCLE_STAGES = {"B", "C", "I"}

PLACEHOLDER_PATTERNS = (
    (re.compile(r"\bYYYY-MM-DD\b"), "YYYY-MM-DD"),
    (re.compile(r"\bHH:MM\b"), "HH:MM"),
    (re.compile(r"<RUN_ID>"), "<RUN_ID>"),
    (re.compile(r"<SPRINT_ID>"), "<SPRINT_ID>"),
    (re.compile(r"<X>"), "<X>"),
    (re.compile(r"\.\.\."), "..."),
)

HANDOFF_SECTIONS = (
    "## Version",
    "## Change Log",
    "## Stage",
    "## Inputs (LOAD)",
    "## Inputs (DISK)",
    "## Skill Routing Contract",
    "## Outputs Produced (paths)",
    "## Verification Steps Recommended",
    "## Exit Criteria Status",
)

STAGE_OUTPUTS: dict[str, tuple[str, ...]] = {
    "A": ("pack/intent.md",),
    "B": ("pack/intent_redteam.md",),
    "C": ("pack/intent.md", "pack/intent_synthesis.md"),
    "D": ("pack/intent_lock_report.md",),
    "E": ("pack/premortem.md", "pack/risk_register.md"),
    "F": ("pack/fixtures", "pack/verification_plan.md", "pack/traceability_matrix.md"),
    "G": ("pack/micro_sprints.md",),
    "J": ("pack/PACK_MANIFEST.md", "pack/PACK_CHECKLIST.md"),
    "I2": ("pack/PACK_AUDIT_REPORT.md", "pack/PACK_MANIFEST.md"),
}


def lint_stage(root: Path, run: str, stage: str) -> dict[str, Any]:
    stage = stage.upper()
    if stage not in STAGES:
        raise FactoryStageLintError(f"unknown stage: {stage}")

    run_root = _resolve_run(root=root, run=run)
    pack_dir = run_root / "pack"
    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    handoff = pack_dir / "HANDOFF" / f"HANDOFF_STAGE_{stage}.md"
    checked_files.append(str(handoff))
    if not handoff.exists():
        errors.append(f"missing required handoff: {handoff}")
        text = ""
    elif not handoff.is_file():
        errors.append(f"handoff path is not a file: {handoff}")
        text = ""
    elif handoff.stat().st_size == 0:
        errors.append(f"handoff file is empty: {handoff}")
        text = ""
    else:
        text = _read_text(handoff)

    if text:
        _check_handoff_shape(handoff, text, stage, errors, warnings)

    for output in _stage_outputs(run_root=run_root, stage=stage):
        path = run_root / output
        checked_files.append(str(path))
        if not path.exists():
            errors.append(f"missing expected stage output: {path}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"expected stage output is empty: {path}")
        elif path.is_dir() and not any(path.iterdir()):
            errors.append(f"expected stage output directory is empty: {path}")

    unique_checked_files = sorted(set(checked_files))
    return {
        "status": "PASS" if not errors else "FAIL",
        "run_root": str(run_root),
        "stage": stage,
        "checked_file_count": len(unique_checked_files),
        "checked_files": unique_checked_files,
        "errors": errors,
        "warnings": warnings,
    }


def format_stage_lint(payload: dict[str, Any]) -> str:
    lines = [
        f"stage_lint: {payload['status']}",
        f"run_root={payload['run_root']}",
        f"stage={payload['stage']}",
        (
            f"checked_files={payload['checked_file_count']} "
            f"errors={len(payload['errors'])} warnings={len(payload['warnings'])}"
        ),
    ]
    if payload["errors"]:
        lines.append("")
        lines.append("Errors:")
        lines.extend(f"- {item}" for item in payload["errors"])
    if payload["warnings"]:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"- {item}" for item in payload["warnings"])
    return "\n".join(lines) + "\n"


def _resolve_run(root: Path, run: str) -> Path:
    run_candidate = Path(run).expanduser()
    if not run_candidate.is_absolute():
        direct = (root / run_candidate).resolve()
        by_id = (root / "docs" / "Factory" / "runs" / run).resolve()
        run_candidate = direct if direct.exists() else by_id
    else:
        run_candidate = run_candidate.resolve()

    if not run_candidate.exists():
        raise FactoryStageLintError(f"run root does not exist: {run_candidate}")
    return run_candidate


def _check_handoff_shape(path: Path, text: str, stage: str, errors: list[str], warnings: list[str]) -> None:
    for pattern, label in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path} contains unresolved placeholder {label}")

    for section in HANDOFF_SECTIONS:
        if section not in text:
            errors.append(f"{path} is missing {section}")

    if not re.search(r"## Exit Criteria Status\s*\n-\s*(PASS|FAIL)\b", text):
        errors.append(f"{path} does not record concrete exit criteria PASS or FAIL")

    if stage in CYCLE_STAGES and "Iteration:" not in text:
        errors.append(f"{path} is missing required iteration metadata")

    word_count = _word_count_without_code_blocks(text)
    if word_count > 500:
        errors.append(f"{path} exceeds handoff word cap: {word_count} words > 500")

    if re.search(r"^-\s*Skill used \(or `NONE`\):\s*$", text, flags=re.MULTILINE):
        warnings.append(f"{path} may not have instantiated the Skill Routing Contract")


def _stage_outputs(run_root: Path, stage: str) -> tuple[str, ...]:
    if stage == "H":
        sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
        if sprint_id:
            return ("SPRINT_ID.txt", f"pack/{sprint_id}_ENVELOPE.md")
        return ("SPRINT_ID.txt",)
    if stage == "I":
        sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
        if sprint_id:
            return (f"pack/{sprint_id}_ENVELOPE.md", f"pack/{sprint_id}_ENVELOPE_REDTEAM.md")
        return ()
    return STAGE_OUTPUTS.get(stage, ())


def _word_count_without_code_blocks(text: str) -> int:
    lines: list[str] = []
    in_code_block = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            lines.append(line)
    return len(re.findall(r"\b[\w'-]+\b", "\n".join(lines)))


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
