## Version
- v3
## Change Log
- v1 (2026-08-10): Created verification assets and fixtures.
- v2 (2026-08-10): Normalized four verification types to the schema vocabulary after pack-lint.
- v3 (2026-08-10): Added required targets to both source-revalidation checks.
## Stage
- Stage ID: STAGE_F
- Stage Name: Verification Assets
- Timestamp: 2026-08-10 18:35 WEST
- Execution profile used: High-reasoning
- Contradiction status: No contradiction with locked intent.
- Applicable hard rules: Every Critical/High constraint has V1–V4 coverage.
## Inputs (LOAD)
- `pack/intent.md`; `pack/risk_register.md`.
## Inputs (DISK)
- `pack/intent_lock_report.md`.
## Skill Routing Contract
- Skill used: NONE
- Use when: no domain verification skill is required.
- Do not use when: consolidating or executing checks.
- Expected output artifacts: fixtures, verification plan, traceability matrix, verification manifest.
## Outputs Produced (paths)
- `pack/verification_plan.md`
- `pack/traceability_matrix.md`
- `pack/verification_manifest.yaml`
- Six fixture directories under `pack/fixtures/`.
## Changes Made
- Bound C-01–C-15 to VM-001–VM-011.
- Used `source_revalidation`, `static`, and `command` for V4, lint, and regression checks.
- Bound VM-006 to official Claude dependency docs and VM-011 to the pinned npm package.
## Assumptions
- Planned commands will be created by MS-00 before feature code.
## Open Issues
### BLOCKING
- None.
### NON-BLOCKING
- V4 checks remain network/auth dependent and fail closed.
## Verification Steps Recommended
- Validate manifest schema and fixture naming.
## Exit Criteria Status
- PASS
