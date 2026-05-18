# SPRINT_20260518_002 Envelope

## Version
v1

## Change Log
- v1 (2026-05-18): Initial envelope for Factory v3 advisory validator design.

## Sprint Objective
Design a future non-blocking Factory v3 advisory validator without implementing code or changing Factory v2 behavior.

## Execution Mode
- Mode: PLANNING_ONLY
- Implementation is not authorized by this pack.

## First Advisory Checks
- V3-A001: v2 core preservation.
- V3-A002: v3 research-only posture.
- V3-A003: shadow schema isolation from required validators.
- V3-A004: AEGIS optionality.
- V3-A005: runtime-kernel boundary.
- V3-A006: promotion evidence requirement.

## Advisory Report Shape
Candidate fields:
- `schema_version`
- `report_id`
- `target`
- `generated_at`
- `promotion_level`
- `status`
- `blocking_effect`
- `checked_artifacts`
- `findings`
- `warnings`
- `recommended_next_steps`
- `review_status`
- `review_notes`
- `reviewer`
- `follow_up_false_negative_notes`

Allowed status values:
- `ADVISORY_PASS`
- `ADVISORY_WARN`
- `ADVISORY_FAIL_NON_BLOCKING`

Required invariant:
- `blocking_effect` must equal `none`.

## Fixture Examples
Future implementation planning should include:
- clean pass report
- warning report with non-blocking output
- boundary vocabulary warning
- promotion claim warning
- required-gate wiring warning

## False-positive Review Workflow
Each advisory finding should be classified as:
- `accepted`
- `rejected_false_positive`
- `needs_more_context`
- `deferred`

Each classification should record reviewer, date, evidence path, and notes.

## False-negative Review Workflow
Each pilot should include a follow-up section for missed issues found after advisory review. Missed issues should record source artifact, expected warning, reason missed, and whether the check should change.

## Implementation Exclusions
- No code changes in this run.
- No `factoryctl` subcommand in this run.
- No required validator wiring.
- No JSON schema files.
- No runtime enforcement.
- No AEGIS dependency.

## Criteria Before Writing Validator Code
- This pack passes I2 and pack-lint.
- Human approves a separate implementation planning run.
- The implementation run names exact files to edit.
- Fixtures are expanded before code changes.
- Required v2 validators remain isolated.

## File-touch Budget
- MS-01: max files modified 0, created 1, deleted 0.
- MS-02: max files modified 0, created 1, deleted 0.
- MS-03: max files modified 0, created 5, deleted 0.
- MS-04: max files modified 0, created 1, deleted 0.
- MS-05: max files modified 0, created 1, deleted 0.
- Sprint total: max files modified 0, created 9, deleted 0.

## Verification Before Merge
- Run `bash scripts/knowledge_lint.sh`.
- Run `./scripts/factoryctl pack-lint --run RUN_20260518_1155_v3_advisory_validator_design`.
- Confirm no required v2 validator files changed.

## Open Questions
- Whether future implementation should start as a separate script before becoming a `factoryctl` subcommand.
- Whether report output should be markdown, JSON, or both.

