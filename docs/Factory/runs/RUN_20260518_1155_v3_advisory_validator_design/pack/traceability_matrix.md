# Traceability Matrix

## Version
v1

## Change Log
- v1 (2026-05-18): Initial traceability matrix for v3 advisory validator design.

| Constraint ID | Severity | Statement | Source | Scope Tag | Verification Tier | Verification | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical | Design only; no validator implementation. | [SOURCE:RAW] | OK | V0 | Scope review | intent_lock_report.md |
| C-002 | Critical | Advisory checks must not block v2 runs. | [SOURCE:RAW] | OK | V1 | Non-blocking output shape | verification_plan.md |
| C-003 | Critical | Required v2 validators must remain unchanged. | [SOURCE:RAW] | OK | V1 | Required-gate isolation review | verification_plan.md |
| C-004 | High | Report shape must support false-positive review. | [SOURCE:RAW] | OK | V2 | Warning report fixture | fixtures/verification/advisory_report_shape |
| C-005 | High | Boundary checks must not duplicate AEGIS. | [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md] | OK | V0 | Boundary review | verification_plan.md |
| C-006 | High | Criteria before writing validator code must be explicit. | [SOURCE:RAW] | OK | V0 | Pack review | micro_sprints.md |

