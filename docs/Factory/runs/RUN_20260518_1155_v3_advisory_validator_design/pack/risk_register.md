# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-18): Initial risk register for v3 advisory validator design.

| ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-001 | Critical | Advisory validator blocks v2 runs. | Define non-blocking output and exclude required command wiring. | V1-CHECK-001 |
| R-002 | Critical | Advisory output implies v3 release authority. | Require Level 0 research status in report. | V1-CHECK-002 |
| R-003 | High | Boundary checks duplicate AEGIS judgments. | Limit to warning flags and human review. | V0-REVIEW-001 |
| R-004 | High | False positives are not tracked. | Add `review_status` and `review_notes` fields. | V2-FIXTURE-001 |
| R-005 | High | False negatives are invisible. | Require follow-up review after pilot use. | V0-REVIEW-002 |
| R-006 | Medium | Future command location is chosen too early. | Keep command name candidate-only. | V0-REVIEW-003 |

## Required Verification
- Critical and High risks must be represented in verification planning before pack closure.

