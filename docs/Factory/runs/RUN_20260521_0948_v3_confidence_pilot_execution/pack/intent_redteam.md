# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-21): Stage B red-team review.

## Iteration
Iteration: 1 of max 2

## Findings

| ID | Severity | Finding | Why It Matters | Recommendation | Status |
|---|---|---|---|---|---|
| RT-01 | Critical | Running pilots could be misread as V3 operational use. | The goal is confidence building, not promotion. | Require every report to state advisory-only and `promotion_decision: not_authorized`. | Fixed |
| RT-02 | High | Positive V3-G012 and V3-G013 pilots have no trigger findings. | A pass case could be mistaken for missing coverage. | Classify them as positive routing evidence, not negative detection. | Fixed |
| RT-03 | High | Failed-verification halt pilot could duplicate V3-G005 seeded text only. | Operational confidence needs actual halt semantics later. | Record current pilot as controlled seeded halt evidence and carry forward real failed-check pilot gap. | Fixed |
| RT-04 | Medium | Natural-language detection design could imply implementation. | That would expand scope. | Keep it as design-only with no code changes. | Fixed |

## Agent Failure Modes
- Treat advisory runner output as promotion approval.
- Modify matcher logic without approval.
- Hide that the current runner remains trigger-marker based.

## Verification Holes
- Real natural-language false-positive measurement remains future work.
- Real failed-command halt behavior remains future work unless implemented by later profile tooling.

## Exit Criteria Status
- PASS
