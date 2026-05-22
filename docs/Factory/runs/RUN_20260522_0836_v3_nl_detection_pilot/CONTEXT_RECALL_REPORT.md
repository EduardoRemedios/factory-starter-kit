# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-22): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260522_0836_v3_nl_detection_pilot
- Effective Scope: docs
- Attempted Scopes: RUN_20260522_0836_v3_nl_detection_pilot, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-22T07:36:59Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 378
- Artifact types: {"canonical_doc": 54, "factory_run_pack_artifact": 250, "factory_run_root_artifact": 74}
- Focus terms: None
- Trace IDs: None
- Required refs: docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md, docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/NATURAL_LANGUAGE_DETECTION_DESIGN.md, docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 416
- Evidence:
  - `docs/PROJECT_STATE.md:40` [PROJECT_STATE.md — Canonical Build State > Current Tracking Snapshot]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/EXECUTION_CLOSEOUT.md:27` [Execution Closeout - V3 Confidence Pilot Batch > Pilot Results]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/CONFIDENCE_PILOT_BATCH_ROLLUP.md:15` [V3 Confidence Pilot Batch Rollup > Results]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/fixtures/confidence_pilot_batch/README.md:9` [Confidence Pilot Batch Fixtures > Fixture / Pilot Inventory]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:24` [SPRINT_20260518_002 Envelope > Advisory Report Shape]

### Q2. `Critical`
- Result count: 143
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]

### Q3. `deferral`
- Result count: 71
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]

### Q4. `human GO`
- Result count: 118
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/CONFIDENCE_PILOT_BATCH_ROLLUP.md:43` [V3 Confidence Pilot Batch Rollup > Decision]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]

### Q5. `scope expansion`
- Result count: 104
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md` (canonical_doc)

### R2. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/NATURAL_LANGUAGE_DETECTION_DESIGN.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/NATURAL_LANGUAGE_DETECTION_DESIGN.md` (factory_run_root_artifact)

### R3. `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md` (factory_run_root_artifact)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
