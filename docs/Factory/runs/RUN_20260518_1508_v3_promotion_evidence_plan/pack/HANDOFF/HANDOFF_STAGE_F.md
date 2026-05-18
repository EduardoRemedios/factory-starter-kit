# Stage F Handoff

## Version
v1

## Change Log
- v1 (2026-05-18): Initial Stage F verification-assets handoff.

## Stage
- Stage ID: STAGE_F
- Stage Name: Verification Assets
- Timestamp: 2026-05-18 15:08 local
- Execution profile used: Standard
- Contradiction status: No contradiction with locked intent detected.
- Applicable hard rules: STAGE_F exit criteria satisfied.

## Inputs (LOAD)
- pack/intent.md
- pack/risk_register.md

## Inputs (DISK)
- pack/intent_lock_report.md

## Skill Routing Contract
- Skill used: factory-root-planner.
- Use when: coordinating Factory stage progression and stage-lint validation.
- Do not use when: implementing validator code.
- Expected output artifacts: verification plan, traceability matrix, fixture sketch, and this handoff.

## Outputs Produced (paths)
- docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/verification_plan.md
- docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/traceability_matrix.md
- docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/fixtures/verification/promotion_evidence_warning/
- docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/HANDOFF/HANDOFF_STAGE_F.md

## Changes Made
- Added verification tiers for every Critical and High risk.
- Added a fixture sketch for promotion-evidence warning behavior.

## Assumptions
- Planning-only packs do not require `verification_manifest.yaml`.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- Future pilot may choose a different real-doc target if it preserves the same evidence shape.

## Verification Steps Recommended
- Run `./scripts/factoryctl stage-lint --run RUN_20260518_1508_v3_promotion_evidence_plan --stage F`.

## Exit Criteria Status
- PASS

