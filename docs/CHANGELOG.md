# Changelog

## 2026-09-04

- Began the Conductor lineage. Merged the qualified Factory-BMAD 0.2.5
  candidate to `main` as the last Factory-lineage release (tag
  `factory-lineage-v0.2.5`) and archived the MS-06 planning run as V2
  qualification evidence; MS-06 execution was not performed.
- Added the Conductor design brief and design pack under `docs/Conductor/`
  (three gates, contracts with JSON Schemas, BMAD lane policy, disposition,
  migration, qualification, decided open questions).
- Migration step 1: golden-pack regression fixtures under `tests/golden_packs/`
  with `tests/test_golden_packs.py`.
- Migration step 2: renamed internal identifiers from Factory to Conductor
  (`docs/Factory` -> `docs/Conductor`, `factoryctl` -> `conductorctl`,
  `factory_*` scripts and modules -> `conductor_*`, `FACTORY_*` reason codes
  -> `CONDUCTOR_*`, plugin ids `factory`/`factory-bmad` ->
  `conductor`/`conductor-bmad`, slash namespace `/conductor:`). Historical
  run evidence and golden packs keep their original identifiers. Installation
  state written by Factory <= 0.2.5 (`factory_version`) is still readable.

## 2026-09-03

- Deterministically qualified the integrated Factory-BMAD 0.2.5 solution-context
  candidate under
  `RUN_20260902_0725_factory_bmad_025_solution_context_integration`: MS-04
  regenerated both derived packages (exactly 18 modified generated files, 9/9
  gate PASS) and the MS-05 corrective activation passed the complete 339-test
  discovery suite, all governance lints, and full no-touch verification. Human
  evidence review accepted the run; achieved status is
  `FACTORY_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`.
- Repaired the run's planning pack after a fail-closed MS-05 pre-activation
  stop: added the executable `pack/verification_manifest.yaml` binding VM-001
  through VM-015, restored VM-011 to its traceability cell, and recorded the
  run's first canonical `EXECUTION_CLOSEOUT.json` (`REVIEW_READY`) through the
  updated closeout validator, which now survives restoration to
  `PLANNING_ONLY` and control archival.
- One ledgered corrective touch reconciled a stale bootstrap test expectation
  to the locked layout contract (public `FACTORY_BMAD_NON_CANONICAL_LAYOUT`
  with subordinate `layout_reason_code`). MS-06, BMAD workflow invocation,
  AuditEdge, merge, publication, pilot, and rollout remain separately gated
  and unclaimed.

## 2026-08-27

- Added fail-closed Factory-BMAD detection for nested BMAD installs such as
  `bmad/_bmad`. Doctor and Audit now report
  `FACTORY_BMAD_NON_CANONICAL_LAYOUT` instead of treating nested BMAD as absent
  or suggesting bootstrap, and the audit evidence preserves nested module and
  capability classifications including `bmad-loop` blockers.

## 2026-08-24

- Advanced the coordinated Factory and Factory-BMAD Claude Code candidate to
  `0.2.5` for first-team CLI rollout readiness after Mark verified the F10
  cache-integrity guard on `0.2.4`.
- Clarified that `claude plugin prune` is dependency-state cleanup and may leave
  cached payload directories on disk; rollout preflight remains the authority
  for same-version cache integrity.
- Improved Factory and Factory-BMAD concise output by labelling approval values
  as `Approval Plan ID`; Factory-BMAD bootstrap also labels the separate
  inventory digest as `Pre-inventory SHA-256`, reducing approval-gate ambiguity
  for first-team testers.

## 2026-08-22

- Advanced the coordinated Factory and Factory-BMAD Claude Code candidate to
  `0.2.4` after first-tester greenfield, brownfield-neither, and BMAD-only
  brownfield rehearsals passed on the repaired `0.2.3` branch.
- Repaired the F10 rollout integrity blocker where Claude Code could silently
  reuse a stale same-version `factory` dependency cache during retest. The
  rollout preflights now compare same-version cached package bytes against the
  durable marketplace checkout and block stale-cache retests before install.
- Updated first-tester and first-team CLI handoff docs to uninstall both
  `factory-bmad` and `factory`, run `claude plugin prune`, rerun preflight, and
  only then reinstall from the durable checkout.

## 2026-08-15

- Added Claude Code CLI rollout hardening for first-team adoption: a read-only
  rollout preflight, a guided first-team playbook, a bootstrap recovery guide,
  and a compatibility policy that keeps Claude Desktop and broader organization
  rollout outside support until separately validated.
- Prepared coordinated Factory and Factory-BMAD `0.2.3` sources after the
  retained `0.2.2` live-verification halt, without modifying or cleaning the
  failed candidate, test root, isolated configuration, or evidence.
- Added runtime-owned no-bytecode protection before dynamic policy import and a
  zero-Claude verifier preflight for explicit binary/version, least-authority
  permissions, isolated configuration, evidence retention, and protected roots.
- Regenerated all four packages and passed 291 deterministic tests with three
  live-only tests skipped, plus package-current, privacy, policy, knowledge-lint,
  pack-lint, and source/generated-boundary checks. This deterministic checkpoint
  did not itself imply release or rollout.
