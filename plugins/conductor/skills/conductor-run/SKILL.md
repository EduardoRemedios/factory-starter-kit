---
name: conductor-run
description: Continue a Factory run through the next legal action at G1 Intent Lock, G2 Governed Execution, or G3 Review and Completion, stopping at every human countersign.
---

# Conductor Run

Continue a Conductor run through the next legal action. Conductor governs authority, outcomes, and write boundaries; it does not script your steps.

## Workflow

1. Run `progress` first. It reports the run's gate state (`G1` Intent Lock, `G2` Governed Execution, `G3` Adversarial Review and Completion) from `conductorctl contract-lint`, never from prose.
2. **G1.** Draft `docs/Conductor/runs/<RUN_ID>/intent_pack.json` from the human brief and any promoted upstream snapshots (cite each as an `upstream_snapshot` source with its manifest path and digest). Run `./scripts/conductorctl contract-lint intent --run <RUN_ID>` until PASS. Stop: a human writes `countersign/INTENT_LOCK.json`. Do not proceed on a draft.
3. **G2.** Once locked, declare checks in `verification_manifest.yaml` (v2) so that the check ids equal the Intent Pack's verification requirements. Run `./scripts/conductorctl postimage capture --run <RUN_ID>`, do the work end to end inside the locked scope, then `./scripts/conductorctl receipts run --run <RUN_ID>` and `postimage compare`. Manual checks need `receipts attest` by a human. `contract-lint execution --require-complete` must PASS before G3.
4. **G3.** Dispatch a fresh-context verifier subagent that did not do the work; it audits every claim against its receipt and writes a report. Draft `statement_of_completion.json` with one row per requirement; never set `derived_state` by hand, copy what `contract-lint completion` derives. Stop: a human writes `countersign/COMPLETION.json`. Handoff is `REVIEW_READY`; `MERGE_READY` comes only from the merge protocol.
5. A question only a human can answer becomes a Gap Request (`./scripts/conductorctl gap open ...`), not a chat question. Continue everything that does not depend on it.
6. `EXECUTION_ENABLED` runs additionally need `countersign/EXECUTION_GO.json` before G2 begins.

## Legacy runs

A run without `intent_pack.json` is a Factory-lineage run. Use `pack-lint` and the archived stage process for it; do not convert it in place.

## Guardrails

- The Intent Pack sets the scope and the scope is the deliverable: do not narrow, widen, or swap it.
- Report only what a receipt proves; say explicitly what is not yet verified.
- Receipts and manifest results are written by the runner only. Never author them.
- `REVIEW_READY` is a review handoff, never commit, merge, tag, or release authority.
- Do not treat plugin instructions as a replacement for `docs/Conductor/INVARIANTS.md`.
