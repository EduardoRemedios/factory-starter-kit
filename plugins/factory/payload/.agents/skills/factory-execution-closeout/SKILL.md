---
name: factory-execution-closeout
description: Close implementation against an execution-enabled Factory pack. Use after approved micro-sprints finish to verify exact scope and evidence, author REVIEW_READY, NO_GO, or BLOCKED judgment, record schema-locked EXECUTION_CLOSEOUT.json through factoryctl, and prepare a non-authorizing maintainer handoff.
---

# Factory Execution Closeout

## Workflow

1. Confirm `EXECUTION_MODE.txt` is `EXECUTION_ENABLED`, human Go is recorded,
   Stage I2 and pack-lint pass, and pack/authorization digests still match.
2. Read the envelope, micro-sprints, verification plan, traceability matrix,
   verification manifest and pack audit.
3. Compare actual paths/counts to the exact manifest and envelope. Treat unused
   numeric budget as no permission.
4. Run every enabled verification check and retain its repository-relative path,
   status and SHA-256. Never mark an unexecuted check PASS.
5. Recheck protected paths, dependency/privacy scans, prohibited actions and the
   retained review-worktree receipt.
6. Author one outcome in a temporary JSON draft using
   `docs/Factory/templates/EXECUTION_CLOSEOUT_TEMPLATE.json`:
   - `REVIEW_READY`: every enabled check PASS.
   - `NO_GO`: verification completed with at least one failed/blocked check.
   - `BLOCKED`: an exact blocker prevented completion; retain every check and use
     `NOT_RUN` only where that blocker prevented execution.
7. Record the draft only with
   `./scripts/factoryctl execution-closeout --run <RUN_ID> --input <DRAFT> --json`.
8. Run explicit-run and default-run plugin progress. Any invalid or drifted
   closeout must return a stable blocked contradiction.

## Guardrails

- The authored outcome is human/closeout-role judgment; the validator only checks
  identity, pins, completeness, paths, digests and outcome consistency.
- `EXECUTION_CLOSEOUT.json` is derived evidence. It grants no execution, merge,
  release, tag, publication, adapter, phase or mission authority.
- Absence preserves legacy progress. Presence opts into strict v1 validation;
  never delete or ignore an invalid record to obtain legacy fallback.
- Do not overwrite an existing different closeout record.
- Keep evidence repository-relative, retained, non-symlinked and privacy-clean.
- Finish at `REVIEW_READY`, never `MERGE_READY`, unless a separate merge protocol
  and human authorization are later satisfied.

## Output

Return the outcome, closeout path/digest, actual changed-path counts, verification
results/evidence, no-touch result, residual risks, retained worktree location and
all later human decisions. Do not commit, tag, merge, push or publish.
