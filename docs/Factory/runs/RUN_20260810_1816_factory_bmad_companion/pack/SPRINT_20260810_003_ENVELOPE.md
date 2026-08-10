# Sprint Envelope — Factory BMAD Companion

## Version

v4

## Change Log

- v1 (2026-08-10): Created the implementation envelope.
- v2 (2026-08-10): Added exact path/no-touch, isolated live-state, dependency-error, and support-claim controls after envelope Red Team.
- v3 (2026-08-10): Allowed only deterministic canonical-doc mirrors and payload ownership digests in existing Factory packages.
- v4 (2026-08-10): Replaced the local pilot repository name with its public-safe role.

## Sprint Metadata

- RUN_ID: `RUN_20260810_1816_factory_bmad_companion`
- Sprint ID: `SPRINT_20260810_003`
- Owner: Project owner
- Created: 2026-08-10 18:38 WEST

## Iteration

- Iteration: 1 of max 2

## Purpose

Build a separate Claude Code-first companion that safely converts selected BMAD
6.10.0 upstream discovery output into immutable Factory intake evidence while
Factory remains the sole SDLC authority.

## Scope

### In Scope

- One authored `factory-bmad` companion source and deterministic generated packages.
- Five-state diagnosis, BMAD bootstrap preview/audit, authority policy, project adapter, promotion, intake, concise output, tests, docs, and isolated live proof.
- Same-marketplace Factory 0.2.x dependency and stable namespace.
- Canonical `PROJECT_STATE`, `ROADMAP`, and `CHANGELOG` alignment.

### Out of Scope

- Factory Core changes, BMAD vendoring, downstream BMAD solution/implementation workflows, TEA delivery, live application pilot, real-profile mutation, Claude Desktop, organization rollout, merge, tag, or publication.

### Domain Areas

- plugin-composition
- bmad-bootstrap
- authority-policy
- upstream-promotion
- factory-intake
- claude-code-ux

## Allowed Implementation Paths

- `plugin-src/factory-bmad/**`
- `plugins/factory-bmad-claude/**`
- `plugins/factory-bmad/**`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `scripts/build_factory_bmad_plugins.py`
- `scripts/verify_factory_bmad_*.sh`
- `tests/test_factory_bmad_*.py`
- `tests/fixtures/factory_bmad/**`
- `docs/adapters/bmad/**`
- `docs/onboarding/FACTORY_BMAD_*.md`
- `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, `docs/CHANGELOG.md`
- `plugins/factory/payload/docs/PROJECT_STATE.md`, `plugins/factory/payload/docs/ROADMAP.md`, `plugins/factory/payload/docs/CHANGELOG.md`
- `plugins/factory-claude/payload/docs/PROJECT_STATE.md`, `plugins/factory-claude/payload/docs/ROADMAP.md`, `plugins/factory-claude/payload/docs/CHANGELOG.md`
- `plugins/factory/payload/OWNERSHIP.json`, `plugins/factory-claude/payload/OWNERSHIP.json`
- `artifacts/verification/factory_bmad_companion/**`
- current run execution evidence and closeout files.

All other paths are no-touch. Existing Factory package changes are limited to
byte-identical mirrors of the three canonical root documents and their
deterministically regenerated payload ownership digests; every other Factory
package file must retain its starting digest.

## Acceptance Criteria

- AC-01 through AC-12 from `raw_brief.md` pass with retained evidence.

## Constraints

- C-01 through C-08 are Critical; C-09 through C-15 are High and must match `intent.md` v2 and `traceability_matrix.md`.
- BMAD installer execution occurs only in a synthetic temporary repository after exact approval; npm and Claude cache/profile effects are inventoried separately from repository writes.
- Claude dependency proof uses isolated `CLAUDE_CONFIG_DIR`; the real authenticated profile may be consulted only if separately authorized and exact digest protected.
- `.claude/settings.local.json` is unmanaged and never hashed solely to prove exclusion.
- The live application-pilot repository and all customer repositories are prohibited paths for this sprint.
- Public docs must say Claude Code CLI technical pilot only; Codex packaging is portable/unverified and Claude Desktop is unsupported.

### SIMPLE-CODE-GATE (v2)

- Implement the smallest clear local change.
- Prefer direct standard-library code and existing utilities.
- No copy-paste runtime, speculative registry, hidden side effect, dependency creep, silent failure, or broad abstraction.
- Add a helper only when it removes current duplication, names a stable domain concept, simplifies callers, and has one owner.
- Comments explain why, not what.

## File-Touch Budgets

| Micro-sprint | Modified max | Created max | Deleted max | Justification |
|---|---:|---:|---:|---|
| MS-00 | 4 | 10 | 0 | Fixture/test scaffold spans named risk areas. |
| MS-01 | 8 | 22 | 0 | Generated Claude/Codex package skeletons exceed normal creation guidance. |
| MS-02 | 8 | 10 | 0 | Runtime, receipts, fixtures, and focused tests. |
| MS-03 | 10 | 12 | 0 | Policy plus project-adapter ownership surfaces. |
| MS-04 | 12 | 14 | 0 | Promotion, intake, preflight, schemas, and tests. |
| MS-05 | 18 | 12 | 0 | Canonical docs and two generated packages update together. |
| MS-06 | 4 | 10 | 0 | Isolated evidence and closeout artifacts. |

| Sprint modified max | Sprint created max | Sprint deleted max | Justification |
|---:|---:|---:|---|
| 50 | 80 | 0 | Dual generated packages, fixtures, tests, and retained evidence dominate count. |

## Execution and Gates

- Gate 0: MS-00 freezes paths/digests and proves every VM command exists.
- Gate 1: MS-01 passes package/dependency contracts.
- Gate 2: MS-02 passes routing/bootstrap safety.
- Gate 3: MS-03 passes authority/ownership policy.
- Gate 4: MS-04 passes promotion and preflight matrices.
- Gate 5: MS-05 passes UX, privacy, canonical docs, package current, and regression.
- Gate 6: MS-06 passes isolated VM-006/VM-011 and schema-locked closeout.

## Verification Before Review

- Run VM-001 through VM-011 in `verification_manifest.yaml` order.
- `verification_plan.md` defines tier and evidence expectations.
- `traceability_matrix.md` confirms every Critical/High constraint has coverage.
- All verification evidence must be nonempty, privacy-safe, and digest-pinned before `REVIEW_READY`.

## Rollback and Abort

- Abort on any stop condition in `micro_sprints.md` or any VM failure.
- Revert only companion-created unchanged paths within the explicit envelope.
- Preserve unexpected/user-owned state and halt with recovery evidence.
- Never clean the real Claude profile or the live application-pilot repository.

## Risks to Watch

- R-01 authority duplication; R-02 unsafe installer recovery; R-04 mutable promotion; R-08 dependency failure; R-11 private-data leakage; R-12 Factory regression.

## Open Issues

### BLOCKING
- None for execution after exact human Go.
### NON-BLOCKING
- Codex live support remains a later release decision.

## Scope Expansion Log

- None.
