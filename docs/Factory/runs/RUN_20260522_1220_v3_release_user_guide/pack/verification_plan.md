# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-22): Stage F verification plan.

| ID | Tier | Check | Pass Criteria |
|---|---|---|---|
| VP-01 | V1 | Knowledge lint. | `bash scripts/knowledge_lint.sh` exits 0. |
| VP-02 | V1 | V3 advisory lint. | `docs/Factory/v3` returns `ADVISORY_PASS`. |
| VP-03 | V2 | V3 operational-readiness eval. | `docs/Factory/v3` returns `ADVISORY_PASS`. |
| VP-04 | V2 | V3 natural-language pilot scan. | `docs/Factory/v3` returns `ADVISORY_PASS` with `--nl-pilot`. |
| VP-05 | V1 | Stage and pack lint. | Current run stage lint and pack lint return PASS. |
| VP-06 | V1 | Diff hygiene. | `git diff --check` exits 0. |

## Exit Criteria Status
PASS
