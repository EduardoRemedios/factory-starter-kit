# Intent - V3 Eval Evolution Decision Plan

## Version
v2

## Change Log
- v1 (2026-05-21): Initial Stage A intent.
- v2 (2026-05-21): Stage C synthesis clarified the operational-confidence target and staged detection path.

## Purpose
Define the next planning step needed to build confidence for eventual Factory v3 operational use without prematurely promoting V3 or weakening V2 fallback.

## Goal
Produce a planning-only Factory v2 pack that selects the next V3 eval evolution path and identifies the evidence required before Factory v3 can be used operationally.

## Decision Target
Recommended path: **staged combined path**.

1. Keep deterministic trigger-marker fixtures as the stable regression backbone.
2. Run the missing confidence pilots under V2 authority.
3. Design broader natural-language drift detection only as a bounded advisory layer with explicit false-positive controls.
4. Reassess operational V3 use only after the pilots and detection evidence meet the thresholds in this pack.

## Non-goals
- Do not promote Factory v3.
- Do not deprecate, discourage, or hide Factory v2.
- Do not implement new matcher logic or natural-language detection in this run.
- Do not wire V3 evals into required Factory gates or CI.
- Do not claim runtime-kernel authority, AEGIS proof, production mediation, or fail-closed runtime enforcement.

## Principles
- Confidence requires real operational evidence, not only narrative docs.
- Deterministic fixtures are necessary for regression control but insufficient for broad drift discovery.
- Broader detection must earn trust through measured false positives before influencing readiness decisions.
- V3 can become operational only for named mission profiles with explicit V2 fallback.
- SIMPLE-CODE-GATE v2 remains mandatory for code-changing V2 and V3 work.

## Roles
- Factory v2: authoritative planning process for this run.
- Factory v3 eval runner: advisory evidence source only.
- Human sponsor: sole authority for any future V3 operational promotion.
- Future implementation agent: may implement only from a later execution-enabled pack.

## Acceptance Criteria
- The pack reaches Stage I2 PASS or CONDITIONAL PASS.
- The pack states the chosen eval evolution path.
- The pack defines operational-confidence thresholds for V3 use.
- The pack names the next required pilots and their expected evidence.
- The pack keeps V2 authoritative and available as fallback.

## Operational Confidence Thresholds
Factory v3 can be reconsidered for optional operational use only when all are true:

1. At least three real V2-authoritative V3 shadow pilots complete with classified findings.
2. One interruption/reentry pilot proves resume from authored artifacts and halt on stale or conflicting continuity.
3. One V2 fallback pilot proves V3 declines unsuitable work.
4. One failed-verification pilot proves halt behavior with preserved evidence.
5. Seeded drift coverage includes V3-G003, V3-G006, V3-G010, V3-G012, V3-G013, and V3-G014, in addition to current V3-G005, V3-G007, V3-G009, and V3-G011.
6. Any broader natural-language detection has a recorded false-positive rate at or below the agreed pilot budget.
7. A decision report names exact revisions, paths, pilots, false positives, false negatives, residual risks, and a human approval record.

## Open Issues
### BLOCKING
- None for this planning pack.

### NON-BLOCKING
- Future false-positive budget may need tuning after two additional real-run shadow pilots.
