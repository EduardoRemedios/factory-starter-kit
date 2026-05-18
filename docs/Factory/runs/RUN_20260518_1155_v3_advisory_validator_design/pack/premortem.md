# Premortem

## Version
v1

## Change Log
- v1 (2026-05-18): Initial premortem for v3 advisory validator design.

## Failure Scenarios

### PM-001 - Advisory check becomes a gate
- Failure: Future implementation is wired into required v2 lint paths.
- Mitigation: Require `blocking_effect: none` in output and keep implementation out of required commands.

### PM-002 - Report status causes confusion
- Failure: Users treat advisory warnings as pack-lint failures.
- Mitigation: Use explicit status `ADVISORY_FAIL_NON_BLOCKING` and include remediation text.

### PM-003 - Checks are too semantic and noisy
- Failure: First version produces subjective warnings that reviewers ignore.
- Mitigation: Start with deterministic file, phrase, and path checks.

### PM-004 - AEGIS boundary check overreaches
- Failure: Advisory lint tries to judge runtime governance correctness.
- Mitigation: Report possible boundary vocabulary only and route to human review.

### PM-005 - False negatives are never reviewed
- Failure: Missed issues are not captured, so promotion evidence is weak.
- Mitigation: Require follow-up review fields in evals and pilot reports.

## Early Warning Signals
- A required v2 command invokes a v3 advisory check.
- Report output omits non-blocking status.
- A finding claims runtime proof or kernel policy violation.
- A future implementation lacks fixtures for both clean and warning cases.

