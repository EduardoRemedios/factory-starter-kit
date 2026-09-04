# Conductor Design Pack — 07 Open Questions (human decision required)

Not resolved by assumption. Each names the default the pack was written against so the build can start; a different answer changes the marked steps in 06 §1.

| # | Question | Default assumed in this pack | Affects |
|---|---|---|---|
| 1 | Rename internal identifiers (`docs/Factory` → `docs/Conductor`, `factoryctl` → `conductorctl`, plugin ids `factory` → `conductor`, reason codes `FACTORY_*` → `CONDUCTOR_*`) in 0.3.0, or user-facing names only in 0.3.0 and internals in 0.3.x? | User-facing in 0.3.0 (step 11); internals deferred. Only Eduardo's clone has a Factory install, so the cost is lowest now, but a full rename touches ~200 files and every test string. | Steps 4, 9, 11, 12 |
| 2 | Does adopting the Statement of Completion make the verification manifest mandatory on all execution runs? | Yes, at step 13 (post-pilot). Warning level during the pilot. | Steps 4, 13 |
| 3 | Public GitHub marketplace, or private for the pilot? | Public (repo is public today; onboarding docs are customer-neutral by test). Private adds a credential step per developer. | Step 14, INSTALL.md |
| 4 | Cursor: accept CLI-only operation for the pilot, or add a Cursor skill wrapping doctor/progress? | CLI-only; add a skill only if the friction log asks. | Q4 |
| 5 | Which TEA design-level workflows are in `evidence_only` on day one? | `test-design`, `nfr`, `trace`, `test-review`, `teach-me-testing`. `framework` stays delivery. | Step 7, AC-L5 |
| 6 | May the agent author Gap Requests, or must a human? | Agent authors; human resolves. `resolution` is the only human-written block. | Step 8, AC-L6 |
| 7 | `bmad-retrospective` and `bmad-check-implementation-readiness`: delivery lane (default) or product-context? | Delivery. Both read sprint/story state. | Step 7 |
| 8 | Recall trigger default: `when_index_nonempty` or `always`? | `when_index_nonempty`. | Step 6, Project Config |
| 9 | Do the archived Factory V2 docs (`ORCHESTRATION.md`, `STAGE_CONTRACTS.md`) stay in the repo under `docs/Conductor/archive/` after step 12, or move to a tag only? | Tag only (`factory-lineage-v0.2.5`), plus golden packs in tests. | Step 12 |
| 10 | Any Factory_V3 concept required? | None identified. The pack imports nothing from the private V3 repository. | — |

## Decisions already closed (brief §0), restated for the build run

Conductor naming on user-facing surfaces · 0.2.5 candidate merged as last Factory-lineage release · MS-06 not executed, archived · party mode allowed in the product-context lane · no workshop; self-serve onboarding · rehearsal on the local AuditEdge clone before handover · brief and pack internal until after the pilot.
