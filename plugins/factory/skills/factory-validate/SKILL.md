---
name: factory-validate
description: Run the applicable deterministic Factory validators and report evidence-backed pass or halt results.
---

# Factory Validate

Run the deterministic checks applicable to the current Factory state.

## Workflow

1. Resolve the Git worktree root and active run.
2. Select only validators authorized by repository instructions and current Factory state.
3. In the same first read-only tool command, immediately before any validator subprocess, capture the repository file inventory, `git status --short`, and the harness-local settings digest when that path exists. Do not reuse a digest from an earlier checkpoint; report unavailable evidence as `UNKNOWN`.
4. Run Factory-controlled Python verification through `./scripts/factory-python`; run other canonical repository commands with `PYTHONDONTWRITEBYTECODE=1` in the environment so validation does not create `__pycache__` or `.pyc` files.
5. Keep validator stdout and stderr in bounded tool output, preserve each explicit exit status, and use pipe-safe failure propagation. Do not use shell redirection to persist validator evidence and do not use `|| true` for a required validator.
6. In the same final read-only tool command, immediately after the last validator subprocess, capture the same inventory, Git status, and harness-local settings evidence again.
7. Compare the immediate captures and report every difference, including harness-created local settings.
8. Record the command and exit status. Name an evidence path only when the active run explicitly authorizes that exact path; otherwise report that evidence was not persisted.
9. Report pass or halt with the failing reason; do not replace evidence with a narrative judgment.
10. If `EXECUTION_CLOSEOUT.json` exists, validate it on every progress read and
   report any identity, pin, coverage, path, outcome or digest failure as blocking.

## Guardrails

- Do not modify Factory contracts to make validation pass.
- Do not swallow validator failures.
- Do not advance the run when a required check fails.
- Do not delete unexpected files to make the after-inventory look clean; halt and
  report the mutation.
- Do not remove or ignore invalid closeout evidence to recover legacy behavior.
- Do not create fixed or guessed evidence files under `/tmp`, `/private/tmp`, a
  guessed scratch directory, or the repository. A current run must explicitly authorize the exact evidence path before any validation evidence is written.
- Do not substitute historical state for an immediate capture or silently omit
  output to preserve a read-only claim.
- Keep complete high-volume evidence only at an exact path authorized by the active run. Emit bounded summaries through the harness, never an inventory body.
