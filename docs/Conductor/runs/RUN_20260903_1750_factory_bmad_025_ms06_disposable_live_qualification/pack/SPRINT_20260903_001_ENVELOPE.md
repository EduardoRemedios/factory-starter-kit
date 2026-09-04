# Sprint Envelope — MS-06 Disposable Live Qualification

## Version
v2

## Change Log
- v1 (2026-09-03): Bound the planning-only disposable live qualification envelope.
- v2 (2026-09-03): Absorbed envelope Red findings: declined promotion is a recorded human No-Go distinct from a missing-review halt, and Gate 0 pins the live harness binary path and version; ER-03 accepted with rationale.

## Sprint Metadata
- RUN_ID: `RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification`
- Sprint ID: `SPRINT_20260903_001`
- Owner: Eduardo dos Remedios
- Created: 2026-09-03 18:14 WEST
- Audited mode: `PLANNING_ONLY`
- Locked intent: v2, SHA-256 `40d281e56319c05782a74b288e3b8cdf1393d040fac454d1cbccac127623c6d8`
- Authority: this envelope grants no execution; each micro-sprint requires fresh exact human approval.

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
- `verification_manifest.yaml`
- `fixtures/`

## Purpose
Prove live, in one contained disposable repository, that the deterministically qualified 0.2.5 solution-context candidate permits exactly the three BMAD authoring workflows with typed non-binding output, denies every prohibited family before causal sentinels, supports one human-reviewed promotion, and tears down without residue, closing with a canonical closeout under the status ceiling.

## Scope
### In Scope
- Pin revalidation of candidate commit `c23be98034215c17c9c49a7e9b6302cb2ad1f18d`, plugin package digests, driver digests, the local BMAD 6.10.0 tree, and the contract fixture.
- Containment preflight, disposable-repository provisioning, and protected preimages including harness caches and registrations.
- Live authoring, typed-output, and denial proofs through the pinned drivers across both hook paths.
- One human-reviewed, hash-pinned, immutable promotion with claim dispositions.
- Digest-pinned evidence export strictly before evidenced teardown and residue proof.
- Governance checks and canonical closeout.

### Out of Scope
- Any change to the qualified candidate, Factory Core, this repository's source, tests, or generated packages; donors, registrations, and unrelated paths.
- AuditEdge access or preview; BMAD implementation, sprint execution, code review authority, unattended development, quick-dev, bmad-loop.
- Commit, merge, push, publication, pilot, release, rollout.

### Domain Areas
- None.

## Acceptance Criteria
- AC-01 through AC-07 exactly as locked in `intent.md` v2.

## Constraints
- C-001 through C-007 exactly as locked in `intent.md` v2, with severities carried into traceability.

### SIMPLE-CODE-GATE v2
- Applies vacuously: this sprint authorizes no code change; any write outside controls and evidence is a halt.

## File-Touch Budgets
### Per Micro-sprint Implementation Budgets
| Micro-sprint | Modified max | Created max | Deleted max | Justification |
|---|---:|---:|---:|---|
| MS-01 | 0 | 0 | 0 | Provisioning happens outside this repository; controls and evidence are separately governed. |
| MS-02 | 0 | 0 | 0 | Live proofs and promotion happen inside the disposable repository only. |
| MS-03 | 0 | 0 | 0 | Teardown, governance, and closeout evidence only. |

### Sprint Total Implementation Budget
| Modified max | Created max | Deleted max | Justification |
|---:|---:|---:|---|
| 0 | 0 | 0 | This repository's source, tests, docs, and packages are byte-frozen at the qualified candidate commit. |

### External and Control Budgets
- External root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/`.
- Per micro-sprint activation: maximum 30 files and 10 MiB; total ceiling 90 files and 30 MiB.
- Disposable repository root: activation-pinned, outside every protected root; destroyed before closeout.
- Closeout evidence: at most 11 bounded files under `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/`; `EXECUTION_CLOSEOUT.json` references only these in-repo files and is recorded through the canonical validator while `EXECUTION_ENABLED` with live controls, before restoration and archival.
- Run-root controls: at most two canonical live controls at once, archived per milestone after use; maximum 7 final persistent control/evidence files - the MS01/MS02/MS03 archived authorization-plus-prompt pairs (6) plus `EXECUTION_CLOSEOUT.json`. Any corrective activation requires a new human-authorized accounting decision; this ceiling must not be expanded silently.
- Candidate, donor, and registration mutation budget: zero.

## Execution Plan
- Gate 0: pack/activation/digest/environment validation, driver digest pins, the live harness binary path and reported version recorded in activation evidence, and containment preflight readiness; a harness change mid-activation halts.
- Gate 1 after MS-01: pins and preimages PASS; disposable repository seeded and contained.
- Gate 2 after MS-02: live authoring, typed-output, and denial proofs PASS; one human-reviewed promotion recorded; all exports digest-pinned externally. A reviewed-and-declined promotion is a deliberate human No-Go recorded as `NO_GO`; an absent review is a `BLOCKED` halt; neither may be retried inside the same activation.
- Gate 3 after MS-03: teardown and residue PASS; governance PASS; canonical closeout recorded; controls archived; `PLANNING_ONLY`; STOP.

## Verification Plan
- Authoritative checks: `verification_plan.md` VM-001 through VM-010, `verification_manifest.yaml`, and `traceability_matrix.md`.
- The executable manifest is present and pack-lint validates it; its audited mode is `PLANNING_ONLY` and activation must not rewrite it.
- All Critical/High constraints have V3-V4 coverage: YES at planning time.

## Rollback and Abort
- Abort immediately on any pin mismatch, containment breach, driver failure, untyped or binding output, sentinel execution, missing human review, unexported-evidence teardown attempt, residue, or status overclaim.
- Do not auto-rollback or delete evidence. Preserve failure state, archive controls, return to `PLANNING_ONLY`, and request a separately authorized correction.

## Risks to Watch
- R-001: simulated proof bypassing the pinned drivers.
- R-002: containment escape through a stale or symlinked disposable root.
- R-003: teardown destroying unexported evidence.
- R-008: promotion proceeding without the human review.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- Live AuditEdge index-exclusion proof remains a separately gated future run.

## Scope Expansion Log
- None.
