#!/usr/bin/env python3
"""Local validator for generic Agent Loop Bridge event fixtures.

This validator checks structured JSON and permission rules only. It does not
call Slack, GitHub, CI, or Factory tools.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path
from typing import Any


HANDOFF_EVENT_TYPE = "factory.handoff.v1"
REVIEW_RESULT_EVENT_TYPE = "factory.review_result.v1"

ALLOWED_ACTIONS = {
    "read_handoff",
    "inspect_pr",
    "inspect_ci_status",
    "inspect_factory_pack",
    "post_review_result",
    "post_pr_comment",
}

FORBIDDEN_ACTIONS = {
    "merge",
    "push_commits",
    "patch_code",
    "open_downstream_run",
    "generate_execution_prompt",
    "change_policy_runtime_schema_evidence",
    "react_to_casual_chat_text",
}

REQUIRED_CHECKS = {
    "pr_diff",
    "ci_status",
    "factory_pack_lint_evidence",
    "stage_i2_verdict",
    "execution_mode_and_human_go",
    "no_touch_boundary",
    "test_evidence",
    "docs_sync",
}

VERDICTS = {"PASS", "PASS_WITH_NOTES", "BLOCKING", "NEEDS_HUMAN"}
CHECK_STATUSES = {"PASS", "FAIL", "NOTE", "NOT_APPLICABLE", "NEEDS_HUMAN"}
EXECUTION_MODES = {"PLANNING_ONLY", "EXECUTION_ENABLED"}


def _get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _as_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def _posting_permissions(allowed: set[str], forbidden: set[str]) -> dict[str, bool]:
    return {
        "review_result": "post_review_result" in allowed and "post_review_result" not in forbidden,
        "pr_comment": "post_pr_comment" in allowed and "post_pr_comment" not in forbidden,
    }


def validate_handoff(
    event: dict[str, Any],
    *,
    live_pr_head_sha: str | None = None,
) -> dict[str, Any]:
    errors: list[str] = []

    required_paths = {
        "event_type": "missing_event_type",
        "event_id": "missing_event_id",
        "repo.full_name": "missing_repo",
        "pull_request.number": "missing_pr_number",
        "pull_request.head_sha": "missing_head_sha",
        "factory.run_id": "missing_run_id",
        "factory.sprint_id": "missing_sprint_id",
        "factory.execution_mode": "missing_execution_mode",
    }
    for dotted, code in required_paths.items():
        if _get_path(event, dotted) in (None, ""):
            errors.append(code)

    if event.get("event_type") not in (None, HANDOFF_EVENT_TYPE):
        errors.append("unknown_event_type")

    allowed_raw = event.get("allowed_actions")
    forbidden_raw = event.get("forbidden_actions")
    required_checks_raw = event.get("required_checks")

    if not isinstance(allowed_raw, list):
        errors.append("missing_actions")
    if not isinstance(forbidden_raw, list):
        errors.append("missing_actions")
    if not isinstance(required_checks_raw, list):
        errors.append("missing_required_checks")

    allowed = _as_set(allowed_raw)
    forbidden = _as_set(forbidden_raw)
    required_checks = _as_set(required_checks_raw)

    unknown_allowed = sorted(allowed - ALLOWED_ACTIONS)
    unknown_forbidden = sorted(forbidden - FORBIDDEN_ACTIONS - ALLOWED_ACTIONS)
    unknown_checks = sorted(required_checks - REQUIRED_CHECKS)
    conflicts = sorted(allowed & forbidden)

    if unknown_allowed:
        errors.append("unknown_allowed_actions")
    if unknown_forbidden:
        errors.append("unknown_forbidden_actions")
    if unknown_checks:
        errors.append("unknown_required_checks")
    if conflicts:
        errors.append("allowed_forbidden_conflict")

    mode = _get_path(event, "factory.execution_mode")
    if mode is not None and mode not in EXECUTION_MODES:
        errors.append("unknown_execution_mode")

    event_sha = _get_path(event, "pull_request.head_sha")
    if live_pr_head_sha and event_sha and live_pr_head_sha != event_sha:
        errors.append("stale_pr_head_sha")

    inspect_allowed = not any(
        code in errors
        for code in (
            "missing_event_type",
            "missing_event_id",
            "missing_repo",
            "missing_pr_number",
            "missing_head_sha",
            "missing_run_id",
            "missing_sprint_id",
            "missing_execution_mode",
            "missing_actions",
            "missing_required_checks",
            "unknown_event_type",
            "unknown_required_checks",
            "allowed_forbidden_conflict",
        )
    )

    if "stale_pr_head_sha" in errors:
        verdict_floor = "BLOCKING"
    elif errors:
        verdict_floor = "NEEDS_HUMAN"
    else:
        verdict_floor = "review_may_continue"

    return {
        "valid": not errors,
        "verdict_floor": verdict_floor,
        "error_codes": errors,
        "permissions": _posting_permissions(allowed, forbidden),
        "unknown_allowed_actions": unknown_allowed,
        "unknown_forbidden_actions": unknown_forbidden,
        "unknown_required_checks": unknown_checks,
        "conflicting_actions": conflicts,
        "may_inspect_remote": inspect_allowed,
        "may_inspect_filesystem": inspect_allowed,
    }


def validate_review_result(result: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if result.get("event_type") != REVIEW_RESULT_EVENT_TYPE:
        errors.append("unknown_event_type")
    if not result.get("handoff_event_id"):
        errors.append("missing_handoff_event_id")
    if result.get("verdict") not in VERDICTS:
        errors.append("unknown_verdict")

    checks = result.get("checks")
    if not isinstance(checks, list):
        errors.append("missing_checks")
    else:
        for check in checks:
            if not isinstance(check, dict):
                errors.append("invalid_check")
                continue
            if check.get("status") not in CHECK_STATUSES:
                errors.append("unknown_check_status")
            if check.get("id") not in REQUIRED_CHECKS:
                errors.append("unknown_check_id")

    return {
        "valid": not errors,
        "error_codes": sorted(set(errors), key=errors.index),
        "must_not_post": bool(errors),
    }


def validate_posting_permissions(
    allowed_actions: list[str],
    requested_post_targets: list[str],
) -> dict[str, Any]:
    allowed = _as_set(allowed_actions)
    post_result = "review_result" in requested_post_targets and "post_review_result" in allowed
    post_pr = "pr_comment" in requested_post_targets and "post_pr_comment" in allowed
    errors: list[str] = []
    if "review_result" in requested_post_targets and not post_result:
        errors.append("missing_post_review_result")
    if "pr_comment" in requested_post_targets and not post_pr:
        errors.append("missing_post_pr_comment")
    return {
        "post_review_result": post_result,
        "post_pr_comment": post_pr,
        "local_result_only": bool(errors),
        "error_codes": errors,
    }


def validate_docs_sync_branches(data: dict[str, Any]) -> dict[str, Any]:
    planning = data["planning_only_event"]
    closed = data["closed_go_event"]
    return {
        "planning_only_requires_docs_sync": bool(planning.get("sprint_go_claimed")),
        "closed_go_requires_docs_sync": bool(closed.get("sprint_go_claimed")),
        "docs": ["docs/PROJECT_STATE.md", "docs/ROADMAP.md", "docs/CHANGELOG.md"],
    }


def validate_no_touch_diff(data: dict[str, Any]) -> dict[str, Any]:
    changed = data.get("changed_paths", [])
    patterns = data.get("no_touch_paths", [])
    violations = [
        path
        for path in changed
        if any(fnmatch.fnmatch(path, pattern) for pattern in patterns)
    ]
    return {
        "valid": not violations,
        "verdict_floor": "BLOCKING" if violations else "review_may_continue",
        "violations": violations,
    }


def validate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    kind = fixture["kind"]
    payload = fixture["input"]
    if kind == "handoff":
        return validate_handoff(payload, live_pr_head_sha=fixture.get("live_pr_head_sha"))
    if kind == "review_result":
        return validate_review_result(payload)
    if kind == "posting_permissions":
        return validate_posting_permissions(
            payload.get("allowed_actions", []),
            payload.get("requested_post_targets", []),
        )
    if kind == "docs_sync_branches":
        return validate_docs_sync_branches(payload)
    if kind == "no_touch_diff":
        return validate_no_touch_diff(payload)
    raise ValueError(f"unknown fixture kind: {kind}")


def _matches_expected(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    for key, expected_value in expected.items():
        actual_value = actual.get(key)
        if key == "error_codes":
            if set(actual_value or []) != set(expected_value):
                return False
        elif actual_value != expected_value:
            return False
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    actual = validate_fixture(fixture)
    ok = _matches_expected(actual, fixture["expected"])
    output = {"ok": ok, "actual": actual, "expected": fixture["expected"]}
    if args.as_json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(f"{args.fixture}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
