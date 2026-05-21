# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E risk register.

| Risk ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Critical | Required-gate wiring slips in. | Limit file scope and no-touch check gate scripts. | VP-05 |
| R-02 | Critical | Runner implies V3 promotion. | Assert advisory-only output fields. | VP-02 |
| R-03 | High | Fixture coverage misses negative cases. | Require V3-G001 through V3-G014. | VP-01 |
| R-04 | High | Implementation adds dependency creep. | Use standard library only. | VP-04 |
| R-05 | High | V2 fallback not protected. | Include deprecation and fallback fixtures. | VP-01 |
| R-06 | Medium | Real-doc smoke is forgotten. | Add `docs/Factory/v3` smoke command. | VP-03 |

## Residual Risk
Matcher tuning may be needed after first real pilots. The runner must remain advisory while tuning evidence accumulates.
