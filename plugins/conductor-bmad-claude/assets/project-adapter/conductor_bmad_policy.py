#!/usr/bin/env python3
"""Shared Factory/BMAD policy, activation, audit, and reconciliation logic."""

from __future__ import annotations

import hashlib
import csv
import json
import os
import re
from pathlib import Path
from typing import Any


POLICY_VERSION = "2.0.0"
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

DISCOVERY_AUTHORING_WORKFLOWS = frozenset({
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
    "bmad-validate-prd",
})

SOLUTION_CONTEXT_AUTHORING_WORKFLOWS = frozenset({
    "bmad-architecture",
    "bmad-spec",
    "bmad-ux",
})

# Lane model (policy 2.0.0). Policy is expressed by responsibility, not per workflow.
# The authoritative contract is docs/adapters/bmad/templates/lane_policy.template.json;
# tests assert these sets equal it. Every known 6.10.0 skill has exactly one lane.
PERSONA_AGENT_WORKFLOWS = frozenset({
    "bmad-agent-analyst",
    "bmad-agent-pm",
    "bmad-agent-ux-designer",
    "bmad-agent-architect",
    "bmad-agent-tech-writer",
})

HELPER_WORKFLOWS = frozenset({
    "bmad-review-adversarial-general",
    "bmad-review-edge-case-hunter",
    "bmad-editorial-review-prose",
    "bmad-editorial-review-structure",
    "bmad-advanced-elicitation",
    "bmad-party-mode",
    "bmad-shard-doc",
    "bmad-index-docs",
})

EVIDENCE_ONLY_WORKFLOWS = frozenset({
    "bmad-testarch-test-design",
    "bmad-testarch-nfr",
    "bmad-testarch-trace",
    "bmad-testarch-test-review",
    "bmad-teach-me-testing",
})

NEUTRAL_TOOLING_WORKFLOWS = frozenset({
    "bmad-customize",
    "bmad-checkpoint-preview",
    "bmad-project-settings",
    "bmad-manifest",
})

DELIVERY_WORKFLOWS = frozenset({
    "bmad-create-epics-and-stories",
    "bmad-create-story",
    "bmad-dev-story",
    "bmad-dev-auto",
    "bmad-quick-dev",
    "bmad-sprint-planning",
    "bmad-sprint-status",
    "bmad-code-review",
    "bmad-correct-course",
    "bmad-check-implementation-readiness",
    "bmad-retrospective",
    "bmad-qa-generate-e2e-tests",
    "bmad-testarch-automate",
    "bmad-testarch-ci",
    "bmad-testarch-atdd",
    "bmad-testarch-framework",
    "bmad-generate-project-context",
    "bmad-create-architecture",
    "bmad-agent-dev",
    "bmad-tea",
    "bmad-loop",
})

PRODUCT_CONTEXT_WORKFLOWS = DISCOVERY_AUTHORING_WORKFLOWS | SOLUTION_CONTEXT_AUTHORING_WORKFLOWS | PERSONA_AGENT_WORKFLOWS
PRODUCT_CONTEXT_WRITE_ROOTS = ("_bmad-output",)
UNSAFE_LAYOUT_BLOCKS = frozenset({"intake", "promote", "solution_context_authoring"})
# Workflows whose output may be promoted to an immutable snapshot.
ALLOWED_UPSTREAM_WORKFLOWS = DISCOVERY_AUTHORING_WORKFLOWS | SOLUTION_CONTEXT_AUTHORING_WORKFLOWS | EVIDENCE_ONLY_WORKFLOWS

PROJECT_CONFIG_PATH = Path("docs/Conductor/PROJECT_CONFIG.json")
DEFAULT_BMAD_ROOT = Path("_bmad")


def active_bmad_root(root: Path) -> Path:
    """Repo-relative active BMAD root: PROJECT_CONFIG.json adapters.bmad.declared_root, else `_bmad`.

    Invalid declarations (absolute, traversal, under docs/, not ending in _bmad) fall back to the
    default so the layout assessment reports the resulting mismatch rather than crashing.
    """
    config_path = root / PROJECT_CONFIG_PATH
    if not config_path.is_file() or config_path.is_symlink():
        return DEFAULT_BMAD_ROOT
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        declared = config.get("adapters", {}).get("bmad", {}).get("declared_root")
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
        return DEFAULT_BMAD_ROOT
    if not isinstance(declared, str) or not declared:
        return DEFAULT_BMAD_ROOT
    candidate = Path(declared)
    if candidate.is_absolute() or ".." in candidate.parts or candidate.parts[0] == "docs" or candidate.name != "_bmad":
        return DEFAULT_BMAD_ROOT
    return candidate

