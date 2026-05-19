#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ADVISORY_PASS = "ADVISORY_PASS"
ADVISORY_WARN = "ADVISORY_WARN"
ADVISORY_FAIL_NON_BLOCKING = "ADVISORY_FAIL_NON_BLOCKING"

STAGE_ORDER = "A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2"

RUNTIME_CLAIM_PATTERNS = (
    re.compile(r"\bfactory\s+(?:v3\s+)?(?:owns|governs|enforces)\s+runtime\b", re.IGNORECASE),
    re.compile(r"\bfactory\s+(?:v3\s+)?(?:provides|produces)\s+runtime\s+proof\b", re.IGNORECASE),
    re.compile(r"\bfactory\s+(?:v3\s+)?(?:mediates|executes)\s+production\s+actions\b", re.IGNORECASE),
    re.compile(r"\bfactory\s+(?:v3\s+)?is\s+(?:the\s+)?runtime\s+authority\b", re.IGNORECASE),
)

REQUIRED_GATE_PATTERNS = (
    re.compile(r"\bknowledge_lint(?:\.sh)?\s+(?:requires|must\s+run|must\s+call)\s+.*v3", re.IGNORECASE),
    re.compile(r"\bstage-lint\s+(?:requires|must\s+run|must\s+call)\s+.*v3", re.IGNORECASE),
    re.compile(r"\bpack-lint\s+(?:requires|must\s+run|must\s+call)\s+.*v3", re.IGNORECASE),
    re.compile(r"\bv3\s+advisory\s+lint\s+is\s+required\s+by\s+(?:knowledge_lint|stage-lint|pack-lint)", re.IGNORECASE),
)

