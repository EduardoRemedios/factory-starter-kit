# Factory v3 Promotion-Evidence Advisory Lint Planning Intent

## Version
v1

## Change Log
- v2 (2026-05-18): Hardened intent with red-team constraints for temporary mutation remediation and no matcher tuning.
- v1 (2026-05-18): Initial planning-only intent for the promotion-evidence advisory lint pilot pack.

## Purpose
Plan the next narrow Factory v3 advisory lint evidence step without implementing code, changing required validators, or promoting Factory v3. [SOURCE:RAW]

## Goal
Define a bounded future real-doc pilot that exercises promotion-evidence warning behavior, especially `V3-A006`, and decide whether current matcher behavior should remain unchanged, be tested further, or be tuned in a later separately approved implementation run. [SOURCE:RAW]

## Non-goals
- Do not implement matcher changes in this planning run. [SOURCE:RAW]
- Do not edit `scripts/factory_v3_advisory_lint.py`. [SOURCE:RAW]
- Do not wire advisory lint into `factoryctl`, CI, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, mission cursor lint, or merge preflight. [SOURCE:RAW]
- Do not promote Factory v3 beyond Level 0 research. [SOURCE:RAW]
- Do not make AEGIS required. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- Do not claim runtime-kernel authority, runtime proof, production action mediation, or deployed autonomous-system enforcement. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]

## Principles
- Factory v2 remains the governing process for this planning pack. [SOURCE:REF:docs/PROJECT_STATE.md]
- Advisory lint remains standalone, optional, and non-blocking with `blocking_effect: none`. [SOURCE:REF:docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md]
- Real-branch evidence should be collected before check expansion. [SOURCE:REF:docs/ROADMAP.md]
- Unsafe promotion language may be used only as a temporary pilot mutation and must not remain in final docs. [INFERRED]
- Matcher tuning requires evidence of false positives, false negatives, ambiguity, or missed signal. [SOURCE:REF:docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_WARNING_PILOT_REPORT.md]

## Roles
- Root Planner: coordinate the Factory v2 planning run and preserve required evidence. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]
- Intent Contractor: keep the pilot scope narrow and planning-only. [SOURCE:RAW]
- Boundary Reviewer: verify Factory v2 and AEGIS boundaries remain intact. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- Verification Specialist: define the promotion-evidence pilot proof shape. [SOURCE:RAW]
- Purple Gate: decide whether the planning pack is ready for human review. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]

## Acceptance Criteria
- The pack defines exactly one future real-doc promotion-evidence pilot. [SOURCE:RAW]
- The pack records that the future pilot must not retain unsafe release or promotion language after evidence capture. [INFERRED]
- The pack requires finding classification as `accepted`, `false_positive`, `needs_more_context`, or `deferred`. [SOURCE:REF:docs/Factory/v3/PILOT_PROFILE_PLAN.md]
- The pack preserves advisory lint as optional and non-blocking. [SOURCE:REF:docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md]
- The pack does not authorize matcher tuning unless pilot evidence later justifies it. [SOURCE:RAW]
- The pack does not authorize Factory v3 promotion or required-gate integration. [SOURCE:RAW]
- The future pilot must capture the non-empty warning output, classify findings, remove unsafe temporary text, and verify final `docs/Factory/v3` returns `ADVISORY_PASS`. [SOURCE:REF:docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_WARNING_PILOT_REPORT.md]

## Open Questions
### BLOCKING
- None.

### NON-BLOCKING
- Whether the future promotion-evidence pilot should mutate `PROMOTION_CRITERIA.md` or a separate v3 pilot evidence note.
- Whether a future implementation run should add a dedicated real-doc fixture after the pilot, if the warning is accepted.

## Go Or No-Go Rule
- GO if the pack authorizes only a bounded future promotion-evidence pilot and keeps advisory lint standalone, optional, and non-blocking.
- NO-GO if the pack authorizes matcher edits, required validator wiring, Factory v3 promotion, AEGIS dependency, or runtime-kernel behavior.
