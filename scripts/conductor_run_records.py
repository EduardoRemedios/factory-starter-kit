"""Run records a human reads: create a run, render its review packet, hand completion back to the upstream lane.

    run-init             --slug SLUG [--new]    create RUN_YYYYMMDD_HHMM_SLUG (planning only) or report the open run
    review-packet        --run RUN_ID           write REVIEW_PACKET.md for the current gate
    completion-feedback  --run RUN_ID           write UPSTREAM_FEEDBACK.md/.json after a countersigned G3

None of these writes a countersign, resolves a gap, or changes scope. Countersigns record a human decision.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from conductor_contract_lint import (
    RUNS_DIR, ContractLintError, lint_completion, lint_execution, lint_intent, read_json, read_yaml, safe_run_root,
    sha256_file,
)
from conductor_gap import load_gaps

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,40}$")
TEMPLATE = Path("docs/Conductor/templates/intent_pack.template.json")
PACKET = "REVIEW_PACKET.md"
NOT_APPROVALS = ("merge", "deployment", "backlog change", "release")


def _utc(now: datetime | None = None) -> datetime:
    return (now or datetime.now(timezone.utc)).astimezone(timezone.utc)


def _template(root: Path) -> str:
    for base in (root, Path(__file__).resolve().parent.parent):
        if (base / TEMPLATE).is_file():
            return (base / TEMPLATE).read_text(encoding="utf-8")
    raise ContractLintError("CONDUCTOR_RUN_TEMPLATE_MISSING", TEMPLATE.as_posix())


def _completed(run_root: Path) -> bool:
    return (run_root / "countersign/COMPLETION.json").is_file()


def init_run(root: Path, slug: str, *, new: bool = False, now: datetime | None = None) -> dict[str, Any]:
    root = root.resolve()
    if not SLUG_RE.fullmatch(slug):
        raise ContractLintError("CONDUCTOR_RUN_SLUG_INVALID", f"{slug!r}: use 2-41 lowercase letters, digits, '-' or '_'")
    runs = root / RUNS_DIR
    own = re.compile(rf"RUN_\d{{8}}_\d{{4}}_{re.escape(slug)}")
    existing = sorted(p.name for p in runs.iterdir() if own.fullmatch(p.name) and p.is_dir() and not _completed(p)) if runs.is_dir() else []
    if existing and not new:
        packet = write_review_packet(root, existing[-1])
        return {"state": "EXISTING", "run_id": existing[-1], "packet": packet["path"], "gate_state": packet["gate_state"],
                "next": "continue this run, or pass --new for a separate run", "open_runs": existing}
    run_id = f"RUN_{_utc(now):%Y%m%d_%H%M}_{slug}"
    target = runs / run_id
    if target.exists():
        raise ContractLintError("CONDUCTOR_RUN_ID_COLLISION", f"{run_id} already exists; retry in the next minute or choose another slug")
    staging = runs / f".tmp-{run_id}"
    if staging.exists():
        raise ContractLintError("CONDUCTOR_RUN_PARTIAL_INIT", f"{staging.relative_to(root)} is left from an interrupted run-init; inspect and remove it")
    staging.mkdir(parents=True)
    for name in ("countersign", "gap_requests", "receipts", "postimage", "notes"):
        (staging / name).mkdir()
    (staging / "intent_pack.json").write_text(_template(root).replace("RUN_YYYYMMDD_HHMM_TAG", run_id), encoding="utf-8")
    (staging / "EXECUTION_MODE.txt").write_text("PLANNING_ONLY\n", encoding="utf-8")
    staging.rename(target)
    packet = write_review_packet(root, run_id)
    return {"state": "CREATED", "run_id": run_id, "packet": packet["path"], "gate_state": packet["gate_state"],
            "next": "draft intent_pack.json from the reviewed inputs, then refresh the packet"}


def g1_readiness(intent: dict[str, Any] | None, gaps: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """Objective exit from grooming: only unresolved active-scope questions keep a slice cycling."""
    reasons = []
    if intent is None:
        return False, ["intent_pack.json does not validate yet"]
    for gap in gaps:
        if "resolution" not in gap and gap["supersession_impact"] != "future_only":
            reasons.append(f"{gap['gap_id']} is open with impact {gap['supersession_impact']}")
        if gap["supersession_impact"] == "future_only" and not gap.get("owner"):
            reasons.append(f"{gap['gap_id']} is future_only but names no owner")
        new_id = gap.get("resolution", {}).get("new_snapshot_id")
        if new_id:
            suffix = f"/{new_id}/SNAPSHOT_MANIFEST.json"
            if not any(source["kind"] == "upstream_snapshot" and source["ref"].endswith(suffix) for source in intent["sources"]):
                reasons.append(f"{gap['gap_id']} introduced snapshot {new_id}, which the intent does not cite yet")
    return not reasons, reasons


def _snapshot_rows(root: Path, intent: dict[str, Any]) -> list[str]:
    rows = []
    for source in intent["sources"]:
        path = root / source["ref"]
        state = "matches" if path.is_file() and sha256_file(path) == source["sha256"] else "MISSING OR CHANGED"
        rows.append(f"| {source['kind']} | `{source['ref']}` | `{source['sha256'][:12]}…` | {state} |")
        if source["kind"] != "upstream_snapshot" or state != "matches":
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        companions = manifest.get("provenance", {}).get("repository_companions") or {}
        binding = f"git @ `{companions['approval_commit'][:12]}`" if companions.get("binding") == "git" else ("root-bound" if companions else "path")
        supersedes = manifest.get("supersedes", {}).get("snapshot_id", "none")
        rows.append(f"|  | snapshot `{manifest.get('snapshot_id')}`, binding {binding}, supersedes {supersedes} | | |")
        for artifact in manifest.get("artifacts", {}).values():
            rows.append(f"|  | `{artifact['source_path']}` | `{artifact['sha256'][:12]}…` | frozen |")
    return rows


def write_review_packet(root: Path, run_id: str) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    g1 = lint_intent(root, run_id)
    errors: list[str] = []
    intent = read_json(run_root / "intent_pack.json", "intent_pack.json", errors) if g1["state"] != "INTENT_INVALID" else None
    gaps = load_gaps(root, run_root)
    gate_state, lines = g1["state"], [f"# Review packet: {run_id}", "",
                                       f"Generated {_utc():%Y-%m-%d %H:%M} UTC from the run's files. It reports; it approves nothing.", ""]
    g2 = g3 = None
    if g1["state"] == "INTENT_LOCKED":
        g2 = lint_execution(root, run_id)
        gate_state = g2.get("state", gate_state)
        if (run_root / "statement_of_completion.json").is_file():
            g3 = lint_completion(root, run_id)
            gate_state = g3.get("state", gate_state)
    ready, reasons = g1_readiness(intent, gaps)
    lines += ["## Status", "", f"- Gate state: **{gate_state}**"]
    if g1["state"] != "INTENT_LOCKED":
        lines.append(f"- Ready for G1 review: **{'yes' if ready else 'no'}**")
        lines += [f"  - {reason}" for reason in reasons]
    for label, payload in (("G1", g1), ("G2", g2), ("G3", g3)):
        for error in (payload or {}).get("errors", []):
            lines.append(f"- {label} error: `{error}`")
    lines.append("")
    if intent is not None:
        lines += ["## 1. Inputs and snapshots", "", "| Kind | Reference | SHA-256 | State |", "|---|---|---|---|", *_snapshot_rows(root, intent), "",
                  "## 2. Intent", "", intent["goal"], "", f"Execution mode: `{intent['execution_mode']}`", "",
                  "| Requirement | Statement | Acceptance |", "|---|---|---|",
                  *[f"| {r['id']} | {r['statement']} | {r['acceptance']} |" for r in intent["requirements"]], "",
                  "Constraints:", *[f"- {c['id']}: {c['statement']} (source `{c['source']}`)" for c in intent["constraints"]], "",
                  "In scope:", *[f"- {item}" for item in intent["scope_in"]], "",
                  "Out of scope:", *[f"- {item}" for item in intent["scope_out"]], ""]
    lines += ["## 3. Questions and decisions", ""]
    if gaps:
        lines += ["| Gap | Requirement | Impact | Owner | State |", "|---|---|---|---|---|"]
        for gap in gaps:
            resolution = gap.get("resolution")
            state = f"decided by {resolution['decided_by']}: {resolution['decision']}" if resolution else "open"
            lines.append(f"| {gap['gap_id']} | {gap['requirement_id']} | {gap['supersession_impact']} | {gap.get('owner', '')} | {state} |")
    else:
        lines.append("No gap requests.")
    lines.append("")
    manifest = read_yaml(run_root / "verification_manifest.yaml", "manifest", []) if (run_root / "verification_manifest.yaml").is_file() else None
    if manifest:
        lines += ["## 4. Verification plan and evidence", "", "| Check | Requirements | Command | Result |", "|---|---|---|---|"]
        for check in manifest.get("checks", []):
            command = " ".join(check["command"]) if isinstance(check.get("command"), list) else str(check.get("command"))
            result = check.get("result", {}).get("status", "NOT_RUN")
            lines.append(f"| {check['id']} | {', '.join(check.get('requirement_ids', []))} | `{command}` | {result} |")
        if g2:
            lines += ["", f"Write-boundary compare: {g2.get('postimage', 'MISSING')}"]
        lines.append("")
    statement_path = run_root / "statement_of_completion.json"
    if statement_path.is_file():
        statement = read_json(statement_path, "statement", [])
        if isinstance(statement, dict):
            lines += ["## 5. Statement of Completion", "", f"Derived state: {statement.get('derived_state')}; handoff: {statement.get('handoff_state')}",
                      f"Independent review: `{statement.get('verifier', {}).get('report_path')}`", "",
                      "| Requirement | Status | Limitation | Residual gap |", "|---|---|---|---|",
                      *[f"| {r['requirement_id']} | {r['status']} | {r.get('limitation', '')} | {r.get('residual_gap', '')} |" for r in statement.get("rows", [])], ""]
    lines += ["## What a human signs", ""]
    if (run_root / "intent_pack.json").is_file():
        lines.append(f"- G1 Intent Lock (and G2 Execution Go when enabled): `intent_pack.json` SHA-256 `{sha256_file(run_root / 'intent_pack.json')}`")
    if statement_path.is_file():
        lines.append(f"- G3 Completion: `statement_of_completion.json` SHA-256 `{sha256_file(statement_path)}`")
    lines += ["", "Completion is not merge, deployment or backlog approval; each is a separate decision."]
    path = run_root / PACKET
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"run_id": run_id, "path": path.relative_to(root).as_posix(), "gate_state": gate_state, "ready_for_g1": ready}


def _git(root: Path, *args: str) -> str | None:
    completed = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return completed.stdout.strip() if completed.returncode == 0 else None


def completion_feedback(root: Path, run_id: str) -> dict[str, Any]:
    """Tell the upstream product-context lane what a countersigned run delivered; PM/BA own every backlog decision."""
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    g3 = lint_completion(root, run_id)
    if g3["state"] != "COMPLETION_COUNTERSIGNED":
        raise ContractLintError("CONDUCTOR_FEEDBACK_NOT_COUNTERSIGNED", f"G3 state is {g3['state']}; feedback follows a countersigned completion only")
    intent = json.loads((run_root / "intent_pack.json").read_text(encoding="utf-8"))
    statement = json.loads((run_root / "statement_of_completion.json").read_text(encoding="utf-8"))
    sign = json.loads((run_root / "countersign/COMPLETION.json").read_text(encoding="utf-8"))
    gaps = load_gaps(root, run_root)
    requirements = {r["id"]: r for r in intent["requirements"]}
    snapshots = []
    for source in intent["sources"]:
        if source["kind"] == "upstream_snapshot":
            manifest = json.loads((root / source["ref"]).read_text(encoding="utf-8"))
            companions = manifest.get("provenance", {}).get("repository_companions") or {}
            snapshots.append({"snapshot_id": manifest["snapshot_id"], "aggregate_sha256": manifest["aggregate_sha256"],
                              "manifest": source["ref"], "approval_commit": companions.get("approval_commit"),
                              "sources": sorted(a["source_path"] for a in manifest["artifacts"].values())})
    feedback = {
        "schema_version": 1, "kind": "UPSTREAM_COMPLETION_FEEDBACK", "run_id": run_id,
        "intent_pack_sha256": sha256_file(run_root / "intent_pack.json"),
        "statement_sha256": sha256_file(run_root / "statement_of_completion.json"),
        "completion": {"signer": sign["signer"], "utc": sign["utc"], "derived_state": statement["derived_state"],
                       "handoff_state": statement["handoff_state"]},
        "not_approved_by_this_record": list(NOT_APPROVALS),
        "code_revision": {"head": _git(root, "rev-parse", "HEAD"), "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
                          "working_tree_clean": _git(root, "status", "--porcelain") == ""},
        "source_snapshots": snapshots,
        "requirements": [{"id": row["requirement_id"], "statement": requirements[row["requirement_id"]]["statement"],
                          "status": row["status"], "evidence": [e["check_id"] for e in row["evidence"]],
                          "limitation": row.get("limitation"), "residual_gap": row.get("residual_gap")} for row in statement["rows"]],
        "deferred_findings": [{"gap_id": g["gap_id"], "requirement_id": g["requirement_id"], "question": g["question"],
                               "owner": g.get("owner"), "decision": g.get("resolution", {}).get("decision"),
                               "disposition": "backlog decision for PM/BA; not delivered by this run"}
                              for g in gaps if g["supersession_impact"] == "future_only"],
    }
    json_path = run_root / "UPSTREAM_FEEDBACK.json"
    json_path.write_text(json.dumps(feedback, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [f"# Completion feedback for the product-context lane: {run_id}", "",
             "This records a reviewed, countersigned completion. It is **not** merge, deployment, release or backlog approval,",
             "and it does not mark any product capability as delivered upstream. PM/BA decide what changes in the backlog.", "",
             f"- Completion countersigned by {sign['signer']} at {sign['utc']}; derived state {statement['derived_state']}, handoff {statement['handoff_state']}",
             f"- Code revision: `{feedback['code_revision']['head']}` on `{feedback['code_revision']['branch']}`"
             + ("" if feedback["code_revision"]["working_tree_clean"] else " (working tree not clean)"),
             f"- Intent SHA-256 `{feedback['intent_pack_sha256']}`; statement SHA-256 `{feedback['statement_sha256']}`", "",
             "## Source Spec snapshots", ""]
    lines += [f"- `{s['snapshot_id']}` `{s['aggregate_sha256']}`" + (f" approved at `{s['approval_commit']}`" if s["approval_commit"] else "")
              + ": " + ", ".join(f"`{p}`" for p in s["sources"]) for s in snapshots] or ["- none cited"]
    lines += ["", "## What was completed and verified", "", "| Requirement | Status | Evidence | Limitation |", "|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['status']} | {', '.join(r['evidence'])} | {r['limitation'] or ''} |" for r in feedback["requirements"]]
    lines += ["", "## Deferred findings for PM/BA", ""]
    lines += [f"- {d['gap_id']} ({d['requirement_id']}), owner {d['owner'] or 'NOT NAMED'}: {d['question']}"
              + (f" Decision so far: {d['decision']}" if d["decision"] else "") for d in feedback["deferred_findings"]] or ["- none"]
    md_path = run_root / "UPSTREAM_FEEDBACK.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"run_id": run_id, "paths": [md_path.relative_to(root).as_posix(), json_path.relative_to(root).as_posix()],
            "deferred": len(feedback["deferred_findings"])}
