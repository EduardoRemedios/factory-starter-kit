# Factory v3 Pilot Profile Plan

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial pilot profile plan for Factory v3 research.

## Status
Research only. This plan does not authorize Factory v3 release or runtime integration.

## Purpose
Define how to stress-test Factory v3 research artifacts before promotion. Pilots should use Factory v2 as the governing process and run v3 checks in shadow or advisory mode.

## Pilot Goals
- Confirm v3 docs improve clarity without confusing v2 usage.
- Detect whether advisory checks catch real drift.
- Measure overhead added to normal Factory work.
- Verify AEGIS compatibility without dependency.
- Confirm no runtime-kernel behavior is introduced into Factory.

## Pilot Inputs
- A current Factory v2 run.
- One historical Factory run, when available.
- The v3 research docs under `docs/Factory/v3/`.
- Any future advisory validator output.
- Human review notes.

## Pilot Profiles

### Profile P1 - Documentation Clarity
- Target: README and `docs/Factory/v3/`.
- Method: Review whether a new adopter can identify that v2 is current and v3 is research-only.
- Evidence: reviewer notes and proposed wording changes.
- Pass signal: no ambiguity about v2 versus v3.

### Profile P2 - v2 Drift Shadow Check
- Target: Factory Core docs and validators.
- Method: Run future advisory checks without blocking.
- Evidence: advisory report and manual review.
- Pass signal: drift warnings are accurate and useful.

### Profile P3 - AEGIS Boundary Review
- Target: v3 concepts and shadow schema candidates.
- Method: Review each candidate against `docs/Factory/AEGIS_BOUNDARY.md`.
- Evidence: boundary findings.
- Pass signal: Factory-owned and kernel-owned responsibilities remain separated.

### Profile P4 - Promotion Simulation
- Target: promotion criteria and fixture-like examples.
- Method: Simulate promotion with missing evidence, weak evidence, and complete evidence.
- Evidence: decision table.
- Pass signal: promotion is rejected unless evidence and human release approval exist.

### Profile P5 - Overhead Review
- Target: a normal Factory v2 planning run.
- Method: Compare time and artifacts with and without advisory v3 review.
- Evidence: run metrics or reviewer estimate.
- Pass signal: overhead is justified by risk reduction.

## Metrics
Capture:
- number of warnings
- number of useful warnings
- false positives
- false negatives
- time added
- docs changed after pilot
- boundary violations found
- reviewer confidence

## Pilot Exit Criteria
A pilot may pass only if:
- v2 remains current and usable
- v3 remains research-only
- advisory checks do not block required v2 gates
- no AEGIS dependency is introduced
- no runtime-kernel behavior is introduced
- findings are documented with evidence paths

## Pilot Failure Conditions
Fail the pilot if:
- v3 language implies replacement of v2
- shadow schemas are treated as required contracts
- advisory checks are wired into required gates
- Factory claims runtime proof
- AEGIS becomes required
- promotion can occur without human release approval

## Next Step
Use pilot evidence to refine the v3 docs before writing any validator code.

