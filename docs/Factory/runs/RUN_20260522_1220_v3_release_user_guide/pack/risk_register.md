# Risk Register - V3-OP-001 Release Approval And User Guide

## Version
v1

## Change Log
- v1 (2026-05-22): Stage E risk register.

| ID | Risk | Severity | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Optional release is overstated as default V3. | Critical | Approval artifact and guide state optional `V3-OP-001` only. | VP-02, VP-03 |
| R-02 | V2 fallback is weakened. | Critical | Guide and templates require fallback review. | VP-01, VP-04 |
| R-03 | Slot-game example crosses regulated/payment scope. | High | Route real-money, auth, payments, compliance, deployment, and production RNG to V2/heavier governance. | VP-03, guide review |
| R-04 | Templates create bloat. | High | Keep four minimal templates. | VP-06 |

## Exit Criteria Status
PASS
