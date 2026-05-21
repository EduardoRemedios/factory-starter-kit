# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F verification plan.

| ID | Tier | Check | Pass Criteria |
|---|---|---|---|
| VP-01 | V0 | Reports preserve advisory-only status. | Reports state no promotion and blocking effect none. |
| VP-02 | V1 | Real shadow scans run. | Two real run outputs are recorded. |
| VP-03 | V0 | Natural-language design is bounded. | Design has false-positive budget and no gate effect. |
| VP-04 | V1 | V2 fallback positive pilot runs. | V3-G012 returns `ADVISORY_PASS`. |
| VP-05 | V1 | Reentry and evidence gap pilots run. | V3-G010 and V3-G006 findings are accepted. |
| VP-06 | V1 | Scope and promotion gaps run. | V3-G003 and V3-G014 findings are accepted. |
| VP-07 | V1 | Pack and repo checks pass. | stage-lint, pack-lint, advisory scans, and diff check pass. |

## Verification Manifest
This execution-enabled run uses command verification recorded in the envelope and execution closeout. A YAML manifest is not created because the repo's current pack-lint manifest schema is optional and the approved verification commands are already explicit in the envelope.

## Exit Criteria Status
- PASS
