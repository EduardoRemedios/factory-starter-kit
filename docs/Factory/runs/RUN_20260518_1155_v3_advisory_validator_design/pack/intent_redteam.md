# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-18): Initial red-team review of advisory validator design intent.

## Iteration
- Iteration: 1 of max 2

## Findings

### F-001 - Critical - Advisory design can become implementation by drift
- Why it matters: Naming a future command can encourage code edits inside the same run.
- Fix recommendation: Keep command names candidate-only and make implementation a separate future run.

### F-002 - Critical - Non-blocking output must be unmistakable
- Why it matters: A report with `FAIL` language could be mistaken for a required gate.
- Fix recommendation: Use statuses `ADVISORY_PASS`, `ADVISORY_WARN`, and `ADVISORY_FAIL_NON_BLOCKING`.

### F-003 - High - Boundary checks may become too subjective
- Why it matters: Over-broad semantic checks can create noise and block adoption.
- Fix recommendation: First checks should be simple path and phrase checks, with human review for boundary vocabulary.

### F-004 - High - False-negative review needs a source
- Why it matters: Missed issues are hard to detect without later reviewer feedback.
- Fix recommendation: Require a follow-up review field in each eval or pilot artifact.

## Verification Holes
- No fixture currently models a clean advisory pass.
- No fixture currently models a warning that remains non-blocking.
- No review workflow yet records accepted versus rejected warnings.

## Scope Concerns
- No scope expansion required.

