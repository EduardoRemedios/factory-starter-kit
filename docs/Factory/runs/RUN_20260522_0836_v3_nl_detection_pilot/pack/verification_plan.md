# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-22): Stage F verification plan.

| ID | Tier | Check | Pass Criteria |
|---|---|---|---|
| VP-01 | V2 | Default fixture regression. | Existing expected JSON matches without pilot flag. |
| VP-02 | V2 | Clean corpus false-positive test. | Pilot mode returns zero findings on at least 10 clean artifacts. |
| VP-03 | V2 | Drift corpus detection test. | Pilot mode emits expected natural-language finding IDs. |
| VP-04 | V1 | Advisory non-gate behavior. | Pilot reports retain `blocking_effect: none` and `promotion_decision: not_authorized`. |
| VP-05 | V1 | SIMPLE-CODE-GATE implementation review. | Standard library only, direct local patterns, no broad abstraction. |
| VP-06 | V1 | Repo checks. | knowledge lint, V3 scans, pack-lint, diff check pass. |
| VP-07 | V2 | Real V3 docs smoke. | Pilot mode returns zero findings on current `docs/Factory/v3` planning docs. |

## Exit Criteria Status
- PASS
