# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-18): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260518_1508_v3_promotion_evidence_plan
- Effective Scope: RUN_20260518_1508_v3_promotion_evidence_plan
- Attempted Scopes: RUN_20260518_1508_v3_promotion_evidence_plan, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: NO
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-18T14:08:59Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 1
- Artifact types: {"factory_run_root_artifact": 1}
- Focus terms: None
- Trace IDs: None
- Required refs: None
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 1
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/raw_brief.md:12` [Raw Brief - Factory v3 Promotion-Evidence Advisory Lint Planning > Scope]

### Q2. `Critical`
- Result count: 0
- Evidence: None

### Q3. `deferral`
- Result count: 0
- Evidence: None

### Q4. `human GO`
- Result count: 0
- Evidence: None

### Q5. `scope expansion`
- Result count: 1
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/raw_brief.md:12` [Raw Brief - Factory v3 Promotion-Evidence Advisory Lint Planning > Scope]

## Trace Queries
## Required Reference Checks
## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
