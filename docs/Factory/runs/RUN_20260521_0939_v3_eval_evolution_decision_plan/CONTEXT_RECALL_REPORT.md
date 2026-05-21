# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-21): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260521_0939_v3_eval_evolution_decision_plan
- Effective Scope: docs
- Attempted Scopes: RUN_20260521_0939_v3_eval_evolution_decision_plan, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-21T08:39:58Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 254
- Artifact types: {"canonical_doc": 53, "factory_run_pack_artifact": 164, "factory_run_root_artifact": 37}
- Focus terms: None
- Trace IDs: None
- Required refs: docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md, docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md, docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md, docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md, docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 319
- Evidence:
  - `docs/PROJECT_STATE.md:36` [PROJECT_STATE.md — Canonical Build State > Current Tracking Snapshot]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:24` [SPRINT_20260518_002 Envelope > Advisory Report Shape]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md:56` [Execution Closeout - Factory v3 Advisory Lint Prototype > Residual Risk]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/pack/SPRINT_20260518_003_ENVELOPE.md:43` [SPRINT_20260518_003 Envelope > Output Requirements]
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:31` [Context Recall Report > Recall Queries > Q1. `BLOCKING`]

### Q2. `Critical`
- Result count: 120
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:209` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.13) > STAGE_F — Verification Assets]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]

### Q3. `deferral`
- Result count: 55
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:44` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Deferrals Summary]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]

### Q4. `human GO`
- Result count: 90
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]
  - `docs/Factory/MISSION_MODE.md:214` [docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension) > 11. Mission artifacts (minimum) > 11.3 Codex Mission Goal Continuity adapter (experimental)]

### Q5. `scope expansion`
- Result count: 80
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:51` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Scope Expansion Check]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md` (canonical_doc)

### R2. `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md` (canonical_doc)

### R3. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md` (factory_run_root_artifact)

### R4. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md` (factory_run_root_artifact)

### R5. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md` (factory_run_root_artifact)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