# These receipts pin only the BMAD 6.10.0 capability bytes reviewed in MS-01.
# Future versions or changed customization must fail closed and be requalified.
SOLUTION_CONTEXT_CAPABILITY_PROFILES = {
    "bmad-architecture": {
        "logical_path": "bmm/3-solutioning/bmad-architecture/SKILL.md",
        "skill_sha256": "a56c7a0abc45e1dba719ae5e66b7169a1098b403e7fd69b30c19f16c12cddc6a",
        "customize_sha256": "137b418e1bb940411a6e77460a7c74af66a6ad732edcc7c7363746995b89e65d",
    },
    "bmad-spec": {
        "logical_path": "core/bmad-spec/SKILL.md",
        "skill_sha256": "a2baaf6b6bf000403a3b309b3dae48d328ece922e726541924585afbaf131b16",
        "customize_sha256": "b0181ba5d4038feb779a7a082a265df753220f868b66b5adb0fb2ed18401c763",
    },
    "bmad-ux": {
        "logical_path": "bmm/2-plan-workflows/bmad-ux/SKILL.md",
        "skill_sha256": "250d2794f2b8e316bb1ba4666f0728970afd8a5d2707ac1cceac6c21e63730b6",
        "customize_sha256": "c6f94676004a24eed7ff1d546d5b7e7b3889b84d9bab6bbb56bc297d6eabaeb8",
    },
}

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
LEGACY_EVIDENCE_ROOT = Path("docs/adapters/bmad/legacy-evidence")
LAYOUT_SCAN_IGNORES = frozenset({
    ".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__",
})
LINK_SCAN_SUFFIXES = frozenset({
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py", ".sh",
    ".js", ".jsx", ".ts", ".tsx",
})
MAX_LINK_SCAN_BYTES = 1024 * 1024

CONDUCTOR_BOUND_UPSTREAM_CONTEXT = (
    "Conductor-bound BMAD session, product-context lane: research, brief, PRD, and their helpers "
    "(review, editorial review, advanced elicitation, party mode, sharding, indexing) are permitted and "
    "may nest freely. Write only beneath _bmad-output. Do not invoke or recommend prohibited BMAD workflows: "
    "the delivery lane (epics or stories, sprint planning or status, implementation, quick-dev, loop, "
    "code review, QA automation, CI) is closed for Conductor-bound work. Treat all BMAD output as draft "
    "evidence; Conductor remains the sole downstream SDLC authority."
)

CONDUCTOR_BOUND_SOLUTION_CONTEXT = (
    "Conductor-bound BMAD solution-context session: produce mutable candidate authoring only beneath "
    "_bmad-output. Do not use external or design handoffs or activation/completion callbacks; product-context "
    "helpers may nest, delivery-lane skills may not. Architecture, UX, and specs remain proposed "
    "SOLUTION_CONTEXT / EVIDENCE_ONLY; BMAD labels such as canonical, binding, final, implementation-ready, "
    "or release approved have no Conductor authority. Conductor independently hardens intent and scope, plans "
    "implementation and verification, and requires exact-pack human Go before execution. This invocation gate "
    "is not a filesystem sandbox; stop on any write outside the BMAD draft workspace."
)

