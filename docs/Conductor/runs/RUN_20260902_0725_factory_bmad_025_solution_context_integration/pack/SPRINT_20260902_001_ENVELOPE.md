# Sprint Envelope — Factory-BMAD 0.2.5 Solution-Context Integration

## Version
v5

## Change Log
- v1 (2026-09-02): Bound the planning-only integration execution envelope.
- v2 (2026-09-02): Hardened protected-path and closeout-draft handling after envelope Red review.
- v3 (2026-09-02): Repaired test ownership so authored, release-fixture, generated-package, and full-suite gates follow their prerequisites.
- v4 (2026-09-02): Human-authorized arithmetic/evidence-ledger correction of MS-03, cumulative-touch, evidence-allowance, and control accounting; no design change and no third Red/Blue iteration.
- v5 (2026-09-03): Human-authorized manifest repair after the MS-05 pre-activation blocker: verification manifest present, bounded in-repo closeout evidence authorized, MS-05 external allowance corrected; no design change and no new Red/Blue iteration.

## Sprint Metadata
- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Owner: Eduardo dos Remedios
- Created: 2026-09-02 07:54 WEST
- Audited mode: `PLANNING_ONLY`
- Locked intent: v2, SHA-256 `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`
- Authority: this envelope grants no execution; activation requires fresh exact human approval.

## Iteration
- Iteration: 1 of max 2

## Inputs (LOAD)
- `intent.md`
- `micro_sprints.md`
- `verification_plan.md`
- `traceability_matrix.md`

## Inputs (DISK)
- `risk_register.md`
- `premortem.md`
- `intent_lock_report.md`
- `fixtures/`

## Purpose
Semantically integrate qualified solution-context behavior and the separate 0.2.5 nested-layout safeguards onto the clean 0.2.5 base, regenerate both derived Factory-BMAD packages once, and deterministically qualify the combined candidate without touching donors or acquiring MS-06/rollout authority.

## Scope
### In Scope
- Exact preimages for base, donors, registrations, dependencies, generated roots, Factory Core, Git/config, and source allowlists.
- Twenty named authored modifications and one named authored creation from `fixtures/verification/source_coupling/input.json`.
- Behavior-level resolution of five overlapping runtime/test collisions.
- Preservation of 0.2.5 identity, cache/approval behavior, direct Factory/companion command passthrough, public layout compatibility, and nested capability evidence.
- Integration of solution profiles, immutable multi-file promotion, supersession, claim dispositions, legacy-index mechanics, adapters, skills, tests, and bounded documentation.
- Exactly one canonical replacement of `plugins/factory-bmad` and `plugins/factory-bmad-claude`, followed by deterministic qualification.

### Out of Scope
- Factory Core, dependencies, configurable active BMAD roots, universal gateway/sandbox/stage-aware framework, unrelated product/docs/tests, donor/pilot/video worktrees, registration cleanup, or generated-byte transplant.
- BMAD workflow invocation, MS-06, AuditEdge, commit, merge, push, publication, pilot, release, customer action, or rollout.

### Domain Areas
- None.

## Acceptance Criteria
- AC-01: Activation and preimages exactly pin the clean base, donors, protected roots, registrations, pack, and evidence destinations.
- AC-02: All five collision resolutions preserve both behavior families and their union regression cases.
- AC-03: 0.2.5 identity, dependency, cache/approval, command passthrough, and operator compatibility remain intact.
- AC-04: Unsafe layouts and unknown/prohibited workflows deny before execution through both hook paths.
- AC-05: Candidate architecture/UX/spec classification remains exact-version and `EVIDENCE_ONLY`; no workflow runs.
- AC-06: Promotion/preflight/supersession/claim/index mechanics pass deterministic tests without acquiring Factory authority.
- AC-07: The exact 53-test MS-02 authored gate and MS-03 release-fixture/authored-feature gate pass before exactly one builder replacement; generated-package checks run only after replacement; generated delta is exactly 18 modified, 0 created, 0 deleted.
- AC-08: Full regression, privacy, no-bytecode, dependency, parity/currentness, knowledge, stage, pack, and no-touch checks pass.
- AC-09: Donors, existing registrations, Factory Core, Git/config, and unrelated paths remain byte-identical.
- AC-10: Final status does not exceed `FACTORY_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`; MS-06 remains separately gated.

## Constraints
- C-001 (Critical): Factory/Conductor and exact-pack human Go retain all implementation authority.
- C-002 (Critical): No 0.2.5 safeguard or Factory-command compatibility regression.
- C-003 (Critical): Unsafe, malformed, unknown, and prohibited BMAD paths fail closed.
- C-004 (Critical): Solution promotion is immutable, reviewed, provenance-bound, and non-authorizing.
- C-005 (Critical): Every donor/protected/unrelated state change is forbidden and detected.
- C-006 (High): Generated output comes only from one builder invocation after authored PASS.
- C-007 (High): Stable public layout code and subordinate granular evidence coexist.
- C-008 (High): Both donor regression families remain covered.
- C-009 (High): Docs and status claims remain deterministic-only.
- C-010 (High): Paths, budgets, commands, evidence roots, invocation counts, and stop gates remain exact.

