#!/usr/bin/env python3
"""Read-only Factory plugin diagnosis and progress reporting."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PLUGIN_VERSION = "0.2.3"
STAGE_ORDER = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "I2")
SUPPORTED_HARNESSES = {"claude", "codex"}
SUPPORTED_PLATFORM = "darwin"
CLAUDE_BRIDGE = b"@AGENTS.md\n"
CODEX_PLUGIN_SKILLS = {
    "factory-brownfield",
    "factory-doctor",
    "factory-greenfield",
    "factory-progress",
    "factory-run",
    "factory-update",
    "factory-validate",
}
INSTALLATION_STATE_PATH = "docs/Factory/installation/INSTALLATION_STATE.json"
TRANSACTION_RECEIPTS_DIR = "docs/Factory/installation/receipts"
EXECUTION_CLOSEOUT_NAME = "EXECUTION_CLOSEOUT.json"


def result(
    *,
    state: str,
    reason_code: str,
    next_legal_action: str,
    **details: Any,
) -> dict[str, Any]:
    return {
        "state": state,
        "reason_code": reason_code,
        "next_legal_action": next_legal_action,
        **details,
    }


def resolve_git_root(start: Path) -> Path:
    completed = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise ValueError("FACTORY_GIT_ROOT_REQUIRED")
    return Path(completed.stdout.strip()).resolve()


def environment_problem(
    *, harness: str, platform_name: str, python_version: tuple[int, ...]
) -> str | None:
    if harness not in SUPPORTED_HARNESSES:
        return "FACTORY_HARNESS_UNSUPPORTED"
    if platform_name != SUPPORTED_PLATFORM or python_version < (3, 11):
        return "FACTORY_ENVIRONMENT_UNVERIFIED"
    return None


def project_compatibility(root: Path) -> tuple[str, list[str]]:
    required = (
        Path("AGENTS.md"),
        Path("docs/Factory/ARCHITECTURE.md"),
        Path("docs/Factory/ORCHESTRATION.md"),
        Path("scripts/factoryctl"),
    )
    missing = [path.as_posix() for path in required if not (root / path).is_file()]
    if len(missing) == len(required):
        return "NOT_CONFIGURED", missing
    if missing:
        return "INCOMPLETE", missing
    return "COMPATIBLE", []


def skill_name(path: Path) -> str | None:
    if not path.is_file():
        return None
    in_frontmatter = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "---":
            if in_frontmatter:
                return None
            in_frontmatter = True
            continue
        if in_frontmatter and line.startswith("name:"):
            return line.removeprefix("name:").strip()
    return None


def evaluate_skill_coexistence(
    root: Path, *, plugin_skill_names: set[str]
) -> dict[str, Any]:
    repo_skills: set[str] = set()
    skills_root = root / ".agents" / "skills"
    if skills_root.is_dir():
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            name = skill_name(skill_file)
            if name:
                repo_skills.add(name)
    collisions = sorted(repo_skills & plugin_skill_names)
    details = {
        "repository_skills": sorted(repo_skills),
        "plugin_skills": sorted(plugin_skill_names),
        "collisions": collisions,
        "automatic_deletions": [],
        "migration_guidance": (
            "Keep repository-scoped Factory role skills. The plugin supplies public "
            "entry points; it does not delete or replace project-owned skills."
        ),
        "mutations": [],
    }
    if collisions:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_SKILL_COLLISION",
            next_legal_action="rename_or_remove_the_collision_only_with_owner_approval",
            **details,
        )
    return result(
        state="COMPATIBLE",
        reason_code="FACTORY_SKILLS_COMPATIBLE",
        next_legal_action="preserve_repository_scoped_skills",
        **details,
    )


def evaluate_doctor(
    root: Path,
    *,
    harness: str,
    platform_name: str | None = None,
    python_version: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    actual_platform = platform_name or sys.platform
    actual_python = python_version or sys.version_info[:3]
    problem = environment_problem(
        harness=harness,
        platform_name=actual_platform,
        python_version=actual_python,
    )
    compatibility, missing = project_compatibility(root)
    try:
        installation_state = load_installation_state(root)
    except ValueError as error:
        installation_state = None
        installation_problem = str(error)
    else:
        installation_problem = None
    installed_factory_version = (
        installation_state["factory_version"] if installation_state else None
    )
    if installed_factory_version == PLUGIN_VERSION:
        version_status = "CURRENT"
    elif installed_factory_version is None:
        version_status = "NOT_INSTALLED"
    else:
        version_status = "DIFFERENT_VERSION"
    coexistence = (
        evaluate_skill_coexistence(root, plugin_skill_names=CODEX_PLUGIN_SKILLS)
        if harness == "codex"
        else {
            "state": "NAMESPACED",
            "reason_code": "FACTORY_SKILLS_NAMESPACED",
            "collisions": [],
            "automatic_deletions": [],
            "migration_guidance": (
                "Claude plugin skills remain under the factory namespace; preserve "
                "repository-owned skills and instructions."
            ),
            "mutations": [],
        }
    )
    details = {
        "harness": harness,
        "plugin_version": PLUGIN_VERSION,
        "repository_root": str(root),
        "environment": {
            "platform": actual_platform,
            "python": ".".join(str(item) for item in actual_python),
            "machine": platform.machine(),
        },
        "project_compatibility": compatibility,
        "project_factory_version": installed_factory_version,
        "project_version_status": version_status,
        "project_source_revision": (
            installation_state["source_revision"] if installation_state else None
        ),
        "missing_prerequisites": missing,
        "skill_coexistence": coexistence,
        "model_policy": {
            "default": "selected_session_model_serves_all_factory_roles",
            "roles": ["red", "blue", "purple"],
            "separate_routing_configured": False,
        },
        "mutations": [],
    }
    if problem:
        return result(
            state="BLOCKED",
            reason_code=problem,
            next_legal_action="use_a_supported_environment_or_revalidate_compatibility",
            **details,
        )
    if installation_problem:
        return result(
            state="BLOCKED",
            reason_code=installation_problem,
            next_legal_action="repair_the_installation_state_or_reinstall",
            **details,
        )
    if compatibility == "NOT_CONFIGURED":
        return result(
            state="READY_TO_INITIALIZE",
            reason_code="FACTORY_PROJECT_NOT_CONFIGURED",
            next_legal_action="preview_greenfield_or_brownfield_setup",
            **details,
        )
    if coexistence["state"] == "BLOCKED":
        return result(
            state="BLOCKED",
            reason_code="FACTORY_SKILL_COLLISION",
            next_legal_action=coexistence["next_legal_action"],
            **details,
        )
    if compatibility == "INCOMPLETE":
        return result(
            state="BLOCKED",
            reason_code="FACTORY_PROJECT_INCOMPLETE",
            next_legal_action="review_missing_factory_prerequisites",
            **details,
        )
    return result(
        state="READY",
        reason_code="FACTORY_DOCTOR_OK",
        next_legal_action="inspect_factory_progress",
        **details,
    )


def select_run(root: Path, run_id: str | None) -> Path | None:
    runs_root = root / "docs" / "Factory" / "runs"
    if run_id:
        if "/" in run_id or "\\" in run_id or run_id in {".", ".."}:
            raise ValueError("FACTORY_UNSAFE_RUN_ID")
        candidate = runs_root / run_id
        return candidate if candidate.is_dir() else None
    if not runs_root.is_dir():
        return None
    candidates = sorted(
        path for path in runs_root.iterdir() if path.is_dir() and path.name.startswith("RUN_")
    )
    return candidates[-1] if candidates else None


def field_value(path: Path, label: str) -> str | None:
    if not path.is_file():
        return None
    prefix = f"- {label}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return None


def section_bullet_value(path: Path, heading: str) -> str | None:
    if not path.is_file():
        return None
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == f"## {heading}":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            return None
        if in_section and line.startswith("- "):
            return line[2:].strip()
    return None


def output_paths(handoff: Path) -> list[str]:
    if not handoff.is_file():
        return []
    in_outputs = False
    outputs: list[str] = []
    for line in handoff.read_text(encoding="utf-8").splitlines():
        if line == "## Outputs Produced (paths)":
            in_outputs = True
            continue
        if in_outputs and line.startswith("## "):
            break
        if in_outputs and line.startswith("- `") and line.endswith("`"):
            outputs.append(line[3:-1])
    return outputs


def output_path_contradiction(root: Path, run_root: Path, handoff: Path) -> str | None:
    if not handoff.is_file():
        return None
    in_outputs = False
    saw_heading = False
    for line in handoff.read_text(encoding="utf-8").splitlines():
        if line == "## Outputs Produced (paths)":
            in_outputs = True
            saw_heading = True
            continue
        if in_outputs and line.startswith("## "):
            break
        if not in_outputs or not line.strip():
            continue
        if not (line.startswith("- `") and line.endswith("`") and line.count("`") == 2):
            return "malformed_output_declaration"
        value = line[3:-1]
        candidate = Path(value)
        if (
            not value
            or candidate.is_absolute()
            or any(part in {"", ".", ".."} for part in candidate.parts)
            or any(char in value for char in "*?[]{}$()|;\\")
        ):
            return f"unsafe_output_path:{value}"
        anchor = root if candidate.parts[0] == "docs" else run_root
        target = anchor / candidate
        try:
            target.resolve(strict=False).relative_to(anchor.resolve())
        except ValueError:
            return f"output_path_escapes_root:{value}"
        if not target.exists():
            return f"claims_missing_output:{value}"
        if target.is_file() and target.stat().st_size == 0:
            return f"claims_empty_output:{value}"
        if target.is_dir() and not any(target.iterdir()):
            return f"claims_empty_output:{value}"
        if not target.is_file() and not target.is_dir():
            return f"claims_unsupported_output:{value}"
    if not saw_heading:
        return "missing_output_declaration_section"
    return None


def resolve_output_path(root: Path, run_root: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    if candidate.parts and candidate.parts[0] == "docs":
        return root / candidate
    return run_root / candidate


def recall_is_weak(run_root: Path) -> bool:
    report = run_root / "CONTEXT_RECALL_REPORT.md"
    if not report.is_file():
        return False
    text = report.read_text(encoding="utf-8")
    weak = "Coverage Verdict: WEAK" in text
    repaired = (
        "Direct-Source Repair Status: APPLIED" in text
        and "Materiality Check: PASS" in text
        and "Remaining Material Unresolved Refs: None" in text
    )
    return weak and not repaired


def intent_lock_problem(run_root: Path, stages: list[str]) -> str | None:
    if "D" not in stages:
        return None
    report = run_root / "pack" / "intent_lock_report.md"
    if field_value(report, "Verdict") != "PASS":
        return "intent_purple_verdict_not_pass"
    digest = field_value(report, "Locked SHA-256")
    if digest is None:
        return "intent_lock_digest_missing"
    digest = digest.strip("`")
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        return "intent_lock_digest_invalid"
    intent = run_root / "pack" / "intent.md"
    if not intent.is_file() or file_sha256(intent) != digest:
        return "intent_lock_digest_mismatch"
    return None


def passed_stages(run_root: Path) -> list[str]:
    handoff_root = run_root / "pack" / "HANDOFF"
    return [
        stage
        for stage in STAGE_ORDER
        if section_bullet_value(
            handoff_root / f"HANDOFF_STAGE_{stage}.md", "Exit Criteria Status"
        )
        == "PASS"
    ]


def evidence_contradiction(root: Path, run_root: Path, stages: list[str]) -> str | None:
    expected_prefix = list(STAGE_ORDER[: len(stages)])
    if stages != expected_prefix:
        return "completed_stage_order_has_a_gap"
    for stage in stages:
        handoff = run_root / "pack" / "HANDOFF" / f"HANDOFF_STAGE_{stage}.md"
        contradiction = output_path_contradiction(root, run_root, handoff)
        if contradiction:
            return f"stage_{stage.lower()}_{contradiction}"
    knowledge = run_root / "KNOWLEDGE_LINT.txt"
    if stages and (not knowledge.is_file() or "knowledge_lint: PASS" not in knowledge.read_text(encoding="utf-8")):
        return "stage_handoff_exists_without_passing_knowledge_lint"
    return None


def persisted_validators(run_root: Path) -> list[dict[str, str]]:
    validators: list[dict[str, str]] = []
    knowledge = run_root / "KNOWLEDGE_LINT.txt"
    if knowledge.is_file():
        status = "PASS" if "knowledge_lint: PASS" in knowledge.read_text(encoding="utf-8") else "FAIL"
        validators.append({"validator": "knowledge_lint", "status": status})
    audit = run_root / "pack" / "PACK_AUDIT_REPORT.md"
    verdict = field_value(audit, "Verdict")
    if verdict:
        validators.append({"validator": "purple_pack_audit", "status": verdict})
    return validators


def evaluate_execution_closeout(root: Path, run_root: Path) -> dict[str, Any] | None:
    closeout = run_root / EXECUTION_CLOSEOUT_NAME
    if not closeout.exists():
        return None
    validator = root / "scripts" / "factory_execution_closeout.py"
    if not validator.is_file():
        return {
            "status": "FAIL",
            "reason_code": "FACTORY_EXECUTION_CLOSEOUT_VALIDATOR_MISSING",
            "detail": "scripts/factory_execution_closeout.py",
            "mutations": [],
        }
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(validator),
                "validate",
                "--root",
                str(root),
                "--run",
                run_root.name,
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except (OSError, subprocess.TimeoutExpired):
        return {
            "status": "FAIL",
            "reason_code": "FACTORY_EXECUTION_CLOSEOUT_VALIDATOR_ERROR",
            "detail": "validator_invocation",
            "mutations": [],
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {
            "status": "FAIL",
            "reason_code": "FACTORY_EXECUTION_CLOSEOUT_VALIDATOR_ERROR",
            "detail": "validator_output",
            "mutations": [],
        }
    if completed.returncode not in {0, 1} or not isinstance(payload, dict):
        return {
            "status": "FAIL",
            "reason_code": "FACTORY_EXECUTION_CLOSEOUT_VALIDATOR_ERROR",
            "detail": "validator_exit",
            "mutations": [],
        }
    return payload


def evaluate_progress(root: Path, *, run_id: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    run_root = select_run(root, run_id)
    if run_root is None:
        return result(
            state="READY_TO_INITIALIZE",
            reason_code="FACTORY_NO_ACTIVE_RUN",
            next_legal_action="create_a_factory_run",
            repository_root=str(root),
            run_id=None,
            completed_stages=[],
            completed_validators=[],
            mutations=[],
        )

    stages = passed_stages(run_root)
    common = {
        "repository_root": str(root),
        "run_id": run_root.name,
        "execution_mode": (
            (run_root / "EXECUTION_MODE.txt").read_text(encoding="utf-8").strip()
            if (run_root / "EXECUTION_MODE.txt").is_file()
            else None
        ),
        "completed_stages": stages,
        "completed_validators": persisted_validators(run_root),
        "mutations": [],
    }
    contradiction = evidence_contradiction(root, run_root, stages)
    if contradiction:
        next_action = (
            "repair_stage_a_and_rerun_stage_lint"
            if contradiction.startswith("stage_a_")
            else "repair_stage_evidence_and_rerun_the_applicable_validator"
        )
        return result(
            state="BLOCKED",
            reason_code="FACTORY_EVIDENCE_CONTRADICTION",
            next_legal_action=next_action,
            blocker=contradiction,
            **common,
        )
    if recall_is_weak(run_root):
        return result(
            state="BLOCKED",
            reason_code="FACTORY_WEAK_RECALL",
            next_legal_action="refresh_recall_and_resolve_material_gaps",
            **common,
        )
    lock_problem = intent_lock_problem(run_root, stages)
    if lock_problem:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_INTENT_NOT_LOCKED",
            next_legal_action="repair_intent_and_repeat_purple",
            blocker=lock_problem,
            **common,
        )
    if "I2" in stages:
        audit_verdict = field_value(run_root / "pack" / "PACK_AUDIT_REPORT.md", "Verdict")
        if audit_verdict not in {"PASS", "CONDITIONAL PASS"}:
            return result(
                state="BLOCKED",
                reason_code="FACTORY_PACK_AUDIT_NOT_PASSING",
                next_legal_action="repair_pack_and_repeat_purple_audit",
                **common,
            )
        execution_prompt = run_root / "EXECUTION_PROMPT.md"
        human_go = field_value(execution_prompt, "Human Go")
        has_human_go = human_go == "RECORDED" or bool(
            human_go and human_go.startswith("RECORDED ")
        )
        if common["execution_mode"] == "EXECUTION_ENABLED" and not has_human_go:
            return result(
                state="WAITING_HUMAN_GO",
                reason_code="FACTORY_HUMAN_GO_REQUIRED",
                next_legal_action="obtain_explicit_human_go",
                **common,
            )
        closeout = evaluate_execution_closeout(root, run_root)
        if closeout is not None:
            if closeout.get("status") != "PASS":
                return result(
                    state="BLOCKED",
                    reason_code="FACTORY_EXECUTION_CLOSEOUT_INVALID",
                    next_legal_action="repair_the_closeout_evidence_without_bypassing_human_gates",
                    blocker=closeout.get(
                        "reason_code", "FACTORY_EXECUTION_CLOSEOUT_VALIDATOR_ERROR"
                    ),
                    closeout_detail=closeout.get("detail"),
                    **common,
                )
            return result(
                state=closeout["outcome"],
                reason_code=closeout["reason_code"],
                next_legal_action=closeout["next_legal_action"],
                execution_closeout={
                    "schema": closeout["schema"],
                    "path": closeout["path"],
                    "sha256": closeout["sha256"],
                    "verification_result_count": closeout[
                        "verification_result_count"
                    ],
                },
                **common,
            )
        if common["execution_mode"] == "EXECUTION_ENABLED" and has_human_go:
            return result(
                state="AUTHORIZED_FOR_EXECUTION",
                reason_code="FACTORY_HUMAN_GO_RECORDED",
                next_legal_action="execute_the_next_approved_micro_sprint",
                **common,
            )
        return result(
            state="PACK_COMPLETE_WAITING_HUMAN_REVIEW",
            reason_code="FACTORY_PLANNING_COMPLETE",
            next_legal_action="review_the_pack",
            **common,
        )

    next_stage = STAGE_ORDER[len(stages)]
    return result(
        state="PLANNING_IN_PROGRESS",
        reason_code="FACTORY_NEXT_STAGE_READY",
        next_legal_action=f"run_stage_{next_stage.lower()}",
        **common,
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stable_plan_id(value: dict[str, Any]) -> str:
    plan_input = {
        key: copy.deepcopy(value[key])
        for key in (
            "mode",
            "harness",
            "plugin_version",
            "installed_version",
            "bootstrap_plan",
            "planned_files",
        )
        if key in value
    }
    bootstrap = plan_input.get("bootstrap_plan")
    if isinstance(bootstrap, dict):
        for preserved in bootstrap.get("preserved_paths", []):
            if isinstance(preserved, dict) and "approval_sha256" in preserved:
                preserved["sha256"] = preserved.pop("approval_sha256")
    encoded = json.dumps(
        plan_input, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def transaction_receipt_path(transaction_id: str) -> str:
    return f"{TRANSACTION_RECEIPTS_DIR}/{transaction_id}.json"


def plan_pre_digests(root: Path, planned_files: list[dict[str, str]]) -> dict[str, str | None]:
    digests: dict[str, str | None] = {}
    for item in planned_files:
        target = safe_target(root, item["path"])
        digests[item["path"]] = file_sha256(target) if target.is_file() else None
    return digests


def attach_change_plan(
    value: dict[str, Any], *, root: Path, source_version: str | None
) -> None:
    transaction_id = value["plan_id"]
    receipt_path = transaction_receipt_path(transaction_id)
    no_op = (
        source_version == value["plugin_version"]
        and all(
            item["action"] in {"no_change", "preserve"}
            for item in value["planned_files"]
        )
    )
    state_action = (
        "modify" if source_version and source_version != value["plugin_version"]
        else "no_change" if source_version else "create"
    )
    value["metadata_plan"] = [
        {
            "path": INSTALLATION_STATE_PATH,
            "classification": "generated/pinned",
            "action": state_action,
        }
    ]
    if not no_op:
        value["metadata_plan"].append(
            {
                "path": receipt_path,
                "classification": "generated/pinned",
                "action": "create",
            }
        )
        value["allowed_paths"] = list(value["allowed_paths"]) + [receipt_path]
    value["change_plan"] = {
        "transaction_id": transaction_id,
        "operation": value["mode"],
        "source_version": source_version,
        "target_version": value["plugin_version"],
        "ordered_file_actions": [
            {"path": item["path"], "action": item["action"]}
            for item in value["planned_files"] + value["metadata_plan"]
        ],
        "ordered_transaction_steps": [
            *value.get("bootstrap_plan", {}).get("steps", []),
            *[
                {"kind": "payload", "path": item["path"], "action": item["action"]}
                for item in value["planned_files"]
            ],
            *[
                {"kind": "metadata", "path": item["path"], "action": item["action"]}
                for item in value["metadata_plan"]
            ],
            {"kind": "validation", "path": ".", "action": "verify"},
        ],
        "pre_digests": plan_pre_digests(
            root, value["planned_files"] + value["metadata_plan"]
        ),
        "conflicts": list(value.get("conflicts", [])),
        "approval_state": "NOT_REQUIRED" if no_op else "REVIEW_REQUIRED",
    }


def load_installation_state(root: Path) -> dict[str, Any] | None:
    state_path = root / INSTALLATION_STATE_PATH
    if not state_path.is_file():
        return None
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("FACTORY_INSTALLATION_STATE_INVALID") from error
    if (
        state.get("schema_version") != 1
        or not isinstance(state.get("factory_version"), str)
        or not isinstance(state.get("source_revision"), str)
        or not isinstance(state.get("managed_files"), list)
        or not isinstance(state.get("adapter_state"), dict)
        or not isinstance(state.get("last_successful_transaction"), dict)
    ):
        raise ValueError("FACTORY_INSTALLATION_STATE_INVALID")
    return state


def load_payload(payload_root: Path) -> tuple[str, list[dict[str, str]]]:
    ownership_path = payload_root / "OWNERSHIP.json"
    if not ownership_path.is_file():
        raise ValueError("FACTORY_PAYLOAD_MANIFEST_MISSING")
    ownership = json.loads(ownership_path.read_text(encoding="utf-8"))
    if ownership.get("schema_version") != 1:
        raise ValueError("FACTORY_PAYLOAD_MANIFEST_INVALID")
    entries = ownership.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("FACTORY_PAYLOAD_MANIFEST_INVALID")
    seen: set[str] = set()
    for entry in entries:
        relative = entry.get("path")
        classification = entry.get("classification")
        expected_digest = entry.get("sha256")
        if (
            not isinstance(relative, str)
            or relative in seen
            or classification not in {"release-owned", "project-owned"}
            or not isinstance(expected_digest, str)
        ):
            raise ValueError("FACTORY_PAYLOAD_MANIFEST_INVALID")
        seen.add(relative)
        source = payload_root / relative
        if not source.is_file() or file_sha256(source) != expected_digest:
            raise ValueError("FACTORY_PAYLOAD_DIGEST_MISMATCH")
    return str(ownership.get("version", "unknown")), entries


def effective_payload_entries(
    entries: list[dict[str, str]], *, harness: str
) -> list[dict[str, str]]:
    effective = list(entries)
    if harness == "claude":
        effective.append(
            {
                "path": "CLAUDE.md",
                "classification": "generated/pinned",
                "sha256": hashlib.sha256(CLAUDE_BRIDGE).hexdigest(),
            }
        )
    return sorted(effective, key=lambda entry: entry["path"])


def payload_bytes(payload_root: Path, path: str, *, harness: str) -> bytes:
    if harness == "claude" and path == "CLAUDE.md":
        return CLAUDE_BRIDGE
    return (payload_root / path).read_bytes()


def payload_mode(payload_root: Path, path: str, *, harness: str) -> int:
    if harness == "claude" and path == "CLAUDE.md":
        return 0o644
    return (payload_root / path).stat().st_mode & 0o777


def safe_target(root: Path, relative_text: str) -> Path:
    relative = Path(relative_text)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError("FACTORY_UNSAFE_PATH")
    target = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("FACTORY_UNSAFE_PATH")
    if not target.resolve(strict=False).is_relative_to(root):
        raise ValueError("FACTORY_UNSAFE_PATH")
    return target


def git_state_digest(git_path: Path) -> str:
    digest = hashlib.sha256()
    if git_path.is_file():
        digest.update(b"file\0")
        digest.update(git_path.read_bytes())
        return digest.hexdigest()
    if not git_path.is_dir():
        raise ValueError("FACTORY_GIT_STATE_INVALID")
    for path in sorted(
        git_path.rglob("*"),
        key=lambda item: item.relative_to(git_path).as_posix(),
    ):
        relative = path.relative_to(git_path).as_posix().encode("utf-8")
        if path.is_symlink():
            digest.update(b"symlink\0" + relative + b"\0" + os.readlink(path).encode("utf-8") + b"\0")
        elif path.is_dir():
            digest.update(b"dir\0" + relative + b"\0")
        elif path.is_file():
            digest.update(b"file\0" + relative + b"\0" + path.read_bytes() + b"\0")
        else:
            raise ValueError("FACTORY_GIT_STATE_INVALID")
    return digest.hexdigest()


def claude_greenfield_preserved_paths(
    root: Path, *, harness: str
) -> list[dict[str, Any]]:
    if harness != "claude" or not root.is_dir():
        return []
    directory = root / ".claude"
    if directory.is_symlink():
        raise ValueError("FACTORY_UNSAFE_PATH")
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise ValueError("FACTORY_UNSAFE_PATH")
    entries = sorted(path.name for path in directory.iterdir())
    if entries != ["settings.local.json"]:
        return []
    settings = directory / "settings.local.json"
    if settings.is_symlink() or not settings.is_file():
        raise ValueError("FACTORY_UNSAFE_PATH")
    raw = settings.read_bytes()
    approval_sha256 = bytes_sha256(raw)
    try:
        parsed = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = None
    if isinstance(parsed, dict):
        permissions = parsed.get("permissions")
        if isinstance(permissions, dict):
            allow = permissions.get("allow")
            if isinstance(allow, list) and all(isinstance(item, str) for item in allow):
                approval_value = copy.deepcopy(parsed)
                approval_value["permissions"]["allow"] = []
                approval_sha256 = bytes_sha256(
                    json.dumps(
                        approval_value,
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=False,
                    ).encode("utf-8")
                )
    return [
        {
            "path": ".claude/settings.local.json",
            "sha256": bytes_sha256(raw),
            "approval_sha256": approval_sha256,
            "mode": settings.stat().st_mode & 0o777,
            "directory": ".claude",
            "directory_mode": directory.stat().st_mode & 0o777,
            "directory_entries": entries,
            "directory_type": "directory",
            "file_type": "regular",
        }
    ]


def validate_greenfield_preserved_paths(
    root: Path,
    *,
    harness: str,
    bootstrap: dict[str, Any],
    check_top_level: bool,
) -> None:
    expected = bootstrap.get("preserved_paths", [])
    if not expected:
        return
    try:
        current = claude_greenfield_preserved_paths(root, harness=harness)
    except (OSError, ValueError) as error:
        raise ValueError("FACTORY_PLAN_STALE") from error
    if current != expected:
        raise ValueError("FACTORY_PLAN_STALE")
    if check_top_level:
        expected_entries = {".claude"}
        if bootstrap["git_existed"]:
            expected_entries.add(".git")
        if {path.name for path in root.iterdir()} != expected_entries:
            raise ValueError("FACTORY_PLAN_STALE")


def greenfield_bootstrap_plan(
    root: Path, *, preserved_paths: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    if root.exists() and not root.is_dir():
        raise ValueError("FACTORY_UNSAFE_PATH")
    root_action = "no_change" if root.is_dir() else "create"
    git_path = root / ".git"
    if git_path.is_symlink():
        raise ValueError("FACTORY_UNSAFE_PATH")
    git_action = "no_change" if git_path.exists() else "create"
    return {
        "root_existed": root.is_dir(),
        "git_existed": git_path.exists(),
        "git_pre_digest": git_state_digest(git_path) if git_path.exists() else None,
        "preserved_paths": preserved_paths or [],
        "steps": [
            {"kind": "root", "path": ".", "action": root_action},
            {"kind": "git", "path": ".git", "action": git_action},
        ],
    }


def evaluate_setup_plan(
    root: Path,
    *,
    mode: str,
    harness: str,
    payload_root: Path,
    platform_name: str | None = None,
    python_version: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    if mode not in {"greenfield", "brownfield"}:
        raise ValueError("FACTORY_SETUP_MODE_INVALID")
    problem = environment_problem(
        harness=harness,
        platform_name=platform_name or sys.platform,
        python_version=python_version or sys.version_info[:3],
    )
    common = {
        "mode": mode,
        "harness": harness,
        "repository_root": str(root),
        "mutations": [],
    }
    if problem:
        return result(
            state="BLOCKED",
            reason_code=problem,
            next_legal_action="use_a_supported_environment_or_revalidate_compatibility",
            **common,
        )
    try:
        installation_state = load_installation_state(root)
    except ValueError as error:
        return result(
            state="BLOCKED",
            reason_code=str(error),
            next_legal_action="repair_the_installation_state_or_reinstall",
            **common,
        )
    preserved_paths: list[dict[str, Any]] = []
    if mode == "greenfield" and root.is_dir() and installation_state is None:
        try:
            preserved_paths = claude_greenfield_preserved_paths(
                root, harness=harness
            )
        except (OSError, ValueError) as error:
            return result(
                state="BLOCKED",
                reason_code=str(error),
                next_legal_action="choose_a_safe_empty_target",
                **common,
            )
        preserved_top_level = {".claude"} if preserved_paths else set()
        unexpected = sorted(
            path.name
            for path in root.iterdir()
            if path.name != ".git" and path.name not in preserved_top_level
        )
        if unexpected and installation_state is None:
            return result(
                state="BLOCKED",
                reason_code="FACTORY_GREENFIELD_NOT_EMPTY",
                next_legal_action=(
                    "use_brownfield_preview"
                    if (root / ".git").exists()
                    else "choose_an_empty_target_or_remove_non_project_harness_content"
                ),
                unexpected_paths=unexpected,
                **common,
            )

    try:
        bootstrap_plan = (
            greenfield_bootstrap_plan(root, preserved_paths=preserved_paths)
            if mode == "greenfield"
            else None
        )
        installed_files = {
            entry["path"]: entry
            for entry in installation_state["managed_files"]
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        } if installation_state else {}
        payload_version, raw_entries = load_payload(payload_root)
        entries = effective_payload_entries(raw_entries, harness=harness)
        planned_files: list[dict[str, str]] = []
        conflicts: list[str] = []
        for entry in entries:
            target = safe_target(root, entry["path"])
            if not target.exists():
                action = "create"
            elif not target.is_file():
                action = "conflict"
                conflicts.append(entry["path"])
            elif file_sha256(target) == entry["sha256"]:
                action = "no_change"
            elif (
                entry["classification"] == "project-owned"
                and entry["path"] in installed_files
            ):
                action = "preserve"
            else:
                action = "conflict"
                conflicts.append(entry["path"])
            planned_files.append(
                {
                    "path": entry["path"],
                    "classification": entry["classification"],
                    "action": action,
                    "source_sha256": entry["sha256"],
                }
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        reason_code = (
            str(error)
            if str(error).startswith("FACTORY_")
            else "FACTORY_PAYLOAD_MANIFEST_INVALID"
        )
        return result(
            state="BLOCKED",
            reason_code=reason_code,
            next_legal_action="repair_or_reinstall_the_factory_plugin",
            **common,
        )

    plan_details = {
        **common,
        "plugin_version": payload_version,
        "allowed_paths": [entry["path"] for entry in entries]
        + [INSTALLATION_STATE_PATH],
        "planned_files": planned_files,
        "conflicts": conflicts,
    }
    if bootstrap_plan:
        plan_details["bootstrap_plan"] = bootstrap_plan
        plan_details["allowed_paths"] = [".", ".git", *plan_details["allowed_paths"]]
    plan_details["plan_id"] = stable_plan_id(plan_details)
    attach_change_plan(
        plan_details,
        root=root,
        source_version=(
            installation_state["factory_version"] if installation_state else None
        ),
    )
    if conflicts:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_CONFLICT_USER_OWNED",
            next_legal_action="review_conflicts_without_applying_changes",
            **plan_details,
        )
    if plan_details["change_plan"]["approval_state"] == "NOT_REQUIRED":
        return result(
            state="NO_CHANGE",
            reason_code="FACTORY_ALREADY_CURRENT",
            next_legal_action="inspect_factory_progress",
            **plan_details,
        )
    return result(
        state="PLAN_READY",
        reason_code="FACTORY_PLAN_READY",
        next_legal_action="review_and_explicitly_approve_the_plan",
        **plan_details,
    )


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def capture_snapshots(root: Path, paths: list[str]) -> dict[str, dict[str, Any]]:
    snapshots: dict[str, dict[str, Any]] = {}
    for relative in sorted(set(paths)):
        target = safe_target(root, relative)
        if target.exists() and not target.is_file():
            raise ValueError("FACTORY_CONFLICT_USER_OWNED")
        snapshots[relative] = {
            "existed": target.is_file(),
            "data": (
                base64.b64encode(target.read_bytes()).decode("ascii")
                if target.is_file()
                else None
            ),
            "mode": (target.stat().st_mode & 0o777) if target.is_file() else None,
        }
    return snapshots


def remove_empty_parents(root: Path, path: Path) -> None:
    parent = path.parent
    while parent != root and parent.is_relative_to(root):
        try:
            parent.rmdir()
        except OSError:
            break
        parent = parent.parent


def restore_snapshots(root: Path, snapshots: dict[str, dict[str, Any]]) -> None:
    for relative in sorted(snapshots, reverse=True):
        target = safe_target(root, relative)
        snapshot = snapshots[relative]
        if snapshot["existed"]:
            atomic_write(
                target,
                base64.b64decode(snapshot["data"]),
                int(snapshot["mode"]),
            )
        elif target.exists():
            if not target.is_file():
                raise RuntimeError(f"cannot restore non-file path: {relative}")
            target.unlink()
            remove_empty_parents(root, target)


def apply_changes(
    root: Path, changes: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    snapshots = capture_snapshots(root, [change["path"] for change in changes])
    try:
        for change in changes:
            target = safe_target(root, change["path"])
            if change["action"] == "delete":
                target.unlink()
                remove_empty_parents(root, target)
            else:
                atomic_write(target, change["data"], change.get("mode", 0o644))
    except Exception:
        restore_snapshots(root, snapshots)
        raise
    return snapshots


def managed_files_from_plan(
    root: Path,
    payload_root: Path,
    plan: dict[str, Any],
    previous_state: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    previous = {
        entry["path"]: entry
        for entry in (previous_state or {}).get("managed_files", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    files: list[dict[str, str]] = []
    for item in plan["planned_files"]:
        if item["action"] == "delete":
            continue
        if item["action"] == "preserve" and item["path"] in previous:
            prior = previous[item["path"]]
            if prior.get("ownership_class") == item["classification"]:
                files.append(prior)
            else:
                files.append(
                    {
                        "path": item["path"],
                        "ownership_class": item["classification"],
                        "expected_digest": file_sha256(root / item["path"]),
                        "source_version": plan["plugin_version"],
                    }
                )
            continue
        target = root / item["path"]
        digest = (
            item["source_sha256"]
            if item["action"] in {"create", "modify"}
            else file_sha256(target)
        )
        files.append(
            {
                "path": item["path"],
                "ownership_class": item["classification"],
                "expected_digest": digest,
                "source_version": plan["plugin_version"],
            }
        )
    return sorted(files, key=lambda entry: entry["path"])


def validate_plan_preconditions(
    root: Path, plan: dict[str, Any], previous_state: dict[str, Any] | None
) -> None:
    bootstrap = plan.get("bootstrap_plan")
    if bootstrap:
        validate_greenfield_preserved_paths(
            root,
            harness=plan["harness"],
            bootstrap=bootstrap,
            check_top_level=True,
        )
        root_step, git_step = bootstrap["steps"]
        if root_step["action"] == "create" and root.exists():
            raise ValueError("FACTORY_PLAN_STALE")
        if root_step["action"] == "no_change" and not root.is_dir():
            raise ValueError("FACTORY_PLAN_STALE")
        git_path = root / ".git"
        if git_step["action"] == "create" and git_path.exists():
            raise ValueError("FACTORY_PLAN_STALE")
        if git_step["action"] == "no_change" and (
            not git_path.exists()
            or git_state_digest(git_path) != bootstrap["git_pre_digest"]
        ):
            raise ValueError("FACTORY_PLAN_STALE")
    installed = {
        entry["path"]: entry
        for entry in (previous_state or {}).get("managed_files", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    for item in plan["planned_files"]:
        target = safe_target(root, item["path"])
        action = item["action"]
        if action == "create" and target.exists():
            raise ValueError("FACTORY_PLAN_STALE")
        if action == "no_change" and (
            not target.is_file() or file_sha256(target) != item["source_sha256"]
        ):
            raise ValueError("FACTORY_PLAN_STALE")
        if action == "preserve" and not target.is_file():
            raise ValueError("FACTORY_PLAN_STALE")
        if action in {"modify", "delete"}:
            prior = installed.get(item["path"])
            if (
                not prior
                or not target.is_file()
                or file_sha256(target) != prior.get("expected_digest")
            ):
                raise ValueError("FACTORY_PLAN_STALE")


def validate_setup_result(
    root: Path, managed_files: list[dict[str, str]], installation_state_bytes: bytes
) -> None:
    for entry in managed_files:
        target = safe_target(root, entry["path"])
        if not target.is_file() or file_sha256(target) != entry["expected_digest"]:
            raise RuntimeError("FACTORY_SETUP_VALIDATION_FAILED")
    state_path = safe_target(root, INSTALLATION_STATE_PATH)
    if not state_path.is_file() or file_sha256(state_path) != bytes_sha256(
        installation_state_bytes
    ):
        raise RuntimeError("FACTORY_SETUP_VALIDATION_FAILED")


def restore_bootstrap_paths(
    root: Path, *, root_created: bool, git_created: bool, git_digest: str | None
) -> str | None:
    git_path = root / ".git"
    if git_created:
        if (
            not git_path.exists()
            or git_digest is None
            or git_state_digest(git_path) != git_digest
        ):
            return "FACTORY_ROLLBACK_GIT_STATE_CHANGED"
        shutil.rmtree(git_path)
    if root_created:
        try:
            root.rmdir()
        except OSError:
            pass
    return None


def apply_setup_plan(
    root: Path,
    *,
    plan: dict[str, Any],
    approved_plan_id: str | None,
    payload_root: Path,
) -> dict[str, Any]:
    root = root.resolve()
    if plan["state"] != "PLAN_READY":
        return plan
    if approved_plan_id != plan["plan_id"]:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_PLAN_APPROVAL_REQUIRED",
            next_legal_action="approve_the_exact_previewed_plan_id",
            plan_id=plan["plan_id"],
            mutations=[],
        )
    changes: list[dict[str, Any]] = []
    previous_state = load_installation_state(root)
    try:
        validate_plan_preconditions(root, plan, previous_state)
    except ValueError as error:
        return result(
            state="BLOCKED",
            reason_code=str(error),
            next_legal_action="preview_and_approve_a_fresh_plan",
            plan_id=plan["plan_id"],
            mutations=[],
        )
    for item in plan["planned_files"]:
        if item["action"] != "create":
            continue
        changes.append(
            {
                "path": item["path"],
                "action": "write",
                "data": payload_bytes(
                    payload_root, item["path"], harness=plan["harness"]
                ),
                "mode": payload_mode(
                    payload_root, item["path"], harness=plan["harness"]
                ),
            }
        )
    managed_files = managed_files_from_plan(
        root, payload_root, plan, previous_state=previous_state
    )
    transaction_path = transaction_receipt_path(plan["plan_id"])
    if safe_target(root, transaction_path).exists():
        return result(
            state="BLOCKED",
            reason_code="FACTORY_TRANSACTION_RECEIPT_EXISTS",
            next_legal_action="inspect_existing_transaction_evidence_and_preview_again",
            plan_id=plan["plan_id"],
            mutations=[],
        )
    bootstrap = plan.get("bootstrap_plan")
    transaction_receipt = {
        "schema_version": 1,
        **plan["change_plan"],
        "approval_state": "APPROVED",
        "post_digests": {
            entry["path"]: entry["expected_digest"] for entry in managed_files
        },
        "outcome": "APPLIED",
        "recovery_status": "AVAILABLE" if plan["mode"] == "greenfield" else "NOT_REQUIRED",
    }
    installation_state = {
        "schema_version": 1,
        "factory_version": plan["plugin_version"],
        "source_revision": f"factory-plugin@{plan['plugin_version']}",
        "managed_files": managed_files,
        "adapter_state": {
            "harness": plan["harness"],
            "claude_bridge": plan["harness"] == "claude",
        },
        "last_successful_transaction": {
            "transaction_id": plan["plan_id"],
            "operation": plan["mode"],
            "receipt": transaction_path,
            "outcome": "APPLIED",
        },
    }
    installation_state_bytes = (
        json.dumps(installation_state, indent=2) + "\n"
    ).encode()
    transaction_receipt["post_digests"][INSTALLATION_STATE_PATH] = bytes_sha256(
        installation_state_bytes
    )
    root_created = False
    git_created = False
    git_digest: str | None = None
    snapshots: dict[str, dict[str, Any]] | None = None
    try:
        if bootstrap and bootstrap["steps"][0]["action"] == "create":
            root.mkdir()
            root_created = True
        if bootstrap and bootstrap["steps"][1]["action"] == "create":
            subprocess.run(
                ["git", "init", "-q", str(root)],
                check=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            git_created = True
            git_digest = git_state_digest(root / ".git")
        if bootstrap:
            transaction_receipt["bootstrap"] = {
                "root_created": root_created,
                "git_created": git_created,
                "git_post_init_digest": git_digest,
            }
            if bootstrap["preserved_paths"]:
                transaction_receipt["bootstrap"]["preserved_paths"] = bootstrap[
                    "preserved_paths"
                ]
        changes.extend(
            [
                {
                    "path": transaction_path,
                    "action": "write",
                    "data": (
                        json.dumps(transaction_receipt, indent=2, sort_keys=True) + "\n"
                    ).encode(),
                    "mode": 0o600,
                },
                {
                    "path": INSTALLATION_STATE_PATH,
                    "action": "write",
                    "data": installation_state_bytes,
                    "mode": 0o644,
                },
            ]
        )
        snapshots = apply_changes(root, changes)
        if bootstrap:
            validate_greenfield_preserved_paths(
                root,
                harness=plan["harness"],
                bootstrap=bootstrap,
                check_top_level=False,
            )
        validate_setup_result(root, managed_files, installation_state_bytes)
    except Exception as error:
        if snapshots is not None:
            try:
                restore_snapshots(root, snapshots)
            except Exception:
                pass
        rollback_reason = restore_bootstrap_paths(
            root,
            root_created=root_created,
            git_created=git_created,
            git_digest=git_digest,
        )
        return result(
            state="BLOCKED",
            reason_code=rollback_reason or "FACTORY_SETUP_ABORTED",
            next_legal_action="resolve_the_write_failure_and_preview_again",
            plan_id=plan["plan_id"],
            blocker=f"{type(error).__name__}: {error}",
            mutations=[],
        )
    return result(
        state="APPLIED",
        reason_code="FACTORY_SETUP_APPLIED",
        next_legal_action="run_factory_doctor",
        plugin_version=plan["plugin_version"],
        plan_id=plan["plan_id"],
        receipt=transaction_path,
        installation_state=INSTALLATION_STATE_PATH,
        mutations=[
            *(["."] if root_created else []),
            *([".git"] if git_created else []),
            *[change["path"] for change in changes],
        ],
    )


def semver(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError("FACTORY_VERSION_INVALID")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def evaluate_update_plan(
    root: Path,
    *,
    harness: str,
    payload_root: Path,
    platform_name: str | None = None,
    python_version: tuple[int, ...] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    problem = environment_problem(
        harness=harness,
        platform_name=platform_name or sys.platform,
        python_version=python_version or sys.version_info[:3],
    )
    common = {
        "mode": "update",
        "harness": harness,
        "repository_root": str(root),
        "mutations": [],
    }
    if problem:
        return result(
            state="BLOCKED",
            reason_code=problem,
            next_legal_action="use_a_supported_environment_or_revalidate_compatibility",
            **common,
        )
    try:
        installation_state = load_installation_state(root)
        if installation_state is None:
            raise ValueError("FACTORY_INSTALLATION_STATE_MISSING")
        target_version, raw_target_entries = load_payload(payload_root)
        target_entries = effective_payload_entries(
            raw_target_entries, harness=harness
        )
        installed_version = installation_state["factory_version"]
        if semver(target_version) < semver(installed_version):
            return result(
                state="BLOCKED",
                reason_code="FACTORY_DOWNGRADE_UNSUPPORTED",
                next_legal_action="use_rollback_for_a_previously_installed_version",
                installed_version=installed_version,
                plugin_version=target_version,
                **common,
            )
        installed = {
            entry["path"]: entry
            for entry in installation_state["managed_files"]
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        }
        target = {entry["path"]: entry for entry in target_entries}
        planned_files: list[dict[str, str]] = []
        conflicts: list[str] = []
        for path, entry in sorted(target.items()):
            target_path = safe_target(root, path)
            prior = installed.get(path)
            if entry["classification"] == "project-owned":
                action = "create" if not target_path.exists() else "preserve"
            elif not target_path.exists():
                action = "conflict" if prior else "create"
            elif not target_path.is_file():
                action = "conflict"
            elif prior and file_sha256(target_path) != prior["expected_digest"]:
                action = "conflict"
            elif file_sha256(target_path) == entry["sha256"]:
                action = "no_change"
            else:
                action = "modify"
            if action == "conflict":
                conflicts.append(path)
            planned_files.append(
                {
                    "path": path,
                    "classification": entry["classification"],
                    "action": action,
                    "source_sha256": entry["sha256"],
                }
            )
        for path, prior in sorted(installed.items()):
            if path in target:
                continue
            target_path = safe_target(root, path)
            classification = prior["ownership_class"]
            if classification == "project-owned":
                action = "preserve"
            elif (
                not target_path.is_file()
                or file_sha256(target_path) != prior["expected_digest"]
            ):
                action = "conflict"
                conflicts.append(path)
            else:
                action = "delete"
            planned_files.append(
                {
                    "path": path,
                    "classification": classification,
                    "action": action,
                    "source_sha256": "",
                }
            )
    except (KeyError, OSError, json.JSONDecodeError, ValueError) as error:
        reason_code = (
            str(error)
            if str(error).startswith("FACTORY_")
            else "FACTORY_INSTALLATION_STATE_INVALID"
        )
        return result(
            state="BLOCKED",
            reason_code=reason_code,
            next_legal_action="repair_the_installation_state_or_reinstall",
            **common,
        )

    details = {
        **common,
        "installed_version": installed_version,
        "plugin_version": target_version,
        "planned_files": planned_files,
        "conflicts": conflicts,
        "allowed_paths": sorted(target)
        + sorted(path for path in installed if path not in target)
        + [INSTALLATION_STATE_PATH],
    }
    details["plan_id"] = stable_plan_id(details)
    attach_change_plan(details, root=root, source_version=installed_version)
    if conflicts:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_CONFLICT_USER_OWNED",
            next_legal_action="resolve_release_owned_file_conflicts_before_update",
            **details,
        )
    if installed_version == target_version:
        return result(
            state="NO_CHANGE",
            reason_code="FACTORY_ALREADY_CURRENT",
            next_legal_action="inspect_factory_progress",
            **details,
        )
    return result(
        state="PLAN_READY",
        reason_code="FACTORY_UPDATE_REVIEW_REQUIRED",
        next_legal_action="review_and_explicitly_approve_the_update_plan",
        **details,
    )


def apply_update_plan(
    root: Path,
    *,
    plan: dict[str, Any],
    approved_plan_id: str | None,
    payload_root: Path,
    interrupt_after_staging: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    if plan["state"] != "PLAN_READY":
        return plan
    if approved_plan_id != plan["plan_id"]:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_PLAN_APPROVAL_REQUIRED",
            next_legal_action="approve_the_exact_previewed_plan_id",
            plan_id=plan["plan_id"],
            mutations=[],
        )
    previous_state = load_installation_state(root)
    assert previous_state is not None
    try:
        validate_plan_preconditions(root, plan, previous_state)
    except ValueError as error:
        return result(
            state="ROLLED_BACK",
            reason_code=str(error),
            next_legal_action="preview_and_approve_a_fresh_update_plan",
            final_version=plan["installed_version"],
            mutations=[],
        )
    file_changes: list[dict[str, Any]] = []
    for item in plan["planned_files"]:
        if item["action"] in {"create", "modify"}:
            file_changes.append(
                {
                    "path": item["path"],
                    "action": "write",
                    "data": payload_bytes(
                        payload_root, item["path"], harness=plan["harness"]
                    ),
                    "mode": payload_mode(
                        payload_root, item["path"], harness=plan["harness"]
                    ),
                }
            )
        elif item["action"] == "delete":
            file_changes.append({"path": item["path"], "action": "delete"})

    if interrupt_after_staging:
        return result(
            state="ROLLED_BACK",
            reason_code="FACTORY_UPDATE_ABORTED",
            next_legal_action="preview_the_update_again",
            final_version=plan["installed_version"],
            mutations=[],
        )

    transaction_path = transaction_receipt_path(plan["plan_id"])
    try:
        if safe_target(root, transaction_path).exists():
            raise ValueError("FACTORY_TRANSACTION_RECEIPT_EXISTS")
        rollback_snapshots = capture_snapshots(
            root,
            [change["path"] for change in file_changes]
            + [INSTALLATION_STATE_PATH],
        )
        managed_files = managed_files_from_plan(
            root, payload_root, plan, previous_state=previous_state
        )
        transaction_receipt = {
            "schema_version": 1,
            **plan["change_plan"],
            "approval_state": "APPROVED",
            "post_digests": {
                entry["path"]: entry["expected_digest"] for entry in managed_files
            },
            "outcome": "APPLIED",
            "recovery_status": "AVAILABLE",
            "rollback_snapshots": rollback_snapshots,
        }
        next_state = {
            "schema_version": 1,
            "factory_version": plan["plugin_version"],
            "source_revision": f"factory-plugin@{plan['plugin_version']}",
            "managed_files": managed_files,
            "adapter_state": {
                "harness": plan["harness"],
                "claude_bridge": plan["harness"] == "claude",
            },
            "last_successful_transaction": {
                "transaction_id": plan["plan_id"],
                "operation": "update",
                "receipt": transaction_path,
                "outcome": "APPLIED",
            },
        }
        next_state_bytes = (json.dumps(next_state, indent=2) + "\n").encode()
        transaction_receipt["post_digests"][INSTALLATION_STATE_PATH] = (
            bytes_sha256(next_state_bytes)
        )
        changes = file_changes + [
            {
                "path": transaction_path,
                "action": "write",
                "data": (
                    json.dumps(transaction_receipt, indent=2, sort_keys=True) + "\n"
                ).encode(),
                "mode": 0o600,
            },
            {
                "path": INSTALLATION_STATE_PATH,
                "action": "write",
                "data": next_state_bytes,
                "mode": 0o644,
            },
        ]
        apply_changes(root, changes)
    except Exception as error:
        reason_code = (
            str(error)
            if isinstance(error, ValueError) and str(error).startswith("FACTORY_")
            else "FACTORY_UPDATE_ABORTED"
        )
        return result(
            state="ROLLED_BACK",
            reason_code=reason_code,
            next_legal_action="resolve_the_write_failure_and_preview_again",
            final_version=plan["installed_version"],
            blocker=f"{type(error).__name__}: {error}",
            mutations=[],
        )
    return result(
        state="APPLIED",
        reason_code="FACTORY_UPDATE_APPLIED",
        next_legal_action="run_factory_doctor_and_validation",
        installed_version=plan["plugin_version"],
        rollback_receipt=transaction_path,
        plan_id=plan["plan_id"],
        mutations=[change["path"] for change in changes],
    )


def apply_rollback(root: Path, *, approved: bool) -> dict[str, Any]:
    root = root.resolve()
    try:
        installation_state = load_installation_state(root)
        if installation_state is None:
            raise ValueError("FACTORY_ROLLBACK_UNAVAILABLE")
        transaction_path = installation_state["last_successful_transaction"].get(
            "receipt"
        )
        if not isinstance(transaction_path, str):
            raise ValueError("FACTORY_ROLLBACK_UNAVAILABLE")
        transaction_target = safe_target(root, transaction_path)
        transaction = json.loads(transaction_target.read_text(encoding="utf-8"))
        if transaction.get("operation") == "greenfield":
            return apply_greenfield_rollback(
                root,
                installation_state=installation_state,
                transaction=transaction,
                transaction_path=transaction_path,
                approved=approved,
            )
        if (
            transaction.get("operation") != "update"
            or transaction.get("target_version")
            != installation_state["factory_version"]
            or transaction.get("recovery_status") != "AVAILABLE"
        ):
            raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")
        if not approved:
            return result(
                state="BLOCKED",
                reason_code="FACTORY_ROLLBACK_APPROVAL_REQUIRED",
                next_legal_action="explicitly_approve_rollback",
                installed_version=installation_state["factory_version"],
                target_version=transaction["source_version"],
                mutations=[],
            )
        snapshots = transaction["rollback_snapshots"]
        if not isinstance(snapshots, dict):
            raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")
        current = capture_snapshots(root, list(snapshots) + [transaction_path])
        try:
            restore_snapshots(root, snapshots)
            transaction["recovery_status"] = "ROLLED_BACK"
            transaction["recovery_outcome"] = "APPLIED"
            atomic_write(
                transaction_target,
                (json.dumps(transaction, indent=2, sort_keys=True) + "\n").encode(),
                0o600,
            )
        except Exception:
            restore_snapshots(root, current)
            raise
    except (KeyError, OSError, RuntimeError, json.JSONDecodeError, ValueError) as error:
        reason_code = (
            str(error)
            if str(error).startswith("FACTORY_")
            else "FACTORY_ROLLBACK_EVIDENCE_MISMATCH"
        )
        return result(
            state="BLOCKED",
            reason_code=reason_code,
            next_legal_action="repair_or_restore_the_factory_installation_manually",
            blocker=f"{type(error).__name__}: {error}",
            mutations=[],
        )
    return result(
        state="ROLLED_BACK",
        reason_code="FACTORY_ROLLBACK_APPLIED",
        next_legal_action="run_factory_doctor_and_validation",
        final_version=transaction["source_version"],
        mutations=sorted(snapshots) + [transaction_path],
    )


def _greenfield_allowed_paths(
    installation_state: dict[str, Any], transaction_path: str
) -> tuple[set[str], set[str]]:
    files = {
        entry["path"]
        for entry in installation_state["managed_files"]
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    files.update({INSTALLATION_STATE_PATH, transaction_path})
    directories: set[str] = set()
    for relative in files:
        parent = Path(relative).parent
        while parent != Path("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    return files, directories


def apply_greenfield_rollback(
    root: Path,
    *,
    installation_state: dict[str, Any],
    transaction: dict[str, Any],
    transaction_path: str,
    approved: bool,
) -> dict[str, Any]:
    bootstrap = transaction.get("bootstrap")
    if (
        transaction.get("target_version") != installation_state["factory_version"]
        or transaction.get("recovery_status") != "AVAILABLE"
        or not isinstance(bootstrap, dict)
        or not isinstance(bootstrap.get("root_created"), bool)
        or not isinstance(bootstrap.get("git_created"), bool)
    ):
        raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")
    if not approved:
        return result(
            state="BLOCKED",
            reason_code="FACTORY_ROLLBACK_APPROVAL_REQUIRED",
            next_legal_action="explicitly_approve_rollback",
            installed_version=installation_state["factory_version"],
            target_version=None,
            mutations=[],
        )

    git_path = root / ".git"
    if bootstrap["git_created"]:
        expected_git = bootstrap.get("git_post_init_digest")
        if (
            not isinstance(expected_git, str)
            or not git_path.exists()
            or git_state_digest(git_path) != expected_git
        ):
            return result(
                state="BLOCKED",
                reason_code="FACTORY_ROLLBACK_GIT_STATE_CHANGED",
                next_legal_action="preserve_user_git_state_and_recover_manually",
                mutations=[],
            )

    expected_digests = transaction.get("post_digests")
    if not isinstance(expected_digests, dict):
        raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")
    files, directories = _greenfield_allowed_paths(
        installation_state, transaction_path
    )
    for relative in files - {transaction_path}:
        target = safe_target(root, relative)
        expected = expected_digests.get(relative)
        if (
            not isinstance(expected, str)
            or not target.is_file()
            or file_sha256(target) != expected
        ):
            raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")

    if bootstrap["root_created"]:
        for path in root.rglob("*"):
            relative = path.relative_to(root)
            if relative.parts and relative.parts[0] == ".git":
                continue
            value = relative.as_posix()
            if path.is_file() and value in files:
                continue
            if path.is_dir() and value in directories:
                continue
            raise ValueError("FACTORY_ROLLBACK_EVIDENCE_MISMATCH")

    changes = [
        {"path": relative, "action": "delete"}
        for relative in sorted(
            files,
            key=lambda value: (len(Path(value).parts), value),
            reverse=True,
        )
    ]
    snapshots = apply_changes(root, changes)
    try:
        if bootstrap["git_created"]:
            if git_state_digest(git_path) != bootstrap["git_post_init_digest"]:
                raise ValueError("FACTORY_ROLLBACK_GIT_STATE_CHANGED")
            shutil.rmtree(git_path)
        if bootstrap["root_created"]:
            root.rmdir()
    except Exception:
        restore_snapshots(root, snapshots)
        raise
    return result(
        state="ROLLED_BACK",
        reason_code="FACTORY_ROLLBACK_APPLIED",
        next_legal_action="confirm_target_state_before_reinitializing",
        final_version=None,
        mutations=[
            *sorted(files),
            *([".git"] if bootstrap["git_created"] else []),
            *(["."] if bootstrap["root_created"] else []),
        ],
    )


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def concise(value: dict[str, Any]) -> str:
    lines = [
        f"Factory: {value['state']}",
        f"Reason: {value['reason_code']}",
    ]
    target = value.get("repository_root") or value.get("target")
    if target:
        lines.append(f"Target: {target}")
    if value.get("plan_id"):
        lines.append(f"Plan: {value['plan_id']}")
    mutations = value.get("mutations")
    if isinstance(mutations, list):
        lines.append(f"Changes: {len(mutations)}")
    else:
        lines.append("Changes: 0")
    lines.append(f"Next: {value['next_legal_action']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(prog="factory-plugin")
    parser.add_argument(
        "--root",
        type=Path,
        help="repository path; defaults to current directory for greenfield; Git root otherwise",
    )
    parser.add_argument("--json", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)
    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--harness", required=True, choices=sorted(SUPPORTED_HARNESSES))
    progress_parser = subparsers.add_parser("progress")
    progress_parser.add_argument("--run")
    for command in ("greenfield", "brownfield"):
        setup_parser = subparsers.add_parser(command)
        setup_parser.add_argument(
            "--harness", required=True, choices=sorted(SUPPORTED_HARNESSES)
        )
        setup_parser.add_argument("--apply", action="store_true")
        setup_parser.add_argument("--approve-plan")
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "--harness", required=True, choices=sorted(SUPPORTED_HARNESSES)
    )
    update_parser.add_argument("--apply", action="store_true")
    update_parser.add_argument("--approve-plan")
    rollback_parser = subparsers.add_parser("rollback")
    rollback_parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()

    try:
        if args.root:
            root = args.root.resolve()
        elif args.command == "greenfield":
            root = Path.cwd().resolve()
        else:
            root = resolve_git_root(Path.cwd())
        if args.command == "doctor":
            output = evaluate_doctor(root, harness=args.harness)
        elif args.command == "progress":
            output = evaluate_progress(root, run_id=args.run)
        elif args.command in {"greenfield", "brownfield"}:
            payload_root = Path(__file__).resolve().parent.parent / "payload"
            output = evaluate_setup_plan(
                root,
                mode=args.command,
                harness=args.harness,
                payload_root=payload_root,
            )
            if args.apply:
                output = apply_setup_plan(
                    root,
                    plan=output,
                    approved_plan_id=args.approve_plan,
                    payload_root=payload_root,
                )
        elif args.command == "update":
            payload_root = Path(__file__).resolve().parent.parent / "payload"
            output = evaluate_update_plan(
                root, harness=args.harness, payload_root=payload_root
            )
            if args.apply:
                output = apply_update_plan(
                    root,
                    plan=output,
                    approved_plan_id=args.approve_plan,
                    payload_root=payload_root,
                )
        else:
            output = apply_rollback(root, approved=args.approve)
    except ValueError as error:
        output = result(
            state="BLOCKED",
            reason_code=str(error),
            next_legal_action="invoke_from_a_supported_git_worktree",
            mutations=[],
        )
    if args.json:
        print_json(output)
    else:
        print(concise(output))
    return 2 if output["state"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
