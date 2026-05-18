# Raw Brief - Factory v3 Advisory Validator Design

## Request
Use Factory v2 to plan MS-03 advisory validator design for Factory v3 research.

## Context
- Factory v2 remains the current operating process.
- Factory v3 remains Level 0 research.
- `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md` defines candidate advisory checks but no implementation.
- `docs/Factory/v3/evals/EVAL_20260518_001.md` recommends designing advisory validator shape before writing validator code.

## Goal
Create a planning-only pack that defines the exact advisory validator design, output shape, fixture examples, false-positive review workflow, and guardrails needed before any validator code is implemented.

## Constraints
- Planning only.
- Do not implement validator code.
- Do not edit `scripts/factoryctl`, `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, or `scripts/factory_pack_lint.py`.
- Do not add JSON schema files.
- Do not make any v3 advisory check block Factory v2 runs.
- Do not change Factory v2 stage contracts, Mission Mode, or execution authorization behavior.
- Keep AEGIS optional and external.
- Keep runtime-kernel behavior out of Factory.

## Required Answers
1. What exact advisory checks should exist first?
2. What should the advisory report output shape be?
3. What fixtures should prove the advisory design catches useful issues?
4. How should false positives and false negatives be reviewed?
5. What must stay out of implementation scope?
6. What criteria should be met before writing validator code?

