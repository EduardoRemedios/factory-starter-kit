from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


class FactoryPackLintError(Exception):
    """Raised when pack-lint cannot resolve the requested run or pack."""


STAGES = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "I2")

RUN_ROOT_FILES = (
    "raw_brief.md",
    "KNOWLEDGE_LINT.txt",
    "CONTEXT_RECALL_REPORT.md",
    "EXECUTION_MODE.txt",
    "SPRINT_ID.txt",
)

PACK_FILES = (
    "intent.md",
    "intent_redteam.md",
    "intent_synthesis.md",
    "intent_lock_report.md",
    "premortem.md",
    "risk_register.md",
    "verification_plan.md",
    "traceability_matrix.md",
    "micro_sprints.md",
    "PACK_MANIFEST.md",
    "PACK_CHECKLIST.md",
    "PACK_AUDIT_REPORT.md",
)

VERIFICATION_MANIFEST = "verification_manifest.yaml"

VERIFICATION_TIERS = {"V0", "V1", "V2", "V3", "V4"}
VERIFICATION_CHECK_TYPES = {
    "artifact",
    "static",
    "command",
    "test",
    "fixture",
    "no_touch",
    "source_revalidation",
    "manual",
}

WORD_CAPS = {
    "intent.md": 1200,
    "intent_redteam.md": 1500,
    "intent_synthesis.md": 800,
    "intent_lock_report.md": 600,
    "premortem.md": 900,
    "risk_register.md": 900,
    "verification_plan.md": 1000,
    "micro_sprints.md": 1200,
    "PACK_AUDIT_REPORT.md": 900,
    "PACK_MANIFEST.md": 600,
    "PACK_CHECKLIST.md": 800,
}

PLACEHOLDER_PATTERNS = (
    (re.compile(r"\bYYYY-MM-DD\b"), "YYYY-MM-DD"),
    (re.compile(r"\bHH:MM\b"), "HH:MM"),
    (re.compile(r"<RUN_ID>"), "<RUN_ID>"),
    (re.compile(r"<SPRINT_ID>"), "<SPRINT_ID>"),
    (re.compile(r"<X>"), "<X>"),
    (re.compile(r"\.\.\."), "..."),
)


def lint_pack(root: Path, run: str | None = None, pack_path: Path | None = None) -> dict[str, Any]:
    run_root, pack_dir = _resolve_paths(root=root, run=run, pack_path=pack_path)

    errors: list[str] = []
    warnings: list[str] = []
    checked_files: list[str] = []

    _check_required_files(run_root, RUN_ROOT_FILES, errors, checked_files)
    _check_required_files(pack_dir, PACK_FILES, errors, checked_files)
    _check_required_files(pack_dir / "HANDOFF", tuple(f"HANDOFF_STAGE_{stage}.md" for stage in STAGES), errors, checked_files)

    sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
    if sprint_id:
        envelope_files = (f"{sprint_id}_ENVELOPE.md", f"{sprint_id}_ENVELOPE_REDTEAM.md")
        _check_required_files(pack_dir, envelope_files, errors, checked_files)
    else:
        errors.append("SPRINT_ID.txt is empty or unreadable")

    fixtures_dir = pack_dir / "fixtures"
    if not fixtures_dir.is_dir():
        errors.append("pack/fixtures directory is missing")
    elif not any(path.is_dir() for path in fixtures_dir.rglob("*")):
        errors.append("pack/fixtures must contain at least one fixture directory")

    execution_mode = _read_text(run_root / "EXECUTION_MODE.txt").strip()
    if execution_mode not in {"PLANNING_ONLY", "EXECUTION_ENABLED"}:
        errors.append("EXECUTION_MODE.txt must contain exactly PLANNING_ONLY or EXECUTION_ENABLED")
    if execution_mode == "PLANNING_ONLY" and (run_root / "EXECUTION_PROMPT.md").exists():
        errors.append("EXECUTION_PROMPT.md exists even though EXECUTION_MODE.txt is PLANNING_ONLY")

    _check_text_contracts(run_root=run_root, pack_dir=pack_dir, sprint_id=sprint_id, execution_mode=execution_mode, errors=errors, warnings=warnings)
    _check_artifact_shapes(pack_dir=pack_dir, checked_files=checked_files, errors=errors, warnings=warnings)
    _check_verification_manifest(
        run_root=run_root,
        pack_dir=pack_dir,
        sprint_id=sprint_id,
        execution_mode=execution_mode,
        checked_files=checked_files,
        errors=errors,
        warnings=warnings,
    )

    unique_checked_files = sorted(set(checked_files))
    status = "PASS" if not errors else "FAIL"
    return {
        "status": status,
        "run_root": str(run_root),
        "pack_dir": str(pack_dir),
        "checked_file_count": len(unique_checked_files),
        "checked_files": unique_checked_files,
        "errors": errors,
        "warnings": warnings,
    }


