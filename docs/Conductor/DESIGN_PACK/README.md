# Conductor Design Pack

Design-only output for the Conductor lineage (successor to Factory V2). Produced 2026-09-04 from `docs/Conductor/CONDUCTOR_DESIGN_BRIEF.md` v1.0 on branch `conductor/design-pack`, base `7d0d20e` (main + merged 0.2.5 candidate). Internal until after the pilot.

| File | Content |
|---|---|
| `01_ARCHITECTURE.md` | Governing principle, three layers, three gates with entry/exit/validator, run layout, target repo tree, autonomy block |
| `02_BOUNDARY_AND_CHECK_MAPPING.md` | Per-boundary classification (keep/remove/reclassify), 657-check → gate mapping, continuity classification, orphan list |
| `03_CONTRACTS.md` | Field-level sketches for the eight contracts |
| (schemas) | Landed in step 2b: core contracts in `docs/Conductor/contracts/` (intent_pack, verification_manifest_v2, statement_of_completion, gap_request, project_config, evidence_receipt, countersign); adapter contracts in `docs/adapters/bmad/contracts/` (lane_policy, bmad_adapter_config). Tests: `tests/test_schemas.py` |
| `04_LANE_POLICY.md` | BMAD lane model, workflow classification, invoked-skill hook rule, layout rule, declared root, deny message, AC-L1..L6 → qualification |
| `05_DISPOSITION.md` | Per-file keep / rewrite / demote / delete / archive / create |
| `06_MIGRATION_AND_QUALIFICATION.md` | 14 mergeable steps, pilot scope guard, ablation note, Q1–Q8 qualification, onboarding deliverable |
| `07_OPEN_QUESTIONS.md` | Ten human decisions with the defaults assumed |

## Acceptance against brief §14

| Criterion | Where satisfied |
|---|---|
| Every §5 contract has a field-level schema sketch | 03 + `docs/Conductor/contracts/` and `docs/adapters/bmad/contracts/` (9 files) |
| Every existing lint check appears in the G1/G2/G3 mapping or in the orphan list | 02 §2 (by check family, with counts totalling 657) and 02 §4 (≈91 orphans) |
| Every §6 acceptance criterion maps to a qualification step | 04 §9 ↔ 06 §4 |
| Migration sequence's first step is the golden-pack fixture | 06 §1 step 1 |
| Open questions listed, not resolved by assumption | 07 (defaults stated, marked as assumptions) |

## Source verification note

Model-behavior claims cite only the brief §3 table. Anthropic guides and OpenAI developer docs and system card were fetched and verified on 2026-09-04; the two openai.com posts were not fetchable and are not cited as verified.
