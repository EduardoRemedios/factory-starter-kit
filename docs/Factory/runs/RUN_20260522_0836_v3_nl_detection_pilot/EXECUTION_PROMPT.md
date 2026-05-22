# Execution Prompt - V3 Natural-language Advisory Detection Pilot

## Version
v1

## Change Log
- v1 (2026-05-22): Generated after Stage I2 PASS and human GO.

## Run Metadata
- RUN_ID: RUN_20260522_0836_v3_nl_detection_pilot
- Sprint ID: SPRINT_20260522_024
- Created: 2026-05-22
- Source Pack: `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/pack/`

## Purpose
Implement and measure an opt-in natural-language advisory detection pilot for the V3 operational-readiness eval runner.

## Skill Routing Contract
- Use the factory-execution-closeout skill for final closeout.

## Hard Guardrails
- Keep V3 research-only and advisory.
- Keep the pilot opt-in.
- Preserve default deterministic output and expected fixture JSON.
- Do not wire any V3 eval into required gates.
- Use no external dependencies.

## SIMPLE-CODE-GATE (v2)
- Implement the smallest direct candidate layer.
- Use paragraph-local patterns.
- Avoid framework, registry, strategy layer, plugin seam, or broad indirection.
- Do not swallow fixture or JSON errors.

## Verification Contract
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_nl_pilot/clean --nl-pilot --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_nl_pilot/drift --nl-pilot --json`
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- `python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json`
- `./scripts/factoryctl pack-lint --run RUN_20260522_0836_v3_nl_detection_pilot`
- `git diff --check`

## Final Exit Checklist
- [ ] Default regression still passes.
- [ ] Clean corpus has zero findings.
- [ ] Drift corpus emits expected IDs.
- [ ] C-03 checklist status is updated accurately.
- [ ] Verification commands pass.
