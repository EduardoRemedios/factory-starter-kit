# Intent Synthesis

## Version
v1

## Change Log
- v1 (2026-05-18): Initial synthesis for implementation-plan intent.

## Iteration
- Iteration: 1 of max 2

## Synthesis
- The run remains valid if it produces an implementation plan only.
- Future implementation should add one standalone optional script, not a `factoryctl` subcommand.
- Fixtures must prove `blocking_effect: none` for every status.
- Required v2 validator files must be excluded from write scope.

## Hardened Requirements
- Future write set: `scripts/factory_v3_advisory_lint.py` and fixtures under `tests/fixtures/factory_v3_advisory_lint/`.
- Optional docs update: `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md` only after implementation evidence exists.
- Explicit no-touch set: required v2 validators and stage contracts.

## Scope Expansion Review
- No scope expansion introduced.

