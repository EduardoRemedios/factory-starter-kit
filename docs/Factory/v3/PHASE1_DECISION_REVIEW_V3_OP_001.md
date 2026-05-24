# Factory v3 Phase 1 Decision Review For V3-OP-001

## Version
v0.1

## Change Log
- v0.1 (2026-05-24): Initial Phase 1 decision review after the first 5 real-project `V3-OP-001` trial records.

## Status
Decision review complete. This document is research-only and non-enforcing: it does not make Factory v3 the default, approve new V3 profiles, deprecate Factory v2, wire V3 checks into required gates, or approve Phase 2 implementation beyond shadow mission-record design.

## Decision Metadata
- Decision: START_PHASE_2
- Decision scope: design a shadow structured mission-record format for `V3-OP-001`
- Date: 2026-05-24
- Human owner: Eduardo Remedios
- V3 profile reviewed: `V3-OP-001 Bounded Code Change`
- Factory v2 fallback retained: YES
- Required-gate integration approved: NO
- Default-mode promotion approved: NO
- New V3 profile approved: NO
- Runtime-kernel authority introduced: NO

## Decision Summary
The Phase 1 batch supports starting Phase 2 structured mission-record design in shadow mode.

It does not support making V3 the default, adding required gates, removing Factory v2 fallback, or expanding beyond `V3-OP-001`.

The strongest signal is that V3 handled three bounded happy-path implementation trials across Harmony and Temper, and correctly refused two unsuitable/pre-envelope cases before creating mission authority. The main design lesson is that Phase 2 needs an explicit machine-readable way to represent both pre-envelope rejection and thread-local mission envelopes.

## Evidence Inputs

| Evidence | Path | Result |
|---|---|---|
| Phase 1 trial plan | `docs/Factory/v3/PHASE1_TRIAL_PLAN.md` | Defines trial target, fallback rules, exit criteria, and expected decisions. |
| Trial index | `docs/Factory/v3/trials/TRIAL_INDEX.md` | 5 of 5 trial records complete; verdict `READY_FOR_PHASE_1_DECISION_REVIEW`. |
| Owner waiver | `docs/Factory/v3/trials/PHASE1_REQUIREMENT_WAIVER_20260524.md` | Non-author user trial requirement waived for solo AI-native development context. |
| V3 full roadmap | `docs/Factory/v3/ROADMAP_TO_FULL_VISION.md` | Phase 2 remains blocked until this decision review explicitly selects `START_PHASE_2`. |
| V3 user guide | `docs/Factory/v3/USER_GUIDE.md` | Updated from observed placeholder and thread-local-envelope friction. |

## Trial Batch Summary

| Trial | Repository | Outcome | Key Signal |
|---|---|---|---|
| `TRIAL_20260524_001_no_bounded_code_change` | factory-starter-kit | FALLBACK_TO_V2 | V3 rejected a vague continuation request before envelope creation. |
| `TRIAL_20260524_002_harmony_placeholder_fallback` | Harmony | FALLBACK_TO_V2 | V3 rejected unresolved prompt placeholders before envelope creation. |
| `TRIAL_20260524_003_harmony_faq_ingestion_utf8` | Harmony | COMPLETED_WITH_V3 | Happy-path parser/error-boundary change; focused unittest command passed. |
| `TRIAL_20260524_004_harmony_currency_blank_defaults` | Harmony | COMPLETED_WITH_V3 | Happy-path display utility hardening; focused unittest command passed. |
| `TRIAL_20260524_005_temper_cs_send_aria_disabled` | Temper | COMPLETED_WITH_V3 | Happy-path verifier-backed UI/accessibility change; npm verifier passed. |

## Requirement Review

| Requirement | Result | Evidence |
|---|---|---|
| At least 5 real-project trials | PASS | 5 trial records in `docs/Factory/v3/trials/`. |
| At least 2 ordinary repositories | PASS | Harmony and Temper trials. |
| At least 1 trial by a user other than V3 doc author | WAIVED | Owner waiver at `docs/Factory/v3/trials/PHASE1_REQUIREMENT_WAIVER_20260524.md`. |
| At least 1 V2 fallback or V3-unsuitable decision | PASS | Trials 001 and 002. |
| Every trial records friction | PASS | All 5 trial records include friction/usability sections. |
| Every trial records fallback review | PASS | All 5 trial records include fallback/halt review. |
| Every trial records SIMPLE-CODE-GATE review | PASS | All 5 trial records include SIMPLE-CODE-GATE review. |
| Every trial records false-positive/false-negative notes | PASS | All 5 trial records include false-positive/false-negative notes. |
| Stop conditions triggered | NO | No V3 use outside `V3-OP-001`, missed fallback, failed-verification continuation, V2 deprecation confusion, or required-gate drift was recorded. |

