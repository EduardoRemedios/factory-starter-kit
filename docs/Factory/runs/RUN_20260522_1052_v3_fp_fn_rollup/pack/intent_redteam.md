# Intent Red Team - V3-OP-001 Finding Rollup

## Version
v1

## Change Log
- v1 (2026-05-22): Stage B red-team review.

## Iteration
Iteration: 1 of max 2

## Findings

| ID | Severity | Finding | Why It Matters | Recommendation |
|---|---|---|---|---|
| RT-01 | High | Rollup could overstate false-negative proof. | Current evidence includes curated and seeded corpora, not broad production coverage. | State production false-negative discovery remains not measured. |
| RT-02 | High | Clean shadow scans could be mistaken for drift discovery. | Clean scans mainly prove low false positives. | Classify clean shadows separately from seeded drift. |
| RT-03 | High | C-08 update could imply operational release. | C-09 and C-10 are still required. | Keep C-09 and C-10 open and preserve research-only status. |

## Verification Holes
- Need V3 scans after rollup addition to ensure no promotion or runtime-authority findings.

## Exit Criteria
PASS
