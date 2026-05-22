# PROJECT_STATE.md — Canonical Build State

> **Purpose:** Single source of truth for the current state of the build. Updated after every sprint.
>
> **Last updated:** 2026-05-22

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
- A V3 operational-readiness evidence rollup exists at `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md`.
- A V3 operational decision checklist exists at `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md`.
- An execution-enabled V3 real halt and reentry pilot exists at `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md`.
- An execution-enabled V3 natural-language advisory detection pilot exists at `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/EXECUTION_CLOSEOUT.md`.
- A cross-version SIMPLE-CODE-GATE severity policy exists at `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`.
- A bounded V3 operational profile candidate exists at `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`.
- A V2 guarantee preservation matrix for that profile exists at `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md`.
- A V3 finding classification rollup for `V3-OP-001` exists at `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md`.
- A V3 AEGIS/runtime-kernel boundary review for `V3-OP-001` exists at `docs/Factory/v3/AEGIS_RUNTIME_BOUNDARY_REVIEW_V3_OP_001.md`.
- A V3 operational-readiness decision report for `V3-OP-001` exists at `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`.
- A Factory v2 planning pack for the V3 eval evolution decision exists at `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/PACK_AUDIT_REPORT.md`.
- An execution-enabled V3 confidence pilot batch exists at `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/EXECUTION_CLOSEOUT.md`.
- The first real-run V3 operational-readiness shadow pilot report exists at `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md`.
- The first seeded V3 operational-readiness drift pilot report exists at `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot/SEEDED_DRIFT_PILOT_REPORT.md`.
- The second seeded V3 operational-readiness drift pilot report exists at `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g009/SEEDED_DRIFT_PILOT_V3G009_REPORT.md`.
- Seeded V3 operational-readiness drift pilot reports for verification halt behavior and SIMPLE-CODE-GATE coverage exist at `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md` and `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md`.
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

- Current tracked evidence: V3-OP-001 operational-readiness decision report closeout.
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
- Latest V3 operational-readiness shadow pilot result: real implementation-plan run root returns `ADVISORY_PASS` with 0 findings and `promotion_decision: not_authorized`.
- Latest seeded drift pilot result: run-shaped V2 deprecation fixture returns `ADVISORY_FAIL_NON_BLOCKING` with accepted `V3-G007` and `blocking_effect: none`.
- Latest runtime-boundary seeded drift pilot result: run-shaped runtime-kernel authority fixture returns `ADVISORY_FAIL_NON_BLOCKING` with accepted `V3-G009` and `blocking_effect: none`.
- Latest halt-behavior seeded drift pilot result: run-shaped verification-halt fixture returns `ADVISORY_FAIL_NON_BLOCKING` with accepted `V3-G005` and `blocking_effect: none`.
- Latest SIMPLE-CODE-GATE seeded drift pilot result: run-shaped over-abstraction fixture returns `ADVISORY_WARN` with accepted `V3-G011` and `blocking_effect: none`.
- Latest V3 operational-readiness evidence rollup result: NO-GO for V3 operational promotion; GO for continued V3 advisory shadowing under V2 authority; next decision is whether to keep deterministic trigger-marker coverage or design broader natural-language drift detection.
- Latest V3 eval evolution planning result: `RUN_20260521_0939_v3_eval_evolution_decision_plan` pack returns `PASS`, selects a staged combined path, and defines confidence thresholds for future operational V3 use while retaining V2 authority.
- Latest V3 confidence pilot batch result: `RUN_20260521_0948_v3_confidence_pilot_execution` returns READY; two additional real-run shadows pass, seeded V3-G003/G006/G010/G014 and controlled V3-G005 are accepted, V3-G012/V3-G013 positive routing passes, and V3 remains not operationally promoted.
- Latest V3 decision-checklist result: `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md` records C-01 through C-09 as DONE and C-10 as ready for explicit approval.
- Latest V3 real behavior pilot result: `RUN_20260522_0824_v3_real_halt_reentry_pilot` returns READY; C-01 and C-02 are DONE with run-local evidence for nonzero halt/no-continuation, authored-artifact resume, and stale-cursor halt.
- Latest V3 natural-language pilot result: `RUN_20260522_0836_v3_nl_detection_pilot` returns READY; C-03 is DONE with opt-in pilot mode, 0 false positives across 10 clean artifacts, and expected drift IDs detected.
- Latest V3-G011 policy result: `RUN_20260522_0948_v3_g011_severity_policy` returns READY; C-04 is DONE with a cross-version SIMPLE-CODE-GATE severity policy for ordinary repos, plus an optional runtime-kernel addendum for repos with AEGIS-like governance.
- Latest V3 profile result: `RUN_20260522_1019_v3_operational_profile_matrix` returns READY; C-05, C-06, and C-07 are DONE with `V3-OP-001` bounded code change profile, explicit V2 fallback triggers, and a V2 guarantee preservation matrix.
- Latest V3 finding-classification result: `RUN_20260522_1052_v3_fp_fn_rollup` returns READY; C-08 is DONE with accepted clean shadows, seeded drift findings, positive routing, natural-language pilot evidence, and no known false positives or measured seeded/natural-language false negatives.
- Latest V3 boundary-review result: `RUN_20260522_1120_v3_boundary_review` returns READY; C-09 is DONE with evidence that `V3-OP-001` remains coding-governance only, keeps AEGIS optional, supports ordinary non-AEGIS repositories, and does not claim runtime-kernel authority.
- Latest V3 decision-report result: `RUN_20260522_1150_v3_decision_report` returns READY; C-10 is ready for explicit human release approval, with `V3-OP-001` recommended for optional operational release only after approval names the profile, commit or release tag, V2 fallback, and accepted residual risks.

## What Does NOT Exist Yet

- Factory v3 is not promoted for release.
- A human release decision has not yet been recorded, even though decision-prep evidence is sufficient for that decision on optional `V3-OP-001` operational use.
- Factory v3 has no approved operational profile yet; a future release decision must still name the approving commit or release tag, V2 fallback, accepted residual risks, and human approver.
- Factory v3 does not yet have a user guide for Codex users adopting V3 from V2.
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
./scripts/factoryctl pack-lint --run RUN_20260521_0939_v3_eval_evolution_decision_plan
./scripts/factoryctl pack-lint --run RUN_20260521_0948_v3_confidence_pilot_execution
./scripts/factoryctl pack-lint --run RUN_20260522_0824_v3_real_halt_reentry_pilot
./scripts/factoryctl pack-lint --run RUN_20260522_0836_v3_nl_detection_pilot
./scripts/factoryctl pack-lint --run RUN_20260522_0948_v3_g011_severity_policy
./scripts/factoryctl pack-lint --run RUN_20260522_1019_v3_operational_profile_matrix
./scripts/factoryctl pack-lint --run RUN_20260522_1052_v3_fp_fn_rollup
./scripts/factoryctl pack-lint --run RUN_20260522_1120_v3_boundary_review
./scripts/factoryctl pack-lint --run RUN_20260522_1150_v3_decision_report

# Run your test suite
# (add your project's test command here)
```
