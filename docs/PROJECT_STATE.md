# PROJECT_STATE.md — Canonical Build State

> **Purpose:** Single source of truth for the current state of the build. Updated after every sprint.
>
> **Last updated:** 2026-05-21

---

## What Exists

- Factory v2 remains the canonical planning process.
- Factory v3 exists as a research-only documentation track under `docs/Factory/v3/`.
- SIMPLE-CODE-GATE v2 exists as a mandatory cross-version implementation guardrail for both Factory v2 and Factory v3 code-changing work.
- Factory v3 operational-readiness eval planning exists at `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md`.
- A Factory v2 planning pack for the V3 operational-readiness eval suite exists at `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/pack/PACK_AUDIT_REPORT.md`.
- An execution-enabled Factory v2 implementation-plan pack for the standalone V3 eval suite exists at `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/pack/PACK_AUDIT_REPORT.md`.
- A standalone Factory v3 operational-readiness eval runner exists at `scripts/factory_v3_operational_readiness_eval.py`.
- Golden operational-readiness eval fixtures exist at `tests/fixtures/factory_v3_operational_readiness_eval/`.
- A V3 operational-readiness decision report template exists at `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_TEMPLATE.md`.
- A standalone, optional Factory v3 advisory lint prototype exists at `scripts/factory_v3_advisory_lint.py`.
- Advisory lint fixtures exist under `tests/fixtures/factory_v3_advisory_lint/` for clean, warning, promotion-claim, and pilot boundary-stressor cases.
- Factory v3 advisory lint execution closeout evidence exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md`.
- The first deterministic advisory lint pilot report exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/PILOT_USAGE_REPORT.md`.
- The first real-branch advisory lint pilot report exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_PILOT_REPORT.md`.
- The first non-empty real-branch advisory lint pilot report exists at `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_WARNING_PILOT_REPORT.md`.
- A planning-only Factory v2 pack for the next promotion-evidence advisory lint pilot exists at `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/PACK_AUDIT_REPORT.md`.
- Promotion-evidence pilot evidence exists at `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/PROMOTION_EVIDENCE_PILOT_REPORT.md`.
- Bounded `V3-A006` matcher tuning closeout evidence exists at `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/A006_MATCHER_TUNING_CLOSEOUT.md`.
- Post-tuning `V3-A006` real-doc smoke evidence exists at `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/POST_TUNING_A006_SMOKE_REPORT.md`.

## Current Tracking Snapshot

- Current tracked evidence: standalone V3 operational-readiness eval suite implementation closeout.
- Factory v3 status: Level 0 research only.
- Advisory lint status: optional standalone prototype only.
- Latest fixture pilot result: deliberate boundary-stressor fixture returns `ADVISORY_FAIL_NON_BLOCKING` with `blocking_effect: none`.
- Latest real-branch pilot result: `docs/Factory/v3` returns `ADVISORY_PASS` with 0 findings after a bounded research-doc change.
- Latest non-empty real-branch pilot result: temporary real-doc drift returns `ADVISORY_FAIL_NON_BLOCKING` with 2 accepted findings and `blocking_effect: none`; final docs return `ADVISORY_PASS` after remediation.
- Latest planning result: promotion-evidence pilot plan pack returns `PASS` and remains `PLANNING_ONLY`.
- Latest promotion-evidence pilot result: temporary local release claim returned `ADVISORY_PASS` with 0 findings; this is classified as a `V3-A006` false negative / missed signal.
- Latest matcher tuning result: `V3-A006` now evaluates local promotion or release claim paragraphs and the masked promotion-claim fixture returns `ADVISORY_WARN`.
- Latest post-tuning smoke result: temporary local release claim returns `ADVISORY_WARN` with accepted `V3-A006` at `docs/Factory/v3/PROMOTION_CRITERIA.md`; final docs return `ADVISORY_PASS`.
- Latest clean-doc result: `docs/Factory/v3` returns `ADVISORY_PASS`.
- Latest V3 operational-readiness planning result: `RUN_20260521_0815_v3_operational_readiness_eval_plan` pack returns `PASS` and remains `PLANNING_ONLY`.
- Latest V3 eval-suite implementation result: standalone operational-readiness fixture regression passes; real `docs/Factory/v3` smoke returns `ADVISORY_PASS`; runner remains advisory and outside required gates.

## What Does NOT Exist Yet

- Factory v3 is not promoted for release.
- Factory v3 does not yet have operational-readiness fixtures, a V3 mission-envelope eval suite, or enough real-run pilot evidence to become an optional operational mode.
- Factory v3 advisory lint is not wired into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, mission cursor lint, merge preflight, or any required Factory v2 gate.
- Factory v3 does not implement runtime-kernel authority, proof, leases, sandboxing, policy, or production action mediation.
- No advisory check expansion has been approved yet; current real-branch evidence supports continued standalone advisory use only.
- No required-gate integration has been approved; advisory lint remains standalone and optional.

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
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/expected.json --json

# Run the standalone Factory v3 operational-readiness eval suite
python3 scripts/factory_v3_operational_readiness_eval.py --target tests/fixtures/factory_v3_operational_readiness_eval --expect tests/fixtures/factory_v3_operational_readiness_eval/expected.json --json
python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json

# Verify the relevant Factory packs still lint
./scripts/factoryctl pack-lint --run RUN_20260518_1155_v3_advisory_validator_design
./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan
./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan
./scripts/factoryctl pack-lint --run RUN_20260521_0815_v3_operational_readiness_eval_plan
./scripts/factoryctl pack-lint --run RUN_20260521_0833_v3_eval_suite_impl_plan

# Run your test suite
# (add your project's test command here)
```
