"""Conductor Gap Requests: the artifact that carries a question from a governed run back to the upstream lane.

    gap open     --run RUN_ID --requirement R-ID --type TYPE --question TEXT [--impact ...] [--owner NAME] [--snapshot-id ID --snapshot-sha256 HEX] [--proposal TEXT]
    gap resolve  --run RUN_ID --gap GAP-ID --decided-by NAME --decision TEXT [--new-snapshot-id ID --new-snapshot-sha256 HEX]
    gap export   --run RUN_ID   writes UPSTREAM_QUESTIONS.md, the file a human hands to the upstream Spec workflow

The agent may open gaps; only a human resolves them. A resolution that introduces a new snapshot
for an active_scope gap makes contract-lint completion demand a G1 re-lock.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from conductor_contract_lint import ContractLintError, read_json, safe_run_root, schema_errors, sha256_file


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _next_gap_id(gaps_dir: Path) -> str:
    existing = sorted(p.stem for p in gaps_dir.glob("GAP-*.json"))
    numbers = [int(name.split("-", 1)[1]) for name in existing if name.split("-", 1)[1].isdigit()]
    return f"GAP-{(max(numbers) + 1 if numbers else 1):03d}"


def open_gap(root: Path, run_id: str, *, requirement_id: str, gap_type: str, question: str,
             supersession_impact: str = "unknown", snapshot_id: str | None = None, snapshot_sha256: str | None = None,
             proposed_resolution: str | None = None, owner: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    intent_path = run_root / "intent_pack.json"
    if not intent_path.is_file():
        raise ContractLintError("CONDUCTOR_GAP_INTENT_MISSING", "a gap needs a locked or drafted intent_pack.json to bind to")
    errors: list[str] = []
    intent = read_json(intent_path, "intent_pack.json", errors)
    if intent is None:
        raise ContractLintError("CONDUCTOR_GAP_INTENT_INVALID", "; ".join(errors))
    if requirement_id not in {r["id"] for r in intent.get("requirements", [])}:
        raise ContractLintError("CONDUCTOR_GAP_UNKNOWN_REQUIREMENT", requirement_id)
    gaps_dir = run_root / "gap_requests"
    gaps_dir.mkdir(exist_ok=True)
    gap: dict[str, Any] = {
        "schema_version": 1,
        "gap_id": _next_gap_id(gaps_dir),
        "run_id": run_id,
        "intent_pack_sha256": sha256_file(intent_path),
        "requirement_id": requirement_id,
        "gap_type": gap_type,
        "question": question,
        "supersession_impact": supersession_impact,
    }
    if snapshot_id or snapshot_sha256:
        gap["origin_snapshot_id"] = snapshot_id
        gap["origin_snapshot_sha256"] = snapshot_sha256
    if proposed_resolution:
        gap["proposed_resolution"] = proposed_resolution
    if owner:
        gap["owner"] = owner.strip()
    problems = schema_errors(root, "gap_request", gap)
    if problems:
        raise ContractLintError("CONDUCTOR_GAP_SCHEMA_INVALID", "; ".join(problems))
    path = gaps_dir / f"{gap['gap_id']}.json"
    path.write_text(json.dumps(gap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"run_id": run_id, "gap_id": gap["gap_id"], "path": path.relative_to(root).as_posix(), "supersession_impact": supersession_impact}


def resolve_gap(root: Path, run_id: str, gap_id: str, *, decided_by: str, decision: str,
                new_snapshot_id: str | None = None, new_snapshot_sha256: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    path = run_root / "gap_requests" / f"{gap_id}.json"
    errors: list[str] = []
    gap = read_json(path, gap_id, errors)
    if gap is None:
        raise ContractLintError("CONDUCTOR_GAP_MISSING", "; ".join(errors))
    if "resolution" in gap:
        raise ContractLintError("CONDUCTOR_GAP_ALREADY_RESOLVED", gap_id)
    if not decided_by.strip():
        raise ContractLintError("CONDUCTOR_GAP_DECIDER_REQUIRED", "resolution needs a human name")
    resolution: dict[str, Any] = {"decided_by": decided_by.strip(), "utc": utc_now(), "decision": decision}
    if new_snapshot_id or new_snapshot_sha256:
        resolution["new_snapshot_id"] = new_snapshot_id
        resolution["new_snapshot_sha256"] = new_snapshot_sha256
    gap["resolution"] = resolution
    problems = schema_errors(root, "gap_request", gap)
    if problems:
        raise ContractLintError("CONDUCTOR_GAP_SCHEMA_INVALID", "; ".join(problems))
    path.write_text(json.dumps(gap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    reopens = gap["supersession_impact"] == "active_scope" and bool(new_snapshot_id)
    return {"run_id": run_id, "gap_id": gap_id, "path": path.relative_to(root).as_posix(), "g1_reopen_required": reopens}


def load_gaps(root: Path, run_root: Path) -> list[dict[str, Any]]:
    gaps = []
    for path in sorted((run_root / "gap_requests").glob("GAP-*.json")):
        errors: list[str] = []
        gap = read_json(path, path.name, errors)
        problems = errors or schema_errors(root, "gap_request", gap)
        if problems:
            raise ContractLintError("CONDUCTOR_GAP_SCHEMA_INVALID", "; ".join(problems))
        gaps.append(gap)
    return gaps


def _question_block(gap: dict[str, Any]) -> list[str]:
    lines = [f"### {gap['gap_id']}: {gap['gap_type']} question for {gap['requirement_id']}", "",
             gap["question"], "",
             f"- Impact on this slice: {gap['supersession_impact']}",
             f"- Owner: {gap.get('owner', 'not named')}"]
    if gap.get("origin_snapshot_id"):
        lines.append(f"- Raised against snapshot: {gap['origin_snapshot_id']} ({gap['origin_snapshot_sha256']})")
    if gap.get("proposed_resolution"):
        lines.append(f"- Agent's proposal (not a decision): {gap['proposed_resolution']}")
    return lines + [""]


def export_questions(root: Path, run_id: str) -> dict[str, Any]:
    """Render open gaps as one Markdown input for upstream reconciliation; answers belong in its decision log, not here."""
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    gaps = load_gaps(root, run_root)
    open_gaps = [g for g in gaps if "resolution" not in g]
    blocking = [g for g in open_gaps if g["supersession_impact"] != "future_only"]
    deferred = [g for g in open_gaps if g["supersession_impact"] == "future_only"]
    decided = [g for g in gaps if "resolution" in g]
    lines = [f"# Questions from Factory run {run_id}", "",
             "Input for upstream reconciliation: give this file to the Spec workflow that owns the source Spec, as its input.",
             "Record each answer as a decision in the Spec's own decision log and let that workflow re-derive the Spec; do not",
             "edit the derived Spec or this file by hand. PRD, architecture and UX sources change only through their own workflows.",
             "When reconciliation is done, a human reviews the changed inputs and Factory promotes a superseding snapshot.",
             "Nothing in this file approves scope, implementation or completion.", "",
             f"## Blocking this slice ({len(blocking)})", ""]
    for gap in blocking:
        lines += _question_block(gap)
    if not blocking:
        lines += ["None.", ""]
    lines += [f"## Deferred, not blocking this slice ({len(deferred)})", ""]
    for gap in deferred:
        lines += _question_block(gap)
    if not deferred:
        lines += ["None.", ""]
    lines += [f"## Already decided in this run ({len(decided)})", ""]
    for gap in decided:
        resolution = gap["resolution"]
        lines.append(f"- {gap['gap_id']} ({gap['requirement_id']}): {resolution['decision']} (decided by {resolution['decided_by']}, {resolution['utc']})")
    if not decided:
        lines.append("None.")
    path = run_root / "UPSTREAM_QUESTIONS.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"run_id": run_id, "path": path.relative_to(root).as_posix(), "blocking": len(blocking), "deferred": len(deferred), "decided": len(decided)}
