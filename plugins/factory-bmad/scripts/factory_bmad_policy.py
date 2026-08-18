#!/usr/bin/env python3
"""Shared Factory/BMAD policy, activation, audit, and reconciliation logic."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


POLICY_VERSION = "1.0.0"
SUPPORTED_BMAD_VERSION = "6.10.0"
SUPPORTED_TEA_VERSION = "v1.21.1"

# Exact Core+BMM skill inventory from npm:bmad-method@6.10.0.
SUPPORTED_BMAD_SKILLS = frozenset({
    "bmad-advanced-elicitation",
    "bmad-agent-analyst",
    "bmad-agent-architect",
    "bmad-agent-dev",
    "bmad-agent-pm",
    "bmad-agent-tech-writer",
    "bmad-agent-ux-designer",
    "bmad-architecture",
    "bmad-brainstorming",
    "bmad-check-implementation-readiness",
    "bmad-checkpoint-preview",
    "bmad-code-review",
    "bmad-correct-course",
    "bmad-create-architecture",
    "bmad-create-epics-and-stories",
    "bmad-create-prd",
    "bmad-create-story",
    "bmad-customize",
    "bmad-dev-auto",
    "bmad-dev-story",
    "bmad-document-project",
    "bmad-domain-research",
    "bmad-edit-prd",
    "bmad-editorial-review-prose",
    "bmad-editorial-review-structure",
    "bmad-forge-idea",
    "bmad-generate-project-context",
    "bmad-help",
    "bmad-index-docs",
    "bmad-market-research",
    "bmad-party-mode",
    "bmad-prd",
    "bmad-prfaq",
    "bmad-product-brief",
    "bmad-qa-generate-e2e-tests",
    "bmad-quick-dev",
    "bmad-retrospective",
    "bmad-review-adversarial-general",
    "bmad-review-edge-case-hunter",
    "bmad-shard-doc",
    "bmad-spec",
    "bmad-sprint-planning",
    "bmad-sprint-status",
    "bmad-technical-research",
    "bmad-ux",
    "bmad-validate-prd",
})

SUPPORTED_TEA_SKILLS = frozenset({
    "bmad-tea",
    "bmad-teach-me-testing",
    "bmad-testarch-atdd",
    "bmad-testarch-automate",
    "bmad-testarch-ci",
    "bmad-testarch-framework",
    "bmad-testarch-nfr",
    "bmad-testarch-test-design",
    "bmad-testarch-test-review",
    "bmad-testarch-trace",
})

ALLOWED_UPSTREAM_WORKFLOWS = frozenset({
    "bmad-brainstorming",
    "bmad-create-prd",
    "bmad-document-project",
    "bmad-domain-research",
    "bmad-edit-prd",
    "bmad-forge-idea",
    "bmad-help",
    "bmad-market-research",
    "bmad-prd",
    "bmad-prfaq",
    "bmad-product-brief",
    "bmad-technical-research",
    "bmad-ux",
    "bmad-validate-prd",
})

BMAD_MANIFESTS = (
    Path("_bmad/_config/manifest.yaml"),
    Path("_bmad/_config/manifest.yml"),
    Path("_bmad/manifest.yaml"),
)
BMAD_NAME_RE = re.compile(r"bmad-[a-z0-9][a-z0-9-]*")
UPSTREAM_PATH_TERMS = (
    "brainstorm", "product-brief", "prfaq", "research", "prd", "ux", "document-project",
)
DOWNSTREAM_PATH_TERMS = (
    "architecture", "epic", "story", "sprint", "implementation", "code-review",
    "correct-course", "retrospective", "dev-auto", "dev-story", "quick-dev", "spec",
)

FACTORY_BOUND_UPSTREAM_CONTEXT = (
    "Factory-bound BMAD session: remain at product-discovery level. "
    "Do not invoke or recommend prohibited BMAD workflows, including party mode, "
    "advanced elicitation, architecture, specs, epics or stories, sprint planning, "
    "implementation, QA automation, or code review. Treat all BMAD output as draft "
    "evidence; Factory remains the sole downstream SDLC authority."
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def result(state: str, code: str, action: str, **details: Any) -> dict[str, Any]:
    return {
        "state": state,
        "reason_code": code,
        **details,
        "next_legal_action": action,
        "mutations": [],
    }


def canonical_bmad_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    token = value.strip().split(maxsplit=1)[0] if value.strip() else ""
    token = token.removeprefix("/").lower()
    if ":" in token:
        token = token.rsplit(":", 1)[1]
    return token if BMAD_NAME_RE.fullmatch(token) else None


def contains_bmad_marker(value: object) -> bool:
    try:
        return "bmad-" in json.dumps(value, sort_keys=True).lower()
    except (TypeError, ValueError):
        return False


def policy_classify(value: object) -> dict[str, Any]:
    name = canonical_bmad_name(value)
    if name is None:
        return {
            "name": None,
            "classification": "UNRELATED_OR_INVALID",
            "allowed": False,
            "reason_code": "FACTORY_BMAD_HOOK_INPUT_INVALID",
            "policy_version": POLICY_VERSION,
        }
    if name in ALLOWED_UPSTREAM_WORKFLOWS:
        classification = "ALLOWED_UPSTREAM"
        allowed = True
        code = "FACTORY_BMAD_WORKFLOW_ALLOWED"
    elif name in SUPPORTED_TEA_SKILLS:
        classification = "OPTIONAL_STAGE_F_EVIDENCE_ONLY"
        allowed = False
        code = "FACTORY_BMAD_WORKFLOW_PROHIBITED"
    elif name in SUPPORTED_BMAD_SKILLS:
        classification = "PROHIBITED_DOWNSTREAM"
        allowed = False
        code = "FACTORY_BMAD_WORKFLOW_PROHIBITED"
    else:
        classification = "UNRECOGNIZED_BLOCKING"
        allowed = False
        code = "FACTORY_BMAD_WORKFLOW_PROHIBITED"
    return {
        "name": name,
        "classification": classification,
        "allowed": allowed,
        "reason_code": code,
        "policy_version": POLICY_VERSION,
    }


def git_root(root: Path) -> Path | None:
    cursor = root.resolve()
    for candidate in (cursor, *cursor.parents):
        marker = candidate / ".git"
        if marker.is_dir() or marker.is_file():
            return candidate
    return None


def _factory_present(root: Path) -> bool:
    return (root / "docs/Factory/ARCHITECTURE.md").is_file() and (root / "scripts/factoryctl").is_file()


def _bmad_marker_present(root: Path) -> bool:
    if (root / "_bmad").exists() or (root / "_bmad-output").exists():
        return True
    for directory in (root / ".claude/skills", root / ".claude/commands"):
        if directory.is_dir() and any("bmad-" in child.name.lower() for child in directory.iterdir()):
            return True
    return False


def _manifest_path(root: Path) -> tuple[Path | None, bool]:
    found = [root / relative for relative in BMAD_MANIFESTS if (root / relative).is_file()]
    return (found[0] if len(found) == 1 else None, len(found) > 1)


def enforcement_activation(root: Path) -> dict[str, Any]:
    repository = git_root(root)
    if repository is None:
        return {"active": False, "reason_code": "FACTORY_BMAD_ENFORCEMENT_INACTIVE_NO_GIT"}
    if not _factory_present(repository):
        return {"active": False, "reason_code": "FACTORY_BMAD_ENFORCEMENT_INACTIVE_NO_FACTORY"}
    if not _bmad_marker_present(repository):
        return {"active": False, "reason_code": "FACTORY_BMAD_ENFORCEMENT_INACTIVE_NO_BMAD"}
    manifest, ambiguous = _manifest_path(repository)
    if ambiguous or manifest is None:
        return {"active": True, "reason_code": "FACTORY_BMAD_ENFORCEMENT_ACTIVE_PARTIAL"}
    return {"active": True, "reason_code": "FACTORY_BMAD_ENFORCEMENT_ACTIVE"}


def _deny_message(code: str, name: str | None) -> str:
    subject = name or "malformed BMAD invocation"
    return (
        f"{code}: {subject} is not permitted for Factory-bound work. "
        "Doctor was not run; /factory-bmad:doctor is only the suggested next action."
    )


def _companion_command(value: object) -> bool:
    if not isinstance(value, str):
        return False
    token = value.strip().split(maxsplit=1)[0].removeprefix("/").lower()
    return bool(re.fullmatch(r"factory-bmad:[a-z0-9][a-z0-9-]*", token))


def _upstream_context(event: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": FACTORY_BOUND_UPSTREAM_CONTEXT,
        }
    }


def _skill_name(payload: dict[str, Any]) -> tuple[str | None, bool]:
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None, contains_bmad_marker(tool_input)
    values = [tool_input[key] for key in ("skill", "skill_name", "name") if key in tool_input]
    names = {canonical_bmad_name(value) for value in values if canonical_bmad_name(value) is not None}
    malformed = contains_bmad_marker(tool_input) and (len(names) != 1 or len(values) != 1)
    return (next(iter(names)) if len(names) == 1 else None), malformed


def hook_decision(root: Path, payload: dict[str, Any]) -> dict[str, Any] | None:
    event = payload.get("hook_event_name")
    raw_name: object | None = None
    malformed = False
    if event == "UserPromptExpansion":
        raw_name = payload.get("command_name")
        if _companion_command(raw_name):
            return None
        malformed = contains_bmad_marker(payload) and canonical_bmad_name(raw_name) is None
    elif event == "PreToolUse" and payload.get("tool_name") == "Skill":
        raw_name, malformed = _skill_name(payload)
    else:
        return None

    name = canonical_bmad_name(raw_name)
    if name is None and not malformed:
        return None
    activation = enforcement_activation(root)
    if not activation["active"]:
        return None
    if malformed:
        code = "FACTORY_BMAD_HOOK_INPUT_INVALID"
    elif activation["reason_code"] == "FACTORY_BMAD_ENFORCEMENT_ACTIVE_PARTIAL":
        code = "FACTORY_BMAD_ENFORCEMENT_STATE_INVALID"
    else:
        verdict = policy_classify(name)
        if verdict["allowed"]:
            return _upstream_context(event)
        code = verdict["reason_code"]
    reason = _deny_message(code, name)
    if event == "UserPromptExpansion":
        return {"decision": "block", "reason": reason}
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def parse_manifest(path: Path) -> tuple[str | None, dict[str, str]]:
    installation_version: str | None = None
    modules: dict[str, str] = {}
    current: str | None = None
    section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        top = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if top:
            section = top.group(1)
        if section == "installation" and installation_version is None:
            match = re.match(r"\s+version:\s*['\"]?([^'\"#\s]+)", line)
            if match:
                installation_version = match.group(1)
        if section != "modules":
            continue
        name = re.match(r"\s*-\s+name:\s*['\"]?([^'\"#\s]+)", line)
        version = re.match(r"\s+version:\s*['\"]?([^'\"#\s]+)", line)
        if name:
            current = name.group(1)
            if current in modules:
                raise ValueError("duplicate module")
            modules[current] = "unknown"
        elif version and current:
            modules[current] = version.group(1)
    if not modules:
        raise ValueError("modules unreadable")
    return installation_version, modules


def _path_record(root: Path, path: Path, name: str, classification: str) -> dict[str, str]:
    if path.is_symlink():
        digest = digest_bytes(f"symlink:{os.readlink(path)}".encode())
    elif path.is_file():
        digest = digest_file(path)
    else:
        digest = digest_bytes(path.relative_to(root).as_posix().encode())
    return {
        "name": name,
        "path": path.relative_to(root).as_posix(),
        "sha256": digest,
        "classification": classification,
    }


def _named_capabilities(root: Path, directory: Path, kind: str) -> list[dict[str, str]]:
    if not directory.is_dir() or directory.is_symlink():
        return []
    records: list[dict[str, str]] = []
    candidates = sorted(directory.iterdir()) if kind == "skills" else sorted(directory.rglob("*"))
    for path in candidates:
        if path.is_symlink():
            if "bmad-" in path.relative_to(directory).as_posix().lower():
                records.append(_path_record(root, path, path.name.lower(), "UNRECOGNIZED_BLOCKING"))
            continue
        if path.is_dir() and kind != "skills":
            continue
        source_name = path.name if kind == "skills" else path.stem
        name = canonical_bmad_name(source_name)
        if name is None and "bmad-" not in path.relative_to(directory).as_posix().lower():
            continue
        if name is None:
            classification = "UNRECOGNIZED_BLOCKING"
            name = source_name.lower()
        elif name in SUPPORTED_TEA_SKILLS:
            classification = "OPTIONAL_STAGE_F_EVIDENCE_ONLY"
        else:
            classification = policy_classify(name)["classification"]
        evidence_path = path / "SKILL.md" if kind == "skills" and path.is_dir() else path
        records.append(_path_record(root, evidence_path, name, classification))
    return records


def capability_inventory(root: Path) -> dict[str, list[dict[str, str]]]:
    root = root.resolve()
    capabilities = {
        "skills": _named_capabilities(root, root / ".claude/skills", "skills"),
        "commands": _named_capabilities(root, root / ".claude/commands", "commands"),
        "agents": _named_capabilities(root, root / ".claude/agents", "agents"),
        "hooks": _named_capabilities(root, root / ".claude/hooks", "hooks"),
        "configuration": [],
    }
    manifest, _ = _manifest_path(root)
    if manifest is not None:
        capabilities["configuration"].append(_path_record(root, manifest, "bmad-manifest", "VERSION_EVIDENCE"))
    settings = root / ".claude/settings.json"
    if settings.is_file() and not settings.is_symlink():
        try:
            text = settings.read_text(encoding="utf-8") if settings.stat().st_size <= 1024 * 1024 else ""
        except (OSError, UnicodeError):
            text = ""
        if "bmad" in text.lower():
            capabilities["configuration"].append(_path_record(root, settings, "bmad-project-settings", "UNRECOGNIZED_BLOCKING"))
    return capabilities


def reconcile_brownfield(root: Path) -> dict[str, Any]:
    root = root.resolve()
    output = root / "_bmad-output"
    artifacts: list[dict[str, str]] = []
    if output.is_dir() and not output.is_symlink():
        for path in sorted(output.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            lowered = relative.lower()
            if any(term in lowered for term in DOWNSTREAM_PATH_TERMS):
                classification = "NON_BINDING_HISTORY"
            elif any(term in lowered for term in UPSTREAM_PATH_TERMS):
                classification = "UPSTREAM_REVIEW_CANDIDATE"
            else:
                classification = "REVIEW_REQUIRED"
            artifacts.append({"path": relative, "sha256": digest_file(path), "classification": classification})
    core = {
        "schema_version": 1,
        "policy_version": POLICY_VERSION,
        "authority": "FACTORY_ONLY",
        "brownfield_baseline": "EXISTING_CODE_PRESERVED",
        "artifacts": artifacts,
    }
    return {**core, "aggregate_sha256": digest_bytes(canonical(core))}


def capability_audit(root: Path, harness: str) -> dict[str, Any]:
    root = root.resolve()
    manifest, ambiguous = _manifest_path(root)
    capabilities = capability_inventory(root)
    reconciliation = reconcile_brownfield(root)
    base = {
        "harness": harness,
        "policy_version": POLICY_VERSION,
        "installation_version": None,
        "modules": {},
        "module_classifications": {},
        "capabilities": capabilities,
        "reconciliation": reconciliation,
        "uncovered_capabilities": [],
        "missing_capabilities": [],
    }
    if not _factory_present(root) or manifest is None or ambiguous:
        return result("BLOCKED", "FACTORY_BMAD_AUDIT_PREREQUISITES_MISSING", "run_factory_bmad_doctor", **base)
    try:
        installation_version, modules = parse_manifest(manifest)
    except (OSError, UnicodeError, ValueError):
        return result("BLOCKED", "FACTORY_BMAD_MANIFEST_UNREADABLE", "repair_bmad_manifest_with_human_review", **base)
    classifications: dict[str, str] = {}
    for name in sorted(modules):
        if name == "bmad-loop":
            classifications[name] = "PROHIBITED_BLOCKER"
        elif name == "tea":
            classifications[name] = "OPTIONAL_STAGE_F_EVIDENCE_ONLY"
        elif name in {"core", "bmm"}:
            classifications[name] = "POLICY_COVERED"
        else:
            classifications[name] = "UNRECOGNIZED_BLOCKING"
    base.update({"installation_version": installation_version, "modules": modules, "module_classifications": classifications})
    if "bmad-loop" in modules:
        return result("BLOCKED", "FACTORY_BMAD_LOOP_INSTALLED", "human_remove_or_isolate_bmad_loop_before_intake", **base)
    if any(value == "UNRECOGNIZED_BLOCKING" for value in classifications.values()):
        return result("BLOCKED", "FACTORY_BMAD_MODULE_REVIEW_REQUIRED", "classify_unrecognized_modules", **base)
    versions_ok = installation_version == SUPPORTED_BMAD_VERSION and all(
        modules.get(name) == SUPPORTED_BMAD_VERSION for name in ("core", "bmm")
    )
    tea_ok = "tea" not in modules or modules["tea"] == SUPPORTED_TEA_VERSION
    if not versions_ok or not tea_ok:
        return result("BLOCKED", "FACTORY_BMAD_VERSION_QUARANTINED", "review_supported_bmad_migration_without_mutation", **base)

    invocation = capabilities["skills"] + capabilities["commands"] + capabilities["agents"]
    observed = {item["name"] for item in invocation if item["name"] in SUPPORTED_BMAD_SKILLS}
    missing = sorted(SUPPORTED_BMAD_SKILLS - observed)
    if "tea" in modules:
        observed_tea = {item["name"] for item in invocation if item["name"] in SUPPORTED_TEA_SKILLS}
        missing.extend(sorted(SUPPORTED_TEA_SKILLS - observed_tea))
    uncovered = sorted(
        item["path"] for category in capabilities.values() for item in category
        if item["classification"] == "UNRECOGNIZED_BLOCKING"
    )
    base["missing_capabilities"] = missing
    base["uncovered_capabilities"] = uncovered
    coverage_core = {
        "policy_version": POLICY_VERSION,
        "installation_version": installation_version,
        "modules": modules,
        "capabilities": capabilities,
        "missing_capabilities": missing,
        "uncovered_capabilities": uncovered,
    }
    base["coverage_sha256"] = digest_bytes(canonical(coverage_core))
    if uncovered:
        return result("BLOCKED", "FACTORY_BMAD_CAPABILITY_UNRECOGNIZED", "review_or_remove_unrecognized_bmad_capabilities", **base)
    if missing:
        return result("BLOCKED", "FACTORY_BMAD_CAPABILITY_INCOMPLETE", "repair_or_reinstall_supported_bmad_with_human_approval", **base)
    return result("READY", "FACTORY_BMAD_POLICY_OK", "preview_or_verify_project_intake", **base)


def policy_lint(root: Path, harness: str) -> dict[str, Any]:
    return capability_audit(root, harness)
