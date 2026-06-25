# Changelog

## 2026-06-25

- Added Kilo External Lane Mode as an optional reliable path for model-routed Factory stages, including a reusable Codex orchestration prompt.
- Hardened the Kilo Code CLI stage runner after field testing: it now rejects nested Kilo execution by default, uses a per-run stage lock, and records timeout failures.
- Added `docs/Factory/Harnesses/KILO.md` for Kilo Code CLI model-routed Factory stage lanes.
- Added `./scripts/factoryctl kilo-stage` with dry-run support, per-stage prompts, Kilo `--model` routing, JSON evidence, and post-run write-boundary checks.
- Linked the Kilo harness from `docs/Factory/Harnesses/README.md` and `docs/Factory/ORCHESTRATION.md`.
- Updated `docs/PROJECT_STATE.md` and `docs/ROADMAP.md`.

## 2026-06-24

- Added `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` with beginner setup steps for local project folders, Cursor, Claude, Codex, and first Factory setup prompts.
- Linked the non-technical guide from `README.md`, `docs/onboarding/ONBOARDING_GUIDE.md`, `docs/Factory/ARCHITECTURE.md`, and `docs/Factory/ORCHESTRATION.md`.
- Added review/merge handoff discipline to the starter-kit Factory process.
- `docs/Factory/MERGE_PROTOCOL.md` now separates `REVIEW_READY` from `MERGE_READY`, defines final sync window behavior, and preserves merge-preflight authorization.
- `docs/Factory/ORCHESTRATION.md` and `docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md` now carry branch/PR handoff-state guidance.
- Updated `docs/PROJECT_STATE.md` and `docs/ROADMAP.md`.

## 2026-05-25

- Restored this repository's project state and roadmap to Factory V2 and earlier scope.