### SIMPLE-CODE-GATE v2
- Implement the smallest clear behavior-preserving semantic merge.
- Use existing standard-library and repository utilities; add no dependency.
- Add no generic framework, registry, strategy layer, hidden side effect, silent failure, or speculative abstraction.
- Comments explain why; tests prove collision behavior.

## File-Touch Budgets
### Per Micro-sprint Implementation Budgets
| Micro-sprint | Modified max | Created max | Deleted max | Justification |
|---|---:|---:|---:|---|
| MS-01 | 0 | 0 | 0 | Evidence/control artifacts are separately governed. |
| MS-02 | 6 | 0 | 0 | Two runtime and four overlapping test/helper files. |
| MS-03 | 15 | 1 | 0 | The 14 authored allowlist paths untouched in MS-02 plus a second `tests/test_factory_bmad_enforcement.py` touch replacing its transient donor-run fixture reference with `tests/plugin_fixtures/factory_bmad_solution_context_contract.json`; one contract fixture created. |
| MS-04 | 18 | 0 | 0 | Exact two-platform generated delta derived from shared source. |
| MS-05 | 0 | 0 | 0 | Verification and external evidence only. |

Budgets are activation-relative; MS-03 does not change the unchanged 20-path authored allowlist.

### Sprint Total Implementation Budget
| Modified max | Created max | Deleted max | Justification |
|---:|---:|---:|---|
| 38 | 1 | 0 | 38 unique modified paths: 20 authored and exactly 18 mechanically generated cross-platform files. Cumulative milestone-relative modified touches are 39 because the enforcement test is counted in both MS-02 and MS-03. |

### External and Control Budgets
- External root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/`.
- Per micro-sprint activation: maximum 40 files and 10 MiB; total ceiling 160 files and 40 MiB.
- MS-01 through the MS-02 corrective closeout retain exactly 58 files; the remaining 102-file allowance is allocated as MS-03 maximum 40, MS-04 maximum 30, and MS-05 maximum 32 files. The MS-05 pre-activation blocker and pack-repair records consume 2 of the MS-05 allocation, leaving at most 30 files for the MS-05 activation itself.
- Closeout evidence: MS-05 may create at most 16 bounded files under `artifacts/verification/RUN_20260902_0725_factory_bmad_025_solution_context_integration/` inside the repository; `EXECUTION_CLOSEOUT.json` references only these in-repo files and is recorded through the canonical validator while `EXECUTION_ENABLED` with live controls, before restoration to `PLANNING_ONLY` and control archival.
- Run-root controls: at most two canonical live controls at once (`EXECUTION_AUTHORIZATION.md`, `EXECUTION_PROMPT.md`), archived per milestone after use; maximum 13 final persistent control/evidence files — the MS01/MS02/MS02-corrective/MS03/MS04/MS05 archived authorization-plus-prompt pairs (12) plus `EXECUTION_CLOSEOUT.json`. Any additional corrective activation requires a new human-authorized accounting decision; this ceiling must not be expanded silently. Any closeout draft stays inside the bounded external evidence root.
- Donor and existing-registration mutation budget: zero.

## Execution Plan
- Gate 0: pack/activation/hash/evidence-root validation plus static builder call-topology confirmation.
- Gate 1 after MS-01: complete donor/base/protected preimages PASS.
- Gate 2 after MS-02: the exact 53 source-owned collision, compatibility, layout, denial, and solution-profile tests PASS; the one release-fixture test and three generated-package tests are not executed; generated roots remain unchanged.
- Gate 3 after MS-03: the MS-02 gate is rerun; promotion/preflight/index/source-coupling tests PASS; the parent-permission/non-transitivity test consumes the release-owned solution-context fixture and PASSes.
- Gate 4 after MS-04: exactly one builder invocation occurs; only then do packaged-hook sentinel, generated command-contract, policy-copy parity, package-currentness, ownership, and exact generated topology checks PASS.
- Gate 5 after MS-05: full regression/no-touch/closeout PASS, controls archived, `PLANNING_ONLY`, STOP.

## Verification Plan
- Authoritative checks: `verification_plan.md` VM-001 through VM-015 and `traceability_matrix.md`.
- `verification_manifest.yaml` binds those checks for canonical closeout recording; its audited mode is `PLANNING_ONLY` and activation must not rewrite it.
- All Critical/High constraints have V3-V4 fixture/test/check coverage: YES at planning time.

## Rollback and Abort
- Abort immediately on any mismatch, unexpected path, donor drift, test failure, extra builder call, residue, dependency change, authority escalation, or status overclaim.
- Do not auto-rollback or delete evidence. Preserve failure state, archive controls, return to `PLANNING_ONLY`, and request a separately authorized correction.

## Risks to Watch
- R-003: textual merge silently drops 0.2.5 safeguards.
- R-006: unsafe layout allows a nominally permitted workflow.
- R-010: dirty donor or existing worktree state is altered.
- R-016: deterministic integration is overclaimed as MS-06 or rollout proof.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- Stale temporary worktree registration cleanup remains outside scope.

## Scope Expansion Log
- None.
