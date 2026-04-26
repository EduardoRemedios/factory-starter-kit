---
name: factory-execution-closeout
description: Close implementation work against an approved Factory pack. Use when Codex is asked to verify execution after human Go, compare a code/doc diff to the approved envelope and micro-sprints, prepare execution completion notes, check residual risk, or decide whether a completed implementation is ready for project-specific merge gates.
---

# Factory Execution Closeout

## Workflow

1. Confirm execution was explicitly authorized and the run is `EXECUTION_ENABLED`.
2. Read the approved envelope, micro-sprints, verification plan, traceability matrix, and pack audit report.
3. Compare actual changes against scope, non-goals, file-touch budgets, and stop/go gates.
4. Run the project-specific verification commands from `AGENTS.md` and the pack.
5. Record evidence paths for tests, lint, screenshots, reports, or manual checks.
6. Identify residual risk and any deviation from the approved pack.
7. Do not merge or request merge if required project gates fail.

## Closeout Decision

- `READY`: implementation matches the approved pack and required verification passed.
- `BLOCKED`: verification failed, scope drift occurred, or required evidence is missing.
- `NEEDS HUMAN DECISION`: implementation is technically complete but a product, policy, or scope decision is unresolved.

## Outputs

Return:
- execution status
- files changed
- verification commands and results
- pack alignment notes
- residual risks
- merge-readiness blockers
