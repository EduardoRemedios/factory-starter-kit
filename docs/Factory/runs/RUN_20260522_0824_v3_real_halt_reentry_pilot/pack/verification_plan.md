# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-22): Stage F verification plan.

| ID | Tier | Check | Pass Criteria |
|---|---|---|---|
| VP-01 | V2 | Failed-command halt behavior. | Evidence records nonzero exit, `halted: true`, and no continuation marker. |
| VP-02 | V2 | Authored-artifact reentry behavior. | Valid scenario resumes from source artifacts; stale cursor scenario halts. |
| VP-03 | V0 | No promotion claim. | Reports and checklist retain research/advisory posture. |
| VP-04 | V1 | No production validator changes. | Diff touches no production validator or runner files. |
| VP-05 | V1 | Repo governance checks pass. | knowledge lint, pack-lint, V3 advisory scans, and diff check pass. |

## Exit Criteria Status
- PASS
