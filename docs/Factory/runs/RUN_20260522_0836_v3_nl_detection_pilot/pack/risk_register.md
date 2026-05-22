# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-22): Stage E risk register.

| Risk ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Critical | Default runner contract changes. | Existing fixture regression must pass. | VP-01 |
| R-02 | High | False positives on clean corpus. | Clean corpus target must return zero findings. | VP-02 |
| R-03 | High | Drift corpus misses intended families. | Seeded natural-language corpus must emit expected IDs. | VP-03 |
| R-04 | High | Advisory output becomes gate-like. | Check `blocking_effect: none`. | VP-04 |
| R-05 | High | Implementation violates SIMPLE-CODE-GATE. | Keep code direct and dependency-free. | VP-05 |

## Exit Criteria Status
- PASS
