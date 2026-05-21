# Sprint Envelope - SPRINT_20260521_020

## Version
v2

## Change Log
- v1 (2026-05-21): Stage H envelope.
- v2 (2026-05-21): Stage I hardening clarified no implementation authorization.

## Sprint
- Sprint ID: SPRINT_20260521_020
- Run ID: RUN_20260521_0939_v3_eval_evolution_decision_plan
- Execution Mode: PLANNING_ONLY

## Objective
Create the planning decision path needed to reach confidence for operational Factory v3 use while keeping Factory v2 authoritative until a future approved promotion decision.

## File-touch Budget
- Total planned file touches: planning artifacts only in this run root plus repo tracking docs after closure.
- Code files: 0.
- Runtime validator files: 0.
- Factory v3 research docs outside this run: 0.

## Required Next Pilots
1. Two more real-run V3 shadow scans under V2 authority.
2. One interruption/reentry pilot.
3. One V2 fallback pilot.
4. One controlled failed-verification halt pilot.
5. Seeded drift pilots for V3-G003, V3-G006, V3-G010, V3-G012, V3-G013, and V3-G014.

## Detection Strategy
- Use deterministic trigger-marker fixtures as stable regression coverage.
- Design broader natural-language detection only as advisory and only with:
  - a fixed false-positive budget
  - human classification of every finding
  - no required-gate effect
  - no V3 promotion language

## Operational V3 Confidence Gate
No V3 operational use should be recommended until the thresholds in `intent.md` are satisfied and a future decision report names exact evidence paths and human approval.

## SIMPLE-CODE-GATE v2
This run is planning-only and changes no code. Future code-changing implementation of eval logic must apply SIMPLE-CODE-GATE v2: smallest clear change, no speculative abstraction, no dependency creep, no silent failures, and no brittle hidden side effects.

## Verification Required Before Merge
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl pack-lint --run RUN_20260521_0939_v3_eval_evolution_decision_plan`
- `git diff --check`

## Exit Criteria
- Pack reaches Stage I2 PASS or CONDITIONAL PASS.
- No V3 operational promotion is implied.
- V2 fallback remains explicit.
- Next pilots and confidence thresholds are reviewable.
