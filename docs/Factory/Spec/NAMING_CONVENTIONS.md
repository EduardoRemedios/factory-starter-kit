# docs/Factory/Spec/NAMING_CONVENTIONS.md — Doc Factory (v4.2)

## Version
v4.2

## Change Log
- v4.2 (2026-02-12): Promoted `EXECUTION_PROMPT.md` from optional to required post-I2 PASS + human GO.
- v4.1 (2026-02-10): Fixed envelope filename contract to `<SPRINT_ID>_ENVELOPE*.md` and added explicit anti-double-prefix rule.
- v4 (2026-02-08): Updated to reflect Stage J → I2 reordering (STAGE_CONTRACTS v4). No naming changes — handoff filenames unchanged. Added EXECUTION_PROMPT.md as optional run-root artifact.
- v3.1 (2026-02-07): Added applicability section clarifying that Factory v2 applies from Phase 1 forward.
- v3 (2026-02-06): Canonicalized Stage I½ to STAGE_I2 (handoff naming), added raw_brief.md + SPRINT_ID.txt requirements explicitly, and aligned required handoff filenames.

## 0. Applicability (HARD)
The Factory pipeline (v2) applies to all Harmony sprints from **Phase 1 forward**.

Phase 0 sprints (Sprint 00 through Sprint 03) predated the Factory pipeline and were executed manually. Their artifacts live in `docs/sprints/` and follow an earlier, informal convention (envelope + test plan + completion report). Phase 0 artifacts are not governed by these naming conventions and are preserved as-is for traceability.

All new sprint work MUST use the Factory pipeline. The orchestration guide (`docs/Factory/ORCHESTRATION.md`) describes how to initiate and run the pipeline end-to-end.

## 1. Root locations (HARD)
- Factory specs: `docs/Factory/Spec/`
- Templates: `docs/Factory/templates/`
- Runs (output packs): `docs/Factory/runs/`

## 2. Run directory (HARD)
Each factory run creates:
- `docs/Factory/runs/<RUN_ID>/`

RUN_ID format (HARD):
- `RUN_YYYYMMDD_HHMM_<TAG>`
  - Example: `RUN_20260206_0930_factory`
  - `<TAG>` default: `factory`

Run root required files:
- `raw_brief.md`
- `SPRINT_ID.txt` (created in STAGE_H)
- `EXECUTION_PROMPT.md` (required post-I2 PASS + human GO, created per ORCHESTRATION.md §6.1)

## 3. Pack directory (HARD)
The sprint doc pack directory:
- `docs/Factory/runs/<RUN_ID>/pack/`

## 4. Sprint ID (HARD)
Sprint ID format:
- `SPRINT_YYYYMMDD_NNN` (NNN is zero-padded, 001..999)
- Assigned in STAGE_H
- Must be unique across the repository
- Stored in `docs/Factory/runs/<RUN_ID>/SPRINT_ID.txt`

## 5. Required artifact filenames (HARD)
Within `docs/Factory/runs/<RUN_ID>/pack/`:

Core:
- `intent.md`
- `intent_redteam.md`
- `intent_synthesis.md`
- `intent_lock_report.md`
- `premortem.md`
- `risk_register.md`
- `verification_plan.md`
- `micro_sprints.md`

Envelope:
- `<SPRINT_ID>_ENVELOPE.md`
- `<SPRINT_ID>_ENVELOPE_REDTEAM.md`

Important:
- `SPRINT_ID` already includes the `SPRINT_` prefix.
- Do not prepend another `SPRINT_` when constructing envelope filenames.

Verification assets:
- `fixtures/` (directory)
- `traceability_matrix.md`

Pack gates:
- `PACK_AUDIT_REPORT.md`
- `PACK_MANIFEST.md`
- `PACK_CHECKLIST.md`

Handoffs:
- `HANDOFF/` (directory)
  - `HANDOFF_STAGE_A.md`
  - `HANDOFF_STAGE_B.md`
  - `HANDOFF_STAGE_C.md`
  - `HANDOFF_STAGE_D.md`
  - `HANDOFF_STAGE_E.md`
  - `HANDOFF_STAGE_F.md`
  - `HANDOFF_STAGE_G.md`
  - `HANDOFF_STAGE_H.md`
  - `HANDOFF_STAGE_I.md`
  - `HANDOFF_STAGE_I2.md`
  - `HANDOFF_STAGE_J.md`
  - (optional) `HANDOFF_SUMMARY.md`

## 6. Versioning (HARD)
Artifacts may be preserved with suffixes:
- `*_v1.md`, `*_v2.md`, etc.

Canonical artifact is always the non-suffixed filename (e.g., `intent.md`) and must match the latest version content.

Every artifact must include:
- `## Version`
- `## Change Log` (format defined in `DEFINITIONS.md`)

## 7. Fixtures naming (HARD)
Fixtures live under:
- `pack/fixtures/<AREA>/<NAME>/`

Each fixture directory contains:
- `input.json` or `input.yaml`
- `expected.json` or `expected.yaml`
- `notes.md` (1–10 bullets max)

AREA rules:
- Core areas allowed: `intent`, `policy`, `routing`, `verification`, `envelope`
- Domain areas allowed ONLY IF:
  1) listed explicitly in `pack/intent.md` under **Scope → Domain Areas**
  2) recorded in `pack/traceability_matrix.md`

## 8. No naming forks (HARD)
If a file is listed as required above:
- it must exist with that exact name
- it must be non-empty
