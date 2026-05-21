# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-21): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260521_0948_v3_confidence_pilot_execution
- Effective Scope: docs
- Attempted Scopes: RUN_20260521_0948_v3_confidence_pilot_execution, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-21T08:49:12Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 285
- Artifact types: {"canonical_doc": 53, "factory_run_pack_artifact": 191, "factory_run_root_artifact": 41}
- Focus terms: None
- Trace IDs: None
- Required refs: docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/PACK_AUDIT_REPORT.md, docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/SPRINT_20260521_020_ENVELOPE.md, docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md, docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 345
- Evidence:
  - `docs/PROJECT_STATE.md:37` [PROJECT_STATE.md — Canonical Build State > Current Tracking Snapshot]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:24` [SPRINT_20260518_002 Envelope > Advisory Report Shape]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md:56` [Execution Closeout - Factory v3 Advisory Lint Prototype > Residual Risk]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/pack/SPRINT_20260518_003_ENVELOPE.md:43` [SPRINT_20260518_003 Envelope > Output Requirements]
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:31` [Context Recall Report > Recall Queries > Q1. `BLOCKING`]

### Q2. `Critical`
- Result count: 129
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:209` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.13) > STAGE_F — Verification Assets]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]

### Q3. `deferral`
- Result count: 61
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:44` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Deferrals Summary]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]

### Q4. `human GO`
- Result count: 96
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]
  - `docs/Factory/MISSION_MODE.md:214` [docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension) > 11. Mission artifacts (minimum) > 11.3 Codex Mission Goal Continuity adapter (experimental)]

### Q5. `scope expansion`
- Result count: 85
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/PACK_AUDIT_REPORT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/PACK_AUDIT_REPORT.md` (factory_run_pack_artifact)

### R2. `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/SPRINT_20260521_020_ENVELOPE.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/SPRINT_20260521_020_ENVELOPE.md` (factory_run_pack_artifact)

### R3. `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md` (canonical_doc)

### R4. `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md` (canonical_doc)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
