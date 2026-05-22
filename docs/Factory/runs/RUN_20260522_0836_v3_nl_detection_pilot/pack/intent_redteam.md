# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-22): Stage B red-team review.

## Iteration
Iteration: 1 of max 2

## Findings

| ID | Severity | Finding | Recommendation | Status |
|---|---|---|---|---|
| RT-01 | Critical | Natural-language detection could create noisy gate-like behavior. | Keep it opt-in, advisory, and outside required gates. | Fixed |
| RT-02 | High | Adding fields to default JSON could break fixture contracts. | Preserve default output unless pilot mode is enabled. | Fixed |
| RT-03 | High | Broad semantic matching could be brittle. | Use small paragraph-local patterns and clean corpus measurement. | Fixed |

## Exit Criteria Status
- PASS
