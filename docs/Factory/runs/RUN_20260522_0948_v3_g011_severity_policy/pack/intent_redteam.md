# Intent Red Team - V3-G011 Severity Policy

## Version
v1

## Change Log
- v1 (2026-05-22): Stage B red-team review.

## Iteration
Iteration: 1 of max 2

## Findings

| ID | Severity | Finding | Why It Matters | Recommendation |
|---|---|---|---|---|
| RT-01 | High | Policy could become V3-only. | The user clarified Factory V2 and V3 are used across ordinary projects. | Put the policy under `docs/Factory/` and cite it from V3 docs. |
| RT-02 | High | AEGIS framing could dominate. | Most adopting repos do not have a runtime kernel. | Make AEGIS an optional addendum only. |
| RT-03 | Medium | Blocker language could be too broad. | Over-broad blockers would make Factory noisy. | Define blocker class around material implementation risk and operational closeout. |

## Verification Holes
- Need repo checks to confirm policy wording does not trigger V3 advisory findings.

## Exit Criteria
PASS
