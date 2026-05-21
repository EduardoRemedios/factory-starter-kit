# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E risk register.

| Risk ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Critical | Premature V3 operational use before evidence thresholds are met. | Require decision report plus human approval after named pilots. | VP-01, TM-01 |
| R-02 | Critical | V3 loses V2 fallback or implies V2 deprecation. | Preserve fallback criteria in all next-step artifacts. | VP-02, TM-02 |
| R-03 | High | Broader detection produces excessive false positives. | Pilot behind advisory-only review with a numeric budget. | VP-03, TM-03 |
| R-04 | High | Trigger-marker fixtures miss natural drift. | Combine fixtures with real shadow and seeded drift pilots. | VP-04, TM-04 |
| R-05 | High | Reentry and halt behavior remain untested. | Require interruption/reentry and failed-verification pilots. | VP-05, TM-05 |
| R-06 | High | SIMPLE-CODE-GATE remains warning-only in unsuitable cases. | Decide severity policy before operational profile use. | VP-06, TM-06 |

## Exit Criteria Status
- PASS
