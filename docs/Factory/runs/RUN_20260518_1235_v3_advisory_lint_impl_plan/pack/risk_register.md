# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-18): Initial risk register for v3 advisory lint implementation plan.

| ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-001 | Critical | Future script blocks v2 runs. | Keep standalone and non-blocking. | V1-CHECK-001 |
| R-002 | Critical | Protected validators are edited. | No-touch protected files. | V1-CHECK-002 |
| R-003 | High | Output confuses advisory warning with failure. | Require advisory status names. | V2-FIXTURE-001 |
| R-004 | High | Checks overreach into runtime-kernel semantics. | Only flag boundary vocabulary for review. | V0-REVIEW-001 |
| R-005 | Medium | Test fixtures are too sparse. | Require clean, warning, and promotion fixtures. | V2-FIXTURE-002 |

## Required Verification
- Critical and High risks require explicit verification coverage.

