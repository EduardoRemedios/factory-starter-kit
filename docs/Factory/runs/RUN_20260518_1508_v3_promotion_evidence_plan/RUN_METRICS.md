# RUN_METRICS.md

<!--
Create at: docs/Factory/runs/<RUN_ID>/RUN_METRICS.md
Purpose: lightweight run telemetry for improving the Factory process without changing the stage artifacts.
Keep this factual. Do not duplicate stage content, private customer details, or implementation narrative.
-->

## Version
v1

## Change Log
- v1 (2026-05-18): Initial run metrics record.

## Run Summary
- Run ID: RUN_20260518_1508_v3_promotion_evidence_plan
- Sprint ID: SPRINT_20260518_007
- Execution Mode: PLANNING_ONLY
- Factory Surface: Codex App/Desktop
- Primary Model: GPT-5 Codex
- Started: 2026-05-18 15:08 local
- Completed: 2026-05-18 15:08 local
- Final Pack Verdict: PASS
- Human Decision: Not yet reviewed

## Stage Timing
| Stage | Started | Completed | Duration | Stage-Lint Result | Rework Count |
|---|---|---|---|---|---|
| A | 15:08 | 15:08 | <1m | PASS | 0 |
| B | 15:08 | 15:08 | <1m | PASS | 1 |
| C | 15:08 | 15:08 | <1m | PASS | 0 |
| D | 15:08 | 15:08 | <1m | PASS | 0 |
| E | 15:08 | 15:08 | <1m | PASS | 0 |
| F | 15:08 | 15:08 | <1m | PASS | 0 |
| G | 15:08 | 15:08 | <1m | PASS | 0 |
| H | 15:08 | 15:08 | <1m | PASS | 0 |
| I | 15:08 | 15:08 | <1m | PASS | 0 |
| J | 15:08 | 15:08 | <1m | PASS | 0 |
| I2 | 15:08 | 15:08 | <1m | PASS | 1 |

## Validator Results
- Knowledge Lint: PASS
- Context Recall Coverage: SUFFICIENT
- Stage-Lint Failures Count: 1
- Pack-Lint: PASS
- Mission Lint: NA

## Drift And Rework
- Scope drift caught: None.
- Placeholder or artifact-shape defects caught: Stage B handoff missing required sections; pack audit verdict and fixture input needed pack-lint formatting repair.
- Missing evidence caught: None.
- Late cleanup burden: Low
- Most expensive rework cause: Mechanical artifact shape repair.

## Harness And Tooling
- Skills used: factory-root-planner, factory-purple-gate, factory-pack-consolidator.
- Plugins/apps/connectors used: None.
- External sources consulted: None.
- Terminal/CLI commands worth preserving: `./scripts/factoryctl stage-lint --run RUN_20260518_1508_v3_promotion_evidence_plan --stage <STAGE>`; `./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan`.

## Lessons For Factory
- Keep: Stage-lint after every stage caught artifact-shape drift early.
- Change: For future runs, template handoffs should always include `Inputs (DISK)` and `Skill Routing Contract`.
- Add to scratchpad? NO
- Candidate reusable improvement: None for this pack.
