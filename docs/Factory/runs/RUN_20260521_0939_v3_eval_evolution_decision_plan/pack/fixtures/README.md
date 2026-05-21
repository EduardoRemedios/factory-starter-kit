# Fixture Plan

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F fixture plan for the next V3 eval evolution decision.

## Planned Fixture / Pilot Classes

| ID | Type | Purpose | Expected Result |
|---|---|---|---|
| FX-01 | real shadow pilot | Scan a clean V2-authoritative run root. | `ADVISORY_PASS` or classified warnings only. |
| FX-02 | interruption/reentry pilot | Verify stale or conflicting continuity halts. | Finding accepted if source artifacts conflict with resume cursor. |
| FX-03 | V2 fallback pilot | Verify V3 declines unsuitable work. | PASS when V2 fallback is selected and documented. |
| FX-04 | failed-verification pilot | Verify failed checks halt and preserve evidence. | Finding accepted if continuation occurs after halt-on-failure check. |
| FX-05 | natural-language drift corpus | Measure broader detection false positives. | False positives stay within budget before operational use. |

## Notes
- This planning run does not create executable fixtures.
- Future fixture implementation requires a separate execution-enabled pack.
