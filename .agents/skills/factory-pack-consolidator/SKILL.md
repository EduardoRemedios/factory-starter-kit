---
name: factory-pack-consolidator
description: Consolidate a Factory pack during Stage J. Use when Codex is asked to create or repair PACK_MANIFEST.md, create or repair PACK_CHECKLIST.md, verify required pack artifacts are present and non-empty before Stage I2, instantiate the Purple Gate checklist, or prepare a completed pack for pack-lint.
---

# Factory Pack Consolidator

## Workflow

1. Read `docs/Factory/Spec/STAGE_CONTRACTS.md`, `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md`, and `docs/Factory/templates/PACK_MANIFEST_TEMPLATE.md`.
2. Inspect the run root and `pack/` directory on disk.
3. Create or update `pack/PACK_MANIFEST.md` with every required artifact and non-empty status.
4. Create or update `pack/PACK_CHECKLIST.md` by instantiating checklist item IDs and wording exactly.
5. Mark `PACK_AUDIT_REPORT.md` as pending only before I2; after I2 it must be present and non-empty.
6. Do not adjudicate quality. Stage J is mechanical packaging; Purple owns judgment.
7. Run `./scripts/factoryctl stage-lint --run <RUN_ID> --stage J` after writing the handoff.

## Required Checks

- run-root evidence exists: `raw_brief.md`, `KNOWLEDGE_LINT.txt`, `CONTEXT_RECALL_REPORT.md`, `EXECUTION_MODE.txt`, `SPRINT_ID.txt`
- pack artifacts exist and are non-empty
- handoff files exist for completed stages
- checklist answers have evidence fields
- unresolved placeholders are removed from Stage J outputs

## Outputs

Return:
- manifest path
- checklist path
- missing or empty artifacts
- checklist items still requiring Purple judgment
- stage-lint result