def format_pack_lint(payload: dict[str, Any]) -> str:
    lines = [
        f"pack_lint: {payload['status']}",
        f"run_root={payload['run_root']}",
        f"pack_dir={payload['pack_dir']}",
        f"checked_files={payload['checked_file_count']} errors={len(payload['errors'])} warnings={len(payload['warnings'])}",
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


def _resolve_paths(root: Path, run: str | None, pack_path: Path | None) -> tuple[Path, Path]:
    if pack_path:
        resolved_pack = pack_path.expanduser().resolve()
        if not resolved_pack.exists():
            raise FactoryPackLintError(f"pack path does not exist: {resolved_pack}")
        if resolved_pack.name != "pack":
            raise FactoryPackLintError(f"pack path must point to a directory named 'pack': {resolved_pack}")
        return resolved_pack.parent, resolved_pack

    if not run:
        raise FactoryPackLintError("provide --run <RUN_ID|path> or --pack <path>")

    run_candidate = Path(run).expanduser()
    if not run_candidate.is_absolute():
        direct = (root / run_candidate).resolve()
        by_id = (root / "docs" / "Factory" / "runs" / run).resolve()
        run_candidate = direct if direct.exists() else by_id
    else:
        run_candidate = run_candidate.resolve()

    if not run_candidate.exists():
        raise FactoryPackLintError(f"run root does not exist: {run_candidate}")
    return run_candidate, run_candidate / "pack"


def _check_required_files(base: Path, names: tuple[str, ...], errors: list[str], checked_files: list[str]) -> None:
    for name in names:
        path = base / name
        checked_files.append(str(path))
        if not path.exists():
            errors.append(f"missing required file: {path}")
        elif not path.is_file():
            errors.append(f"required path is not a file: {path}")
        elif path.stat().st_size == 0:
            errors.append(f"required file is empty: {path}")


def _check_text_contracts(
    run_root: Path,
    pack_dir: Path,
    sprint_id: str,
    execution_mode: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    knowledge_lint = _read_text(run_root / "KNOWLEDGE_LINT.txt")
    if "knowledge_lint: PASS" not in knowledge_lint:
        errors.append("KNOWLEDGE_LINT.txt does not record knowledge_lint: PASS")

    context_report = _read_text(run_root / "CONTEXT_RECALL_REPORT.md")
    if "Coverage Verdict: WEAK" in context_report:
        errors.append("CONTEXT_RECALL_REPORT.md records Coverage Verdict: WEAK")

    checklist = _read_text(pack_dir / "PACK_CHECKLIST.md")
    for item_id in range(1, 10):
        answer = _extract_checklist_answer(checklist, f"C{item_id}")
        if answer is None:
            errors.append(f"PACK_CHECKLIST.md is missing answer for C{item_id}")
        elif answer != "YES":
            errors.append(f"PACK_CHECKLIST.md critical item C{item_id} answer must be YES, found {answer}")

    audit = _read_text(pack_dir / "PACK_AUDIT_REPORT.md")
    verdict = _extract_verdict(audit)
    if verdict is None:
        errors.append("PACK_AUDIT_REPORT.md is missing a concrete Verdict line")
    elif verdict == "FAIL":
        errors.append("PACK_AUDIT_REPORT.md verdict is FAIL")

    mode_mentions = re.findall(r"(?:Execution Mode|Mode):\s*`?(PLANNING_ONLY|EXECUTION_ENABLED)`?", audit)
    if execution_mode and mode_mentions and execution_mode not in mode_mentions:
        errors.append(
            "PACK_AUDIT_REPORT.md execution mode mention does not match EXECUTION_MODE.txt "
            f"({execution_mode})"
        )

    manifest = _read_text(pack_dir / "PACK_MANIFEST.md")
    if sprint_id and f"{sprint_id}_ENVELOPE.md" not in manifest:
        errors.append("PACK_MANIFEST.md does not reference the sprint envelope from SPRINT_ID.txt")
    if re.search(r"PACK_AUDIT_REPORT\.md.*pending", manifest, flags=re.IGNORECASE):
        errors.append("PACK_MANIFEST.md still marks PACK_AUDIT_REPORT.md as pending after I2")
    if re.search(r"\bYES/NO(?:/NA)?\b", manifest):
        errors.append("PACK_MANIFEST.md still contains unresolved YES/NO checklist values")

    if "PASS / CONDITIONAL PASS / FAIL" in checklist:
        errors.append("PACK_CHECKLIST.md still contains unresolved outcome options")
    if "PASS / CONDITIONAL PASS / FAIL" in audit:
        errors.append("PACK_AUDIT_REPORT.md still contains unresolved verdict options")

    if verdict == "CONDITIONAL PASS":
        for item_id in ("K1", "K2"):
            answer = _extract_checklist_answer(checklist, item_id)
            if answer is None:
                errors.append(f"PACK_CHECKLIST.md is missing answer for {item_id}")
            elif answer not in {"YES", "NA"}:
                errors.append(f"PACK_CHECKLIST.md conditional item {item_id} must be YES or NA, found {answer}")

    if execution_mode == "EXECUTION_ENABLED" and not (run_root / "EXECUTION_PROMPT.md").exists():
        warnings.append("EXECUTION_ENABLED run has no EXECUTION_PROMPT.md yet; this is expected before human Go")

    manifest_path = pack_dir / VERIFICATION_MANIFEST
    if execution_mode == "EXECUTION_ENABLED" and not manifest_path.exists():
        warnings.append(
            "EXECUTION_ENABLED run has no pack/verification_manifest.yaml; "
            "this is allowed for legacy packs but expected for new execution packs"
        )


def _check_artifact_shapes(
    pack_dir: Path,
    checked_files: list[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    paths = [
        path
        for path in pack_dir.rglob("*.md")
        if path.is_file() and not path.name.startswith(".")
    ]
    for path in paths:
        checked_files.append(str(path))
        text = _read_text(path)
        _check_placeholders(path, text, errors)
        if not _is_fixture_note(path, pack_dir):
            _check_required_headers(path, text, errors)
            _check_word_cap(path, text, errors)
        if path.parent.name == "HANDOFF" and path.name.startswith("HANDOFF_STAGE_"):
            _check_handoff(path, text, errors, warnings)


def _check_verification_manifest(
    run_root: Path,
    pack_dir: Path,
    sprint_id: str,
    execution_mode: str,
    checked_files: list[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    path = pack_dir / VERIFICATION_MANIFEST
    if not path.exists():
        return
    checked_files.append(str(path))
    if not path.is_file():
        errors.append(f"{path} is not a file")
        return
    if path.stat().st_size == 0:
        errors.append(f"{path} is empty")
        return

    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{path} is not valid YAML: {exc}")
        return

    if not isinstance(loaded, dict):
        errors.append(f"{path} must be a YAML mapping")
        return

    if loaded.get("schema_version") != 1:
        errors.append(f"{path} schema_version must be 1")

    manifest_run_id = loaded.get("run_id")
    if manifest_run_id and manifest_run_id != run_root.name:
        errors.append(f"{path} run_id does not match run root ({run_root.name})")
    elif not isinstance(manifest_run_id, str) or not manifest_run_id.strip():
        errors.append(f"{path} run_id must be a non-empty string")

    manifest_sprint_id = loaded.get("sprint_id")
    if sprint_id and manifest_sprint_id and manifest_sprint_id != sprint_id:
        errors.append(f"{path} sprint_id does not match SPRINT_ID.txt ({sprint_id})")
    elif not isinstance(manifest_sprint_id, str) or not manifest_sprint_id.strip():
        errors.append(f"{path} sprint_id must be a non-empty string")

    manifest_execution_mode = loaded.get("execution_mode")
    if manifest_execution_mode and manifest_execution_mode != execution_mode:
        errors.append(f"{path} execution_mode does not match EXECUTION_MODE.txt ({execution_mode})")
    elif manifest_execution_mode not in {"PLANNING_ONLY", "EXECUTION_ENABLED"}:
        errors.append(f"{path} execution_mode must be PLANNING_ONLY or EXECUTION_ENABLED")

    checks = loaded.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append(f"{path} checks must be a non-empty list")
        return

    seen_ids: set[str] = set()
    for index, check in enumerate(checks, start=1):
        label = f"{path} checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{label} must be a mapping")
            continue

        check_id = check.get("id")
        if not isinstance(check_id, str) or not check_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
        elif check_id in seen_ids:
            errors.append(f"{label}.id duplicates {check_id}")
        else:
            seen_ids.add(check_id)

        tier = check.get("tier")
        if tier not in VERIFICATION_TIERS:
            errors.append(f"{label}.tier must be one of {', '.join(sorted(VERIFICATION_TIERS))}")

        check_type = check.get("type")
        if check_type not in VERIFICATION_CHECK_TYPES:
            errors.append(f"{label}.type must be one of {', '.join(sorted(VERIFICATION_CHECK_TYPES))}")

        constraint_ids = check.get("constraint_ids")
        if not isinstance(constraint_ids, list) or not constraint_ids:
            errors.append(f"{label}.constraint_ids must be a non-empty list")
        elif not all(isinstance(item, str) and item.strip() for item in constraint_ids):
            errors.append(f"{label}.constraint_ids must contain only non-empty strings")

        description = check.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{label}.description must be a non-empty string")

        halt_on_failure = check.get("halt_on_failure")
        if not isinstance(halt_on_failure, bool):
            errors.append(f"{label}.halt_on_failure must be true or false")

        evidence_path = check.get("evidence_path")
        if not isinstance(evidence_path, str) or not evidence_path.strip():
            errors.append(f"{label}.evidence_path must be a non-empty string")

        command = check.get("command")
        if check_type in {"static", "command", "test", "no_touch"}:
            if not isinstance(command, str) or not command.strip():
                errors.append(f"{label}.command is required for type {check_type}")

        expected = check.get("expected")
        if not isinstance(expected, str) or not expected.strip():
            errors.append(f"{label}.expected must be a non-empty string")

        target = check.get("target")
        if check_type in {"artifact", "fixture", "source_revalidation"}:
            if not isinstance(target, str) or not target.strip():
                errors.append(f"{label}.target is required for type {check_type}")

        if tier == "V0" and check_type in {"command", "test"}:
            warnings.append(f"{label} uses tier V0 with executable type {check_type}; consider V1+")


def _check_placeholders(path: Path, text: str, errors: list[str]) -> None:
    for pattern, label in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path} contains unresolved placeholder {label}")


def _check_required_headers(path: Path, text: str, errors: list[str]) -> None:
    if "## Version" not in text:
        errors.append(f"{path} is missing ## Version")
    if "## Change Log" not in text:
        errors.append(f"{path} is missing ## Change Log")


def _check_word_cap(path: Path, text: str, errors: list[str]) -> None:
    cap = WORD_CAPS.get(path.name)
    if cap is None:
        if path.name.endswith("_ENVELOPE.md"):
            cap = 1800
        elif path.name.endswith("_ENVELOPE_REDTEAM.md"):
            cap = 1200
        elif path.name.startswith("HANDOFF_STAGE_"):
            cap = 500
    if cap is None:
        return
    word_count = _word_count_without_code_blocks(text)
    if word_count > cap:
        errors.append(f"{path} exceeds word cap: {word_count} words > {cap}")


def _check_handoff(path: Path, text: str, errors: list[str], warnings: list[str]) -> None:
    required_sections = (
        "## Stage",
        "## Inputs (LOAD)",
        "## Inputs (DISK)",
        "## Skill Routing Contract",
        "## Outputs Produced (paths)",
        "## Verification Steps Recommended",
        "## Exit Criteria Status",
    )
    for section in required_sections:
        if section not in text:
            errors.append(f"{path} is missing {section}")
    if not re.search(r"## Exit Criteria Status\s*\n-\s*(PASS|FAIL)\b", text):
        errors.append(f"{path} does not record concrete exit criteria PASS or FAIL")
    if path.name in {"HANDOFF_STAGE_B.md", "HANDOFF_STAGE_C.md", "HANDOFF_STAGE_I.md"} and "Iteration:" not in text:
        errors.append(f"{path} is missing required iteration metadata")
    if re.search(r"^-\s*Skill used \(or `NONE`\):\s*$", text, flags=re.MULTILINE):
        warnings.append(f"{path} may not have instantiated the Skill Routing Contract")


def _is_fixture_note(path: Path, pack_dir: Path) -> bool:
    try:
        relative = path.relative_to(pack_dir)
    except ValueError:
        return False
    return len(relative.parts) >= 2 and relative.parts[0] == "fixtures" and path.name == "notes.md"


def _extract_checklist_answer(text: str, item_id: str) -> str | None:
    match = re.search(rf"^{re.escape(item_id)}\.\s+.*?\|\s*Answer:\s*([^|]+)", text, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().upper()


def _extract_verdict(text: str) -> str | None:
    match = re.search(r"^\s*-\s*Verdict:\s*(PASS|CONDITIONAL PASS|FAIL)\s*$", text, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1)


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
