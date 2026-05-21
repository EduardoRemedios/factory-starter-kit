# Intent - V3 Confidence Pilot Execution

## Version
v2

## Change Log
- v1 (2026-05-21): Initial Stage A intent.
- v2 (2026-05-21): Stage C synthesis clarified pilot evidence classes and non-promotion limits.

## Purpose
Run the next bounded evidence batch needed to build confidence toward future operational Factory v3 use.

## Goal
Collect advisory pilot evidence under Factory v2 authority for real-run shadow behavior, missing seeded drift cases, positive routing cases, controlled halt behavior, and bounded natural-language detection design.

## Non-goals
- Do not promote V3 operationally.
- Do not deprecate or discourage V2.
- Do not wire V3 evals into required gates.
- Do not change the current eval runner unless a blocking execution defect appears.
- Do not claim runtime-kernel authority or production proof.

## Principles
- Evidence should move us toward confidence, not create a release claim.
- Real-run shadow evidence and negative seeded cases serve different purposes and both are needed.
- Positive routing cases matter because V3 must know when not to operate.
- Failed verification must halt in any future operational profile.
- Natural-language detection remains advisory until its false-positive behavior is measured.

## Roles
- Factory v2: authoritative process and fallback.
- Factory v3 eval runner: advisory evidence source.
- Human sponsor: approved bounded execution, retains release authority.
- Execution agent: creates fixtures/reports and runs approved commands only.

## Acceptance Criteria
1. Two additional real-run shadow scans are recorded and classified.
2. Seeded negative drift pilots cover V3-G003, V3-G006, V3-G010, and V3-G014.
3. Positive routing pilots cover V3-G012 and V3-G013.
4. Controlled failed-verification halt pilot is recorded.
5. Natural-language detection design records a false-positive budget and no gate effect.
6. Batch rollup states whether confidence increased and what remains before operational V3 use.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- V3-G011 severity policy remains unresolved and is carried forward.
