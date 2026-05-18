# Intent Red Team - Promotion-Evidence Advisory Lint Planning

## Version
v1

## Change Log
- v1 (2026-05-18): Initial red-team review of Stage A intent.

## Iteration
Iteration: 1 of max 2

## Findings

### RT-001 - Pilot planning can silently become matcher tuning
- Severity: High
- Why it matters: The current evidence supports more pilot use, not immediate matcher changes.
- Failure mode: An agent treats a promotion-evidence warning as approval to edit `scripts/factory_v3_advisory_lint.py`.
- Recommendation: Make matcher edits explicitly out of scope for this pack and require a separate implementation run if later evidence justifies tuning.

### RT-002 - Temporary unsafe promotion language could be retained
- Severity: High
- Why it matters: A promotion-evidence pilot may temporarily add release-like language to trigger `V3-A006`.
- Failure mode: The temporary mutation remains in `docs/Factory/v3/` and implies Factory v3 promotion.
- Recommendation: Require remediation in the future pilot: final docs must return to `ADVISORY_PASS`.

### RT-003 - Required-gate integration pressure remains unresolved
- Severity: Critical
- Why it matters: Advisory lint is still outside all Factory v2 gates by design.
- Failure mode: A successful pilot is misread as approval to wire the linter into `factoryctl`, CI, or required lint.
- Recommendation: Keep all integration paths explicitly blocked unless a future Factory v2 pack and human release approval authorize them.

### RT-004 - Promotion warning evidence may still be too narrow
- Severity: Medium
- Why it matters: A single future `V3-A006` real-doc pilot may prove signal for one pattern only.
- Failure mode: The team overgeneralizes one accepted finding into broad check expansion.
- Recommendation: Allow only a bounded pilot and require a follow-up decision before expanding checks.

## Verification Holes
- The pack needs an explicit verification command for final clean docs after any future temporary mutation.
- The pack needs a classification table requirement for `accepted`, `false_positive`, `needs_more_context`, and `deferred`.
- The pack needs a no-touch verification list for required gates and runtime-kernel boundaries.

## Summary
The intent is viable if it remains a planning-only pack for one future promotion-evidence pilot and does not authorize matcher edits, required gate wiring, or Factory v3 promotion.

