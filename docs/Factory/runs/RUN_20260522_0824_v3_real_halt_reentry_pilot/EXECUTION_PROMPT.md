# Execution Prompt - V3 Real Halt And Reentry Pilot

## Version
v1

## Change Log
- v1 (2026-05-22): Generated after Stage I2 PASS and human GO.

## Run Metadata
- RUN_ID: RUN_20260522_0824_v3_real_halt_reentry_pilot
- Sprint ID: SPRINT_20260522_023
- Created: 2026-05-22
- Source Pack: `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/pack/`

## Purpose
Execute a bounded run-local pilot that proves real failed-command halt behavior and authored-artifact reentry behavior for Factory v3 operational-readiness checklist items C-01 and C-02.

## Skill Routing Contract
- Use the factory-execution-closeout skill for final execution closeout.

## Hard Guardrails
- Keep V3 research-only and advisory.
- Keep V2 authoritative and available as fallback.
- Do not modify production Factory validators or V3 eval runner code.
- Do not wire anything into required gates.
- Do not claim operational V3 approval.

## SIMPLE-CODE-GATE (v2)
- Keep the run-local harness direct and minimal.
- Use the Python standard library only.
- Do not add a generic framework, registry, plugin layer, or broad abstraction.
- Fail explicitly for invalid state.

## Micro-sprint Execution Sequence
1. MS-01: Run failed-command halt pilot.
2. MS-02: Run valid and stale reentry pilots.
3. MS-03: Update checklist and write closeout.
4. MS-04: Run verification.

## Verification Contract
- `python3 docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/harness/real_behavior_pilot.py`
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl pack-lint --run RUN_20260522_0824_v3_real_halt_reentry_pilot`
- `git diff --check`

## Final Exit Checklist
- [ ] Failed-command halt evidence exists.
- [ ] No continuation marker exists after failure.
- [ ] Valid reentry resumes from authored artifacts.
- [ ] Stale cursor reentry halts.
- [ ] C-01 and C-02 are updated accurately in the checklist.
- [ ] Verification commands pass.
