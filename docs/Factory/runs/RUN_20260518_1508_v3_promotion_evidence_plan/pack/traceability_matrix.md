# Traceability Matrix

## Version
v1

## Change Log
- v1 (2026-05-18): Initial traceability matrix for promotion-evidence advisory lint planning.

| Requirement | Severity | Source | Verification |
| --- | --- | --- | --- |
| R-001: Future pilot must remove temporary unsafe promotion wording and restore clean docs. | High | `pack/intent.md`; `pack/risk_register.md` | V1-CHECK-001, V1-CHECK-003 |
| R-002: Future pilot must not promote Factory v3. | Critical | `docs/PROJECT_STATE.md`; `pack/intent.md` | V1-CHECK-002, V0-REVIEW-001 |
| R-003: Future pilot must not wire advisory lint into required gates or CI. | Critical | `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`; `pack/intent.md` | V1-CHECK-002 |
| R-004: Matcher tuning is forbidden unless evidence justifies a later implementation run. | High | `pack/intent.md`; `REAL_BRANCH_WARNING_PILOT_REPORT.md` | V0-REVIEW-002 |
| R-005: AEGIS and runtime-kernel authority remain external. | Critical | `docs/Factory/AEGIS_BOUNDARY.md` | V0-REVIEW-003 |
| R-006: Every emitted finding must be classified. | High | `docs/Factory/v3/PILOT_PROFILE_PLAN.md`; `pack/intent.md` | V1-CHECK-001, V0-REVIEW-004 |

## Coverage Summary
- Critical requirements: R-002, R-003, R-005 all have verification coverage.
- High requirements: R-001, R-004, R-006 all have verification coverage.
- No requirement depends on required gate integration.

