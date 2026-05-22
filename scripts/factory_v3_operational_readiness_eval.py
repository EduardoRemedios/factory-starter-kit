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

PROMOTION_DECISION = "not_authorized"

CHECKS: tuple[tuple[str, str, str, re.Pattern[str]], ...] = (
    (
        "V3-G002",
        "advisory_critical",
        "mission intent is ambiguous",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G002\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G003",
        "advisory_critical",
        "unapproved scope expansion found",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G003\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G004",
        "advisory_critical",
        "authority lease is incomplete",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G004\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G005",
        "advisory_critical",
        "verification failure does not halt",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G005\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G006",
        "advisory_high",
        "evidence bundle is incomplete",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G006\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G007",
        "advisory_critical",
        "V2 deprecation language found",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G007\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G009",
        "advisory_critical",
        "runtime-kernel authority claim found",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G009\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G010",
        "advisory_critical",
        "derived continuity overrides source artifacts",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G010\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G011",
        "advisory_high",
        "SIMPLE-CODE-GATE violation found",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G011\s*$", re.IGNORECASE | re.MULTILINE),
    ),
    (
        "V3-G014",
        "advisory_critical",
        "promotion approval lacks evidence",
        re.compile(r"^\s*EVAL_TRIGGER:\s*V3-G014\s*$", re.IGNORECASE | re.MULTILINE),
    ),
)

NL_CHECKS: tuple[tuple[str, str, str, tuple[re.Pattern[str], ...]], ...] = (
    (
        "V3-G003",
        "advisory_critical",
        "natural-language scope expansion risk found",
        (
            re.compile(r"\b(?:scope expansion|new requirement|expanded scope)\b", re.IGNORECASE),
            re.compile(r"\b(?:unapproved|without approval|not approved)\b", re.IGNORECASE),
        ),
    ),
    (
        "V3-G005",
        "advisory_critical",
        "natural-language verification halt risk found",
        (
            re.compile(r"\b(?:verification|check|command)\s+fail(?:ed|ure)?\b", re.IGNORECASE),
            re.compile(r"\b(?:continue|continued|keep going|proceed)\b", re.IGNORECASE),
        ),
    ),
    (
        "V3-G007",
        "advisory_critical",
        "natural-language V2 deprecation risk found",
        (
            re.compile(r"\bfactory\s+v2\b", re.IGNORECASE),
            re.compile(r"\b(?:deprecated|retired|replaced|legacy|no longer supported)\b", re.IGNORECASE),
        ),
    ),
    (
        "V3-G009",
        "advisory_critical",
        "natural-language runtime-kernel authority risk found",
        (
            re.compile(r"\bfactory\s+v3\b", re.IGNORECASE),
            re.compile(
                r"\b(?:runtime authority|runtime proof|production mediation|mediates production actions|governs runtime)\b",
                re.IGNORECASE,
            ),
        ),
    ),
    (
        "V3-G010",
        "advisory_critical",
        "natural-language stale continuity risk found",
        (
            re.compile(r"\b(?:derived cursor|resume cursor)\b", re.IGNORECASE),
            re.compile(r"\b(?:authored artifact|source artifact|source artifacts)\b", re.IGNORECASE),
            re.compile(r"\b(?:override|overrides|authoritative|mission truth)\b", re.IGNORECASE),
        ),
    ),
    (
        "V3-G011",
        "advisory_high",
        "natural-language SIMPLE-CODE-GATE risk found",
        (
            re.compile(r"\b(?:generic framework|registry|strategy layer|plugin seam|new dependency)\b", re.IGNORECASE),
            re.compile(r"\b(?:future variation|one local variation|simple-code-gate)\b", re.IGNORECASE),
        ),
    ),
)

