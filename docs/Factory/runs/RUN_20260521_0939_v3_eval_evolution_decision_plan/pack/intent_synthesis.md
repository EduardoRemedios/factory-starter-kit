# Intent Synthesis

## Version
v1

## Change Log
- v1 (2026-05-21): Stage C synthesis after Red Team.

## Iteration
Iteration: 1 of max 2

## Synthesis
Red Team correctly identified that the pack must optimize for confidence to use V3 operationally, not merely for a matcher design choice. The intent was updated to make operational-confidence thresholds explicit.

The selected path is a staged combined path:
- deterministic trigger-marker fixtures remain the regression backbone
- missing real pilots come next
- broader natural-language detection is designed only with a false-positive budget and review loop
- no V3 operational use is authorized until the threshold evidence exists

## Changes Made
- Added operational-confidence thresholds to `intent.md`.
- Made the staged combined path the recommended decision.
- Added explicit false-positive control requirement.
- Preserved V2 as authoritative fallback throughout the evidence-building phase.

## Scope Expansion Review
- No `[SCOPE EXPANSION]` items introduced.

## Remaining Findings
- RT-04 remains as a bounded future severity-policy decision, hooked to MS-02 and MS-04.

## Exit Criteria Status
- PASS