PROMOTION_CLAIM_PATTERNS = (
    re.compile(
        r"\bfactory\s+v3\s+release\s+(?:is\s+)?(?:ready|approved|released|promoted|active|available)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bfactory\s+v3\s+(?:is\s+)?promoted\s+now\b", re.IGNORECASE),
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run non-blocking Factory v3 advisory checks over research docs.",
    )
    parser.add_argument("--target", required=True, help="File or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--expect", help="Optional expected JSON file for deterministic fixture checks.")
    args = parser.parse_args()

    target = Path(args.target)
    report = lint_target(target)

    if args.expect:
        expected = _load_json(Path(args.expect))
        if report != expected:
            print(_format_fixture_diff(expected, report), file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


def lint_target(target: Path) -> dict[str, Any]:
    files = _markdown_files(target)
    findings: list[dict[str, str]] = []
    checked_artifacts = [str(path.as_posix()) for path in files]
    texts = {path: _read_text(path) for path in files}
    all_text = "\n".join(texts.values())

    _check_stage_order(all_text, findings)
    _check_research_posture(texts, findings)
    _check_shadow_schema_isolation(texts, findings)
    _check_aegis_optionality(all_text, findings)
    _check_runtime_boundary(texts, findings)
    _check_required_gate_wiring(texts, findings)
    _check_promotion_evidence(texts, findings)

    findings = sorted(findings, key=lambda item: (item["id"], item["path"], item["message"]))
    warnings = [item for item in findings if item["severity"] in {"advisory_high", "advisory_medium"}]
    status = _status(findings)

    return {
        "blocking_effect": "none",
        "checked_artifacts": checked_artifacts,
        "findings": findings,
        "generated_at": "not_recorded",
        "promotion_level": "research",
        "recommended_next_steps": _recommended_next_steps(findings),
        "report_id": "factory-v3-advisory-lint",
        "review_notes": "",
        "review_status": "needs_human_review" if findings else "not_required",
        "status": status,
        "target": str(target.as_posix()),
        "warnings": warnings,
    }


def format_text(report: dict[str, Any]) -> str:
    lines = [
        f"factory_v3_advisory_lint: {report['status']}",
        "blocking_effect=none",
        f"promotion_level={report['promotion_level']}",
        f"target={report['target']}",
        f"checked_files={len(report['checked_artifacts'])} findings={len(report['findings'])}",
    ]
    if report["findings"]:
        lines.append("")
        lines.append("Findings:")
        for finding in report["findings"]:
            lines.append(
                f"- {finding['id']} [{finding['severity']}] {finding['path']}: {finding['message']}"
            )
    lines.append("")
    lines.append("This report is advisory and non-blocking.")
    return "\n".join(lines)


def _check_stage_order(all_text: str, findings: list[dict[str, str]]) -> None:
    if STAGE_ORDER not in all_text:
        findings.append(
            _finding(
                "V3-A001",
                "advisory_critical",
                "<target>",
                f"v2 stage order phrase is missing: {STAGE_ORDER}",
            )
        )


def _check_research_posture(texts: dict[Path, str], findings: list[dict[str, str]]) -> None:
    posture_markers = (
        "does not",
        "not enforced",
        "non-enforcing",
        "not implement",
        "not promote",
        "not authorize",
        "non-blocking",
    )
    for path, text in texts.items():
        lowered = text.lower()
        if "research" not in lowered or not any(marker in lowered for marker in posture_markers):
            findings.append(
                _finding(
                    "V3-A002",
                    "advisory_high",
                    path.as_posix(),
                    "v3 document does not clearly state research-only or non-enforcing posture",
                )
            )


def _check_shadow_schema_isolation(texts: dict[Path, str], findings: list[dict[str, str]]) -> None:
    for path, text in texts.items():
        if "shadow_schema" not in path.name.lower():
            continue
        lowered = text.lower()
        has_validator_names = all(term in lowered for term in ("knowledge_lint", "stage-lint", "pack-lint"))
        has_isolation_language = "not required" in lowered or "no candidate" in lowered
        if not has_validator_names or not has_isolation_language:
            findings.append(
                _finding(
                    "V3-A003",
                    "advisory_critical",
                    path.as_posix(),
                    "shadow schema candidate lacks explicit required-validator isolation language",
                )
            )


def _check_aegis_optionality(all_text: str, findings: list[dict[str, str]]) -> None:
    lowered = all_text.lower()
    has_optional_language = (
        "aegis-compatible but not aegis-dependent" in lowered
        or "aegis is not required" in lowered
        or "aegis optional" in lowered
    )
    has_dependency_claim = (
        "aegis is required to use" in lowered
        or "factory v3 requires aegis" in lowered
        or "starter kit requires aegis" in lowered
    )
    if has_dependency_claim or not has_optional_language:
        findings.append(
            _finding(
                "V3-A004",
                "advisory_critical",
                "<target>",
                "AEGIS optionality is missing or contradicted",
            )
        )


def _check_runtime_boundary(texts: dict[Path, str], findings: list[dict[str, str]]) -> None:
    for path, text in texts.items():
        for pattern in RUNTIME_CLAIM_PATTERNS:
            if pattern.search(text):
                findings.append(
                    _finding(
                        "V3-A005",
                        "advisory_critical",
                        path.as_posix(),
                        "possible runtime-kernel authority claim found",
                    )
                )
                break


def _check_required_gate_wiring(texts: dict[Path, str], findings: list[dict[str, str]]) -> None:
    for path, text in texts.items():
        for pattern in REQUIRED_GATE_PATTERNS:
            if pattern.search(text):
                findings.append(
                    _finding(
                        "V3-A003",
                        "advisory_critical",
                        path.as_posix(),
                        "possible required v2 gate wiring language found",
                    )
                )
                break


def _check_promotion_evidence(texts: dict[Path, str], findings: list[dict[str, str]]) -> None:
    for path, text in texts.items():
        for paragraph in _paragraphs(text):
            if not any(pattern.search(paragraph) for pattern in PROMOTION_CLAIM_PATTERNS):
                continue
            lowered = paragraph.lower()
            has_evidence = "evidence" in lowered
            has_human_release = "human release approval" in lowered or "explicit human release" in lowered
            if not has_evidence or not has_human_release:
                findings.append(
                    _finding(
                        "V3-A006",
                        "advisory_high",
                        path.as_posix(),
                        "promotion or release language lacks evidence and explicit human release approval",
                    )
                )
                break


def _status(findings: list[dict[str, str]]) -> str:
    if not findings:
        return ADVISORY_PASS
    if any(finding["severity"] == "advisory_critical" for finding in findings):
        return ADVISORY_FAIL_NON_BLOCKING
    return ADVISORY_WARN


def _recommended_next_steps(findings: list[dict[str, str]]) -> list[str]:
    if not findings:
        return ["No advisory findings. Keep v3 artifacts research-only until promoted."]
    return [
        "Review findings manually; this report is non-blocking.",
        "Classify each finding as accepted, rejected_false_positive, needs_more_context, or deferred.",
        "Do not promote any v3 check without Factory v2 governance and explicit human release approval.",
    ]


def _markdown_files(target: Path) -> list[Path]:
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")
    if target.is_file():
        return [target] if target.suffix.lower() == ".md" else []
    return sorted(path for path in target.rglob("*.md") if path.is_file())


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _paragraphs(text: str) -> list[str]:
    return [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]


def _finding(check_id: str, severity: str, path: str, message: str) -> dict[str, str]:
    return {
        "id": check_id,
        "message": message,
        "path": path,
        "review_notes": "",
        "review_status": "needs_human_review",
        "severity": severity,
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"could not load expected JSON {path}: {exc}") from exc


def _format_fixture_diff(expected: dict[str, Any], actual: dict[str, Any]) -> str:
    return "\n".join(
        [
            "factory_v3_advisory_lint fixture mismatch",
            "Expected:",
            json.dumps(expected, indent=2, sort_keys=True),
            "Actual:",
            json.dumps(actual, indent=2, sort_keys=True),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
