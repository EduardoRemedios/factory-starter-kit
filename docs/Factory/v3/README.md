# Factory v3

## Version
v0.8

## Change Log
- v0.8 (2026-05-24): Added the standalone advisory V3 mission-record validator, malformed-record fixtures, and deterministic expected outputs.
- v0.7 (2026-05-24): Added Phase 2 shadow mission-record v0 design and trial-derived JSON fixtures.
- v0.6 (2026-05-24): Added Phase 1 trial operating plan and trial index.
- v0.5 (2026-05-22): Added Phase 1 real-project trial capture template for `V3-OP-001` evidence collection.
- v0.4 (2026-05-22): Added roadmap pre-mortem and golden-fixture backlog for V3 operationalization.
- v0.3 (2026-05-22): Added vision and roadmap documents for the path from `V3-OP-001` to the full mission-governance runtime vision.
- v0.2 (2026-05-22): Updated status after optional `V3-OP-001` operational release approval and user-guide addition.
- v0.1 (2026-05-18): Initial research-only namespace for Factory v3 planning.

## Status
Factory v3 has one approved optional operational profile:

- `V3-OP-001 Bounded Code Change`

Approval is recorded at `OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.

This directory does not make Factory v3 the default mode, deprecate Factory v2, alter the `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2` planning pipeline, or change any required validator behavior.

Factory v2 remains supported and available as fallback.

The prior research and decision-prep evidence remains part of the approval basis; V3 docs remain non-enforcing for required repository gates unless a future integration run explicitly changes that.

## Purpose
This namespace captures Factory v3 operating guidance, release evidence, starter templates, and continuing research for mission-governed autonomous execution by coding agents.

## Current Scope
- Provide user guidance for optional `V3-OP-001` use.
- Provide starter templates for V3 mission envelopes, closeout, fallback review, and SIMPLE-CODE-GATE review.
- Preserve the external governance kernel and runtime-kernel boundary.
- Keep V2 fallback explicit.
- Capture evals, stress tests, pilot evidence, decision reports, and promotion criteria.
- Provide a shadow `V3_MISSION_RECORD` design and standalone advisory validator for Phase 2 replay and evidence-shape testing.
- Continue research for any future V3 profile before promotion.

## Non-authority Rule
Files in this directory are authoritative only for the approved optional `V3-OP-001` profile unless a future release explicitly promotes another profile.

They do not change:
- `docs/Factory/ORCHESTRATION.md`
- `docs/Factory/Spec/STAGE_CONTRACTS.md`
- `docs/Factory/Spec/DEFINITIONS.md`
- `scripts/factory_stage_lint.py`
- `scripts/factory_pack_lint.py`
- `scripts/knowledge_lint.sh`

They also do not approve payment, authentication, compliance, production deployment, infrastructure authority, runtime-kernel authority, or production action mediation.

## Relationship To External Governance Kernels
Factory v3 should be compatible with external governance kernels but does not require one.

If an adopting repository uses a separate lower-level autonomy governance kernel, Factory should act as the SDLC mission-governance profile for coding work while the kernel remains the runtime authority and proof layer.

If an adopting repository does not use a separate governance kernel, Factory v2 and optional `V3-OP-001` remain usable without one.

## Approved Profile
Use `V3-OP-001` only for bounded code-changing work where:

- the objective is clear,
- files or modules can be named,
- commands and verification are known,
- dependencies are authorized,
- V2 fallback triggers are explicit,
- no payment, authentication, compliance, deployment, runtime-kernel, or infrastructure concern is implicated.

Start with `USER_GUIDE.md`.

## Promotion Rule
Any V3 profile beyond `V3-OP-001`, any default-mode promotion, or any required-gate integration requires evidence, human approval, and Factory governance.

## Key Research Artifacts
- `VISION.md`
- `ROADMAP_TO_FULL_VISION.md`
- `ROADMAP_PREMORTEM.md`
- `MISSION_RECORD_DESIGN_V0.md`
- `PHASE1_DECISION_REVIEW_V3_OP_001.md`
- `PHASE1_TRIAL_PLAN.md`
- `USER_GUIDE.md`
- `OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`
- `OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`
- `OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`
- `STRATEGY.md`
- `NON_GOALS_AND_BOUNDARIES.md`
- `PROMOTION_CRITERIA.md`
- `OPERATIONAL_READINESS_EVAL_PLAN.md`
- `OPERATIONAL_READINESS_DECISION_REPORT_TEMPLATE.md`
- `templates/`

## Phase 1 Trial Capture
Use `PHASE1_TRIAL_PLAN.md` to run the first real-project trial batch.

Use `templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md` for real-project `V3-OP-001` trials.

The template is designed to capture fallback decisions, user friction, advisory false positives and false negatives, SIMPLE-CODE-GATE evidence, and roadmap pre-mortem watchpoints before Phase 2 structured mission records are designed.

Track trial records in `trials/TRIAL_INDEX.md`.

## Phase 2 Shadow Mission Records
Phase 2 shadow mission-record design is approved only as research and replay work.

Use:

- `MISSION_RECORD_DESIGN_V0.md`
- `templates/V3_MISSION_RECORD_TEMPLATE.json`
- `tests/fixtures/factory_v3_mission_record/`
- `scripts/factory_v3_mission_record_lint.py`

The v0 record captures pre-envelope fallback, thread-local mission envelopes, bounded authority, command evidence, verification, fallback review, SIMPLE-CODE-GATE review, and Phase 2 design signals.

The validator is standalone and advisory. It emits `blocking_effect: none`, supports deterministic `--expect` fixture checks, and is not wired into required Factory gates.

It does not approve enforcement, required gates, runtime authority, telemetry, governance routing, or new V3 profiles.

## Advisory Eval Tooling
- `scripts/factory_v3_advisory_lint.py` checks research-posture and promotion-evidence drift in V3 docs.
- `scripts/factory_v3_operational_readiness_eval.py` checks standalone operational-readiness fixture scenarios and emits advisory-only reports.
- `scripts/factory_v3_mission_record_lint.py` checks shadow V3 mission-record JSON files and malformed-record fixtures in advisory mode.
- These tools are not wired into required Factory v2 gates and do not authorize broader V3 promotion.
