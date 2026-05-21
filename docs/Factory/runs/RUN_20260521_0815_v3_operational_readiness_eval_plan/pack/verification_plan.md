# Verification Plan - V3 Operational Readiness Eval Suite

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F verification plan.

## Verification Strategy
The future eval-suite implementation must be planned around pre-mortem-derived fixtures and pilot evidence. This run does not implement the runner.

## Required Checks

### VP-01 - Fixture Inventory Completeness
- Tier: V1 static or mechanical check
- Covers: C-04, C-05
- Check: Confirm every pre-mortem failure mode maps to at least one fixture, eval family, or pilot observation.
- Evidence: `pack/fixtures/verification/v3_golden_fixture_inventory/expected.json`

### VP-02 - Golden Fixture Expected Outcomes
- Tier: V2 focused fixture
- Covers: C-04, C-05
- Check: Confirm fixture inventory includes both PASS and FAIL cases with reason codes.
- Evidence: `pack/fixtures/verification/v3_golden_fixture_inventory/expected.json`

### VP-03 - V2 Guarantee Preservation
- Tier: V2 focused fixture
- Covers: C-03
- Check: Confirm V3 ceremony collapse is rejected when no equivalent V2 guarantee is present.
- Evidence: `traceability_matrix.md`

### VP-04 - No Premature Promotion
- Tier: V1 static or mechanical check
- Covers: C-01, C-02
- Check: Confirm planning artifacts say V3 remains research-only and V2 remains supported.
- Evidence: `intent.md`, `SPRINT_20260521_013_ENVELOPE.md`

### VP-05 - Harness Capability Evidence
- Tier: V0 artifact proof
- Covers: C-04
- Check: Confirm pilot template requires model, harness, tool reliability, interruption behavior, and verification execution reliability.
- Evidence: `SPRINT_20260521_013_ENVELOPE.md`

### VP-06 - AEGIS Boundary Review
- Tier: V2 focused fixture
- Covers: C-06
- Check: Confirm fixtures include both boundary violation and adapter-safe positive cases.
- Evidence: `pack/fixtures/verification/v3_golden_fixture_inventory/expected.json`

### VP-07 - SIMPLE-CODE-GATE Coverage
- Tier: V2 focused fixture
- Covers: C-07
- Check: Confirm fixture inventory includes an over-abstracted or dependency-creep V3 implementation plan that must fail.
- Evidence: `pack/fixtures/verification/v3_golden_fixture_inventory/expected.json`

### VP-08 - Pack Validation
- Tier: V1 static or mechanical check
- Covers: all Critical and High constraints
- Check: Run `./scripts/factoryctl pack-lint --run RUN_20260521_0815_v3_operational_readiness_eval_plan`.
- Evidence: command output in final review notes.

## Fixture Coverage Confirmation
All Critical and High constraints have at least one fixture, artifact check, or pilot evidence hook.
