# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-22): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260522_1220_v3_release_user_guide
- Effective Scope: RUN_20260522_1220_v3_release_user_guide
- Attempted Scopes: RUN_20260522_1220_v3_release_user_guide, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: NO
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-22T08:44:05Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 33
- Artifact types: {"factory_run_pack_artifact": 26, "factory_run_root_artifact": 7}
- Focus terms: None
- Trace IDs: None
- Required refs: None
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 24
- Evidence:
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/CONTEXT_RECALL_REPORT.md:31` [Context Recall Report > Recall Queries > Q1. `BLOCKING`]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/HANDOFF/HANDOFF_STAGE_A.md:39` [Handoff Stage A > Open Issues > BLOCKING]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/HANDOFF/HANDOFF_STAGE_A.md:42` [Handoff Stage A > Open Issues > NON-BLOCKING]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/HANDOFF/HANDOFF_STAGE_B.md:37` [Handoff Stage B > Open Issues > BLOCKING]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/HANDOFF/HANDOFF_STAGE_B.md:40` [Handoff Stage B > Open Issues > NON-BLOCKING]

### Q2. `Critical`
- Result count: 11
- Evidence:
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/SPRINT_20260522_030_ENVELOPE_REDTEAM.md:12` [Sprint Envelope Red Team - SPRINT_20260522_030 > Findings]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/intent_redteam.md:12` [Intent Red Team - V3-OP-001 Decision Report > Findings]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/risk_register.md:6` [Risk Register - V3-OP-001 Decision Report > Change Log]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/traceability_matrix.md:6` [Traceability Matrix > Change Log]

### Q3. `deferral`
- Result count: 4
- Evidence:
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/PACK_CHECKLIST.md:24` [Pack Checklist > Conditional]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/CONTEXT_RECALL_REPORT.md:39` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/intent_lock_report.md:21` [Intent Lock Report - V3-OP-001 Decision Report > Bounded Deferrals]

### Q4. `human GO`
- Result count: 7
- Evidence:
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/RUN_METRICS.md:15` [RUN_METRICS.md > Run Summary]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/intent.md:13` [Intent - V3-OP-001 Release Approval And User Guide > Goal]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/micro_sprints.md:9` [Micro-sprints - V3-OP-001 Decision Report > MS-01 Decision Report]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/raw_brief.md:6` [Raw Brief - V3-OP-001 Release Approval And User Guide > Goal]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/CONTEXT_RECALL_REPORT.md:43` [Context Recall Report > Recall Queries > Q4. `human GO`]

### Q5. `scope expansion`
- Result count: 6
- Evidence:
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/SPRINT_20260522_030_ENVELOPE_REDTEAM.md:20` [Sprint Envelope Red Team - SPRINT_20260522_030 > Scope Expansion Review]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/intent_synthesis.md:21` [Intent Synthesis - V3-OP-001 Decision Report > Scope Expansion Review]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/HANDOFF/HANDOFF_STAGE_C.md:9` [Handoff Stage C > Stage]
  - `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]

## Trace Queries
## Required Reference Checks
## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
