# Factory v3 Phase 1 Trial Index

## Version
v0.7

## Change Log
- v0.7 (2026-05-24): Recorded owner waiver for the non-author user trial requirement and moved batch to decision-review readiness.
- v0.6 (2026-05-24): Recorded first completed Temper `V3-OP-001` happy-path implementation trial.
- v0.5 (2026-05-24): Recorded second completed Harmony `V3-OP-001` happy-path implementation trial.
- v0.4 (2026-05-24): Recorded first completed Harmony `V3-OP-001` happy-path implementation trial.
- v0.3 (2026-05-24): Recorded Harmony placeholder-submission trial as a pre-envelope V2 fallback and guide-update signal.
- v0.2 (2026-05-24): Recorded first Phase 1 trial as a V3-unsuitable fallback decision before mission-envelope creation.
- v0.1 (2026-05-24): Initial empty index for Phase 1 `V3-OP-001` real-project trials.

## Status
Research trial evidence index only. This document is non-enforcing and does not approve new V3 profiles, make V3 the default, deprecate V2, or wire V3 checks into required gates.

## Purpose
Track Phase 1 real-project `V3-OP-001` trials.

Use `docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md` for each trial record.

## Trial Summary

| Trial ID | Repository | User | Outcome | V2 Fallback Used | Separate Kernel | Evidence |
|---|---|---|---|---|---|---|
| `TRIAL_20260524_001_no_bounded_code_change` | `factory-starter-kit` | Eduardo Remedios / Codex | FALLBACK_TO_V2 | yes | no | `docs/Factory/v3/trials/TRIAL_20260524_001_no_bounded_code_change.md` |
| `TRIAL_20260524_002_harmony_placeholder_fallback` | Harmony | Eduardo Remedios / Harmony Codex session | FALLBACK_TO_V2 | yes | unknown | `docs/Factory/v3/trials/TRIAL_20260524_002_harmony_placeholder_fallback.md` |
| `TRIAL_20260524_003_harmony_faq_ingestion_utf8` | Harmony | Eduardo Remedios / Harmony Codex session | COMPLETED_WITH_V3 | no | unknown | `docs/Factory/v3/trials/TRIAL_20260524_003_harmony_faq_ingestion_utf8.md` |
| `TRIAL_20260524_004_harmony_currency_blank_defaults` | Harmony | Eduardo Remedios / Harmony Codex session | COMPLETED_WITH_V3 | no | unknown | `docs/Factory/v3/trials/TRIAL_20260524_004_harmony_currency_blank_defaults.md` |
| `TRIAL_20260524_005_temper_cs_send_aria_disabled` | Temper | Eduardo Remedios / Temper Codex session | COMPLETED_WITH_V3 | no | unknown | `docs/Factory/v3/trials/TRIAL_20260524_005_temper_cs_send_aria_disabled.md` |

## Batch Requirements

| Requirement | Target | Current |
|---|---:|---:|
| Total real-project trials | 5 | 5 |
| Ordinary repos without separate governance kernel | 2 | 2 |
| Trial by user other than V3 doc author | 1, or explicit owner waiver | waived by owner on 2026-05-24 |
| Trial with V2 fallback or V3-unsuitable decision | 1 | 2 |
| Trials with friction notes | 5 | 5 |
| Trials with advisory false-positive/false-negative notes | 5 | 5 |

## Current Batch Verdict
READY_FOR_PHASE_1_DECISION_REVIEW

## Notes
- First Phase 1 trial records that `V3-OP-001` was unsuitable because the request did not name a bounded code-changing objective.
- Second Phase 1 trial records that unchanged placeholders in an ordinary-repo prompt are a valid pre-envelope fallback trigger.
- Third Phase 1 trial records the first completed `V3-OP-001` happy-path implementation in Harmony.
- Fourth Phase 1 trial records the second completed `V3-OP-001` happy-path implementation in Harmony.
- Fifth Phase 1 trial records the first completed `V3-OP-001` happy-path implementation in Temper.
- The 5-trial minimum is met.
- The non-author user trial requirement is explicitly waived by the owner for this batch because the project is operated by a solo AI-native developer; see `docs/Factory/v3/trials/PHASE1_REQUIREMENT_WAIVER_20260524.md`.
- Batch is ready for Phase 1 decision review, not automatic Phase 2 implementation.
