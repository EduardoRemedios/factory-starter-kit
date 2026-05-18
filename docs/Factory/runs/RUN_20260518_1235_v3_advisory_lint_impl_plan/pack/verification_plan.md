# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-18): Initial verification plan for v3 advisory lint implementation plan.

## Strategy
Future implementation should be verified as an optional standalone script with deterministic fixtures and no required-gate integration.

## Checks

### V1-CHECK-001 - Standalone Optional Script
- Tier: V1
- Covers: R-001
- Method: Review future diff for absence of calls from required v2 validators.
- Expected: only `scripts/factory_v3_advisory_lint.py` implements advisory behavior.

### V1-CHECK-002 - Protected File No-touch
- Tier: V1
- Covers: R-002
- Method: Check future diff excludes `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, `scripts/factory_pack_lint.py`, and `docs/Factory/Spec/STAGE_CONTRACTS.md`.
- Expected: no protected files changed.

### V2-FIXTURE-001 - Advisory Status Fixture
- Tier: V2
- Covers: R-003
- Method: Fixture asserts `ADVISORY_WARN` and `blocking_effect: none`.
- Expected: warning does not imply required gate failure.

### V0-REVIEW-001 - Runtime Boundary Review
- Tier: V0
- Covers: R-004
- Method: Human review checks that runtime vocabulary is warning-only.
- Expected: no runtime authority claim.

### V2-FIXTURE-002 - Fixture Coverage
- Tier: V2
- Covers: R-005
- Method: Future tests include clean, warning, and promotion-claim cases.
- Expected: each fixture has deterministic expected output.

## Future Commands
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3`
- `bash scripts/knowledge_lint.sh`

## Manifest Decision
- No `verification_manifest.yaml` is created because this is planning-only.

