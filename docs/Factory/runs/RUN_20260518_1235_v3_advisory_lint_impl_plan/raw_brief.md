# Raw Brief - Factory v3 Advisory Lint Implementation Plan

## Request
Use Factory v2 to plan a bounded implementation of the Factory v3 advisory lint prototype.

## Context
- Factory v2 remains the current operating process.
- Factory v3 remains research-only.
- `RUN_20260518_1155_v3_advisory_validator_design` passed and defines advisory checks, report shape, fixtures, and review workflow.
- The user said "Ok go" after the advisory validator design pack.

## Goal
Create an implementation planning pack that names exact files, verification, and constraints for a future advisory lint prototype.

## Execution Mode
PLANNING_ONLY

## Constraints
- Planning only in this run.
- Do not implement code in this run.
- Do not wire advisory lint into required v2 gates.
- Do not edit `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, or `scripts/factory_pack_lint.py`.
- Prefer a standalone optional script before any `factoryctl` integration.
- Keep output non-blocking with `blocking_effect: none`.
- Keep AEGIS optional and runtime-kernel behavior external.

## Required Answers
1. What exact files should a future implementation touch?
2. What initial advisory checks should be implemented?
3. What fixtures and tests should prove behavior?
4. What commands should verify the implementation?
5. What must remain out of scope?

