# Natural-language Detection Pilot Fixtures

## Version
v1

## Change Log
- v1 (2026-05-22): Stage F fixture inventory.

## Fixture Inventory
| Fixture | Purpose | Expected Result |
|---|---|---|
| clean corpus | false-positive measurement across at least 10 artifacts | zero findings |
| drift corpus | candidate natural-language detection | expected finding IDs emitted |

## Notes
- Concrete fixtures live under `tests/fixtures/factory_v3_operational_readiness_nl_pilot/`.
