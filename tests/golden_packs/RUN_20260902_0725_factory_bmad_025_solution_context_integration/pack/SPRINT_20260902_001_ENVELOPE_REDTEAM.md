# Envelope Red Team — Factory-BMAD 0.2.5 Integration

## Version
v1

## Change Log
- v1 (2026-09-02): Challenged the final integration envelope and recorded hardened PASS.

## Iteration
- Iteration: 1 of max 2

## Inputs Reviewed (LOAD)
- `SPRINT_20260902_001_ENVELOPE.md`
- `verification_plan.md`
- `traceability_matrix.md`
- `micro_sprints.md`

## Cross-Reference: Intent Red Team
- Intent findings IR-01 through IR-11 are represented in fixtures, VM-001 through VM-015, budgets, and stop gates.
- IR-12 remains a non-blocking excluded housekeeping item; it did not resurface as execution scope.

## Executive Verdict
- PASS after minimal v2 hardening.
- The envelope is execution-reviewable only after adding an explicit protected-path inventory, moving the closeout draft outside the run root, and requiring builder call-site topology inspection before writes. These changes do not expand scope.

## Severity-Ranked Findings
| ID | Severity | Category | Finding | Why it matters | Fix recommendation | Status |
|---|---|---|---|---|---|---|
| ER-01 | High | No-touch | Protected categories lacked one exact path list. | Category-only protection can omit manifests, builders, or the video checkout. | Add exact protected repository paths and external roots to source coupling. | RESOLVED |
| ER-02 | High | Builder lifecycle | Invocation counts were fixed but call sites were not explicitly inspected before writes. | A changed full-suite topology could execute another replacement/check path late. | Require static call-site confirmation during Gate 0 and MS-01. | RESOLVED |
| ER-03 | Medium | Closeout hygiene | Envelope allowed a closeout draft in the run root. | A noncanonical draft can confuse progress and file budgets. | Keep draft in external evidence; allow only canonical closeout in run root. | RESOLVED |
| ER-04 | Medium | Generated delta | Exact 18-file delta is asserted before combined generation. | If wrong, discovery occurs after an isolated generated replacement. | Retain exact halt condition; isolated worktree and preserved preimages make this safe without widening the budget. | ACCEPTED |

## Agent Failure Modes
- Skip static call-site inspection → full suite adds an unexpected builder invocation → Gate 0 blocks.
- Protect only broad categories → manifest/builder/video checkout drifts unnoticed → exact protected lists and external inventories block.
- Leave a draft closeout beside canonical state → Progress ambiguity → external draft rule blocks.
- Expand generated budget after mismatch → normalize drift → exact 18-file stop gate blocks and requires fresh planning.

## Verification Holes
- None after v2 hardening. Actual hashes and results remain execution evidence, not planning claims.

## Scope / Drift Checks
- Any scope expansion detected? NO.
- File-touch allowlist still contains exactly 20 modified authored paths, one created authored fixture, and two generated roots.
- MS-06, AuditEdge, Git actions, donor mutation, and cleanup remain excluded.

## Minimal Patch Set Applied
- Added explicit protected paths/external roots to source-coupling input.
- Added pre-write builder topology inspection to verification lifecycle and Gate 0.
- Moved closeout draft allowance to external evidence.
