---
name: conductor-run
description: Continue a Factory run through the next legal action at G1 Intent Lock, G2 Governed Execution, or G3 Review and Completion, stopping at every human countersign.
---

# Conductor Run

Continue a Conductor run through the next legal action. Conductor governs authority, outcomes, and write boundaries; it does not script your steps.

## Workflow

1. Run `progress` first. It reports the run's gate state (`G1` Intent Lock, `G2` Governed Execution, `G3` Adversarial Review and Completion) from `conductorctl contract-lint`, never from prose. For new work, run `./scripts/conductorctl run-init --slug <short-name>` (derive the slug from the Spec or task; the command generates the RUN_ID, creates the planning-only records, or reports the run already open for that slug). After every step that changes the run, refresh `./scripts/conductorctl review-packet --run <RUN_ID>` and point the human at `REVIEW_PACKET.md` rather than pasting evidence into chat.
2. **G1.** Draft `docs/Conductor/runs/<RUN_ID>/intent_pack.json` from the human brief and any promoted upstream snapshots (cite each as an `upstream_snapshot` source with its manifest path and digest). Run `./scripts/conductorctl contract-lint intent --run <RUN_ID>` until PASS. Stop: a human writes `countersign/INTENT_LOCK.json`. Do not proceed on a draft.
3. **G2.** Once locked, declare checks in `verification_manifest.yaml` (v2) so that the check ids equal the Intent Pack's verification requirements. Run `./scripts/conductorctl postimage capture --run <RUN_ID>`, do the work end to end inside the locked scope, then `./scripts/conductorctl receipts run --run <RUN_ID>` and `postimage compare`. Manual checks need `receipts attest` by a human. `contract-lint execution --require-complete` must PASS before G3.
4. **G3.** Dispatch a fresh-context verifier subagent that did not do the work; it audits every claim against its receipt and writes a report. Draft `statement_of_completion.json` with one row per requirement; never set `derived_state` by hand, copy what `contract-lint completion` derives. Stop: a human writes `countersign/COMPLETION.json`. Handoff is `REVIEW_READY`; `MERGE_READY` comes only from the merge protocol. After the countersign, `./scripts/conductorctl completion-feedback --run <RUN_ID>` writes `UPSTREAM_FEEDBACK.md/.json` for PM/BA; it is not merge, deployment or backlog approval. An approved requirement cannot be closed through a `future_only` gap.
5. A question only a human can answer becomes a Gap Request (`./scripts/conductorctl gap open ... --owner <person or role>`), not a chat question. Continue everything that does not depend on it. `gap export` writes `UPSTREAM_QUESTIONS.md` for upstream reconciliation.
6. `EXECUTION_ENABLED` runs additionally need `countersign/EXECUTION_GO.json` before G2 begins.

## Legacy runs

A run without `intent_pack.json` is a Factory-lineage run. Use `pack-lint` and the archived stage process for it; do not convert it in place.

## Guardrails

- The Intent Pack sets the scope and the scope is the deliverable: do not narrow, widen, or swap it.
- Report only what a receipt proves; say explicitly what is not yet verified.
- Receipts and manifest results are written by the runner only. Never author them.
- `REVIEW_READY` is a review handoff, never commit, merge, tag, or release authority.
- Do not treat plugin instructions as a replacement for `docs/Conductor/INVARIANTS.md`.
