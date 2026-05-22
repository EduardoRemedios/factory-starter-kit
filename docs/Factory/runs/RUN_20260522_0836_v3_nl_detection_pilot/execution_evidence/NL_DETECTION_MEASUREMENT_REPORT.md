# Natural-language Detection Measurement Report

## Version
v1

## Change Log
- v1 (2026-05-22): Measurement report for the opt-in natural-language advisory detection pilot.

## Status
Advisory pilot evidence only. This report does not promote Factory v3 or wire any check into required gates.

## Scope
- Runner mode: `--nl-pilot`
- Clean corpus: `tests/fixtures/factory_v3_operational_readiness_nl_pilot/clean`
- Drift corpus: `tests/fixtures/factory_v3_operational_readiness_nl_pilot/drift`
- Real-doc smoke target: `docs/Factory/v3`

## Results
| Corpus | Files | Findings | Status |
|---|---:|---:|---|
| Clean | 10 | 0 | PASS |
| Drift | 7 | 7 | PASS |
| Real V3 docs smoke | 13 | 0 | PASS |

## Drift IDs Detected
- V3-G003
- V3-G005
- V3-G007
- V3-G009
- V3-G010
- V3-G011
- V3-G014

## False-positive Review
- Clean false positives: 0
- Real V3 docs smoke false positives: 0
- Budget: at most 1 across at least 10 clean artifacts
- Result: within budget

## False-negative Review
- Known drift misses in this pilot corpus: 0
- Limitation: this is a small curated corpus, not broad production measurement.

## Decision
C-03 has enough pilot evidence to move to DONE for the current operational decision checklist. Future operational profile work still needs C-04 through C-10.
