# Intent Synthesis — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Resolved the first intent Red Team cycle.

## Iteration

Iteration: 1 of max 2

## Accepted Findings

- IR-01: C-04 now makes cleanup proof-based and otherwise fail-closed.
- IR-02: C-09 now separates installed capability from permitted Factory-bound routing and citations.
- IR-03: C-11 now requires current positive and negative live dependency proof.
- IR-04: C-12 now requires explicit companion ownership and conflict halts.
- IR-05: C-13 now requires one source result with concise default and opt-in JSON.
- IR-06: C-13 now forbids unnecessary volatile-settings hashing.
- IR-07: Codex remains mechanically portable but outside the live support claim.

## Changes Made

- Updated `intent.md` from v1 to v2.
- Added explicit transaction-created-and-unchanged cleanup criteria.
- Added prohibited authority/citation verification rather than pretending BMM
  installation can remove downstream capabilities.
- Added project-file ownership and user-content conflict behavior.
- Added live dependency resolution and concise-output obligations.

## Scope and Assumptions

- No new requirement was introduced; all changes harden raw-brief requirements.
- No `[INFERRED]` or `[SCOPE EXPANSION]` item remains.
- BMAD 6.10.0 and Factory 0.2.x stay fixed compatibility targets.

## Open Issues

### BLOCKING

- None.

### NON-BLOCKING

- Codex live support remains a later decision.
