# Traceability Matrix

## Version
v1

## Change Log
- v1 (2026-05-18): Initial traceability matrix for Factory v3 research planning.

| Constraint ID | Severity | Statement | Source | Scope Tag | Verification Tier | Verification | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical | Preserve v2 as the current operating core. | [SOURCE:RAW] | OK | V1 | V2 stage order guard | verification_plan.md |
| C-002 | Critical | Do not duplicate AEGIS or runtime-kernel behavior. | [SOURCE:RAW] | OK | V0 | Boundary review | verification_plan.md |
| C-003 | High | Keep v3 research-only until explicit promotion. | [SOURCE:RAW] | OK | V1 | Required validator isolation | verification_plan.md |
| C-004 | High | Identify exact v3 artifact paths. | [SOURCE:RAW] | OK | V0 | Pack review | micro_sprints.md |
| C-005 | High | Define staged path from v2 intact to runtime integration. | [SOURCE:RAW] | OK | V0 | Pack review | micro_sprints.md |
| C-006 | High | Define eval and promotion criteria. | [SOURCE:RAW] | OK | V2 | Promotion gate fixture | fixtures/verification/v3_promotion_gate |
| C-007 | High | Provide public README split language. | [SOURCE:RAW] | OK | V0 | README split review | verification_plan.md |

