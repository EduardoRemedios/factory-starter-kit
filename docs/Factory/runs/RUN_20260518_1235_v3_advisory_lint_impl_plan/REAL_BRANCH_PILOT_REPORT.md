# Real-Branch Pilot Report - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-18): Recorded the first real-branch advisory lint pilot against Factory v3 research docs.

## Purpose
Exercise the standalone Factory v3 advisory lint prototype against a bounded real documentation branch, not a fixture, and classify any findings before considering additional checks or integrations.

## Pilot Branch
- Branch: `codex/factory-v3-real-doc-advisory-pilot`
- Base revision: `b272eed`
- Target path: `docs/Factory/v3`
- Pilot doc change: added `P6 - Real-Branch Advisory Lint Review` to `docs/Factory/v3/PILOT_PROFILE_PLAN.md`.

## Boundary Conditions
- Factory v2 remains the canonical process.
- Factory v3 remains Level 0 research only.
- Advisory lint remains standalone, optional, and non-blocking.
- Required blocking effect remains `none`.
- AEGIS/runtime-kernel authority remains external.

## Command
```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

## Result
- Status: `ADVISORY_PASS`
- Blocking effect: `none`
- Promotion level: `research`
- Files checked: 9
- Findings: 0
- Warnings: 0
- Review status: `not_required`

## Checked Artifacts
- `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`
- `docs/Factory/v3/CONCEPT_CANDIDATES.md`
- `docs/Factory/v3/NON_GOALS_AND_BOUNDARIES.md`
- `docs/Factory/v3/PILOT_PROFILE_PLAN.md`
- `docs/Factory/v3/PROMOTION_CRITERIA.md`
- `docs/Factory/v3/README.md`
- `docs/Factory/v3/SHADOW_SCHEMA_CANDIDATES.md`
- `docs/Factory/v3/STRATEGY.md`
- `docs/Factory/v3/evals/EVAL_20260518_001.md`

## Finding Classification
No findings were emitted, so there were no individual findings to classify.

| Classification | Count | Notes |
| --- | ---: | --- |
| `accepted` | 0 | No advisory findings. |
| `false_positive` | 0 | No advisory findings. |
| `needs_more_context` | 0 | No advisory findings. |
| `deferred` | 0 | No advisory findings. |

## Matcher Tuning Decision
Decision: no matcher tuning.

Rationale: the real-doc pilot produced `ADVISORY_PASS` with zero findings after a bounded research-only doc update. There is no evidence of a false positive, false negative, or unclear warning that would justify changing matcher rules.

## Verification Evidence
- `bash scripts/knowledge_lint.sh`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: PASS, `ADVISORY_PASS`, 9 files checked, 0 findings.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`: PASS.
- `git diff --check`: PASS.

## Protected Boundary Review
- No changes were made to `scripts/factory_v3_advisory_lint.py`.
- No changes were made to `scripts/factoryctl`.
- No changes were made to `scripts/knowledge_lint.sh`.
- No changes were made to `scripts/factory_stage_lint.py`.
- No changes were made to `scripts/factory_pack_lint.py`.
- No changes were made to mission lint, mission cursor lint, CI, or merge preflight.
- No Factory v3 release or promotion was claimed.

## Interpretation
The first real-branch pilot confirms that a small Factory v3 research-doc update can be reviewed by the standalone advisory lint without introducing v2 gate wiring, AEGIS dependency, runtime-kernel authority claims, or promotion language. This is a signal-quality data point only; it does not justify required gate adoption.

## Residual Risk
- The pilot had zero findings, so it did not exercise human classification of non-empty real-doc warnings.
- Future pilots should include normal v3 docs changes large enough to test whether useful warnings appear without excessive false positives.
- Any integration into `factoryctl`, CI, knowledge lint, stage-lint, pack-lint, mission lint, or merge preflight remains blocked without a new Factory v2-governed pack and explicit human release approval.
