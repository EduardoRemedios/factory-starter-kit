# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-21): Stage G micro-sprint sequence.

## MS-01 - Runner Skeleton And Output Contract
- Objective: Add standalone script with advisory-only JSON output.
- Inputs: intent, verification plan, CLI contract fixture.
- Outputs: `scripts/factory_v3_operational_readiness_eval.py`.
- Entry criteria: pack approved and execution prompt issued.
- Exit criteria: script emits required fields and no promotion authorization.
- Stop or go gate: stop if script needs third-party dependencies or gate wiring.

## MS-02 - Golden Fixtures
- Objective: Add V3-G001 through V3-G014 fixture directories and expected results.
- Inputs: golden fixture layout contract.
- Outputs: `tests/fixtures/factory_v3_operational_readiness_eval/`.
- Entry criteria: MS-01 passed.
- Exit criteria: fixture regression passes.
- Stop or go gate: stop if negative cases are missing.

## MS-03 - Decision Report Template And Docs
- Objective: Add operational-readiness decision report template and V3 doc links.
- Inputs: output contract and promotion criteria.
- Outputs: `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_TEMPLATE.md`.
- Entry criteria: MS-02 passed.
- Exit criteria: template records review fields and V2 fallback.
- Stop or go gate: stop if text implies V3 promotion.

## MS-04 - Verification And Closeout
- Objective: Run fixture regression, real-doc smoke, no-gate-wiring check, knowledge lint, and advisory lint.
- Inputs: all implementation outputs.
- Outputs: execution evidence and closeout notes.
- Entry criteria: MS-03 passed.
- Exit criteria: all required checks pass or execution halts with evidence.
- Stop or go gate: stop on any halt-on-failure manifest failure.