PROMOTION_CLAIM_NL_PATTERN = re.compile(
    r"\bfactory\s+v3\b.{0,80}\b(?:is|now|already|has been|can now be|may now be)\b"
    r".{0,120}\b(?:operational|promoted|released|ready|approved|approved for release)\b",
    re.IGNORECASE,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run standalone advisory Factory v3 operational-readiness evals.",
    )
    parser.add_argument("--target", required=True, help="File or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--expect", help="Optional expected JSON file for fixture checks.")
    parser.add_argument("--nl-pilot", action="store_true", help="Enable opt-in natural-language pilot checks.")
    args = parser.parse_args()

    report = evaluate_target(Path(args.target), natural_language=args.nl_pilot)

    if args.expect:
        expected = _load_json(Path(args.expect))
        if report != expected:
            print(_format_diff(expected, report), file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


def evaluate_target(target: Path, *, natural_language: bool = False) -> dict[str, Any]:
    files = _markdown_files(target)
    findings: list[dict[str, str]] = []

    for path in files:
        text = _read_text(path)
        for check_id, severity, message, pattern in CHECKS:
            if pattern.search(text):
                findings.append(
                    {
                        "id": check_id,
                        "message": message,
                        "path": path.as_posix(),
                        "severity": severity,
                    }
                )
        if natural_language:
            findings.extend(_natural_language_findings(path, text))

    findings.sort(key=lambda item: (item["id"], item["path"], item["message"]))
    warnings = [item for item in findings if item["severity"] == "advisory_high"]

    report = {
        "blocking_effect": "none",
        "checked_files": [path.as_posix() for path in files],
        "false_negative_review": {"items": [], "status": "not_reviewed"},
        "false_positive_review": {"items": [], "status": "not_reviewed"},
        "findings": findings,
        "generated_at": "not_recorded",
        "promotion_decision": PROMOTION_DECISION,
        "recommended_next_steps": _recommended_next_steps(findings),
        "report_id": "factory-v3-operational-readiness-eval",
        "status": _status(findings),
        "target": target.as_posix(),
        "warnings": warnings,
    }
    if natural_language:
        report["natural_language_pilot"] = {
            "enabled": True,
            "false_positive_budget": 1,
            "gate_effect": "none",
        }
    return report


def format_text(report: dict[str, Any]) -> str:
    lines = [
        f"factory_v3_operational_readiness_eval: {report['status']}",
        "blocking_effect=none",
        f"promotion_decision={report['promotion_decision']}",
        f"target={report['target']}",
        f"checked_files={len(report['checked_files'])} findings={len(report['findings'])}",
    ]
    if report["findings"]:
        lines.append("")
        lines.append("Findings:")
        for finding in report["findings"]:
            lines.append(f"- {finding['id']} [{finding['severity']}] {finding['path']}: {finding['message']}")
    lines.append("")
    lines.append("This report is advisory and does not authorize Factory v3 promotion.")
    return "\n".join(lines)


def _status(findings: list[dict[str, str]]) -> str:
    if not findings:
        return ADVISORY_PASS
    if any(finding["severity"] == "advisory_critical" for finding in findings):
        return ADVISORY_FAIL_NON_BLOCKING
    return ADVISORY_WARN


def _recommended_next_steps(findings: list[dict[str, str]]) -> list[str]:
    if not findings:
        return ["No operational-readiness findings. Keep V3 research-only until a promotion pack approves otherwise."]
    return [
        "Review findings manually; this report is advisory and non-blocking.",
        "Classify findings as accepted, false_positive, needs_more_context, or deferred.",
        "Do not treat this eval output as Factory v3 promotion approval.",
    ]


def _natural_language_findings(path: Path, text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for paragraph in _paragraphs(text):
        if _is_nl_context_only(paragraph):
            continue
        for check_id, severity, message, patterns in NL_CHECKS:
            if all(pattern.search(paragraph) for pattern in patterns):
                if check_id == "V3-G009" and _is_runtime_boundary_negated(paragraph):
                    continue
                findings.append(
                    {
                        "id": check_id,
                        "message": message,
                        "path": path.as_posix(),
                        "severity": severity,
                        "source": "natural_language_pilot",
                    }
                )
        if PROMOTION_CLAIM_NL_PATTERN.search(paragraph):
            lowered = paragraph.lower()
            if (
                not _is_promotion_claim_negated(paragraph)
                and ("evidence" not in lowered or "human release approval" not in lowered)
            ):
                findings.append(
                    {
                        "id": "V3-G014",
                        "message": "natural-language promotion evidence risk found",
                        "path": path.as_posix(),
                        "severity": "advisory_critical",
                        "source": "natural_language_pilot",
                    }
                )
    return findings


def _paragraphs(text: str) -> list[str]:
    return [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]


def _is_runtime_boundary_negated(paragraph: str) -> bool:
    return re.search(
        r"\b(?:remain(?:s)? outside|external|does not claim|must not claim|not runtime authority|does not support)\b",
        paragraph,
        re.IGNORECASE,
    ) is not None


def _is_nl_context_only(paragraph: str) -> bool:
    if paragraph.lstrip().startswith("#"):
        return True
    return re.search(
        r"\b(?:fixture id|expected result|evidence does not support|research evidence only|"
        r"research template only|decision-prep checklist only|this plan does not authorize|"
        r"this artifact does not promote|this document does not promote|no-go for factory v3)\b",
        paragraph,
        re.IGNORECASE,
    ) is not None


def _is_promotion_claim_negated(paragraph: str) -> bool:
    return re.search(
        r"\b(?:does not promote|does not authorize|not promote|not promoted|no-go|only if|"
        r"before|future|may only be promoted|research only)\b",
        paragraph,
        re.IGNORECASE,
    ) is not None


def _markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")
    return sorted(path for path in target.rglob("*.md") if path.is_file())


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"failed to read {path}: {exc}") from exc


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"failed to load expected JSON {path}: {exc}") from exc


def _format_diff(expected: Any, actual: Any) -> str:
    return "\n".join(
        [
            "factory_v3_operational_readiness_eval fixture mismatch",
            "Expected:",
            json.dumps(expected, indent=2, sort_keys=True),
            "Actual:",
            json.dumps(actual, indent=2, sort_keys=True),
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
