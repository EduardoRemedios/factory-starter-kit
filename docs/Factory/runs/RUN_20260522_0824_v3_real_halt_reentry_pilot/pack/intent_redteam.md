# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-22): Stage B red-team review.

## Iteration
Iteration: 1 of max 2

## Findings

| ID | Severity | Finding | Why It Matters | Recommendation | Status |
|---|---|---|---|---|---|
| RT-01 | Critical | A run-local harness could be overstated as full V3 operational proof. | Operational promotion requires a named profile and broader evidence. | Mark checklist items as DONE for pilot evidence only and keep V3 unpromoted. | Fixed |
| RT-02 | High | Halt behavior must prove no continuation, not just detect a nonzero exit. | Continuing after failure is the safety failure. | Record a continuation marker only if continuation happens, and assert it is absent. | Fixed |
| RT-03 | High | Reentry must prove authored artifacts are authoritative. | Derived cursors must not become mission truth. | Include both matching and conflicting source/cursor scenarios. | Fixed |

## Agent Failure Modes
- Treat the pilot as permission to operate V3.
- Modify production validators unnecessarily.
- Record only success paths and hide conflict handling.

## Verification Holes
- Future operational profile still needs a decision report and real profile boundary.

## Exit Criteria Status
- PASS
