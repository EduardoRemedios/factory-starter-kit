# Conductor Design Pack — 07 Open Questions → Decisions

All ten questions were decided by Eduardo dos Remedios on 2026-09-04. Defaults that were accepted are marked as such; one default was overridden.

| # | Question | Decision | Effect on 06 §1 |
|---|---|---|---|
| 1 | Rename internal identifiers now or later? | **Rename now, in 0.3.0** (overrides default). `docs/Factory` → `docs/Conductor`, `factoryctl` → `conductorctl`, `factory_*.py` → `conductor_*.py`, plugin ids `factory`/`factory-bmad` → `conductor`/`conductor-bmad`, slash namespace `/conductor:`, reason codes `FACTORY_*` → `CONDUCTOR_*`, skills `.agents/skills/factory-*` → `conductor-*`. | Rename becomes **step 2**, immediately after golden packs, so every later step is built on the new names. Golden packs keep their historical `FACTORY_*` content; pack-lint gains a compatibility path resolution for them. |
| 2 | Manifest mandatory on all execution runs once the Statement of Completion exists? | Yes, **after the pilot** (default accepted). Warning level during the pilot. | Step 13 stays post-pilot |
| 3 | Public or private marketplace? | **Public** (default accepted) | INSTALL.md uses the public GitHub marketplace |
| 4 | Cursor skill? | **Skip Cursor for now**; revisit after the pilot. Cursor still works via AGENTS.md + CLI with no dedicated work. | Q4 becomes an optional smoke check, not a qualification gate; `adapters/cursor.md` is a one-paragraph note |
| 5 | TEA evidence-only set | Default accepted: test-design, nfr, trace, test-review, teach-me-testing; framework stays delivery | Step 7 |
| 6 | Gap Request authorship | Default accepted: agent authors, human resolves | Step 8 |
| 7 | Retrospective and check-implementation-readiness lane | Default accepted: delivery | Step 7 |
| 8 | Recall trigger | Default accepted: `when_index_nonempty` | Step 6 |
| 9 | Archived V2 docs after step 12 | Default accepted: tag `factory-lineage-v0.2.5` only, plus golden packs | Step 12 |
| 10 | Any Factory_V3 concept required? | Confirmed: none | — |

## Decisions already closed (brief §0), restated for the build

Conductor naming on user-facing surfaces (**reversed 2026-09-04**: the public product name stays Factory; Conductor is the working name kept as plugin id, command namespace, and `docs/Conductor/` path) · 0.2.5 candidate merged as last Factory-lineage release (`7d0d20e`, tag `factory-lineage-v0.2.5`) · MS-06 not executed, archived · party mode allowed in the product-context lane · no workshop; self-serve onboarding · rehearsal on the local AuditEdge clone before handover · brief and pack internal until after the pilot.
