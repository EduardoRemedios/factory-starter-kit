# PROJECT_STATE.md — Canonical Build State

> **Purpose:** Single source of truth for the current state of the build. Updated after every sprint.
>
> **Last updated:** 2026-05-18

---

## What Exists

- Factory v2 remains the canonical planning process.
- Factory v3 exists as a research-only documentation track under `docs/Factory/v3/`.
- A standalone, optional Factory v3 advisory lint prototype exists at `scripts/factory_v3_advisory_lint.py`.
- Advisory lint fixtures exist under `tests/fixtures/factory_v3_advisory_lint/` for clean, warning, promotion-claim, and pilot boundary-stressor cases.
- Factory v3 advisory lint execution closeout evidence exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md`.
- The first deterministic advisory lint pilot report exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/PILOT_USAGE_REPORT.md`.
- The first real-branch advisory lint pilot report exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_PILOT_REPORT.md`.

## Current Tracking Snapshot

- Current `main` evidence head: `b272eed Update Factory v3 canonical tracking docs`.
- Factory v3 status: Level 0 research only.
- Advisory lint status: optional standalone prototype only.
- Latest fixture pilot result: deliberate boundary-stressor fixture returns `ADVISORY_FAIL_NON_BLOCKING` with `blocking_effect: none`.
- Latest real-branch pilot result: `docs/Factory/v3` returns `ADVISORY_PASS` with 0 findings after a bounded research-doc change.
- Latest clean-doc result: `docs/Factory/v3` returns `ADVISORY_PASS`.

## What Does NOT Exist Yet

- Factory v3 is not promoted for release.
- Factory v3 advisory lint is not wired into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, mission cursor lint, merge preflight, or any required Factory v2 gate.
- Factory v3 does not implement runtime-kernel authority, proof, leases, sandboxing, policy, or production action mediation.
- No non-empty real-branch warning review has been completed yet; the first real-branch pilot produced no findings to classify.

## How to Verify

```bash
# Run the knowledge lint preflight
bash scripts/knowledge_lint.sh

# Run the optional Factory v3 advisory lint prototype
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json

# Run deterministic advisory lint fixture checks
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json

# Verify the relevant Factory packs still lint
./scripts/factoryctl pack-lint --run RUN_20260518_1155_v3_advisory_validator_design
./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan

# Run your test suite
# (add your project's test command here)
```
