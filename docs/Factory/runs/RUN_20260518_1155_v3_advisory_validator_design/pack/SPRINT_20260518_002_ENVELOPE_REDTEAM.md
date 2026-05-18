# SPRINT_20260518_002 Envelope Red Team

## Version
v1

## Change Log
- v1 (2026-05-18): Initial envelope red-team review for advisory validator design.

## Iteration
- Iteration: 1 of max 2

## Findings

### EF-001 - High - Future command shape is still open
- Why it matters: Choosing `factoryctl` too early could imply core tool integration.
- Recommendation: Keep command placement open until implementation planning.
- Resolution: Envelope lists command placement as an open question and does not authorize code.

### EF-002 - Medium - Report shape may need both markdown and JSON
- Why it matters: Humans need readable reports, while later eval aggregation may need structured output.
- Recommendation: Defer exact output format until implementation planning.
- Resolution: Envelope leaves output format open.

### EF-003 - Critical - Required-gate isolation is explicit
- Why it matters: The central risk is accidental enforcement.
- Recommendation: Preserve `blocking_effect: none` as a hard invariant.
- Resolution: Envelope requires that invariant.

## Verification Review
- Critical and High constraints have verification tiers.
- Fixture covers warning output with non-blocking status.
- No verification manifest is required for this planning-only pack.

## Scope Expansion Review
- No scope expansion found.

## Recommendation
- PASS the envelope for consolidation.

