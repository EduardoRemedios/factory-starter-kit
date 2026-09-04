# First exercise with BMAD: product context in, governed run out

Companion to `docs/Conductor/onboarding/FIRST_EXERCISE.md`. Same 45 minutes, but the intent comes from a promoted BMAD snapshot instead of a plain brief, which is how a product-context team will actually work. Keep the friction log open.

## 0. Start

`/conductor-bmad:doctor`. Expect `BOTH_PRESENT` and a canonical layout. If it reports `CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT`, follow the quick start: declare the existing root in `PROJECT_CONFIG.json` or archive it as legacy evidence. Do not bootstrap a second install.

## 1. Discovery in the product-context lane

Run `bmad-product-brief` for a small feature. Notice the injected context: it names the product-context lane and says helpers may nest. Finish with `bmad-review-adversarial-general` and, if you like, `bmad-party-mode`. Both run. Now try `bmad-dev-story` from inside the same session. Expect a one-line denial naming the reason code, `delivery` lane, layout state, `Allowed here:`, and `Next:`. That denial is the only thing Conductor blocks.

## 2. Promote

Human-review the brief in `_bmad-output/`, then `/conductor-bmad:promote`. Expect an immutable snapshot under `docs/upstream/bmad/<SNAPSHOT_ID>/` with `SNAPSHOT_MANIFEST.json` and an aggregate SHA-256. The brief is now citable evidence and nothing more.

## 3. G1 from the snapshot

Create the run as in the plain exercise. In `intent_pack.json`, add the snapshot as a source:

```json
{ "kind": "upstream_snapshot", "ref": "docs/upstream/bmad/<SNAPSHOT_ID>/SNAPSHOT_MANIFEST.json", "sha256": "<its sha256>" }
```

`contract-lint intent` verifies the digest. Lock it with a countersign. Later BMAD edits cannot alter this run's scope: that is the freeze.

## 4. G2 and G3

Exactly as in the plain exercise. Before writing the Statement, open one Gap Request with `--type product_context --impact active_scope` asking whether the brief's success measure still holds. Resolve it as the human **with** `--new-snapshot-id` and `--new-snapshot-sha256` pointing at a second promotion. Run `contract-lint completion`: expect `CONDUCTOR_CONTRACT_G1_REOPEN_REQUIRED`. That is the supersession rule: new product context that touches active scope sends the run back to G1 rather than silently changing it. Resolve a second gap with `--impact future_only` instead and watch completion pass.

## What you have proven

BMAD keeps evolving product context freely, including with party mode and reviews. Conductor governs delivery against one exact, human-approved snapshot at a time. Feedback flows back as artifacts, and superseding context reopens intent instead of drifting it.
