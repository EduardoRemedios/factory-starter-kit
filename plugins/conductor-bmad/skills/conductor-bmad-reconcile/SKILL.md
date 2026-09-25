---
name: conductor-bmad-reconcile
description: Run the grooming loop for one Spec (inspect inputs, draft scope and questions, hand questions to BMAD, review changed inputs, refresh the draft) and stop at an objective G1 exit.
---

# Factory BMAD Reconcile

Use this when a person names a Spec and wants it ready for Factory G1. You prepare
identifiers, records and questions; people answer questions, review inputs and
approve. Nothing here promotes a snapshot, answers a question or locks intent.

## Loop

1. **Inspect inputs.** Preview the Spec package without writing:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . promote --source <SPEC folder> --repo-companion <path> ... --snapshot-id <generated> --workflow spec --evidence-type SOLUTION_CONTEXT --authority EVIDENCE_ONLY --plan-identity <generated> --reviewer "<person who will review>" --review-ref "<where the review is recorded>" --git-binding`.
   Generate the snapshot ID (for example `spec-042-v1`) and plan identity yourself. Show the person the file list and digests.
2. **Draft scope and questions.** Create or resume the run with `./scripts/conductorctl run-init --slug <short-name>`. Draft `intent_pack.json` from the reviewed inputs. Every question only a person can answer becomes `./scripts/conductorctl gap open --run <RUN_ID> --requirement <R-ID> --type <type> --question "<one question>" --impact active_scope|future_only|unknown --owner "<person or role>"`. Do not guess answers and do not put decisions in the intent.
3. **Hand questions to BMAD.** `./scripts/conductorctl gap export --run <RUN_ID>` writes `UPSTREAM_QUESTIONS.md`. The person runs `bmad-spec` to update the existing Spec with that file as its input. BMAD records answers in the Spec's `.memlog.md` and re-derives `SPEC.md`; PRD, architecture and UX sources change only through their own BMAD workflows. Never edit `SPEC.md` or a snapshot by hand.
4. **Review changed inputs.** Re-run step 1's preview. If any input changed, the person reviews the new package; promote a superseding snapshot with `--supersedes-snapshot-id` and `--supersedes-sha256` after they approve the exact plan ID. Earlier snapshots stay unchanged.
5. **Refresh the draft.** Cite the new snapshot in the intent, record each answer with `gap resolve` only when the person gives it (`--decided-by` is the person), then `./scripts/conductorctl review-packet --run <RUN_ID>`.

## Exit

Stop the loop when `REVIEW_PACKET.md` reports **Ready for G1 review: yes**: no open
`active_scope` or `unknown` gap, every `future_only` finding has a named owner, and
every snapshot introduced by a decision is cited. Future-only findings never keep a
ready slice cycling. Hand the packet to the person for G1; do not write countersigns.
