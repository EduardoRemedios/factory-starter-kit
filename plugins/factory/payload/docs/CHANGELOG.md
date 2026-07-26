# Changelog

## 2026-07-26

- Passed live Claude Code CLI and Desktop Doctor, Brownfield, Progress, and Validate journeys against Factory plugin `0.1.0`.
- Closed all defects found during Claude technical verification, including setup routing, exact-plan approval wording, and validation bytecode cleanliness.
- Moved public golden fixtures into `tests/plugin_fixtures/` so the open-source test suite does not depend on private run or pilot evidence.
- Added a public-release privacy regression that rejects organization-specific names, local usernames, and personal-communication references from published plugin surfaces.
- Added GitHub marketplace installation guidance for both Codex and Claude packages.
- Added Apache-2.0 license and repository metadata to both generated plugin packages.

## 2026-07-24

- Built Factory plugin `0.1.0` from one authored source into deterministic Codex and Claude Code packages.
- Added plugin-first Doctor, Greenfield, Brownfield, Progress, Run, Validate, and Update journeys with preview-before-write, exact-plan approval, durable receipts, and rollback.
- Passed Codex app marketplace loading, Brownfield adoption, disposable Greenfield setup, validation, update, and exact rollback restoration.
- Found and fixed `CODEX-PILOT-001`, which could have included project-specific installation state in regenerated plugin payloads; added regression coverage.
- Passed 58 automated tests, knowledge lint, pack lint, deterministic package generation, protected-path verification, and whitespace checks.
- Recorded Claude CLI/Desktop verification and the formal two-user pilot as the remaining rollout gates.
- Updated `docs/PROJECT_STATE.md` and `docs/ROADMAP.md`.

## 2026-07-02

- Formalized Stage A direct-source repair for generated `CONTEXT_RECALL_REPORT.md` files that remain `Coverage Verdict: WEAK` after index refresh and fallback scopes.
- Updated Factory orchestration, stage contracts, and the context recall template with allowed and forbidden repair conditions, exact direct-source evidence fields, and downstream migration guidance.
- Hardened `pack-lint` so unrepaired `WEAK` recall still fails while `REPAIRED_DIRECT_SOURCE_CHECK` passes only with readable local sources, source summaries, and no material unresolved refs.
- Added unittest coverage for unrepaired weak recall, valid direct-source repair, missing source repair failure, and material unresolved ref failure.
- Updated `docs/PROJECT_STATE.md` and `docs/ROADMAP.md`.

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