CONDUCTOR_LAYOUT_WARNING = (
    " LAYOUT WARNING ({layout_reason}): the BMAD installation layout is not canonical, so intake, promotion, "
    "and solution-context authoring are blocked until a human resolves it; discovery and helpers continue."
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
            "reason_code": "CONDUCTOR_BMAD_HOOK_INPUT_INVALID",
            "policy_version": POLICY_VERSION,
        }
    allowed = True
    code = "CONDUCTOR_BMAD_WORKFLOW_ALLOWED"
    if name in DISCOVERY_AUTHORING_WORKFLOWS:
        classification, lane = "ALLOWED_DISCOVERY_AUTHORING", "product_context"
    elif name in SOLUTION_CONTEXT_AUTHORING_WORKFLOWS:
        classification, lane = "ALLOWED_SOLUTION_CONTEXT_AUTHORING", "product_context"
    elif name in PERSONA_AGENT_WORKFLOWS:
        classification, lane = "ALLOWED_PRODUCT_CONTEXT_AGENT", "product_context"
    elif name in HELPER_WORKFLOWS:
        classification, lane = "ALLOWED_HELPER", "helper"
    elif name in EVIDENCE_ONLY_WORKFLOWS:
        classification, lane = "ALLOWED_EVIDENCE_ONLY", "evidence_only"
    elif name in NEUTRAL_TOOLING_WORKFLOWS:
        classification, lane = "NEUTRAL_TOOLING", "neutral"
    elif name in DELIVERY_WORKFLOWS:
        classification, lane, allowed, code = "PROHIBITED_DELIVERY", "delivery", False, "CONDUCTOR_BMAD_WORKFLOW_PROHIBITED"
    else:
        classification, lane, allowed, code = "UNRECOGNIZED_BLOCKING", "unknown", False, "CONDUCTOR_BMAD_WORKFLOW_PROHIBITED"
    return {
        "name": name,
        "classification": classification,
        "lane": lane,
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
    return (root / "docs/Conductor/ARCHITECTURE.md").is_file() and (root / "scripts/conductorctl").is_file()


def _path_is_within(relative: Path, prefix: Path) -> bool:
    return relative.parts[: len(prefix.parts)] == prefix.parts


def _manifest_candidates(installation_root: Path) -> list[Path]:
    return [
        installation_root / relative
        for relative in BMAD_MANIFESTS
        if (installation_root / relative).is_file() or (installation_root / relative).is_symlink()
    ]


def _nested_bmad_roots(root: Path, active: Path = DEFAULT_BMAD_ROOT) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for current_value, directory_names, _ in os.walk(root, topdown=True, followlinks=False):
        current = Path(current_value)
        kept: list[str] = []
        for name in sorted(directory_names):
            child = current / name
            relative = child.relative_to(root)
            if name in LAYOUT_SCAN_IGNORES or _path_is_within(relative, LEGACY_EVIDENCE_ROOT):
                continue
            if name != "_bmad":
                kept.append(name)
                continue
            if relative == active:
                continue
            installation_root = child.parent
            manifests = _manifest_candidates(installation_root)
            records.append({
                "installation_root": installation_root.relative_to(root).as_posix(),
                "active_root": relative.as_posix(),
                "manifest_paths": [path.relative_to(root).as_posix() for path in manifests],
                "symlink": child.is_symlink() or any(path.is_symlink() for path in manifests),
            })
        directory_names[:] = kept
    return sorted(records, key=lambda record: record["active_root"])


def assess_bmad_layout(root: Path) -> dict[str, Any]:
    root = root.resolve()
    active = active_bmad_root(root)
    canonical_root = root / active
    installation_root = canonical_root.parent
    canonical_marker = canonical_root.exists() or canonical_root.is_symlink()
    canonical_manifests = _manifest_candidates(installation_root)
    canonical_symlink = canonical_root.is_symlink() or any(path.is_symlink() for path in canonical_manifests)
    nested = _nested_bmad_roots(root, active)
    nested_markers = [
        record for record in non_canonical_bmad_layouts(root)
        if active == DEFAULT_BMAD_ROOT or not _path_is_within(active, Path(record["path"]))
    ]
    nested_installation_roots = {record["installation_root"] for record in nested}
    supplemental_markers = [record for record in nested_markers if record["path"] not in nested_installation_roots]
    archive = root / LEGACY_EVIDENCE_ROOT
    archive_present = archive.exists() or archive.is_symlink()
    nested_complete = [record for record in nested if len(record["manifest_paths"]) == 1 and not record["symlink"]]
    nested_partial = [record for record in nested if len(record["manifest_paths"]) != 1]
    root_output_only = (root / "_bmad-output").exists() and not canonical_marker and not nested

    if archive.is_symlink():
        state = "legacy_archive_symlink"
        reason = "CONDUCTOR_BMAD_LEGACY_ARCHIVE_SYMLINK"
        safe = False
    elif canonical_symlink or any(record["symlink"] for record in nested):
        state = "active_root_symlink"
        reason = "CONDUCTOR_BMAD_ACTIVE_ROOT_SYMLINK"
        safe = False
    elif (
        len(canonical_manifests) > 1
        or len(nested_complete) > 1
        or any(len(record["manifest_paths"]) > 1 for record in nested)
    ):
        state = "ambiguous"
        reason = "CONDUCTOR_BMAD_MANIFEST_AMBIGUOUS"
        safe = False
    elif canonical_marker and len(canonical_manifests) == 1 and (nested or supplemental_markers):
        state = "canonical_and_nested"
        reason = "CONDUCTOR_BMAD_MULTIPLE_ACTIVE_ROOTS"
        safe = False
    elif nested_partial or supplemental_markers or (canonical_marker and len(canonical_manifests) != 1) or root_output_only:
        state = "partial"
        reason = "CONDUCTOR_BMAD_PARTIAL_STATE"
        safe = False
    elif len(nested_complete) == 1:
        state = "nested_active"
        reason = "CONDUCTOR_BMAD_NESTED_LAYOUT"
        safe = False
    elif canonical_marker and len(canonical_manifests) == 1:
        state = "canonical_root"
        reason = "CONDUCTOR_BMAD_LAYOUT_CANONICAL"
        safe = True
    elif archive_present:
        state = "legacy_archive_outside_index"
        reason = "CONDUCTOR_BMAD_LEGACY_ARCHIVE_INERT"
        safe = True
    else:
        state = "absent"
        reason = "CONDUCTOR_BMAD_LAYOUT_ABSENT"
        safe = True

    return {
        "schema_version": 1,
        "state": state,
        "reason_code": reason,
        "safe": safe,
        "canonical_active_root": active.as_posix(),
        "declared_root": active.as_posix() if active != DEFAULT_BMAD_ROOT else None,
        "canonical_manifest": canonical_manifests[0].relative_to(root).as_posix() if len(canonical_manifests) == 1 else None,
        "canonical_manifest_paths": [path.relative_to(root).as_posix() for path in canonical_manifests],
        "nested_installations": nested,
        "nested_marker_layouts": nested_markers,
        "legacy_evidence_root": LEGACY_EVIDENCE_ROOT.as_posix(),
        "legacy_archive_present": archive_present,
        "active_marker_present": canonical_marker or bool(nested) or bool(supplemental_markers) or root_output_only,
    }


def _bmad_marker_present(root: Path) -> bool:
    if assess_bmad_layout(root)["active_marker_present"]:
        return True
    for directory in (root / ".claude/skills", root / ".claude/commands"):
        if directory.is_dir() and any("bmad-" in child.name.lower() for child in directory.iterdir()):
            return True
    return False


def _manifest_path(root: Path) -> tuple[Path | None, bool]:
    installation_root = (root / active_bmad_root(root)).parent
    found = [installation_root / relative for relative in BMAD_MANIFESTS if (installation_root / relative).is_file()]
    return (found[0] if len(found) == 1 else None, len(found) > 1)


def non_canonical_bmad_layouts(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    if not root.is_dir():
        return []
    layouts: list[dict[str, Any]] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.name in LAYOUT_SCAN_IGNORES or child.is_symlink() or not child.is_dir():
            continue
        prefix = child.relative_to(root).as_posix()
        manifests = [
            (child / relative).relative_to(root).as_posix()
            for relative in BMAD_MANIFESTS
            if (child / relative).is_file()
        ]
        markers: list[str] = []
        for marker in (Path("_bmad"), Path("_bmad-output")):
            if (child / marker).exists():
                markers.append((child / marker).relative_to(root).as_posix())
        for marker in (Path(".claude/skills"), Path(".claude/commands")):
            directory = child / marker
            if directory.is_dir() and any("bmad-" in item.name.lower() for item in directory.iterdir()):
                markers.append(directory.relative_to(root).as_posix())
        if manifests or markers:
            layouts.append({"path": prefix, "manifests": manifests, "markers": sorted(markers)})
    return layouts


def enforcement_activation(root: Path) -> dict[str, Any]:
    repository = git_root(root)
    if repository is None:
        return {"active": False, "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_INACTIVE_NO_GIT"}
    if not _factory_present(repository):
        return {"active": False, "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_INACTIVE_NO_FACTORY"}
    layout = assess_bmad_layout(repository)
    if not layout["active_marker_present"]:
        return {"active": False, "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_INACTIVE_NO_BMAD"}
    if not layout["safe"] or layout["state"] != "canonical_root":
        return {
            "active": True,
            "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE_UNSAFE_LAYOUT",
            "layout_reason_code": layout["reason_code"],
        }
    manifest, ambiguous = _manifest_path(repository)
    if ambiguous or manifest is None:
        return {"active": True, "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE_PARTIAL"}
    return {"active": True, "reason_code": "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE"}


def _deny_message(code: str, name: str | None, lane: str = "unknown", layout: dict[str, Any] | None = None) -> str:
    """Denial text carries the real cause: reason code, lane, layout finding, what is allowed, next step."""
    subject = name or "malformed BMAD invocation"
    layout_state = layout["state"] if layout else "unknown"
    layout_reason = layout["reason_code"] if layout else "CONDUCTOR_BMAD_LAYOUT_UNKNOWN"
    if code == "CONDUCTOR_BMAD_HOOK_INPUT_INVALID":
        allowed_here, next_step = "none", "repeat the invocation with exactly one BMAD skill name."
    elif lane == "delivery":
        allowed_here, next_step = "product-context lane and helpers", "route delivery work through Conductor (/conductor:run)."
    elif lane == "unknown":
        allowed_here, next_step = "product-context lane and helpers", "check the skill name; unknown BMAD workflows are denied by default."
    elif layout and not layout.get("safe", True):
        allowed_here, next_step = "discovery and helpers", "run /conductor-bmad:audit for the zero-write layout remediation preview."
    else:
        allowed_here, next_step = "discovery and helpers", "run /conductor-bmad:doctor to see the exact profile state."
    return (
        f"{code}: {subject} is {lane} for Conductor-bound work. "
        f"Layout: {layout_state} ({layout_reason}). "
        f"Allowed here: {allowed_here}. Next: {next_step}"
    )


def _factory_or_companion_command(value: object) -> bool:
    if not isinstance(value, str):
        return False
    token = value.strip().split(maxsplit=1)[0].removeprefix("/").lower()
    return bool(re.fullmatch(r"conductor(?:-bmad)?:[a-z0-9][a-z0-9-]*", token))


def _upstream_context(event: str, context: str = CONDUCTOR_BOUND_UPSTREAM_CONTEXT) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": context,
        }
    }


