#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ADVISORY_PASS = "ADVISORY_PASS"
ADVISORY_WARN = "ADVISORY_WARN"
ADVISORY_FAIL_NON_BLOCKING = "ADVISORY_FAIL_NON_BLOCKING"

DECISION_STATES = {"pre_envelope_fallback", "completed_with_v3", "halted", "blocked"}
ENVELOPE_MODES = {"not_created_pre_envelope_fallback", "thread_local", "file_artifact"}
VERIFICATION_RESULTS = {"pass", "fail", "not_run", "not_applicable"}
REVIEW_RESULTS = {"pass", "fail", "not_applicable"}
KERNEL_VALUES = {"yes", "no", "unknown"}

UNSAFE_APPROVAL_FLAGS = {
    "factory_v3_default_approved",
    "new_v3_profile_approved",
    "required_gate_integration_approved",
    "runtime_authority_approved",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run standalone advisory Factory v3 mission-record checks.",
    )
    parser.add_argument("--target", required=True, help="Mission-record JSON file or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--expect", help="Optional expected JSON file for fixture checks.")
    args = parser.parse_args()

    report = lint_target(Path(args.target))

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


def lint_target(target: Path) -> dict[str, Any]:
    files = _json_files(target)
    findings: list[dict[str, str]] = []

    for path in files:
        record = _load_record(path, findings)
        if record is None:
            continue
        findings.extend(_lint_record(path, record))

    findings.sort(key=lambda item: (item["id"], item["path"], item["message"]))
    warnings = [item for item in findings if item["severity"] == "advisory_high"]

    return {
        "blocking_effect": "none",
        "checked_records": [path.as_posix() for path in files],
        "findings": findings,
        "generated_at": "not_recorded",
        "recommended_next_steps": _recommended_next_steps(findings),
        "record_scope": "shadow_advisory",
        "report_id": "factory-v3-mission-record-lint",
        "status": _status(findings),
        "target": target.as_posix(),
        "warnings": warnings,
    }


def format_text(report: dict[str, Any]) -> str:
    lines = [
        f"factory_v3_mission_record_lint: {report['status']}",
        "blocking_effect=none",
        f"record_scope={report['record_scope']}",
        f"target={report['target']}",
        f"checked_records={len(report['checked_records'])} findings={len(report['findings'])}",
    ]
    if report["findings"]:
        lines.append("")
        lines.append("Findings:")
        for finding in report["findings"]:
            lines.append(f"- {finding['id']} [{finding['severity']}] {finding['path']}: {finding['message']}")
    lines.append("")
    lines.append("This report is advisory and non-blocking.")
    return "\n".join(lines)


