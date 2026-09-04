# Conductor in one page

## What it governs

Conductor governs three things about AI-assisted delivery work and nothing else:

| It decides | By means of |
|---|---|
| **Authority**: who may authorize what, against which exact artifact | Human countersign files that pin a SHA-256; hash-pinned intent and upstream snapshots |
| **Proof**: what evidence backs a claim | Receipts written by a runner, never by the agent; a Statement of Completion whose state is computed, not asserted |
| **Write boundary**: where changes may land | Protected roots compared before and after the run |

It does not tell the model how to think or in which order to work. The model owns the how. Read `docs/Conductor/INVARIANTS.md` and `docs/PROJECT_STATE.md`; everything else is on demand.

## Three gates

```
G1 Intent Lock ──(human countersign)──▶ G2 Governed Execution ──(receipts, postimage)──▶ G3 Review + Completion ──(human countersign)──▶ REVIEW_READY
```

- **G1 Intent Lock.** The agent drafts `intent_pack.json` (goal, requirements with acceptance, constraints, scope in/out, sources with digests, verification requirements, budget). `conductorctl contract-lint intent` must pass. A human writes `countersign/INTENT_LOCK.json`. Nothing proceeds on a draft.
- **G2 Governed Execution.** One autonomous run inside the locked scope. Checks are declared in `verification_manifest.yaml`; `conductorctl receipts run` executes them and writes signed receipts; `conductorctl postimage capture` and `compare` prove no protected file changed. `EXECUTION_ENABLED` runs also need `countersign/EXECUTION_GO.json`.
- **G3 Adversarial Review and Completion.** A fresh-context verifier that did not do the work audits every claim against its receipt. The Statement of Completion maps every requirement to evidence; `contract-lint completion` derives READY, BLOCKED, or NEEDS_HUMAN_DECISION. A human writes `countersign/COMPLETION.json`. Merge authorization then follows `MERGE_PROTOCOL.md` unchanged.

Humans are involved at exactly two points per run, three when execution is enabled.

## Two lanes for upstream tools

Product-context tools installed through an adapter author candidate context in their own workspace. Their output becomes citable only when a human promotes it to an immutable, hash-pinned snapshot, and even then G1 may accept, reject, or defer it. Their delivery-lane workflows are prohibited for Conductor-bound work. Questions from a run go back to that lane as Gap Requests (`conductorctl gap open`), not as chat questions.

## Five commands

| Command | What it does |
|---|---|
| `/conductor:doctor` | Read-only diagnosis and the one next legal action |
| `/conductor:greenfield` / `/conductor:brownfield` | Preview and apply adoption by exact plan ID |
| `/conductor:run` | Continue the current run through its next gate |
| `/conductor:validate` | Run the deterministic checks for the current state |
| `/conductor:progress` | Gate state from evidence: waiting for a human, in progress, or blocked with reasons |

## Where things live

```
docs/Conductor/runs/<RUN_ID>/
  intent_pack.json            verification_manifest.yaml     statement_of_completion.json
  receipts/<CHECK>.json       postimage/{preimage,compare}.json
  countersign/{INTENT_LOCK,EXECUTION_GO,COMPLETION}.json     gap_requests/GAP-*.json
```

Everything the agent writes is schema-validated or explicitly labelled non-authority (`notes/`). A countersign is a small JSON file a human writes; the schema is `docs/Conductor/contracts/countersign.schema.json`.

## Three things people get wrong at first

1. A countersign whose digest no longer matches its file is stale and grants nothing. Re-sign after any edit.
2. `verified` in a Statement row means a PASS receipt exists for that check. Prose does not make a row verified.
3. `REVIEW_READY` is a review handoff. Only the merge protocol produces `MERGE_READY`.
