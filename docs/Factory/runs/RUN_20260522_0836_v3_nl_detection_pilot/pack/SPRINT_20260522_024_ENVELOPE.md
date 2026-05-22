# Sprint Envelope - SPRINT_20260522_024

## Version
v2

## Change Log
- v1 (2026-05-22): Stage H envelope.
- v2 (2026-05-22): Stage I hardening clarified default-output and no-gate constraints.

## Sprint
- Sprint ID: SPRINT_20260522_024
- Run ID: RUN_20260522_0836_v3_nl_detection_pilot
- Execution Mode: EXECUTION_ENABLED

## Objective
Implement and measure a bounded opt-in natural-language advisory detection pilot for V3 operational-readiness evals.

## File-touch Budget
- `scripts/factory_v3_operational_readiness_eval.py`: allowed.
- `tests/fixtures/factory_v3_operational_readiness_nl_pilot/`: allowed.
- This run root: allowed.
- Tracking docs and `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md`: allowed.
- Factory v2 validators and required gates: 0 files.

## Approved Commands
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_nl_pilot/clean --nl-pilot --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_nl_pilot/drift --nl-pilot --json`
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl pack-lint --run RUN_20260522_0836_v3_nl_detection_pilot`
- `git diff --check`

## SIMPLE-CODE-GATE v2
- Keep implementation direct and local.
- Use no external dependencies.
- Do not add registries, plugin systems, strategy layers, or broad indirection.
- Do not silently swallow invalid input or expected JSON mismatches.

## Exit Criteria
- Default fixture regression passes unchanged.
- Clean corpus has zero findings.
- Drift corpus emits expected candidate IDs.
- Reports remain advisory and non-blocking.
