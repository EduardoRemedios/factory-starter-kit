# V3 Advisory Lint Implementation Plan Intent

## Version
v1

## Change Log
- v1 (2026-05-18): Initial planning-only intent for v3 advisory lint implementation.

## Purpose
Plan a bounded future implementation of the Factory v3 advisory lint prototype without changing Factory v2 behavior. [SOURCE:RAW]

## Goal
Name exact files, checks, fixtures, and verification commands for a later optional advisory lint script. [SOURCE:RAW]

## Non-goals
- Do not implement code in this run. [SOURCE:RAW]
- Do not wire advisory lint into required v2 gates. [SOURCE:RAW]
- Do not edit `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, or `scripts/factory_pack_lint.py`. [SOURCE:RAW]
- Do not add runtime-kernel behavior or AEGIS dependency. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]

## Principles
- Prefer a standalone optional script before `factoryctl` integration. [SOURCE:RAW]
- Advisory output must include `blocking_effect: none`. [SOURCE:REF:docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md]
- All findings must remain reviewable and non-blocking. [SOURCE:REF:docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/verification_plan.md]

## Roles
- Root Planner: preserve v2 Factory run discipline.
- Implementer: future role only, limited to named files.
- Verification Specialist: define fixtures and commands.
- Purple Gate: confirm implementation scope does not alter v2 gates.

## Acceptance Criteria
- Exact future implementation files are listed. [SOURCE:RAW]
- Initial checks are scoped to deterministic advisory docs checks. [SOURCE:RAW]
- Fixtures and expected reports are specified. [SOURCE:RAW]
- Verification commands are named. [SOURCE:RAW]
- Out-of-scope files are explicit. [SOURCE:RAW]

## Open Questions
### BLOCKING
- None.

### NON-BLOCKING
- Whether a later approved implementation should add `factoryctl` integration after the standalone script proves useful.

## Go Or No-Go Rule
- GO if the pack creates a safe implementation plan with no code changes.
- NO-GO if the pack authorizes required gate wiring, runtime behavior, or AEGIS dependency.

