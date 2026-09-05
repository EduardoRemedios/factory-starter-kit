---
name: conductor-validate
description: Run the applicable deterministic Factory validators and report evidence-backed pass or halt results.
---

---
name: validate
description: Run the applicable deterministic Factory validators and report evidence-backed pass or halt results.
---

# Factory Validate

Run the deterministic checks for the current Factory state and report what they
prove. The validators are the hard layer; this skill only decides which to run
and reports their results faithfully.

## Workflow

1. Resolve the Git worktree root and the active run.
2. For a 0.3 run (`intent_pack.json` present) run
   `./scripts/conductorctl contract-lint intent|execution|completion --run <RUN_ID>`
   as the gate state requires. Receipts and the postimage compare come only from
   `conductorctl receipts` and `conductorctl postimage`, never from you.
3. For a 0.2-era run, run `pack-lint`; if `EXECUTION_CLOSEOUT.json` exists it is
   validated on every progress read and any identity, pin, coverage, path,
   outcome, or digest failure blocks.
4. Run Factory-controlled Python through `./scripts/conductor-python`; run other
   repository commands with `PYTHONDONTWRITEBYTECODE=1` so validation creates no
   `__pycache__` or `.pyc` files.
5. Keep validator stdout and stderr in bounded tool output and preserve each
   explicit exit status.
6. Report pass or halt with the validator's own failing reason, plus
   `git status --short` before and after; report every difference.

## Guardrails

- Do not modify contracts, receipts, or manifests to make validation pass; do
  not use `|| true` on a required validator.
- Do not persist evidence anywhere the active run has not explicitly
  authorized; that excludes `/tmp`, `/private/tmp`, and the repository itself.
- Do not delete or ignore unexpected files or invalid closeout evidence to make
  a result look clean; halt and report the mutation.
- Do not replace a validator result with a narrative judgment.
