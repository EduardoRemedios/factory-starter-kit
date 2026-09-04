# Envelope Red Team — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): First envelope Red iteration on budgets, gates, and authority boundaries.

## Method
Attack the v1 envelope as a hostile executor and as an unlucky honest one: look for gate ambiguities, unpinned dependencies, and budget pressure that could force improvisation mid-activation.

## Findings

### ER-01 (High) — Declined promotion is conflated with missing review
Gate 2 requires "one human-reviewed promotion recorded". If the human reviews the snapshot and declines it, the gate cannot pass, yet nothing distinguishes that deliberate decision from an absent review. Resolution required: the envelope must state that a reviewed-and-declined promotion is a deliberate human No-Go decision recorded as `NO_GO`, while an absent review is a halt (`BLOCKED`); neither may be retried inside the same activation.

### ER-02 (High) — The live harness binary is consumed but not pinned
The composition driver requires an explicit harness binary (`FACTORY_CLAUDE_BIN`), yet Gate 0 pins only pack, driver, candidate, and BMAD digests. An unrecorded harness version makes live results unreproducible. Resolution required: Gate 0 must record the harness binary path and reported version in activation evidence; a harness change mid-activation halts.

### ER-03 (Medium, accepted with rationale) — Per-activation evidence ceiling under live logs
Live drivers can emit verbose logs, and 30 files/10 MiB per activation could pressure MS-02. Accepted without change: the drivers write a small number of log files, full logs are external by contract, and the ceiling exists precisely to force bounded, reviewable evidence; if the ceiling binds, the correct behavior is the abort rule, not silent truncation.

## Attack Summary
- Authority boundaries, zero-implementation budgets, containment gates, and the export-before-teardown ordering withstood attack.
- Two findings require envelope v2 wording; no budget, scope, or authority change is needed.

## Verdict
- Verdict: REVISE
- Required: absorb ER-01 and ER-02 into envelope v2; ER-03 is accepted with recorded rationale.
