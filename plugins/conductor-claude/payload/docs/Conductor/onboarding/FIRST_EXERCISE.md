# First exercise: one run through all three gates

About 45 minutes, on a sandbox branch of a repository that has Conductor adopted. Every step names what you should see, so you can tell you are on track without asking anyone. Keep `FRICTION_LOG_TEMPLATE.md` open and write one line every time you wonder "what now?".

## 0. Start

Run `/conductor:progress`. Expect `READY_TO_INITIALIZE` with reason `CONDUCTOR_NO_ACTIVE_RUN`.

## 1. Create a run and a brief

```bash
RUN=RUN_$(date -u +%Y%m%d_%H%M)_first_exercise
mkdir -p docs/Conductor/runs/$RUN/notes
printf 'PLANNING_ONLY\n' > docs/Conductor/runs/$RUN/EXECUTION_MODE.txt
printf 'Add a short CONTRIBUTING note that names the test command.\n' > docs/Conductor/runs/$RUN/notes/brief.md
```

## 2. G1: draft and lint the Intent Pack

Ask the agent (or do it yourself) to write `docs/Conductor/runs/$RUN/intent_pack.json` from `docs/Conductor/templates/intent_pack.template.json`: two requirements (`R-001` the note exists, `R-002` it names the test command), one verification requirement per requirement (`VM-001`, `VM-002`), the brief as a `human_brief` source with its real SHA-256, no placeholders left.

```bash
./scripts/conductorctl contract-lint intent --run $RUN
```

Expect `contract-lint G1: PASS ... state=INTENT_DRAFT`. If you see `CONDUCTOR_CONTRACT_PLACEHOLDER` or a source digest mismatch, that is the point of the exercise: fix the pack, not the lint.

## 3. G1: lock it

Write `docs/Conductor/runs/$RUN/countersign/INTENT_LOCK.json` from `docs/Conductor/templates/countersign.template.json` with `subject_path: intent_pack.json`, the file's current SHA-256, your name, and the UTC time. Re-run the lint. Expect `state=INTENT_LOCKED`. `/conductor:progress` now says `EXECUTION_IN_PROGRESS` or asks for a manifest.

## 4. G2: declare checks, capture, work, prove

Write `verification_manifest.yaml` (v2 template) with `VM-001` as an `artifact` check on `CONTRIBUTING.md` and `VM-002` as a `command` check, for example `["grep", "-q", "unittest", "CONTRIBUTING.md"]`.

```bash
./scripts/conductorctl postimage capture --run $RUN
# do the work: create CONTRIBUTING.md with the test command
./scripts/conductorctl receipts run --run $RUN
./scripts/conductorctl postimage compare --run $RUN
./scripts/conductorctl contract-lint execution --run $RUN --require-complete
```

Expect two receipts under `receipts/`, `postimage: PASS`, and `state=EXECUTION_COMPLETE`. Open one receipt: note that `payload_sha256` covers every other field. Change one byte in it and re-run the lint to watch `CONDUCTOR_CONTRACT_RECEIPT_TAMPERED` appear; then restore it (re-run `receipts run`).

## 5. G3: verify, state, countersign

Have a fresh agent session (not the one that did the work) read the receipts and write `notes/verifier.md`. Write `statement_of_completion.json` from the template with both rows `verified`, each citing its receipt path and SHA-256. Leave `derived_state` as `READY`.

```bash
./scripts/conductorctl contract-lint completion --run $RUN
```

Expect `derived_state=READY`, `state=COMPLETION_DRAFT`. Now change `R-002` to `not_done` and keep `READY`: the lint reports `CONDUCTOR_CONTRACT_DERIVED_STATE_MISMATCH` and tells you it derives `BLOCKED`. That is the state being computed, not trusted. Restore the row.

Write `countersign/COMPLETION.json` for `statement_of_completion.json`. Expect `state=COMPLETION_COUNTERSIGNED` and `/conductor:progress` reporting `REVIEW_READY`.

## 6. One Gap Request

```bash
./scripts/conductorctl gap open --run $RUN --requirement R-002 --type requirement \
  --question "Should the note also name the lint command?" --impact future_only
```

Expect `GAP-001` under `gap_requests/`. Resolve it as the human:

```bash
./scripts/conductorctl gap resolve --run $RUN --gap GAP-001 --decided-by "Your Name" --decision "Yes, next run."
```

## 7. Open the pull request

Push the branch and open a PR. The `conductor-contract-lint` action runs the same lints you just ran. Expect green. Then fill in the friction log and hand it to the maintainer; it is the input for the next release.

## What you have proven

Intent was locked by a human before work. Every claim of completion is backed by a receipt you could not have forged. Nothing outside the protected roots changed. A human countersigned the outcome. That is the whole of Conductor; everything else is convenience.
