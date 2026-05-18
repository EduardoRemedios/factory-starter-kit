# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-18): Initial micro-sprints for v3 advisory lint implementation plan.

## MS-01 - Standalone Script
- Objective: Add optional `scripts/factory_v3_advisory_lint.py`.
- Inputs: advisory validator design pack.
- Outputs: standalone script with text and JSON output.
- Entry criteria: separate implementation approval.
- Exit criteria: no required v2 validator calls the script.
- Stop or go gate: stop if protected v2 files need edits.

## MS-02 - Fixture Set
- Objective: Add deterministic fixture directories.
- Inputs: verification plan.
- Outputs: `tests/fixtures/factory_v3_advisory_lint/clean`, `warning`, and `promotion_claim`.
- Entry criteria: script output shape exists.
- Exit criteria: each fixture has input files and expected JSON.
- Stop or go gate: stop if fixtures require runtime execution.

## MS-03 - Verification Commands
- Objective: Verify advisory behavior and v2 isolation.
- Inputs: script and fixtures.
- Outputs: command output evidence.
- Entry criteria: fixtures exist.
- Exit criteria: JSON output matches fixtures and `knowledge_lint` still passes.
- Stop or go gate: stop if output lacks `blocking_effect: none`.

## MS-04 - Optional Docs Update
- Objective: Document prototype usage after it passes.
- Inputs: verified script.
- Outputs: bounded update to `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`.
- Entry criteria: implementation verification passes.
- Exit criteria: docs still call the tool advisory and non-blocking.
- Stop or go gate: stop if docs imply required adoption.

