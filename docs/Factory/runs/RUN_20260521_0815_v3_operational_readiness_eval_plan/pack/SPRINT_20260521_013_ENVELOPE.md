# Sprint Envelope - V3 Operational Readiness Eval Suite Planning

## Version
v1

## Change Log
- v1 (2026-05-21): Stage H sprint envelope for planning the V3 operational-readiness eval suite.

## Sprint Metadata
- RUN_ID: RUN_20260521_0815_v3_operational_readiness_eval_plan
- Sprint ID: SPRINT_20260521_013
- Owner: Project owner
- Created: 2026-05-21 08:24 WEST

## Iteration
- Iteration: 1 of max 2

## Inputs
- `intent.md`
- `micro_sprints.md`
- `verification_plan.md`
- `traceability_matrix.md`
- `risk_register.md`
- `premortem.md`
- `intent_lock_report.md`

## Purpose
Plan the next V3 operational-readiness eval-suite work so implementation can later proceed from a bounded, reviewed, fixture-first contract.

## Scope
### In Scope
- Define the future eval-suite contract.
- Define golden fixture IDs and expected outcomes.
- Define pilot evidence and decision report fields.
- Preserve V2 fallback and V3 research-only posture.
- Red-team, blue-team, and Purple-review the key planning steps.

### Out of Scope
- Implementing an eval runner.
- Adding required validators.
- Promoting V3 operationally.
- Deprecating V2.
- Introducing runtime-kernel authority.

### Domain Areas
- Factory v3 operational-readiness eval planning
- Factory v2 guarantee preservation
- Mission-envelope evaluation
- V2 fallback and non-deprecation
- AEGIS boundary review

## Acceptance Criteria
- AC-01: Pre-mortem failure modes map to eval families, fixtures, or pilot evidence.
- AC-02: Golden fixtures include positive and negative cases with expected results.
- AC-03: Pilot evidence template includes branch, revision, model, harness, artifacts, results, classifications, overhead, decision, and residual risks.
- AC-04: V2 guarantee preservation matrix is present.
- AC-05: V3 remains research-only and V2 remains supported.

## Constraints
- C-01 (Critical): V3 remains research-only in this run.
- C-02 (Critical): V2 remains supported and available as fallback.
- C-03 (Critical): V3 collapse of V2 ceremony requires equivalent guarantee preservation.
- C-04 (High): Eval design starts from pre-mortem failure modes.
- C-05 (High): Golden fixtures include negative cases.
- C-06 (High): AEGIS and runtime-kernel boundaries remain intact.
- C-07 (High): SIMPLE-CODE-GATE v2 is represented for code-changing V3 work.

### SIMPLE-CODE-GATE (v2) Constraint
- Mandatory for future code-changing V3 eval-runner implementation.
- Future implementation must stay direct, local, behavior-preserving, and free of speculative abstractions or dependency creep.
- Accepted complexity must map to a concrete fixture, repeated pattern, or verification hook.

## Evidence Expectations
- Fixture inventory JSON under `pack/fixtures/verification/v3_golden_fixture_inventory/`.
- Expected report-shape JSON under `pack/fixtures/verification/v3_eval_suite_contract/`.
- Future implementation pack must add exact command output evidence.

## File-Touch Budgets
### Per Micro-sprint Budgets
| Micro-sprint ID | Modified max | Created max | Deleted max | Justification if outside guidance |
|---|---:|---:|---:|---|
| MS-01 | 4 | 8 | 0 | within planning-doc scope |
| MS-02 | 4 | 6 | 0 | within planning-doc scope |
| MS-03 | 3 | 3 | 0 | planning only |
| MS-04 | 3 | 3 | 0 | review artifacts only |

### Sprint Total Budget
| Modified max | Created max | Deleted max | Justification if outside guidance |
|---:|---:|---:|---|
| 14 | 20 | 0 | planning pack may create fixtures and templates |

## Execution Plan
- Gate 1 after MS-01: fixture inventory covers every Critical and High pre-mortem failure mode.
- Gate 2 after MS-02: report and pilot templates can support a promotion decision.
- Gate 3 after MS-03: future implementation remains separate and advisory first.
- Gate 4 after MS-04: no unresolved Critical review findings remain.

## Verification Plan
References:
- `verification_plan.md`
- `traceability_matrix.md`

Required checks:
- VP-01: Fixture inventory completeness.
- VP-02: Golden fixture expected outcomes.
- VP-03: V2 guarantee preservation.
- VP-04: No premature promotion.
- VP-05: Harness capability evidence.
- VP-06: AEGIS boundary review.
- VP-07: SIMPLE-CODE-GATE coverage.
- VP-08: Pack validation.

Verification tier summary:
- V0 artifact proof: VP-05.
- V1 static or mechanical: VP-01, VP-04, VP-08.
- V2 focused fixture: VP-02, VP-03, VP-06, VP-07.
- V3 regression or conformance: deferred to future runner implementation.
- V4 live or external revalidation: deferred to real pilots.

Fixture coverage confirmation:
- All Critical and High constraints have at least one fixture, artifact check, or pilot evidence hook.

## Rollback And Abort Criteria
Abort if:
- V3 promotion language appears in this planning run.
- V2 fallback is removed or weakened.
- AEGIS boundary claims become runtime authority claims.
- Verification design lacks negative fixtures.

Rollback approach:
- Revert to the last locked intent and rerun affected stages from Stage C onward.

## Risks To Watch
- R-01: Eval suite becomes narrative-only.
- R-02: V2 stages collapse without equivalent guarantees.
- R-05: Harness reliability is assumed instead of measured.
- R-07: SIMPLE-CODE-GATE is omitted.

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- Future eval-runner implementation language is deferred to MS-03 and a later execution-enabled run.

## Scope Expansion Log
- None
