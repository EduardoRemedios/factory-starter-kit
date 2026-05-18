# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-18): Initial verification plan for Factory v3 research planning.

## Verification Strategy
This run is `PLANNING_ONLY`, so verification focuses on artifact proof, advisory lint design, and fixture-driven promotion criteria rather than enforcing new runtime behavior.

## Checks

### V0-REVIEW-001 - Boundary Review
- Tier: V0
- Covers: R-002
- Method: Review proposed v3 docs against `docs/Factory/AEGIS_BOUNDARY.md`.
- Expected: v3 excludes runtime action execution, policy engines, ledgers, cryptographic proof, and persistent world models.

### V0-REVIEW-002 - README Split Review
- Tier: V0
- Covers: R-004
- Method: Review public README language before merge.
- Expected: README says v2 is current and v3 is research/design only.

### V1-CHECK-001 - v2 Stage Order Guard
- Tier: V1
- Covers: R-001
- Method: Future advisory lint checks that `STAGE_CONTRACTS.md` and README preserve `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`.
- Expected: Any drift is reported before promotion.

### V1-CHECK-002 - Required Validator Isolation
- Tier: V1
- Covers: R-003
- Method: Future advisory lint checks that v3 shadow schemas are not required by `stage-lint`, `pack-lint`, or required knowledge-lint checks.
- Expected: v3 candidates remain advisory until promotion.

### V2-FIXTURE-001 - Promotion Gate Fixture
- Tier: V2
- Covers: R-005
- Method: Use `pack/fixtures/verification/v3_promotion_gate/` to model a candidate promotion decision.
- Expected: Promotion is rejected unless evals, pilot feedback, and release approval are present.

## Evals To Capture Later
- False positives and false negatives from advisory v3 validators.
- Drift detected in v2-protection checks.
- Time overhead added to a normal v2 run.
- Boundary violations caught before merge.
- User confusion or clarity from README wording.
- Pilot profile pass, conditional pass, and fail cases.

## Manifest Decision
- No `verification_manifest.yaml` is created because this is a planning-only research pack and the proposed runnable checks are future advisory candidates.

