# Traceability Matrix

## Version
v1

## Change Log
- v1 (2026-05-18): Initial traceability matrix for v3 advisory lint implementation plan.

| Constraint ID | Severity | Statement | Source | Scope Tag | Verification Tier | Verification | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical | This run does not implement code. | [SOURCE:RAW] | OK | V0 | Scope review | intent_lock_report.md |
| C-002 | Critical | Future implementation must be standalone and optional. | [SOURCE:RAW] | OK | V1 | Standalone script review | verification_plan.md |
| C-003 | Critical | Protected v2 validators remain unchanged. | [SOURCE:RAW] | OK | V1 | No-touch diff review | verification_plan.md |
| C-004 | High | Advisory output stays non-blocking. | [SOURCE:RAW] | OK | V2 | Advisory status fixture | fixtures/verification/implementation_scope |
| C-005 | High | Runtime-kernel behavior remains out of scope. | [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md] | OK | V0 | Boundary review | verification_plan.md |