def _regular_file(root: Path, relative: Path) -> Path | None:
    cursor = root
    for part in relative.parts:
        cursor /= part
        if cursor.is_symlink():
            return None
    return cursor if cursor.is_file() else None


def _inert_override(path: Path) -> bool:
    try:
        return all(not line or line.startswith("#") for line in (item.strip() for item in path.read_text(encoding="utf-8").splitlines()))
    except (OSError, UnicodeError):
        return False


def solution_context_authorization(root: Path, name: str) -> dict[str, Any]:
    profile = SOLUTION_CONTEXT_CAPABILITY_PROFILES.get(name)
    if profile is None:
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_MISSING", "name": name}
    root = root.resolve()
    layout = assess_bmad_layout(root)
    if not layout["safe"] or layout["state"] != "canonical_root":
        return {
            "allowed": False,
            "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID",
            "layout_reason_code": layout["reason_code"],
            "name": name,
        }
    manifest, ambiguous = _manifest_path(root)
    if ambiguous or manifest is None or manifest.is_symlink():
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", "name": name}
    try:
        installation_version, modules = parse_manifest(manifest)
    except (OSError, UnicodeError, ValueError):
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", "name": name}
    if installation_version != SUPPORTED_BMAD_VERSION or any(modules.get(module) != SUPPORTED_BMAD_VERSION for module in ("core", "bmm")):
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_VERSION_MISMATCH", "name": name}

    active = active_bmad_root(root)
    skill_root = Path(".claude/skills") / name
    skill = _regular_file(root, skill_root / "SKILL.md")
    customize = _regular_file(root, skill_root / "customize.toml")
    files_manifest = _regular_file(root, active / "_config/files-manifest.csv")
    team_override = _regular_file(root, active / "custom/config.toml")
    user_override = _regular_file(root, active / "custom/config.user.toml")
    if None in {skill, customize, files_manifest, team_override, user_override}:
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", "name": name}
    if digest_file(skill) != profile["skill_sha256"] or digest_file(customize) != profile["customize_sha256"]:
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_DIGEST_MISMATCH", "name": name}
    try:
        with files_manifest.open(newline="", encoding="utf-8") as stream:
            matches = [row for row in csv.DictReader(stream) if row.get("path") == profile["logical_path"]]
    except (OSError, UnicodeError, csv.Error):
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", "name": name}
    if len(matches) != 1 or matches[0].get("hash") != profile["skill_sha256"]:
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_MANIFEST_MISMATCH", "name": name}
    if not _inert_override(team_override) or not _inert_override(user_override):
        return {"allowed": False, "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE", "name": name}
    return {
        "allowed": True,
        "reason_code": "CONDUCTOR_BMAD_SOLUTION_PROFILE_ALLOWED",
        "name": name,
        "policy_version": POLICY_VERSION,
        "bmad_version": SUPPORTED_BMAD_VERSION,
        "skill_sha256": profile["skill_sha256"],
        "customize_sha256": profile["customize_sha256"],
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
        if _factory_or_companion_command(raw_name):
            return None
        malformed = contains_bmad_marker(raw_name) and canonical_bmad_name(raw_name) is None
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
    repository = git_root(root) or root
    layout = assess_bmad_layout(repository)
    unsafe = activation["reason_code"] in {
        "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE_PARTIAL",
        "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE_UNSAFE_LAYOUT",
    }
    lane = "unknown"
    if malformed:
        code = "CONDUCTOR_BMAD_HOOK_INPUT_INVALID"
    else:
        # The invoked skill decides, never its parent: same-lane nesting is permitted by construction.
        verdict = policy_classify(name)
        lane = verdict["lane"]
        if verdict["allowed"]:
            if verdict["classification"] == "NEUTRAL_TOOLING":
                return None
            if name in SOLUTION_CONTEXT_AUTHORING_WORKFLOWS:
                # Authority-bearing action: unsafe layouts and profile drift fail closed here.
                authorization = solution_context_authorization(root, name)
                if authorization["allowed"]:
                    return _upstream_context(event, CONDUCTOR_BOUND_SOLUTION_CONTEXT)
                code = authorization["reason_code"]
            else:
                context = CONDUCTOR_BOUND_UPSTREAM_CONTEXT
                if unsafe:
                    context += CONDUCTOR_LAYOUT_WARNING.format(layout_reason=layout["reason_code"])
                return _upstream_context(event, context)
        else:
            code = verdict["reason_code"]
    reason = _deny_message(code, name, lane, layout)
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


def classify_modules(modules: dict[str, str]) -> dict[str, str]:
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
    return classifications


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
        else:
            classification = policy_classify(name)["classification"]
        evidence_path = path / "SKILL.md" if kind == "skills" and path.is_dir() else path
        records.append(_path_record(root, evidence_path, name, classification))
    return records


def capability_inventory_for(root: Path, install_root: Path) -> dict[str, list[dict[str, str]]]:
    root = root.resolve()
    install_root = install_root.resolve()
    capabilities = {
        "skills": _named_capabilities(root, install_root / ".claude/skills", "skills"),
        "commands": _named_capabilities(root, install_root / ".claude/commands", "commands"),
        "agents": _named_capabilities(root, install_root / ".claude/agents", "agents"),
        "hooks": _named_capabilities(root, install_root / ".claude/hooks", "hooks"),
        "configuration": [],
    }
    manifest, _ = _manifest_path(install_root)
    if manifest is not None:
        capabilities["configuration"].append(_path_record(root, manifest, "bmad-manifest", "VERSION_EVIDENCE"))
    settings = install_root / ".claude/settings.json"
    if settings.is_file() and not settings.is_symlink():
        try:
            text = settings.read_text(encoding="utf-8") if settings.stat().st_size <= 1024 * 1024 else ""
        except (OSError, UnicodeError):
            text = ""
        if "bmad" in text.lower():
            capabilities["configuration"].append(_path_record(root, settings, "bmad-project-settings", "UNRECOGNIZED_BLOCKING"))
    return capabilities


def capability_inventory(root: Path) -> dict[str, list[dict[str, str]]]:
    root = root.resolve()
    return capability_inventory_for(root, root)


def non_canonical_bmad_evidence(root: Path) -> list[dict[str, Any]]:
    root = root.resolve()
    evidence: list[dict[str, Any]] = []
    for layout in non_canonical_bmad_layouts(root):
        install_root = root / layout["path"]
        entry: dict[str, Any] = {
            **layout,
            "installation_version": None,
            "modules": {},
            "module_classifications": {},
            "capabilities": capability_inventory_for(root, install_root),
        }
        if len(layout["manifests"]) == 1:
            try:
                installation_version, modules = parse_manifest(root / layout["manifests"][0])
            except (OSError, UnicodeError, ValueError):
                entry["manifest_status"] = "UNREADABLE"
            else:
                entry["installation_version"] = installation_version
                entry["modules"] = modules
                entry["module_classifications"] = classify_modules(modules)
        elif len(layout["manifests"]) > 1:
            entry["manifest_status"] = "AMBIGUOUS"
        else:
            entry["manifest_status"] = "MISSING"
        evidence.append(entry)
    return evidence


def _inventory_tree(root: Path, directory: Path) -> list[dict[str, str]]:
    if directory.is_symlink():
        relative = directory.relative_to(root).as_posix()
        return [{
            "path": relative,
            "kind": "symlink",
            "sha256": digest_bytes(f"symlink:{os.readlink(directory)}".encode()),
        }]
    if not directory.is_dir():
        return []
    records: list[dict[str, str]] = []
    for current_value, directory_names, file_names in os.walk(directory, topdown=True, followlinks=False):
        current = Path(current_value)
        kept: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                records.append({
                    "path": relative,
                    "kind": "symlink",
                    "sha256": digest_bytes(f"symlink:{os.readlink(path)}".encode()),
                })
            else:
                records.append({
                    "path": relative,
                    "kind": "directory",
                    "sha256": digest_bytes(b"directory"),
                })
                kept.append(name)
        directory_names[:] = kept
        for name in sorted(file_names):
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                records.append({
                    "path": relative,
                    "kind": "symlink",
                    "sha256": digest_bytes(f"symlink:{os.readlink(path)}".encode()),
                })
            elif path.is_file():
                records.append({"path": relative, "kind": "file", "sha256": digest_file(path)})
    return sorted(records, key=lambda record: record["path"])


def _link_impacts(root: Path, source_relative: Path) -> list[dict[str, Any]]:
    source_value = source_relative.as_posix()
    reference_pattern = re.compile(
        rf"(?<![A-Za-z0-9_.-])/?{re.escape(source_value)}(?:/|(?=$|[\s)`'\"#]))"
    )
    impacts: list[dict[str, Any]] = []
    for current_value, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(current_value)
        kept: list[str] = []
        for name in sorted(directory_names):
            child = current / name
            relative = child.relative_to(root)
            if (
                name in LAYOUT_SCAN_IGNORES
                or _path_is_within(relative, source_relative)
                or _path_is_within(relative, LEGACY_EVIDENCE_ROOT)
                or child.is_symlink()
            ):
                continue
            kept.append(name)
        directory_names[:] = kept
        for name in sorted(file_names):
            path = current / name
            relative = path.relative_to(root)
            if path.is_symlink() or path.suffix.lower() not in LINK_SCAN_SUFFIXES:
                continue
            try:
                if path.stat().st_size > MAX_LINK_SCAN_BYTES:
                    continue
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            source_sha = digest_file(path)
            for line_number, line in enumerate(text.splitlines(), start=1):
                if reference_pattern.search(line):
                    impacts.append({
                        "path": relative.as_posix(),
                        "line": line_number,
                        "source_sha256": source_sha,
                        "reference_sha256": digest_bytes(line.encode()),
                    })
    return impacts


def _remediation_previews(root: Path, layout: dict[str, Any]) -> list[dict[str, Any]]:
    previews: list[dict[str, Any]] = []
    installation_roots = sorted({record["installation_root"] for record in layout["nested_installations"]})
    for source_value in installation_roots:
        source_relative = Path(source_value)
        source = root / source_relative
        target_relative = LEGACY_EVIDENCE_ROOT / source_relative
        target = root / target_relative
        core = {
            "schema_version": 1,
            "operation": "RELOCATION_PREVIEW_ONLY",
            "authority": "INERT_EVIDENCE_ONLY",
            "source": source_relative.as_posix(),
            "target": target_relative.as_posix(),
            "target_collision": target.exists() or target.is_symlink(),
            "source_inventory": _inventory_tree(root, source),
            "link_impacts": _link_impacts(root, source_relative),
            "mutations": [],
        }
        previews.append({**core, "plan_sha256": digest_bytes(canonical(core))})
    return previews


def reconcile_brownfield(root: Path) -> dict[str, Any]:
    root = root.resolve()
    layout = assess_bmad_layout(root)
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
        "authority": "CONDUCTOR_ONLY",
        "brownfield_baseline": "EXISTING_CODE_PRESERVED",
        "layout": layout,
        "legacy_archive_inventory": _inventory_tree(root, root / LEGACY_EVIDENCE_ROOT),
        "remediation_previews": _remediation_previews(root, layout),
        "artifacts": artifacts,
    }
    return {**core, "aggregate_sha256": digest_bytes(canonical(core))}


