# Execution Prompt - V3 Eval Suite Implementation

## Version
v1

## Change Log
- v1 (2026-05-21): Generated after Stage I2 PASS and human GO.

## Run Metadata
- RUN_ID: RUN_20260521_0833_v3_eval_suite_impl_plan
- Sprint ID: SPRINT_20260521_014
- Created: 2026-05-21
- Source Pack: `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/`

## Purpose
Implement the first standalone advisory V3 operational-readiness eval suite: a small Python runner, golden fixtures, expected JSON output, and a decision report template. Keep V3 research-only and keep V2 supported.

## Required Read Order
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/SCRATCHPAD.md` Active Pitfalls only
5. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/intent.md`
6. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/verification_plan.md`
7. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/traceability_matrix.md`
8. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/micro_sprints.md`
9. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/SPRINT_20260521_014_ENVELOPE.md`
10. `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/PACK_AUDIT_REPORT.md`

## Skill Routing Contract
- No dedicated skill applies; execute via stage contract only.

## Hard Guardrails
- Preserve fail-closed behavior for consequential changes.
- Do not expand scope implicitly.
- Keep the new runner standalone and advisory.
- Do not wire the runner into required Factory v2 gates.
- Do not promote V3 or deprecate V2.
- Do not add external dependencies.

## SIMPLE-CODE-GATE (v2)
- Implement the smallest direct runner that satisfies the fixture contract.
- Prefer explicit local checks over abstraction.
- Do not add registries, plugin systems, generic policy engines, or new dependencies.
- Do not swallow invalid fixture or expected JSON errors.

## Micro-sprint Execution Sequence
1. MS-01: Add standalone runner with advisory-only JSON output.
2. MS-02: Add V3-G001 through V3-G014 fixture cases and expected JSON.
3. MS-03: Add decision report template and doc links.
4. MS-04: Run verification commands and capture evidence.

## Verification Contract
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `rg -n "factory_v3_operational_readiness_eval" scripts/knowledge_lint.sh scripts/factory_stage_lint.py scripts/factory_pack_lint.py scripts/factoryctl || true`
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl pack-lint --run RUN_20260521_0833_v3_eval_suite_impl_plan`

## Final Exit Checklist
- [ ] Runner and fixtures implemented.
- [ ] SIMPLE-CODE-GATE v2 satisfied.
- [ ] Verification commands pass.
- [ ] Evidence artifacts updated.
- [ ] Canonical docs updated if outcome is GO.