- Closed the 0.2.3 live-recovery loop after authenticated Claude Code 2.1.233
  isolated live lanes passed for BMAD workflow enforcement, marketplace
  dependency composition, protected-root preservation, and pinned-candidate
  source coupling. The Factory-BMAD P1/P2 backlog is closed; publication,
  rollout, and the next fresh pilot remain separate decisions.
- Repaired an Odyssey v3 pilot finding where seeded project adapters could
  write Python bytecode despite the runtime no-bytecode policy. The
  `factory_bmad_policy_lint` and `factory_project_preflight` adapter front
  doors now disable bytecode before policy imports, all Factory-BMAD packages
  were regenerated, focused and full deterministic tests pass, and the Odyssey
  v3 retest shows no new bytecode with the retained pre-repair `.pyc` hash
  unchanged.
- Completed amended-source live requalification against detached candidate
  `334df09`. The first authenticated model-lane attempt halted because the
  isolated Claude config roots were not logged in; after authenticating fresh
  isolated configs, VM-008 workflow enforcement and VM-013 plugin routing passed.
  VM-013 marketplace dependency composition also passed. The amended source is
  live-qualified; publication and rollout remain separate decisions.
- Added a first-tester BMAD-to-Factory handoff checklist that uses the bounded
  Odyssey v3 seed in a greenfield path, requires promoted evidence before
  Factory Stage A, and leaves the two brownfield team states as a required
  follow-up rehearsal before rollout.

## 2026-08-14

- Prepared coordinated Factory and Factory-BMAD `0.2.2` candidates from the
  Odyssey pilot defect and user-experience backlog while preserving Factory as
  the sole downstream SDLC authority.
- Repaired BMAD draft-citation handling, promoted-evidence recall guidance,
  namespaced workflow enforcement, Purple intent locking, stage word-cap
  parity, promotion review qualifiers, plan stability, concise operator output,
  bootstrap fresh-session guidance, and the bytecode-safe Factory launcher.
- Regenerated all four packages and passed the 284-test deterministic suite
  with three live-only tests skipped, plus focused recovery, package-current,
  privacy, policy, knowledge-lint, pack-lint, and source/generated-boundary
  checks. Live Claude/operator retest remains separately gated.

## 2026-08-13

- Integrated the reviewed Factory activation and verification contract into
  the companion's Factory 0.2.1 source without regressing its host-capability,
  execution-closeout, Claude, or BMAD controls.
- Missing audited mode now fails closed; cross-mode activation is digest-bound;
  canonical traceability columns, VM inventory equality, optional execution
  ordering, and non-symlink SHA-pinned no-touch manifests are validated.
- Regenerated all Factory and Factory-BMAD packages and passed 266 tests, the
  companion release check, package-current checks, privacy checks, knowledge
  lint, and diff hygiene.

## 2026-08-12

- Prepared coherent Factory and Factory-BMAD `0.2.1` maintenance sources so
  Claude Code can observe a higher version and use its supported marketplace
  and plugin update lifecycle without manual cache surgery.
- Carried forward the repaired Validate evidence boundary, preserved the
  single-install companion dependency, and kept publication, rollout, BMAD
  bootstrap, product work, and QA automation separately gated.

## 2026-08-11

- Closed the final companion integrity gaps: snapshot IDs now reject
  case-insensitive `receipts` and `install-receipts`, and promoted evidence is
  valid only as an exact two-regular-file inventory with bound artifact and
  manifest modes.
- Added promotion, reuse, rollback, and project-preflight mutation coverage for
  extra, missing, symlinked, type-changed, mode-changed, and content-changed
  snapshot entries.
- Replaced content-only protected-tree checks with deterministic path, kind,
  mode, file-digest, and symlink-target inventories in both publication Python
  and release-shell consumers, with cross-consumer mutation tests.
- Required exact publication-candidate schema, absolute worktree identity,
  candidate commit/HEAD equality, clone commit equality, and an empty final
  `git status --porcelain=v1 -z`; publication, pilot, rollout, and customer
  access remain separate human decisions.
- Repaired publication source-state verification so stable refs remain an exact
  catch-all and only the literal `refs/codex/turn-diffs/` prefix may rotate with
  deterministic added/removed/changed disclosure.
- Added disposable real-Git-repository tests that permit only the exact volatile
  rotation and block HEAD, branch, tag, remote-tracking, other Codex, unexpected
  ref, remote configuration, staged-index, malformed, and duplicate-ref drift.
- Preserved the predecessor BLOCKED closeout and kept candidate, clean-clone,
  source commit, push, merge, release, and publication as separate gates.
- Reconciled the companion candidate's retained execution evidence after a
  post-closeout audit proved that the predecessor created at least 63 evidence
  paths against an approved maximum of 36. Historical budget conformance
  remains `FAIL`; the predecessor's technical verification remains `PASS`.
- Recorded exact human prospective acceptance in `SPRINT_20260811_004` without
  retroactively authorizing the overrun, modifying predecessor history, or
  granting commit, merge, publication, rollout, or customer authority.
