# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-08-10): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260810_1816_factory_bmad_companion
- Effective Scope: RUN_20260810_1816_factory_bmad_companion
- Attempted Scopes: RUN_20260810_1816_factory_bmad_companion, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: NO
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-08-10T17:18:21Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 2
- Artifact types: {"factory_run_root_artifact": 2}
- Focus terms: factory-bmad-companion
- Trace IDs: SPRINT_20260810_003
- Required refs: docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 2
- Evidence:
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md:283` [Raw Brief — Factory BMAD Companion Plugin > Open Issues > BLOCKING]
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md:288` [Raw Brief — Factory BMAD Companion Plugin > Open Issues > NON-BLOCKING]

### Q2. `Critical`
- Result count: 0
- Evidence: None

### Q3. `deferral`
- Result count: 0
- Evidence: None

### Q4. `human GO`
- Result count: 2
- Evidence:
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md:295` [Raw Brief — Factory BMAD Companion Plugin > Go / No-Go]
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md:186` [Raw Brief — Factory BMAD Companion Plugin > Hard Constraints]

### Q5. `scope expansion`
- Result count: 0
- Evidence: None

### Q6. `factory-bmad-companion`
- Result count: 0
- Evidence: None

## Trace Queries
### T1. `SPRINT_20260810_003`
- Match count: 1
- Evidence:
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md:12` [sprint_id]

## Required Reference Checks
### R1. `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260810_1816_factory_bmad_companion/raw_brief.md` (factory_run_root_artifact)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
