# Raw Brief - V3 Natural-language Advisory Detection Pilot

## Source
Human sponsor approved the next recommended step on 2026-05-22: proceed with bounded natural-language advisory detection and false-positive measurement.

## Execution Authorization
- Execution Mode: EXECUTION_ENABLED
- Execution Authorization: Human sponsor message "agree proceed" on 2026-05-22.
- Downstream Fan-Out: NOT APPROVED

## Goal
Implement an opt-in natural-language pilot mode for the standalone V3 operational-readiness eval runner, then measure it against a clean false-positive corpus and a seeded natural-language drift corpus.

## Scope
- Add pilot-only natural-language detection behind an explicit CLI flag.
- Preserve existing deterministic trigger-marker behavior and fixture output.
- Add clean and drift pilot corpora.
- Record false-positive measurement evidence.
- Update the operational decision checklist after closeout.

## Out of Scope
- No required-gate integration.
- No V3 operational promotion.
- No external NLP dependencies.
- No broad semantic scoring.
- No changes to Factory v2 stage or pack validators.

## Acceptance Criteria
- Existing operational-readiness fixture regression still passes unchanged.
- Pilot mode catches seeded natural-language drift cases.
- Pilot mode reports zero false positives on at least 10 clean artifacts.
- Reports remain advisory with `blocking_effect: none` and `promotion_decision: not_authorized`.
