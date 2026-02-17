# RETRO — RUN_20260208_1400_factory (Sprint A)

## What happened
- Ran the first Factory v2 pipeline for Sprint A (Adapter Boundary).
- Generated an execution prompt and completed sprint execution via a separate agent.
- Captured process gaps that later drove spec updates, including stage ordering.

## What got wrong
- Jumped to Sprint B feature work before locking drift exposed by Sprint A execution.
- Added speculative reason codes and decision-contract expansion that were out of Sprint B scope.
- Asserted path casing without verifying the repository structure.
- Used proxy constraints in verification language instead of asserting the invariant directly.

## What worked
- Full stage sequence produced a coherent pack with clean handoffs.
- Red Team findings identified real architectural gaps (entrypoint and evidence timing).
- Execution prompt with explicit data shapes reduced context-hunting during implementation.
- File-touch budgets constrained scope and prevented over-engineering.

## Carry-forward lessons
- Harden contracts before feature expansion when execution reveals ambiguity.
- Treat reason codes as commitments with explicit emission points.
- Verify canonical paths before asserting.
- Test invariants directly.
