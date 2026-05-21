# Premortem

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E premortem for V3 eval evolution decision.

## Failure Scenarios

| ID | Scenario | Impact | Mitigation |
|---|---|---|---|
| PM-01 | The team treats seeded trigger success as enough for operational confidence. | V3 could be used before it detects real drift. | Require real shadow pilots and missing pilot classes before promotion. |
| PM-02 | Natural-language detection is added too broadly and floods reviewers. | Advisory signal loses trust. | Require false-positive budget, review classification, and no required-gate wiring. |
| PM-03 | V3 confidence work accidentally implies V2 is legacy. | Users route unsuitable work to V3. | Keep V2 fallback and non-deprecation in acceptance criteria. |
| PM-04 | Failed-verification halt behavior is only tested narratively. | V3 could continue after a real check failure. | Require a controlled failed-verification pilot with preserved evidence. |
| PM-05 | Reentry is trusted without testing stale context. | Long-running missions resume from weak state. | Require interruption/reentry pilot with authored source artifacts as authority. |
| PM-06 | SIMPLE-CODE-GATE warnings remain too soft for operational work. | V3 may permit brittle or over-abstracted code. | Resolve severity policy before operational profile promotion. |

## Exit Criteria Status
- PASS
