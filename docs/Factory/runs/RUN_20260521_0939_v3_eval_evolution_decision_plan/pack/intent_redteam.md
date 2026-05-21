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
| RT-01 | Critical | The brief could be read as optimizing for a tool decision instead of confidence to use V3 operationally. | A narrow matcher discussion could miss the broader operational readiness goal. | Make confidence thresholds and required pilots first-class acceptance criteria. | Fixed in Stage C |
| RT-02 | High | Broader natural-language detection could create noisy warnings and reduce trust. | False positives could make the advisory runner feel arbitrary before V3 is mature. | Require a false-positive budget and human classification loop before any broader detection matters. | Fixed in Stage C |
| RT-03 | High | Trigger-marker fixtures are too narrow to support operational confidence alone. | Passing seeded triggers proves regression coverage, not real drift discovery. | Keep trigger markers as regression backbone but require real pilots and targeted natural-language evaluation. | Fixed in Stage C |
| RT-04 | Medium | V3-G011 severity remains unresolved. | Code bloat may need to block future operational profiles, not merely warn. | Carry severity policy into the next pilot/design pack. | Bounded deferral |

## Agent Failure Modes
- Agent overfocuses on implementing detection instead of planning the evidence path.
- Agent treats advisory findings as operational authorization.
- Agent underweights V2 fallback because the target is V3 confidence.

## Verification Holes
- Need explicit pilots for interruption/reentry, V2 fallback, and failed-verification halt behavior.
- Need traceability from each confidence threshold to a pilot or eval artifact.

## Exit Criteria Status
- PASS
