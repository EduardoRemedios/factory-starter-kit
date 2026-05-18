# Stage F Handoff

## Version
v1

## Change Log
- v1 (2026-05-18): Initial Stage F handoff for verification design.

## Stage
- Stage ID: STAGE_F
- Stage Name: Verification Assets
- Timestamp: 2026-05-18 11:55 local
- Execution profile used: Standard
- Contradiction status: No contradiction with locked intent detected.
- Applicable hard rules: STAGE_F exit criteria satisfied.

## Inputs (LOAD)
- pack/intent.md
- pack/risk_register.md

## Inputs (DISK)
- pack/intent_lock_report.md

## Skill Routing Contract
- Skill used: NONE.
- Use when: designing planning-only verification.
- Do not use when: writing validator code.
- Expected output artifacts: verification_plan.md, traceability_matrix.md, fixtures, and this handoff.

## Outputs Produced (paths)
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/verification_plan.md
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/traceability_matrix.md
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/fixtures/verification/advisory_report_shape/input.json
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/fixtures/verification/advisory_report_shape/expected.json
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/fixtures/verification/advisory_report_shape/notes.md
- docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/HANDOFF/HANDOFF_STAGE_F.md

## Changes Made
- Added advisory report fixture and verification plan.

## Assumptions
- No verification manifest is required for this planning-only run.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- None.

## Verification Steps Recommended
- Run `./scripts/factoryctl stage-lint --run RUN_20260518_1155_v3_advisory_validator_design --stage F`.

## Exit Criteria Status
- PASS

