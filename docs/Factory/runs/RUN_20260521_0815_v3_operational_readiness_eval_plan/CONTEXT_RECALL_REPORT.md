# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-21): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260521_0815_v3_operational_readiness_eval_plan
- Effective Scope: docs/Factory/runs
- Attempted Scopes: RUN_20260521_0815_v3_operational_readiness_eval_plan, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-21T07:16:47Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 123
- Artifact types: {"factory_run_pack_artifact": 105, "factory_run_root_artifact": 18}
- Focus terms: None
- Trace IDs: None
- Required refs: None
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 183
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:24` [SPRINT_20260518_002 Envelope > Advisory Report Shape]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md:56` [Execution Closeout - Factory v3 Advisory Lint Prototype > Residual Risk]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/pack/SPRINT_20260518_003_ENVELOPE.md:43` [SPRINT_20260518_003 Envelope > Output Requirements]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/SPRINT_20260518_001_ENVELOPE_REDTEAM.md:24` [SPRINT_20260518_001 Envelope Red Team > Findings > EF-003 - High - v2 protection lint candidates need non-blocking posture]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/intent_redteam.md:18` [Intent Red Team > Findings > F-002 - Critical - Non-blocking output must be unmistakable]

### Q2. `Critical`
- Result count: 50
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]

### Q3. `deferral`
- Result count: 27
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_CHECKLIST.md:24` [Pack Checklist > Conditional]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_CHECKLIST.md:24` [Pack Checklist > Conditional]

### Q4. `human GO`
- Result count: 17
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/PACK_AUDIT_REPORT.md:47` [Pack Audit Report - Promotion-Evidence Advisory Lint Planning > Required Human Decision]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/micro_sprints.md:9` [Micro-sprints > MS-01 - Research Namespace]
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_PILOT_REPORT.md:87` [Real-Branch Pilot Report - Factory v3 Advisory Lint > Residual Risk]
  - `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/PROMOTION_EVIDENCE_PILOT_REPORT.md:71` [Promotion-Evidence Pilot Report - Factory v3 Advisory Lint > Missed-Signal Classification]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_AUDIT_REPORT.md:29` [Pack Audit Report > Approved Planning Output]

### Q5. `scope expansion`
- Result count: 25
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/SPRINT_20260518_001_ENVELOPE_REDTEAM.md:34` [SPRINT_20260518_001 Envelope Red Team > Scope Expansion Review]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE_REDTEAM.md:34` [SPRINT_20260518_002 Envelope Red Team > Scope Expansion Review]

## Trace Queries
## Required Reference Checks
## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
