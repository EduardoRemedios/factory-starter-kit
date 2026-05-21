# Confidence Pilot Batch Fixtures

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F fixture inventory for confidence pilot execution.

## Fixture / Pilot Inventory

| ID | Type | Expected Result |
|---|---|---|
| real_shadow_0815 | real run shadow | `ADVISORY_PASS` |
| real_shadow_0939 | real run shadow | `ADVISORY_PASS` |
| v3g003_scope_expansion | seeded negative | `ADVISORY_FAIL_NON_BLOCKING` with V3-G003 |
| v3g006_evidence_gap | seeded warning | `ADVISORY_WARN` with V3-G006 |
| v3g010_reentry | seeded negative | `ADVISORY_FAIL_NON_BLOCKING` with V3-G010 |
| v3g012_v2_fallback | positive routing | `ADVISORY_PASS` |
| v3g013_v3_with_fallback | positive routing | `ADVISORY_PASS` |
| v3g014_promotion_gap | seeded negative | `ADVISORY_FAIL_NON_BLOCKING` with V3-G014 |
| controlled_halt_v3g005 | seeded halt | `ADVISORY_FAIL_NON_BLOCKING` with V3-G005 |

## Notes
- All pilots are advisory and non-blocking.
- Fixture implementation occurs under `execution_evidence/`.