## Findings

| Finding | Evidence | Treatment |
|---|---|---|
| Pre-envelope fallback is a first-class state. | Trials 001 and 002 stopped before mission-envelope creation. | Phase 2 mission record must support `rejected_before_envelope` or equivalent. |
| Thread-local envelopes are necessary for narrow authorized file scopes. | Trials 003, 004, and 005 used thread-local envelopes because Factory artifact files were outside authorized scope. | Phase 2 mission record must support an external/thread-local envelope reference or a separately authorized record path. |
| V3 happy path works for small bounded changes with exact files and exact commands. | Trials 003, 004, and 005 completed with verification passing and no V2 fallback trigger. | Keep `V3-OP-001` scope unchanged. |
| Prompt placeholders are a practical usability hazard. | Trial 002. | User guide already updated; add future natural-language fixture if eval expansion proceeds. |
| Current advisory checks are not deployed in adopting repos. | Harmony and Temper trials did not run starter-kit advisory scripts locally. | Phase 2 should not require these scripts in adopting repos; records should allow "not available / not run" classification. |
| Phase 1 evidence is still narrow. | Only one owner/operator ran trials; all trials were small and Codex-based. | Start Phase 2 in shadow design mode only; do not promote defaults or gates. |

## Decision Options

| Option | Decision | Reason |
|---|---|---|
| `REFINE_V3_OP_001` | Not selected | Profile scope did not need material change; guide/template refinements were already made from trial evidence. |
| `ADD_FIXTURES` | Not selected as primary | Useful fixture ideas exist, but they should be attached to Phase 2/eval evolution rather than blocking mission-record design. |
| `START_PHASE_2` | Selected | Trial evidence shows the next bottleneck is structured capture of pre-envelope decisions, thread-local envelopes, commands, verification, and fallback outcomes. |
| `PAUSE_V3_EXPANSION` | Not selected | No stop condition or missed fallback was recorded. |
| `FALLBACK_TO_V2` | Not selected | V3 completed three bounded happy-path trials and correctly routed two unsuitable cases away from execution. |

## Approved Next Step
Start Phase 2 as a shadow design effort only.

Approved Phase 2 work:

- draft `docs/Factory/v3/templates/V3_MISSION_RECORD_TEMPLATE.json`,
- define a small schema for `V3-OP-001` mission decisions,
- include pre-envelope rejection and thread-local envelope states,
- backfit the schema manually against the 5 Phase 1 trials,
- design fixture cases for valid happy path, pre-envelope fallback, missing authority, verification failure, scope expansion, and thread-local envelope,
- keep all validation advisory and non-enforcing.

Not approved:

- making Factory v3 the default,
- approving any V3 profile beyond `V3-OP-001`,
- deprecating Factory v2,
- wiring V3 checks into `factoryctl`, CI, merge preflight, or required gates,
- runtime-kernel authority, production action mediation, proof, lease enforcement, or deployment authority,
- adding broad telemetry or governance router work before the Phase 2 shadow record is designed and reviewed.

## Residual Risks

| Risk | Treatment |
|---|---|
| Evidence comes from one owner/operator. | Accepted for solo AI-native context with recorded waiver; seek external-user evidence opportunistically later. |
| Trials were small and low-risk. | Intended for `V3-OP-001`; do not generalize to heavier work. |
| Adopting repos did not run starter-kit advisory scripts. | Keep advisory scripts optional; mission records should capture local command evidence first. |
| Thread-local envelopes are less replayable than file artifacts. | Phase 2 must design a replayable record without forcing scope expansion. |
| Phase 2 could become over-abstracted. | Apply SIMPLE-CODE-GATE: design the smallest record that captures actual Phase 1 evidence. |

## Phase 2 Design Constraints

- Keep `V3_MISSION_RECORD` a shadow artifact.
- Start from the five observed trials, not theoretical runtime architecture.
- Represent decisions before execution, during execution, and closeout.
- Include reason codes for fallback and halt states.
- Include explicit allowed files, forbidden scope, commands, dependency policy, verification result, and evidence references.
- Do not store chain-of-thought, full conversation transcripts, or vendor-private cognition state.
- Do not conflict with Mission Mode source-of-truth rules.
- Do not require adopting repos to have separate governance kernels.

## Recommendation
Proceed to a Factory-governed Phase 2 design task for a shadow structured mission record.

The immediate next artifact should be a planning brief or pack for `V3_MISSION_RECORD_TEMPLATE.json`, with golden fixtures derived from the five Phase 1 trials.
