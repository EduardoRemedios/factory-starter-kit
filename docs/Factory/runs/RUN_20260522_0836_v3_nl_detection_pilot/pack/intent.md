# Intent - V3 Natural-language Advisory Detection Pilot

## Version
v2

## Change Log
- v1 (2026-05-22): Initial Stage A intent.
- v2 (2026-05-22): Stage C clarified opt-in behavior and false-positive budget.

## Purpose
Complete V3 operational decision checklist item C-03 by implementing and measuring a bounded natural-language advisory detection pilot.

## Goal
Add an opt-in pilot mode to `scripts/factory_v3_operational_readiness_eval.py` that detects a small set of paragraph-local natural-language drift patterns without changing default deterministic behavior.

## Non-goals
- Do not promote V3.
- Do not wire the runner into required gates.
- Do not add external dependencies.
- Do not implement broad semantic scoring.
- Do not change Factory v2 validators.

## Detection Families
- V2 deprecation / replacement language.
- V3 promotion claims lacking evidence and human release approval.
- Runtime-kernel authority or production mediation claims.
- Explicit continuation after failed verification.
- Derived continuity overriding authored artifacts.
- SIMPLE-CODE-GATE over-abstraction / dependency-creep language.

## Acceptance Criteria
- Default fixture regression remains unchanged.
- Pilot mode reports seeded drift findings.
- Pilot mode reports zero false positives across at least 10 clean artifacts.
- Checklist C-03 is updated only if false-positive budget is met.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- C-04 V3-G011 severity policy remains a later decision.