def _lint_record(path: Path, data: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    path_text = path.as_posix()

    if not isinstance(data, dict):
        return [_finding("V3-MR000", "advisory_critical", path_text, "mission record root must be an object")]

    record = data.get("record")
    mission = data.get("mission")
    authority = data.get("authority")
    execution = data.get("execution")
    reviews = data.get("reviews")

    for name, value in (
        ("record", record),
        ("mission", mission),
        ("authority", authority),
        ("execution", execution),
        ("reviews", reviews),
    ):
        if not isinstance(value, dict):
            findings.append(_finding("V3-MR001", "advisory_critical", path_text, f"missing object: {name}"))

    if not all(isinstance(value, dict) for value in (record, mission, authority, execution, reviews)):
        return findings

    decision_state = record.get("decision_state")
    if decision_state not in DECISION_STATES:
        findings.append(_finding("V3-MR002", "advisory_critical", path_text, "record.decision_state is invalid or missing"))
    if record.get("record_type") != "factory_v3_mission_record":
        findings.append(_finding("V3-MR003", "advisory_critical", path_text, "record.record_type must be factory_v3_mission_record"))
    if record.get("profile_id") != "V3-OP-001":
        findings.append(_finding("V3-MR004", "advisory_critical", path_text, "record.profile_id must stay within V3-OP-001"))
    if record.get("status") != "research_only_non_enforcing":
        findings.append(_finding("V3-MR005", "advisory_critical", path_text, "record.status must be research_only_non_enforcing"))

    findings.extend(_check_approval_scope(path_text, record.get("approval_scope")))
    findings.extend(_check_mission(path_text, mission))
    findings.extend(_check_authority(path_text, authority, decision_state))
    findings.extend(_check_execution(path_text, authority, execution, decision_state))
    findings.extend(_check_reviews(path_text, reviews))
    findings.extend(_check_state_consistency(path_text, mission, authority, execution, decision_state))
    return findings


def _check_approval_scope(path: str, approval_scope: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(approval_scope, dict):
        return [_finding("V3-MR020", "advisory_critical", path, "record.approval_scope must be an object")]

    for flag in sorted(UNSAFE_APPROVAL_FLAGS):
        if approval_scope.get(flag) is not False:
            findings.append(_finding("V3-MR021", "advisory_critical", path, f"unsafe approval flag must be false: {flag}"))
    if approval_scope.get("factory_v2_fallback_retained") is not True:
        findings.append(_finding("V3-MR022", "advisory_critical", path, "factory_v2_fallback_retained must be true"))
    return findings


def _check_mission(path: str, mission: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not _nonempty_string(mission.get("repository")):
        findings.append(_finding("V3-MR030", "advisory_high", path, "mission.repository is missing"))
    if not _nonempty_string(mission.get("objective")):
        findings.append(_finding("V3-MR031", "advisory_critical", path, "mission.objective is missing"))
    if mission.get("separate_governance_kernel_present") not in KERNEL_VALUES:
        findings.append(_finding("V3-MR032", "advisory_critical", path, "separate_governance_kernel_present is invalid"))

    envelope = mission.get("envelope")
    if not isinstance(envelope, dict):
        return findings + [_finding("V3-MR033", "advisory_critical", path, "mission.envelope must be an object")]

    mode = envelope.get("mode")
    reference = envelope.get("reference")
    if mode not in ENVELOPE_MODES:
        findings.append(_finding("V3-MR034", "advisory_critical", path, "mission.envelope.mode is invalid"))
    if mode in {"thread_local", "file_artifact"} and not _meaningful_reference(reference):
        findings.append(_finding("V3-MR035", "advisory_critical", path, "thread-local or file envelope must include a reference"))
    if mode == "not_created_pre_envelope_fallback" and not _nonempty_string(envelope.get("not_created_reason")):
        findings.append(_finding("V3-MR036", "advisory_critical", path, "pre-envelope fallback must include not_created_reason"))
    return findings


def _check_authority(path: str, authority: dict[str, Any], decision_state: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    authorized_files = authority.get("authorized_files")
    allowed_commands = authority.get("allowed_commands")
    fallback_triggers = authority.get("fallback_triggers")

    if not isinstance(authorized_files, list):
        findings.append(_finding("V3-MR040", "advisory_critical", path, "authority.authorized_files must be a list"))
    elif decision_state in {"completed_with_v3", "halted"} and not authorized_files:
        findings.append(_finding("V3-MR041", "advisory_critical", path, "executed V3 records must include authorized files"))

    if not isinstance(allowed_commands, list):
        findings.append(_finding("V3-MR042", "advisory_critical", path, "authority.allowed_commands must be a list"))
    elif decision_state in {"completed_with_v3", "halted"} and not allowed_commands:
        findings.append(_finding("V3-MR043", "advisory_critical", path, "executed V3 records must include allowed commands"))

    if authority.get("v2_fallback_required") is not True:
        findings.append(_finding("V3-MR044", "advisory_critical", path, "authority.v2_fallback_required must be true"))
    if not isinstance(fallback_triggers, list):
        findings.append(_finding("V3-MR045", "advisory_critical", path, "authority.fallback_triggers must be a list"))
    return findings


def _check_execution(
    path: str,
    authority: dict[str, Any],
    execution: dict[str, Any],
    decision_state: Any,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    files_changed = execution.get("files_changed")
    if not isinstance(files_changed, list):
        findings.append(_finding("V3-MR050", "advisory_critical", path, "execution.files_changed must be a list"))

    verification = execution.get("verification")
    if not isinstance(verification, dict):
        findings.append(_finding("V3-MR051", "advisory_critical", path, "execution.verification must be an object"))
    else:
        commands = verification.get("commands")
        result = verification.get("result")
        if not isinstance(commands, list):
            findings.append(_finding("V3-MR052", "advisory_critical", path, "execution.verification.commands must be a list"))
        if result not in VERIFICATION_RESULTS:
            findings.append(_finding("V3-MR053", "advisory_critical", path, "execution.verification.result is invalid or missing"))
        if decision_state == "completed_with_v3" and result != "pass":
            findings.append(_finding("V3-MR054", "advisory_critical", path, "completed V3 records must have passing verification"))
        if decision_state == "pre_envelope_fallback" and result == "pass" and files_changed:
            findings.append(_finding("V3-MR055", "advisory_critical", path, "pre-envelope fallback cannot report changed files with passing verification"))

    halt = execution.get("halt")
    fallback = execution.get("fallback")
    findings.extend(_check_reasoned_boolean(path, halt, "halt", "V3-MR056"))
    findings.extend(_check_reasoned_boolean(path, fallback, "fallback", "V3-MR057"))

    if isinstance(files_changed, list):
        authorized_files = authority.get("authorized_files")
        if isinstance(authorized_files, list) and authorized_files:
            unauthorized = sorted(str(item) for item in files_changed if item not in authorized_files)
            for file_path in unauthorized:
                findings.append(_finding("V3-MR058", "advisory_critical", path, f"changed file is outside authorized_files: {file_path}"))
    return findings


def _check_reviews(path: str, reviews: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for key in ("simple_code_gate", "fallback_halt_review"):
        review = reviews.get(key)
        if not isinstance(review, dict):
            findings.append(_finding("V3-MR060", "advisory_critical", path, f"reviews.{key} must be an object"))
            continue
        if review.get("result") not in REVIEW_RESULTS:
            findings.append(_finding("V3-MR061", "advisory_critical", path, f"reviews.{key}.result is invalid or missing"))
    return findings


def _check_state_consistency(
    path: str,
    mission: dict[str, Any],
    authority: dict[str, Any],
    execution: dict[str, Any],
    decision_state: Any,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    envelope = mission.get("envelope") if isinstance(mission.get("envelope"), dict) else {}
    verification = execution.get("verification") if isinstance(execution.get("verification"), dict) else {}
    halt = execution.get("halt") if isinstance(execution.get("halt"), dict) else {}
    fallback = execution.get("fallback") if isinstance(execution.get("fallback"), dict) else {}

    if decision_state == "pre_envelope_fallback":
        if envelope.get("mode") != "not_created_pre_envelope_fallback":
            findings.append(_finding("V3-MR070", "advisory_critical", path, "pre-envelope fallback must use not_created_pre_envelope_fallback envelope mode"))
        if fallback.get("used") is not True:
            findings.append(_finding("V3-MR071", "advisory_critical", path, "pre-envelope fallback records must mark fallback.used true"))

    if decision_state == "completed_with_v3":
        if fallback.get("used") is True:
            findings.append(_finding("V3-MR072", "advisory_critical", path, "completed V3 records must not mark fallback.used true"))
        if halt.get("halted") is True:
            findings.append(_finding("V3-MR073", "advisory_critical", path, "completed V3 records must not mark halt.halted true"))
        if not verification.get("commands") and not authority.get("allowed_commands"):
            findings.append(_finding("V3-MR074", "advisory_critical", path, "completed V3 records must record verification command evidence"))
    return findings


def _check_reasoned_boolean(path: str, value: Any, name: str, check_id: str) -> list[dict[str, str]]:
    if not isinstance(value, dict):
        return [_finding(check_id, "advisory_critical", path, f"execution.{name} must be an object")]
    key = "halted" if name == "halt" else "used"
    if not isinstance(value.get(key), bool):
        return [_finding(check_id, "advisory_critical", path, f"execution.{name}.{key} must be boolean")]
    reason_codes = value.get("reason_codes")
    if not isinstance(reason_codes, list):
        return [_finding(check_id, "advisory_critical", path, f"execution.{name}.reason_codes must be a list")]
    if value.get(key) and not reason_codes:
        return [_finding(check_id, "advisory_critical", path, f"execution.{name} is true but reason_codes is empty")]
    return []


def _status(findings: list[dict[str, str]]) -> str:
    if not findings:
        return ADVISORY_PASS
    if any(finding["severity"] == "advisory_critical" for finding in findings):
        return ADVISORY_FAIL_NON_BLOCKING
    return ADVISORY_WARN


def _recommended_next_steps(findings: list[dict[str, str]]) -> list[str]:
    if not findings:
        return ["No mission-record findings. Keep records shadow-only until a promotion pack approves otherwise."]
    return [
        "Review findings manually; this report is advisory and non-blocking.",
        "Classify findings as accepted, false_positive, needs_more_context, or deferred.",
        "Do not wire mission-record checks into required gates without explicit Factory governance approval.",
    ]


def _json_files(target: Path) -> list[Path]:
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")
    if target.is_file():
        return [target]
    return sorted(
        path
        for path in target.rglob("*.json")
        if path.is_file() and "expected" not in path.parts
    )


def _load_record(path: Path, findings: list[dict[str, str]]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(_finding("V3-MR000", "advisory_critical", path.as_posix(), f"could not load JSON: {exc}"))
        return None


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"failed to load expected JSON {path}: {exc}") from exc


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _meaningful_reference(value: Any) -> bool:
    return _nonempty_string(value) and value.strip().lower() not in {"none", "not_recorded"}


def _finding(check_id: str, severity: str, path: str, message: str) -> dict[str, str]:
    return {
        "id": check_id,
        "message": message,
        "path": path,
        "severity": severity,
    }


def _format_diff(expected: Any, actual: Any) -> str:
    return "\n".join(
        [
            "factory_v3_mission_record_lint fixture mismatch",
            "Expected:",
            json.dumps(expected, indent=2, sort_keys=True),
            "Actual:",
            json.dumps(actual, indent=2, sort_keys=True),
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
