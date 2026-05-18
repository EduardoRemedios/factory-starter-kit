# SPRINT_20260518_003 Envelope

## Version
v1

## Change Log
- v1 (2026-05-18): Initial envelope for v3 advisory lint implementation plan.

## Sprint Objective
Plan a future optional standalone Factory v3 advisory lint prototype.

## Execution Mode
- Mode: PLANNING_ONLY
- Implementation is not authorized by this pack.

## Future Write Set
- `scripts/factory_v3_advisory_lint.py`
- `tests/fixtures/factory_v3_advisory_lint/clean/input/`
- `tests/fixtures/factory_v3_advisory_lint/clean/expected.json`
- `tests/fixtures/factory_v3_advisory_lint/warning/input/`
- `tests/fixtures/factory_v3_advisory_lint/warning/expected.json`
- `tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/`
- `tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json`
- Optional after verification: `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`

## No-touch Files
- `scripts/knowledge_lint.sh`
- `scripts/factory_stage_lint.py`
- `scripts/factory_pack_lint.py`
- `scripts/factoryctl`
- `docs/Factory/Spec/STAGE_CONTRACTS.md`
- `docs/Factory/Spec/DEFINITIONS.md`
- `docs/Factory/ORCHESTRATION.md`

## Initial Checks
- V3-A001: v2 core preservation phrase check.
- V3-A002: v3 research-only posture check.
- V3-A003: shadow schema isolation phrase check.
- V3-A004: AEGIS optionality phrase check.
- V3-A005: runtime-kernel boundary warning scan.
- V3-A006: promotion evidence requirement check.

## Output Requirements
- `status` is one of `ADVISORY_PASS`, `ADVISORY_WARN`, or `ADVISORY_FAIL_NON_BLOCKING`.
- `blocking_effect` is exactly `none`.
- JSON output is deterministic.
- Text output clearly says advisory and non-blocking.

## Verification Commands
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3`
- `bash scripts/knowledge_lint.sh`
- Future fixture command defined by the implementation run.

## File-touch Budget
- MS-01: max files modified 0, created 1, deleted 0.
- MS-02: max files modified 0, created 6, deleted 0.
- MS-03: max files modified 0, created 1, deleted 0.
- MS-04: max files modified 1, created 0, deleted 0.
- Sprint total: max files modified 1, created 8, deleted 0.

## Out Of Scope
- Required gate wiring.
- `factoryctl` subcommand.
- JSON schema files.
- Runtime-kernel enforcement.
- AEGIS dependency.

## Open Questions
- Whether fixture runner should be built into the script or kept as simple command examples.

