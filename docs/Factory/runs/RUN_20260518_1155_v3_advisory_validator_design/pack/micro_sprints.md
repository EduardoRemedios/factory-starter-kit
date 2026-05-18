# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-18): Initial micro-sprints for v3 advisory validator design.

## MS-01 - Advisory Check Catalog
- Objective: Define first deterministic advisory checks.
- Inputs: `ADVISORY_VALIDATOR_PLAN.md`, `EVAL_20260518_001.md`.
- Outputs: A catalog of checks V3-A001 through V3-A006.
- Entry criteria: This planning pack passes I2.
- Exit criteria: Checks are non-blocking, deterministic where possible, and exclude runtime-kernel judgments.
- Stop or go gate: Stop if any check would block v2 required gates.

## MS-02 - Report Shape
- Objective: Define output fields for future advisory reports.
- Inputs: verification fixture and risk register.
- Outputs: Report field list with `status`, `blocking_effect`, `promotion_level`, `findings`, and review fields.
- Entry criteria: MS-01 catalog is approved.
- Exit criteria: Output cannot be confused with pack-lint or stage-lint failure.
- Stop or go gate: Stop if status names omit advisory wording.

## MS-03 - Fixture Expansion
- Objective: Define fixture cases for a later implementation run.
- Inputs: current warning fixture.
- Outputs: clean pass, warning, boundary vocabulary, promotion claim, and required-gate wiring fixtures.
- Entry criteria: MS-02 report shape is approved.
- Exit criteria: Every fixture has expected non-blocking output.
- Stop or go gate: Stop if fixtures require JSON schemas or runtime execution.

## MS-04 - Review Workflow
- Objective: Define false-positive and false-negative tracking.
- Inputs: pilot profile plan and promotion criteria.
- Outputs: Review workflow requiring `review_status`, `review_notes`, `reviewer`, and follow-up missed-issue fields.
- Entry criteria: MS-03 fixtures are approved.
- Exit criteria: Promotion evidence can distinguish accepted warnings from rejected warnings.
- Stop or go gate: Stop if false negatives have no collection path.

## MS-05 - Implementation Readiness Gate
- Objective: Decide whether a later implementation run is ready.
- Inputs: MS-01 through MS-04 evidence.
- Outputs: GO or NO-GO recommendation for a separate implementation planning run.
- Entry criteria: Design pack passes.
- Exit criteria: Code implementation remains unstarted.
- Stop or go gate: Stop if implementation would touch required v2 gates.

