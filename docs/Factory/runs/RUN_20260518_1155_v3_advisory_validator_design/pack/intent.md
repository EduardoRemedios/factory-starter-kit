# Factory v3 Advisory Validator Design Intent

## Version
v1

## Change Log
- v1 (2026-05-18): Initial planning-only intent for Factory v3 advisory validator design.

## Purpose
Plan the first Factory v3 advisory validator design without implementing validator code or changing Factory v2 behavior. [SOURCE:RAW]

## Goal
Define exact advisory checks, report shape, fixture examples, false-positive review workflow, implementation exclusions, and criteria required before a later run may write validator code. [SOURCE:RAW]

## Non-goals
- Do not implement validator code. [SOURCE:RAW]
- Do not edit `scripts/factoryctl`, `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, or `scripts/factory_pack_lint.py`. [SOURCE:RAW]
- Do not add JSON schema files. [SOURCE:RAW]
- Do not make any v3 advisory check block Factory v2 runs. [SOURCE:RAW]
- Do not change Factory v2 stage contracts, Mission Mode, or execution authorization. [SOURCE:RAW]
- Do not introduce AEGIS dependency or runtime-kernel behavior. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]

## Principles
- Advisory means non-blocking, opt-in, and explicitly separate from v2 required gates. [SOURCE:REF:docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md]
- The first validator design should prefer high-signal doc-boundary checks over broad semantic analysis. [SOURCE:REF:docs/Factory/v3/evals/EVAL_20260518_001.md]
- False positives and false negatives must be captured before any advisory check can be promoted. [SOURCE:REF:docs/Factory/v3/PROMOTION_CRITERIA.md]
- AEGIS-compatible language must not become an AEGIS dependency. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]

## Roles
- Root Planner: keep the run planning-only and preserve v2 run evidence. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]
- Validator Designer: define candidate checks and output shape. [SOURCE:RAW]
- Boundary Reviewer: check v2 and AEGIS separation. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- Verification Specialist: define fixtures and review workflow. [SOURCE:RAW]
- Purple Gate: decide whether the design is ready for a later implementation-planning run. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]

## Acceptance Criteria
- Exact first advisory checks are named and scoped. [SOURCE:RAW]
- Report output shape is defined as non-blocking. [SOURCE:RAW]
- Fixture examples are defined for useful warnings and clean passes. [SOURCE:RAW]
- False-positive and false-negative review workflow is defined. [SOURCE:RAW]
- Implementation exclusions are explicit. [SOURCE:RAW]
- Criteria before writing validator code are explicit. [SOURCE:RAW]

## Open Questions
### BLOCKING
- None.

### NON-BLOCKING
- Should the future command live under `factoryctl v3-advisory-lint` or a separate script first?
- Should fixture examples be markdown-only or include small JSON inputs in the later implementation run?

## Go Or No-Go Rule
- GO if the pack defines a bounded non-blocking advisory validator design and preserves v2 behavior.
- NO-GO if the pack authorizes code changes, required gates, JSON schemas, AEGIS dependency, or runtime enforcement.

