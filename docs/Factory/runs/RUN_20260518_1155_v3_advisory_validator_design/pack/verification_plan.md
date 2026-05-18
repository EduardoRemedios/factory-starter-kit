# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-18): Initial verification plan for v3 advisory validator design.

## Strategy
This is a `PLANNING_ONLY` run. Verification proves that the design remains non-blocking, fixture-backed, and bounded away from Factory v2 gates and runtime-kernel behavior.

## Checks

### V1-CHECK-001 - Non-blocking Output Shape
- Tier: V1
- Covers: R-001
- Method: Review report shape for `blocking_effect: none` and advisory-only statuses.
- Expected: No output status can be mistaken for required v2 gate failure.

### V1-CHECK-002 - Research Status Field
- Tier: V1
- Covers: R-002
- Method: Confirm report shape includes `promotion_level: research` or equivalent.
- Expected: Report cannot imply v3 release authority.

### V0-REVIEW-001 - Boundary Review
- Tier: V0
- Covers: R-003
- Method: Human review of candidate checks against AEGIS boundary.
- Expected: Checks flag boundary vocabulary without deciding runtime policy.

### V2-FIXTURE-001 - Warning Report Fixture
- Tier: V2
- Covers: R-004
- Method: Use `pack/fixtures/verification/advisory_report_shape/` to model warning output.
- Expected: Warning remains non-blocking and requires review classification.

### V0-REVIEW-002 - Follow-up Review Requirement
- Tier: V0
- Covers: R-005
- Method: Review workflow requires later false-negative notes after pilot use.
- Expected: Pilot reports include missed-issue review fields.

### V0-REVIEW-003 - Command Location Deferral
- Tier: V0
- Covers: R-006
- Method: Confirm candidate command names do not authorize implementation.
- Expected: Implementation remains a separate future run.

## Future Fixture Set
- Clean pass report.
- Warning report with non-blocking status.
- Boundary vocabulary warning.
- Promotion claim warning.
- Required-gate wiring warning.

## Manifest Decision
- No `verification_manifest.yaml` is created because this is a planning-only design pack.

