# docs/Factory/Spec/NAMING_CONVENTIONS.md — Doc Factory (v4.5)

## Version
v4.5

## Change Log
- v4.5 (2026-03-21): Added required run-root `CONTEXT_RECALL_REPORT.md` and required Mission Mode artifact `MISSION_CONTEXT_RECALL_REPORT.md`.
- v4.4 (2026-03-10): Added run-root `MISSION_LINT.txt` naming contract for runs operating under Mission Mode.
- v4.3 (2026-02-27): Added Mission Mode naming contract (`docs/Factory/missions/<MISSION_ID>/` with required `MISSION_*` artifacts).
- v4.2 (2026-02-12): Promoted `EXECUTION_PROMPT.md` from optional to required post-I2 PASS plus human GO.
- v4.1 (2026-02-10): Fixed envelope filename contract to `<SPRINT_ID>_ENVELOPE*.md` and added explicit anti-double-prefix rule.
- v4.0 (2026-02-08): Updated to reflect the `STAGE_J -> STAGE_I2` reordering and added `EXECUTION_PROMPT.md` as an optional run-root artifact.

## 0. Applicability (HARD)
The Factory pipeline applies to all governed project sprints after adoption.

Pre-adoption project sprints may follow older conventions and can be preserved as historical references outside the governed Factory naming contract.

All new sprint work MUST use the Factory pipeline.

## 1. Root locations (HARD)
- Factory specs: `docs/Factory/Spec/`
- Templates: `docs/Factory/templates/`
- Product Owner docs: `docs/Factory/ProductOwner/`
- Runs: `docs/Factory/runs/`
- Missions: `docs/Factory/missions/`

## 2. Run directory (HARD)
Each Factory run creates:
- `docs/Factory/runs/<RUN_ID>/`

`RUN_ID` format:
- `RUN_YYYYMMDD_HHMM_<TAG>`
- default tag: `factory`

Run-root required files:
- `raw_brief.md`
- `CONTEXT_RECALL_REPORT.md`
- `SPRINT_ID.txt`
- `EXECUTION_PROMPT.md` (required post-I2 PASS plus human GO)
- `MISSION_LINT.txt` (required only when the run operates under Mission Mode)

## 3. Pack directory (HARD)
The sprint doc pack directory:
- `docs/Factory/runs/<RUN_ID>/pack/`

## 3.1 Mission directory (HARD, Mission Mode only)
Each mission creates:
- `docs/Factory/missions/<MISSION_ID>/`

`MISSION_ID` format:
- `MISSION_YYYYMMDD_NNN`

## 4. Sprint ID (HARD)
`SPRINT_ID` format:
- `SPRINT_YYYYMMDD_NNN`
- assigned in `STAGE_H`
- stored in `docs/Factory/runs/<RUN_ID>/SPRINT_ID.txt`

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

Verification assets:
- `fixtures/`
- `traceability_matrix.md`

Pack gates:
- `PACK_AUDIT_REPORT.md`
- `PACK_MANIFEST.md`
- `PACK_CHECKLIST.md`

Handoffs:
- `HANDOFF/`
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
  - optional `HANDOFF_SUMMARY.md`

Important:
- `SPRINT_ID` already includes the `SPRINT_` prefix
- do not prepend another `SPRINT_` when constructing envelope filenames

## 6. Versioning (HARD)
Artifacts may be preserved with suffixes:
- `*_v1.md`
- `*_v2.md`

The canonical artifact is always the non-suffixed filename and must match the latest version content.

Every artifact must include:
- `## Version`
- `## Change Log`

## 7. Fixtures naming (HARD)
Fixtures live under:
- `pack/fixtures/<AREA>/<NAME>/`

Each fixture directory contains:
- `input.json` or `input.yaml`
- `expected.json` or `expected.yaml`
- `notes.md`

`AREA` rules:
- core areas allowed: `intent`, `policy`, `routing`, `verification`, `envelope`
- domain areas allowed only if:
  1. listed explicitly in `pack/intent.md` under scope or domain areas
  2. recorded in `pack/traceability_matrix.md`

## 8. No naming forks (HARD)
If a file is listed as required above:
- it must exist with that exact name
- it must be non-empty

## 9. Mission artifact filenames (HARD, Mission Mode only)
Within `docs/Factory/missions/<MISSION_ID>/`:
- `MISSION_MANIFEST.md`
- `MISSION_CONTEXT_RECALL_REPORT.md`
- `MISSION_CHECKPOINT.md`
- `MISSION_COMPLETION_REPORT.md`
- optional `MISSION_EXECUTION_PROMPT.md`
