# Execution Prompt - V3 Confidence Pilot Batch

## Version
v1

## Change Log
- v1 (2026-05-21): Generated after Stage I2 PASS and human GO.

## Run Metadata
- RUN_ID: RUN_20260521_0948_v3_confidence_pilot_execution
- Sprint ID: SPRINT_20260521_021
- Created: 2026-05-21
- Source Pack: `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/`

## Purpose
Execute the bounded V3 confidence pilot batch under Factory v2 authority. Produce advisory evidence only; do not promote Factory v3 or wire checks into required gates.

## Required Read Order
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/SCRATCHPAD.md` Active Pitfalls only
5. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/intent.md`
6. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/verification_plan.md`
7. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/traceability_matrix.md`
8. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/micro_sprints.md`
9. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/SPRINT_20260521_021_ENVELOPE.md`
10. `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/pack/PACK_AUDIT_REPORT.md`

## Skill Routing Contract
- Use the factory-execution-closeout skill for final execution closeout comparison against the approved envelope.

## Hard Guardrails
- Keep V3 advisory and research-only.
- Keep V2 authoritative and available as fallback.
- Do not modify matcher or validator code unless a blocking execution defect appears.
- Do not create required-gate, CI, `factoryctl`, `stage-lint`, or `pack-lint` integration.
- Do not claim runtime-kernel authority, AEGIS proof, production mediation, or operational V3 approval.

## SIMPLE-CODE-GATE (v2)
- No code changes are planned.
- If a blocking code fix is unavoidable, make the smallest clear behavior-preserving change.
- Add no speculative abstraction, new dependency, registry, strategy layer, plugin seam, or broad indirection.
- Do not swallow failures; invalid pilot state must fail explicitly.

## Micro-sprint Execution Sequence
1. MS-01: Run two real-run shadow scans.
2. MS-02: Create and run seeded and positive routing pilot fixtures.
3. MS-03: Write bounded natural-language detection design.
4. MS-04: Write confidence pilot batch rollup.
5. MS-05: Run verification and write execution closeout.

## Verification Contract
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json`
- `./scripts/factoryctl pack-lint --run RUN_20260521_0948_v3_confidence_pilot_execution`
- `git diff --check`

## Final Exit Checklist
- [ ] Pilot outputs are present.
- [ ] Findings are classified.
- [ ] Natural-language design is advisory only.
- [ ] Batch rollup states V3 is not yet operationally ready.
- [ ] Verification commands pass.
- [ ] Canonical tracking docs are updated.
