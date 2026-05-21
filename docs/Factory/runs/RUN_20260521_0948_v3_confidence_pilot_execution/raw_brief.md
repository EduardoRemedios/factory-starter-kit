# Raw Brief - V3 Confidence Pilot Execution

## Source
Human sponsor approved the next recommended step with: "agree proceed" on 2026-05-21.

## Execution Authorization
- Execution Mode: EXECUTION_ENABLED
- Execution Authorization: Human sponsor message "agree proceed" on 2026-05-21 after `RUN_20260521_0939_v3_eval_evolution_decision_plan` PASS.
- Downstream Fan-Out: NOT APPROVED

## Problem
Factory v3 is intended to become operational when enough evidence shows that it can preserve Factory v2 safety guarantees with less ceremony for selected mission profiles. The current evidence is not sufficient. The next step is to run a bounded confidence pilot batch under Factory v2 authority.

## Goal
Collect the next V3 operational-confidence evidence batch:
- two additional real-run V3 shadow scans
- seeded drift pilots for V3-G003, V3-G006, V3-G010, and V3-G014
- positive routing pilots for V3-G012 and V3-G013
- a controlled failed-verification halt pilot
- a bounded natural-language detection design with a false-positive budget

## Scope
- Create run-local pilot fixtures and reports under this run root.
- Run the existing standalone operational-readiness eval runner.
- Record outputs as advisory evidence.
- Update canonical tracking docs after execution closeout.

## Out of Scope
- No V3 operational promotion.
- No V2 deprecation.
- No required-gate integration.
- No code changes to matcher logic or validators unless a blocking defect prevents the approved pilots.
- No runtime-kernel, AEGIS authority, production mediation, or proof claims.

## Acceptance Criteria
- Factory pack reaches Stage I2 PASS.
- Human GO is recorded for the bounded execution.
- Pilot output JSON and reports are written for each pilot class.
- A batch rollup summarizes whether the evidence increases confidence and what remains missing.
- Pack-lint and relevant advisory checks pass.
