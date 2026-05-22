# Sprint Envelope - SPRINT_20260522_023

## Version
v2

## Change Log
- v1 (2026-05-22): Stage H envelope.
- v2 (2026-05-22): Stage I hardening clarified file-touch budget and proof criteria.

## Sprint
- Sprint ID: SPRINT_20260522_023
- Run ID: RUN_20260522_0824_v3_real_halt_reentry_pilot
- Execution Mode: EXECUTION_ENABLED

## Objective
Prove real failed-command halt behavior and authored-artifact reentry behavior for V3 operational-readiness checklist items C-01 and C-02.

## File-touch Budget
- Run-local evidence under `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/`: up to 50 files.
- Checklist and tracking docs: `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, `docs/CHANGELOG.md`, `CHANGELOG.md`.
- Production scripts and validators: 0 files.

## Approved Commands
- `python3 docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/harness/real_behavior_pilot.py`
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl stage-lint --run RUN_20260522_0824_v3_real_halt_reentry_pilot --stage <stage>`
- `./scripts/factoryctl pack-lint --run RUN_20260522_0824_v3_real_halt_reentry_pilot`
- `git diff --check`

## SIMPLE-CODE-GATE v2
Run-local harness code must stay direct and minimal:
- no external dependencies
- no generic framework or plugin layer
- explicit failure and halt records
- no silent exception swallowing

## Exit Criteria
- Failed-command result proves halt and no continuation.
- Reentry results prove valid resume and stale-cursor halt.
- Decision checklist is updated accurately.
- Verification commands pass.
