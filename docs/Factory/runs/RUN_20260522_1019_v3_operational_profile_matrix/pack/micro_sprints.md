# Micro-sprints - V3 Operational Profile And Matrix

## Version
v1

## Change Log
- v1 (2026-05-22): Stage G micro-sprints.

## MS-01 Profile Draft
- Objective: Add the bounded `V3-OP-001` profile candidate.
- Inputs: locked intent, risk register.
- Outputs: `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`.
- Entry Criteria: intent lock PASS.
- Exit Criteria: profile names eligible work, exclusions, authority, verification, evidence, and fallback triggers.
- Stop Or Go: stop if profile implies operational release.

## MS-02 Guarantee Matrix
- Objective: Map V2 guarantees to `V3-OP-001` controls.
- Inputs: profile doc and operational-readiness eval plan.
- Outputs: `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md`.
- Entry Criteria: profile exists.
- Exit Criteria: every relevant V2 guarantee has a V3 control and evidence requirement.
- Stop Or Go: stop if any critical guarantee is missing.

## MS-03 Tracking And Verification
- Objective: Update checklist and tracking docs, then verify.
- Inputs: profile and matrix.
- Outputs: checklist, project state, roadmap, changelogs, verification evidence.
- Entry Criteria: profile and matrix complete.
- Exit Criteria: verification plan passes.
- Stop Or Go: stop on failed lint or advisory scan.
