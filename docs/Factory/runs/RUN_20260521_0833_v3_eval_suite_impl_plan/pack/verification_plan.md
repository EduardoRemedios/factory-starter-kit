# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F verification plan.

## Required Checks

### VP-01 - Golden Fixture Regression
- Tier: V2 focused fixture
- Covers: C-03, C-05
- Command: `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json`
- Expected: all V3-G001 through V3-G014 cases match expected results.

### VP-02 - Advisory Output Contract
- Tier: V2 focused fixture
- Covers: C-01, C-02, C-06
- Command: same as VP-01.
- Expected: output includes `blocking_effect: none`, `promotion_decision: not_authorized`, checked files, findings, warnings, false-positive fields, and false-negative fields.

### VP-03 - Real V3 Docs Smoke
- Tier: V1 static or mechanical check
- Covers: C-01, C-02, C-03
- Command: `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- Expected: advisory output only; no V3 promotion.

### VP-04 - No Dependency Creep
- Tier: V1 static or mechanical check
- Covers: C-04, C-07
- Command: inspect script imports for standard-library-only usage.
- Expected: no new third-party dependencies.

### VP-05 - No Required Gate Wiring
- Tier: V1 static or mechanical check
- Covers: C-01
- Command: `rg -n "factory_v3_operational_readiness_eval" scripts/knowledge_lint.sh scripts/factory_stage_lint.py scripts/factory_pack_lint.py scripts/factoryctl || true`
- Expected: no required-gate invocation.

### VP-06 - Existing Factory Checks
- Tier: V1 static or mechanical check
- Covers: all constraints
- Command: `bash scripts/knowledge_lint.sh` and `./scripts/factoryctl pack-lint --run RUN_20260521_0833_v3_eval_suite_impl_plan`
- Expected: both pass.

## Fixture Coverage Confirmation
All Critical and High constraints have at least one fixture, static check, or command.
