# Sprint Envelope - SPRINT_20260518_007

## Version
v1

## Change Log
- v1 (2026-05-18): Initial envelope for promotion-evidence advisory lint pilot planning.

## Sprint Title
Factory v3 promotion-evidence advisory lint pilot plan.

## Execution Mode
PLANNING_ONLY.

## Objective
Prepare a bounded future pilot that exercises promotion-evidence warning behavior in the standalone Factory v3 advisory lint prototype without changing matcher rules, required gates, or Factory v3 release status.

## Authorized Future Pilot Scope
- Target: `docs/Factory/v3/` research docs only.
- Preferred temporary mutation target: `docs/Factory/v3/PROMOTION_CRITERIA.md`.
- Required command: `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`.
- Required output: a pilot report with warning output, finding classification, remediation, final clean run, and matcher tuning decision.

## File-touch Budget

### This Planning Pack
- `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/**`
- Canonical tracking docs only if final planning state changes: `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, `docs/CHANGELOG.md`

### Future Pilot, If Separately Approved
- Allowed temporary doc target: one file under `docs/Factory/v3/`
- Allowed final evidence report: `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/*PROMOTION*PILOT*.md` or successor run evidence path
- Allowed canonical tracking docs only if tracked state changes

### Forbidden Without Separate Approval
- `scripts/factory_v3_advisory_lint.py`
- `scripts/factoryctl`
- `scripts/knowledge_lint.sh`
- `scripts/factory_stage_lint.py`
- `scripts/factory_pack_lint.py`
- mission lint or mission cursor lint scripts
- CI or merge preflight configuration
- Factory v2 stage contracts
- Runtime-kernel, AEGIS policy, evidence, proof, or authority paths

## Micro-sprint Plan
- MS-00: Baseline clean advisory run.
- MS-01: Temporary promotion-evidence warning capture and classification.
- MS-02: Remediation, final clean advisory run, and closeout evidence.

## Required Verification Before Any Future Commit
- `bash scripts/knowledge_lint.sh`
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`
- All advisory fixture `--expect` checks, including `pilot_usage`
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`
- `./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan`
- `git diff --check`

## Stop Gates
- Stop if the future pilot requires matcher tuning before evidence classification.
- Stop if temporary release/promotion wording cannot be removed cleanly.
- Stop if the advisory result implies required gate adoption.
- Stop if Factory v3 promotion, AEGIS dependency, or runtime-kernel authority is implied.

## Completion Conditions
- This pack is complete when Stage I2 passes and pack-lint passes.
- Future pilot execution requires separate human approval after pack review.