def capability_audit(root: Path, harness: str) -> dict[str, Any]:
    root = root.resolve()
    layout = assess_bmad_layout(root)
    manifest, ambiguous = _manifest_path(root)
    capabilities = capability_inventory(root)
    reconciliation = reconcile_brownfield(root)
    non_canonical = non_canonical_bmad_evidence(root)
    base = {
        "harness": harness,
        "policy_version": POLICY_VERSION,
        "installation_version": None,
        "modules": {},
        "module_classifications": {},
        "capabilities": capabilities,
        "layout": layout,
        "layout_reason_code": layout["reason_code"],
        "reconciliation": reconciliation,
        "non_canonical_bmad_layouts": non_canonical,
        "uncovered_capabilities": [],
        "missing_capabilities": [],
    }
    if not layout["safe"]:
        return result(
            "BLOCKED",
            "CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT",
            "review_zero_write_remediation_preview",
            **base,
        )
    if not _factory_present(root) or layout["state"] != "canonical_root" or manifest is None or ambiguous:
        return result("BLOCKED", "CONDUCTOR_BMAD_AUDIT_PREREQUISITES_MISSING", "run_factory_bmad_doctor", **base)
    try:
        installation_version, modules = parse_manifest(manifest)
    except (OSError, UnicodeError, ValueError):
        return result("BLOCKED", "CONDUCTOR_BMAD_MANIFEST_UNREADABLE", "repair_bmad_manifest_with_human_review", **base)
    classifications = classify_modules(modules)
    base.update({"installation_version": installation_version, "modules": modules, "module_classifications": classifications})
    if "bmad-loop" in modules:
        return result("BLOCKED", "CONDUCTOR_BMAD_LOOP_INSTALLED", "human_remove_or_isolate_bmad_loop_before_intake", **base)
    if any(value == "UNRECOGNIZED_BLOCKING" for value in classifications.values()):
        return result("BLOCKED", "CONDUCTOR_BMAD_MODULE_REVIEW_REQUIRED", "classify_unrecognized_modules", **base)
    versions_ok = installation_version == SUPPORTED_BMAD_VERSION and all(
        modules.get(name) == SUPPORTED_BMAD_VERSION for name in ("core", "bmm")
    )
    tea_ok = "tea" not in modules or modules["tea"] == SUPPORTED_TEA_VERSION
    if not versions_ok or not tea_ok:
        return result("BLOCKED", "CONDUCTOR_BMAD_VERSION_QUARANTINED", "review_supported_bmad_migration_without_mutation", **base)

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
        "layout": layout,
        "capabilities": capabilities,
        "missing_capabilities": missing,
        "uncovered_capabilities": uncovered,
    }
    base["coverage_sha256"] = digest_bytes(canonical(coverage_core))
    if uncovered:
        return result("BLOCKED", "CONDUCTOR_BMAD_CAPABILITY_UNRECOGNIZED", "review_or_remove_unrecognized_bmad_capabilities", **base)
    if missing:
        return result("BLOCKED", "CONDUCTOR_BMAD_CAPABILITY_INCOMPLETE", "repair_or_reinstall_supported_bmad_with_human_approval", **base)
    return result("READY", "CONDUCTOR_BMAD_POLICY_OK", "preview_or_verify_project_intake", **base)


def policy_lint(root: Path, harness: str) -> dict[str, Any]:
    return capability_audit(root, harness)
