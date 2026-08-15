# Changelog

## 2026-08-15

- Added Factory-only Claude Code CLI rollout hardening: a read-only local
  prerequisite preflight, a guided first-team playbook, updated Greenfield-first
  quick-start guidance, and a separate optional integration routing matrix that
  keeps Factory standalone adoption first-class.
- Uplifted the Factory-only plugin source and generated Claude/Codex packages
  from `0.2.0` to `0.2.3`, including the repaired runtime, validation,
  execution-closeout, project-preflight, pack/stage lint, launcher, package
  builder, templates, project seeds, and focused regression fixtures.
- Updated public README installation references to the `0.2.3` release
  candidate and added a first-tester handoff for the pre-team CLI pilot.

## 2026-08-05

- Prepared Factory plugin technical RC `0.2.0` from the single authored source for deterministic Codex and Claude Code packages.
- Added generic promoted-upstream evidence indexing and an optional, schema-locked, bounded Stage A project preflight without adding domain-specific policy to Factory Core.
- Added transactional Greenfield bootstrap for absent or empty targets, including Git initialization, exact-plan approval, post-apply validation, interruption recovery, and guarded rollback that preserves changed Git state.
- Made the pilot documentation customer-neutral and documented supported Claude plugin-root resolution.
- Completed bounded two-lane Claude composition proof and full regression/privacy/no-touch closeout; RC `0.2.0` is technical `REVIEW_READY`.
- Retained the formal pilot and all maintainer commit, tag, publication, and rollout actions as separate remaining gates.

## 2026-07-27

- Replaced copy-first README onboarding with plugin-first installation for the ChatGPT/Codex desktop app, Claude Code desktop, and Claude Code CLI.
- Added a developer FAQ covering Factory orchestration, Claude instruction bridging, model roles, coding standards, regression testing, specifications, product vision, NFRs, evidence storage, determinism, brownfield safety, and comparisons with GSD and BMAD.
- Prepared the privacy-safe dual-platform Factory plugin release candidate for merge to `main`; the independent pilot and stable release tag remain separate gates.

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
