# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-22): Stage E risk register.

| Risk ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Critical | Failed command does not halt. | Harness asserts halt and no continuation marker. | VP-01 |
| R-02 | Critical | Reentry trusts stale derived state. | Harness halts when source/cursor conflict. | VP-02 |
| R-03 | High | Pilot overstated as promotion. | Checklist remains decision-prep and V3 unpromoted. | VP-03 |
| R-04 | High | Production validators changed unnecessarily. | File-touch budget forbids production validator changes. | VP-04 |

## Exit Criteria Status
- PASS
