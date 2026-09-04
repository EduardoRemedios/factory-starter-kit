# Golden packs

Frozen copies of two qualified Factory V2 runs. They exist so that changes to
pack-lint, stage contracts, or templates cannot silently invalidate evidence
that a human already accepted.

| Run | What it is | Origin |
|---|---|---|
| `RUN_20260902_0725_factory_bmad_025_solution_context_integration` | Factory-BMAD 0.2.5 solution-context integration; MS-01..MS-05 closed; human evidence review ACCEPTED | `docs/Factory/runs/` at tag `factory-lineage-v0.2.5` |
| `RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification` | MS-06 disposable qualification planning run; complete through I2, Purple PASS; MS-06 execution not performed | same |

Rules:

- Do not edit these files. If a linter change legitimately requires them to
  change, that is a compatibility break: record it in the change and update
  `tests/test_golden_packs.py` in the same commit.
- Evidence paths inside the packs reference `artifacts/verification/<RUN_ID>/`
  at the repository root; those directories must stay in place for the packs
  to lint.
- Conductor's `contract-lint` must keep passing these packs under its Factory
  compatibility mode until the Factory lineage is formally retired
  (design pack 06 §1, steps 4 and 12).