- Added a pre-write repository baseline and deterministic allowed-path/budget
  audit for this reconciliation. Reusable automatic closeout-budget enforcement
  remains a separately scoped follow-up rather than an implicit runtime change.
- Repaired the companion release driver after retained-worktree review found
  that Bash conditional context could mask an intermediate VM-010 failure and
  second-resolution attempt paths could reuse prior-evidence destinations.
- Made source-only loading mutation-free, replaced implicit `set -e` reliance
  with explicit production-step status propagation, required exactly one
  terminal VM-010 result, and added token-owned evidence-root locking plus
  digest-verified unique snapshot publication before old VM receipts clear.
- Added nine focused negative/success cases and passed the fresh release gate
  with 200 tests, three intentionally skipped unauthorized live tests, package-
  current/knowledge/privacy checks, and exact protected digests. One transient
  macOS process-group failure and the earlier bytecode-producing wrapper attempt
  remain preserved as non-promoted evidence.
- Repaired the upstream-evidence companion verification boundary after the predecessor run
  blocked on Claude not voluntarily selecting a Skill tool. The hard property
  now begins at generated `hooks.json`, executes the packaged production
  command with the exact `PreToolUse` schema, and proves structured denial
  prevents a prohibited sentinel action.
- Separated `LIVE_DIRECT_EXPANSION`, `DETERMINISTIC_PACKAGED_PRETOOLUSE`, and
  `ADVISORY_MODEL_CHOICE_SMOKE`; model non-invocation can no longer pass or fail
  the deterministic release gate.
- Removed the out-of-envelope profile-mutating Python helper, retained the first
  failed fixed-order attempt, and passed the fresh VM-001–VM-010 retry: 200 tests,
  strict Claude package/dependency composition, all three pinned-installer
  journeys, package-current, knowledge lint, privacy, and protected digests.
- Marked the upstream-evidence companion 0.2.0 candidate technical `REVIEW_READY`; commit,
  merge, tag, publication, application pilot, and rollout remain unauthorized.
- Locked the single-repository companion decision: users explicitly install one
  upstream-evidence companion, Claude resolves Factory as its protected
  dependency, and every adoption starts with one Doctor front door.
- Prepared and I2-approved the `SPRINT_20260811_001` pack covering
  greenfield/neither, brownfield/neither, and brownfield/upstream-system-only repositories.
- Bound repository-scoped `UserPromptExpansion` and `PreToolUse` enforcement,
  exact upstream allowlisting with default-deny unknown workflows,
  capability/version audit, non-destructive reconciliation, project-preflight/CI
  policy parity, and isolated Claude proof.
- Retained user-scope installation for the first pilot so plugin installation
  does not create target metadata before Factory Greenfield. Project-scope
  `.claude/settings.json` compatibility remains outside the approved sprint.
- Received exact digest-bound execution authorization and implemented the 0.2.0
  single-repository candidate from one authored policy/classifier into runtime,
  Claude hooks, capability audit, reconciliation, project preflight, CI lint,
  deterministic Claude/Codex packages, and focused tests.
- Frozen the exact supported 46-skill core inventory and exact 10-skill optional
  test-extension inventory. The test extension remains Stage F evidence-only
  and unavailable through the upstream invocation allowlist; the autonomous
  loop extension remains blocking.
- Passed isolated one-install dependency composition and the three disposable
  real-installer adoption journeys. The first run correctly exposed and then
  regression-locked the narrow `.claude` container-directory allowance without
  permitting `.claude/settings.json`.
- Recorded the authenticated model-choice observation as inconclusive advisory
  evidence after no Skill tool call occurred; deterministic verification repair,
  final regression, and closeout moved to `SPRINT_20260811_002`.

## 2026-08-10

- Implemented the separate customer-neutral upstream-evidence companion `0.1.0`
  candidate from one authored source into deterministic Claude Code and portable
  Codex packages, without copying Factory Core.
- Added five-state adoption routing, pinned upstream bootstrap preview, authority
  audit, immutable reviewed snapshot promotion and guarded rollback, embedded
  intake checklist, and the existing schema-locked project-preflight seam.
- Passed focused routing, policy, promotion, preflight, concise-output, privacy,
  deterministic-build, strict plugin validation, and isolated same-marketplace
  dependency composition checks, plus the receipt-backed disposable pinned
  installer and post-install authority-audit journey. All eleven checks pass and
  the candidate is technical `REVIEW_READY`.
- Completed the maintainer Claude Code Greenfield slice in a harness-initialized
  new repository: Factory 0.2.0 applied by exact plan approval, Doctor and
  Progress returned the expected states, and applicable Validate checks passed
  without a Factory repository mutation.
- Recorded Claude permission bookkeeping as volatile unmanaged harness state,
  not a Factory-owned file or a Factory validation failure.
- Prepared and I2-approved a separate upstream-evidence companion implementation
  pack with an exact enterprise tool/version pin, Factory-only downstream authority,
  immutable reviewed promotion, existing project-preflight integration,
  concise Claude Code output, and isolated live proof requirements.
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
