# Factory v3 Research

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial research-only namespace for Factory v3 planning.

## Status
Factory v3 is research and design only.

This directory does not replace Factory v2, alter the `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2` planning pipeline, or change any required validator behavior.

Factory v2 remains the current usable operating process in this starter kit.

## Purpose
This namespace captures future Factory v3 thinking before it is promoted into any operating contract. The current research direction is mission-governed autonomous execution for coding agents, evaluated through the existing Factory v2 process.

## Current Scope
- Define strategic v3 direction.
- Preserve the AEGIS and runtime-kernel boundary.
- Identify concepts that may later become shadow schema candidates.
- Design advisory validators before any enforcement.
- Capture evals, stress tests, pilot evidence, and promotion criteria.
- Plan operational-readiness evals before any optional V3 operating profile is promoted.

## Non-authority Rule
Files in this directory are not authoritative for Factory runs unless a future release explicitly promotes them.

They do not change:
- `docs/Factory/ORCHESTRATION.md`
- `docs/Factory/Spec/STAGE_CONTRACTS.md`
- `docs/Factory/Spec/DEFINITIONS.md`
- `scripts/factory_stage_lint.py`
- `scripts/factory_pack_lint.py`
- `scripts/knowledge_lint.sh`

## Relationship To AEGIS
Factory v3 should be AEGIS-compatible but not AEGIS-dependent.

If an adopting repository uses AEGIS or another lower-level autonomy governance kernel, Factory should act as the SDLC mission-governance profile for coding work while the kernel remains the runtime authority and proof layer.

If an adopting repository does not use AEGIS, Factory v2 remains usable without it.

## Promotion Rule
Factory v3 may only be promoted after it has been planned, evaluated, and hardened using Factory v2 governance.

Promotion requires evidence, not confidence by narrative.

## Key Research Artifacts
- `STRATEGY.md`
- `NON_GOALS_AND_BOUNDARIES.md`
- `PROMOTION_CRITERIA.md`
- `OPERATIONAL_READINESS_EVAL_PLAN.md`
- `OPERATIONAL_READINESS_DECISION_REPORT_TEMPLATE.md`

## Advisory Eval Tooling
- `scripts/factory_v3_advisory_lint.py` checks research-posture and promotion-evidence drift in V3 docs.
- `scripts/factory_v3_operational_readiness_eval.py` checks standalone operational-readiness fixture scenarios and emits advisory-only reports.
- These tools are not wired into required Factory v2 gates and do not authorize V3 promotion.
