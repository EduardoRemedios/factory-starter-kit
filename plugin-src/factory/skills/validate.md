# Factory Validate

Run the deterministic checks applicable to the current Factory state.

## Workflow

1. Resolve the Git worktree root and active run.
2. Select only validators authorized by repository instructions and current Factory state.
3. Capture the repository file inventory and `git status --short` before validation.
4. Run canonical repository commands with `PYTHONDONTWRITEBYTECODE=1` in the environment so validation does not create `__pycache__` or `.pyc` files.
5. Capture the inventory and Git status again and report every difference, including harness-created local settings.
6. Record the command, exit status, and evidence path.
7. Report pass or halt with the failing reason; do not replace evidence with a narrative judgment.
8. If `EXECUTION_CLOSEOUT.json` exists, validate it on every progress read and
   report any identity, pin, coverage, path, outcome or digest failure as blocking.

## Guardrails

- Do not modify Factory contracts to make validation pass.
- Do not swallow validator failures.
- Do not advance the run when a required check fails.
- Do not delete unexpected files to make the after-inventory look clean; halt and
  report the mutation.
- Do not remove or ignore invalid closeout evidence to recover legacy behavior.
