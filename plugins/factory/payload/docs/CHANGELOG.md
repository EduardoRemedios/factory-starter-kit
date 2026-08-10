# Changelog

## 2026-08-10

- Repaired the Factory plugin Greenfield CLI bootstrap so an invocation without
  `--root` uses the current directory only for Greenfield, while Doctor and all
  established-project commands retain Git-root discovery.
- Corrected new-project guidance to run Greenfield before Doctor, repeat the
  same explicit target for preview and apply, and never invent a target or
  translate generic approval into a plan ID.
- Added subprocess regression coverage across authored, Claude, and Codex
  runtimes for empty, explicit absent/spaced, rejected nonempty, Doctor-outside-Git,
  help-text, and preview no-mutation behavior.
- Added a fail-closed Claude Greenfield exception for the exact
  `.claude/settings.local.json` bootstrap shape. The plan digest-pins the
  read-only file and directory state, excludes it from Factory ownership and
  writes, fails stale before Git on any change, and preserves it through apply,
  recovery, and rollback.
- Corrected genuinely non-empty non-Git guidance so Brownfield is recommended
  only for an existing Git project, while Codex and all broader non-empty cases
  remain blocked.

## 2026-08-05

- Prepared Factory plugin technical RC `0.2.0` from the single authored source for deterministic Codex and Claude Code packages.
- Added generic promoted-upstream evidence indexing and an optional, schema-locked, bounded Stage A project preflight without adding domain-specific policy to Factory Core.
- Added transactional Greenfield bootstrap for absent or empty targets, including Git initialization, exact-plan approval, post-apply validation, interruption recovery, and guarded rollback that preserves changed Git state.
- Made the pilot documentation customer-neutral and documented supported Claude plugin-root resolution.
- Completed bounded two-lane Claude composition proof and full regression/privacy/no-touch closeout; RC `0.2.0` is technical `REVIEW_READY`.
- Retained the formal pilot and all maintainer commit, tag, publication, and rollout actions as separate remaining gates.
- Added schema-locked execution closeout and read-time progress revalidation so
  completed execution reports `REVIEW_READY`, `NO_GO`, or `BLOCKED` without
  granting merge, tag, publication, adapter, phase, or mission authority.
- Reconstructed RC `0.2.0` in a retained clean review worktree and verified the
  final generated packages, Claude composition, full regression, privacy, and
  protected-source no-touch behavior.
- Repaired the maintainer-review path-safety blocker in execution-closeout and
  project-preflight evidence writes by rejecting symlinked run-root ancestors
  before filesystem reads or writes.
- Added adversarial coverage for symlinked `docs`, `docs/Factory`, and
  `docs/Factory/runs`, including explicit proof that no outside closeout or
  preflight evidence file is created, then rebuilt both plugin packages.
- Independently reran all 12 release verification checks with complete retained
  transcripts; every check passed and the candidate remained `REVIEW_READY`.
- Prepared a customer-neutral public review surface containing the authored
  plugin source, deterministic packages, canonical documentation, and
  reproducible tests while keeping project-specific run evidence out of the
  public distribution.

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
