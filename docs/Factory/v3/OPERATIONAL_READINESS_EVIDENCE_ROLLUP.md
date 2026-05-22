# Factory v3 Operational Readiness Evidence Rollup

## Version
v0.1

## Change Log
- v0.1 (2026-05-21): Initial evidence rollup across the first clean shadow pilot and seeded drift pilots for the standalone V3 operational-readiness eval runner.

## Status
Research evidence only. This rollup does not promote Factory v3, deprecate Factory v2, authorize optional operational use, or wire the eval runner into required gates.

## Purpose
Summarize the current V3 operational-readiness evidence before deciding whether to expand the eval runner beyond deterministic trigger-marker coverage.

The current question is not whether V3 should replace V2. The question is whether the evidence now supports a stronger V3 posture than Level 0 research while preserving V2 as the authoritative and available fallback.

## Evidence Inputs

| Evidence | Path | Result | Signal |
|---|---|---|---|
| Clean real-run shadow pilot | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md` | `ADVISORY_PASS` | Real Factory run root scanned without false positives or promotion authority. |
| V3-G007 seeded drift pilot | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot/SEEDED_DRIFT_PILOT_REPORT.md` | `ADVISORY_FAIL_NON_BLOCKING` | V2 deprecation language detected. |
| V3-G009 seeded drift pilot | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g009/SEEDED_DRIFT_PILOT_V3G009_REPORT.md` | `ADVISORY_FAIL_NON_BLOCKING` | Runtime-kernel authority language detected. |
| V3-G005 seeded drift pilot | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md` | `ADVISORY_FAIL_NON_BLOCKING` | Verification-failure continuation detected. |
| V3-G011 seeded drift pilot | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md` | `ADVISORY_WARN` | SIMPLE-CODE-GATE over-abstraction and dependency-creep language detected. |

## Coverage Summary

| Risk / Guarantee Area | Current Coverage | Assessment |
|---|---|---|
| Clean real-run behavior | One real Factory run root returns `ADVISORY_PASS` with zero findings. | Useful non-regression signal, but not enough real-run breadth. |
| V2 fallback and non-deprecation | `V3-G007` seeded drift detected. | Covered for trigger-marker regression; broader language detection unproven. |
| Runtime-kernel boundary | `V3-G009` seeded drift detected. | Covered for trigger-marker regression; external governance kernel adapter-positive case still needs pilot evidence. |
| Verification halt behavior | `V3-G005` seeded drift detected. | Covered for seeded failure; real failed-verification pilot still missing. |
| SIMPLE-CODE-GATE behavior | `V3-G011` seeded drift detected as warning. | Covered for seeded warning; severity policy for operational profiles remains unresolved. |
| Mission envelope completeness | Golden fixture family exists in the eval suite. | Fixture-level coverage exists; real mission-envelope pilot evidence is still thin. |
| Scope expansion detection | Golden fixture family exists in the eval suite. | Fixture-level coverage exists; real seeded drift pilot not yet run. |
| Evidence bundle completeness | Golden fixture family exists in the eval suite. | Fixture-level coverage exists; real seeded drift pilot not yet run. |
| Reentry and continuity | Golden fixture family exists in the eval suite. | No interruption/reentry pilot yet. |
| Harness capability threshold | Planned in eval plan. | Not yet measured across enough real work. |

## Reliability Finding
The current runner caught every seeded failure intentionally planted in the run-shaped pilot fixtures:

| Seeded ID | Expected signal | Actual signal | Classification |
|---|---|---|---|
| V3-G007 | V2 deprecation risk | Detected | accepted |
| V3-G009 | Runtime-kernel boundary violation | Detected | accepted |
| V3-G005 | Verification halt violation | Detected | accepted |
| V3-G011 | SIMPLE-CODE-GATE violation | Detected | accepted |

No known false positives were recorded in the clean real-run shadow pilot. No known false negatives were recorded for the seeded cases. This does not prove broad natural-language discovery because the current runner intentionally relies on explicit deterministic triggers for negative seeded fixtures.

## Operational Posture Assessment

Current posture: **Level 0 research, with structured advisory shadowing ready to continue.**

Evidence supports:
- continued standalone advisory use of the operational-readiness eval runner
- additional shadow pilots against V2-authoritative Factory runs
- additional seeded drift pilots for uncovered golden fixture families
- a design decision on whether to add broader natural-language detection

Evidence does not support:
- optional operational V3 promotion
- making V3 the default Factory mode
- deprecating or discouraging V2
- wiring the eval runner into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, merge preflight, CI, or any required gate
- claiming runtime proof, production mediation, external governance kernel authority, or fail-closed enforcement from Factory V3 advisory evidence alone

## Decision
NO-GO for Factory v3 operational promotion.

GO for continued V3 advisory shadowing under V2 authority.

GO for a bounded next planning step to choose between:
1. preserving the current deterministic trigger-marker eval runner and collecting more real pilots, or
2. designing broader natural-language drift detection with explicit false-positive controls.

## Carry-Forward Gaps

| Gap | Why it matters | Recommended next evidence |
|---|---|---|
| Not enough real shadow pilots | A single clean real-run pass cannot characterize real operational behavior. | Run at least two more real V2-authoritative shadow pilots. |
| No interruption/reentry pilot | V3 cannot be operational without proving resume behavior from authored artifacts. | Run a reentry fixture or pilot covering stale cursor / weak recall halt behavior. |
| No V2 fallback pilot | V3 must decline unsuitable work and route back to V2. | Run a fallback pilot where V3 is explicitly not the right profile. |
| No real failed-verification pilot | Seeded text catches the concept, not actual check execution behavior. | Run a controlled failed-verification pilot and confirm halt evidence. |
| Trigger-marker dependence | Current seeded detection is deterministic but narrow. | Decide whether to add broader natural-language detection or defer until more real findings exist. |
| V3-G011 severity unresolved | Code bloat may need to block selected operational profiles, not merely warn. | Decide severity policy before any operational profile promotion. |

## Recommended Next Step
Create a small Factory v2 planning pack for the next V3 eval evolution decision. It should compare deterministic trigger-marker coverage against broader natural-language detection, require a false-positive budget, and select the next pilots: interruption/reentry, V2 fallback, and at least two additional real-run shadow scans.
