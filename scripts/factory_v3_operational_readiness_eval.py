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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run standalone advisory Factory v3 operational-readiness evals.",
    )
    parser.add_argument("--target", required=True, help="File or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--expect", help="Optional expected JSON file for fixture checks.")
    args = parser.parse_args()

    report = evaluate_target(Path(args.target))

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


def evaluate_target(target: Path) -> dict[str, Any]:
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

    findings.sort(key=lambda item: (item["id"], item["path"], item["message"]))
    warnings = [item for item in findings if item["severity"] == "advisory_high"]

    return {
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
