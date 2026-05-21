# Raw Brief - V3 Eval Evolution Decision Plan

## Source
Human sponsor approved the next recommended step after the V3 operational-readiness evidence rollup.

## Problem
Factory v3 is intended to become operational when model and harness capability make some Factory v2 ceremony safely collapsible. Current evidence is promising but insufficient: the eval runner catches deterministic seeded drift and passes one clean real-run shadow pilot, but it does not yet establish enough confidence for operational V3 use.

## Goal
Create a Factory v2 planning pack that defines the shortest evidence path to confidence for using Factory v3 operationally while retaining Factory v2 as an available and supported fallback.

## Required Decision
The pack must decide what to do next with the V3 operational-readiness eval approach:
1. keep deterministic trigger-marker coverage and collect more real pilots before broader detection, or
2. design broader natural-language drift detection with explicit false-positive controls, or
3. combine both in a staged path.

## Scope
- Compare deterministic trigger-marker coverage against broader natural-language drift detection.
- Define the false-positive budget and review discipline needed before broader detection can affect operational confidence.
- Specify the next pilots needed for confidence: interruption/reentry, V2 fallback, failed-verification halt behavior, and additional real-run shadow scans.
- Define readiness thresholds for moving from research-only to an optional operational V3 profile.
- Keep V2 authoritative during this planning and evidence-building phase.

## Out of Scope
- No V3 operational promotion.
- No deprecation or discouragement of Factory v2.
- No wiring into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, merge preflight, CI, or required gates.
- No implementation of new matcher logic or natural-language detection in this run.
- No runtime-kernel, AEGIS authority, production mediation, or proof claims.

## Hard Constraints
- Execution Mode: `PLANNING_ONLY`.
- Factory v2 remains the governing process for this run.
- V3 remains research-only unless a later evidence-backed promotion pack receives explicit human approval.
- SIMPLE-CODE-GATE v2 remains mandatory for future code-changing work.
- Any future broader detection must have measurable false-positive controls before it can influence operational-readiness decisions.
- Any operational V3 profile must retain explicit V2 fallback criteria.

## Acceptance Criteria
- A completed Factory v2 pack reaches Stage I2 PASS or CONDITIONAL PASS.
- The pack names the evidence required to reach confidence for V3 operational use.
- The pack recommends the next concrete pilots and gates.
- The pack clearly states what evidence is still missing before V3 can be used operationally.
- Pack lint passes.
