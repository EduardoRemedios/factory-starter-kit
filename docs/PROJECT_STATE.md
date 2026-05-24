# PROJECT_STATE.md — Canonical Build State

> **Purpose:** Single source of truth for the current state of the build. Updated after every sprint.
>
> **Last updated:** 2026-05-24

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
- A V3 external-kernel boundary review for `V3-OP-001` exists at `docs/Factory/v3/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY_REVIEW_V3_OP_001.md`.
- A V3 operational-readiness decision report for `V3-OP-001` exists at `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`.
- Optional operational release approval for `V3-OP-001` exists at `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.
- A V3 Codex user guide exists at `docs/Factory/v3/USER_GUIDE.md`.
- V3 starter templates exist under `docs/Factory/v3/templates/`.
- A V3 full-vision document exists at `docs/Factory/v3/VISION.md`.
- A V3 roadmap from `V3-OP-001` to the full mission-governance runtime vision exists at `docs/Factory/v3/ROADMAP_TO_FULL_VISION.md`.
- A V3 roadmap-level pre-mortem and golden-fixture backlog exists at `docs/Factory/v3/ROADMAP_PREMORTEM.md`.
- A V3 Phase 1 trial operating plan exists at `docs/Factory/v3/PHASE1_TRIAL_PLAN.md`.
- A Phase 1 V3 real-project trial capture template exists at `docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md`.
- A Phase 1 V3 trial index exists at `docs/Factory/v3/trials/TRIAL_INDEX.md`.
- The first Phase 1 V3 trial record exists at `docs/Factory/v3/trials/TRIAL_20260524_001_no_bounded_code_change.md`, recording a V2 fallback / V3-unsuitable decision before mission-envelope creation.
- The second Phase 1 V3 trial record exists at `docs/Factory/v3/trials/TRIAL_20260524_002_harmony_placeholder_fallback.md`, recording a Harmony pre-envelope fallback because the trial prompt placeholders were not replaced.
- The third Phase 1 V3 trial record exists at `docs/Factory/v3/trials/TRIAL_20260524_003_harmony_faq_ingestion_utf8.md`, recording the first completed Harmony `V3-OP-001` happy-path implementation trial.
- The fourth Phase 1 V3 trial record exists at `docs/Factory/v3/trials/TRIAL_20260524_004_harmony_currency_blank_defaults.md`, recording the second completed Harmony `V3-OP-001` happy-path implementation trial.
- The fifth Phase 1 V3 trial record exists at `docs/Factory/v3/trials/TRIAL_20260524_005_temper_cs_send_aria_disabled.md`, recording the first completed Temper `V3-OP-001` happy-path implementation trial.
- A Phase 1 owner waiver for the non-author user trial requirement exists at `docs/Factory/v3/trials/PHASE1_REQUIREMENT_WAIVER_20260524.md`.
- A Phase 1 decision review for `V3-OP-001` exists at `docs/Factory/v3/PHASE1_DECISION_REVIEW_V3_OP_001.md`, selecting `START_PHASE_2` for shadow mission-record design only.
- A Phase 2 shadow mission-record v0 design exists at `docs/Factory/v3/MISSION_RECORD_DESIGN_V0.md`.
- A shadow `V3_MISSION_RECORD` template exists at `docs/Factory/v3/templates/V3_MISSION_RECORD_TEMPLATE.json`.
- Trial-derived shadow mission-record examples exist under `tests/fixtures/factory_v3_mission_record/`.
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

- Current tracked evidence: V3-OP-001 operational release approval, user guide closeout, V3 full-vision roadmap, roadmap pre-mortem, Phase 1 trial operating plan, Phase 1 trial capture template, two Phase 1 fallback trial records, three completed Phase 1 happy-path trial records, and owner waiver for the non-author user trial requirement.
- Factory v3 status: optional operational use approved for `V3-OP-001` only.
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
- Latest V3-G011 policy result: `RUN_20260522_0948_v3_g011_severity_policy` returns READY; C-04 is DONE with a cross-version SIMPLE-CODE-GATE severity policy for ordinary repos, plus an optional runtime-kernel addendum for repos with separate governance kernels.
- Latest V3 profile result: `RUN_20260522_1019_v3_operational_profile_matrix` returns READY; C-05, C-06, and C-07 are DONE with `V3-OP-001` bounded code change profile, explicit V2 fallback triggers, and a V2 guarantee preservation matrix.
- Latest V3 finding-classification result: `RUN_20260522_1052_v3_fp_fn_rollup` returns READY; C-08 is DONE with accepted clean shadows, seeded drift findings, positive routing, natural-language pilot evidence, and no known false positives or measured seeded/natural-language false negatives.
- Latest V3 boundary-review result: `RUN_20260522_1120_v3_boundary_review` returns READY; C-09 is DONE with evidence that `V3-OP-001` remains coding-governance only, keeps separate governance kernels optional, supports ordinary non-kernel repositories, and does not claim runtime-kernel authority.
- Latest V3 decision-report result: `RUN_20260522_1150_v3_decision_report` returned READY for explicit human release approval and is now superseded by the release approval recorded in `RUN_20260522_1220_v3_release_user_guide`.
- Latest V3 release result: `RUN_20260522_1220_v3_release_user_guide` records optional operational approval for `V3-OP-001` at commit `f07fa11`, keeps Factory v2 as fallback, and adds user guidance plus starter templates.
- Latest V3 Phase 1 trial result: `TRIAL_20260524_001_no_bounded_code_change` records `FALLBACK_TO_V2` because the request authorized a next process step but did not name a bounded code-changing objective suitable for `V3-OP-001`.
- Latest V3 guide refinement result: the user guide, Phase 1 plan, and trial capture template now explicitly support pre-envelope fallback and include a paste-ready Phase 1 trial prompt for ordinary adopting repositories.
- Latest Harmony V3 trial result: `TRIAL_20260524_002_harmony_placeholder_fallback` records `FALLBACK_TO_V2` because the Phase 1 trial prompt still contained placeholders for task, authorized file scope, and allowed verification command.
- Latest Harmony V3 happy-path result: `TRIAL_20260524_003_harmony_faq_ingestion_utf8` records `COMPLETED_WITH_V3`; Harmony changed two authorized files, ran `python3 -m unittest tests.test_faq_ingestion -v`, passed 14 tests, and reported no V2 fallback trigger.
- Latest Harmony V3 currency result: `TRIAL_20260524_004_harmony_currency_blank_defaults` records `COMPLETED_WITH_V3`; Harmony changed two authorized files, ran `python3 -m unittest tests.test_currency_formatter -v`, passed 17 tests, and reported no V2 fallback trigger.
- Latest Temper V3 result: `TRIAL_20260524_005_temper_cs_send_aria_disabled` records `COMPLETED_WITH_V3`; Temper changed two authorized files, ran `npm run verify:cs-browser-demo-surface`, passed the verifier including 9/9 runtime operator-surface tests, and reported no V2 fallback trigger.
- Latest V3 Phase 1 batch result: the 5-trial minimum is met and the owner waived the non-author user trial requirement for this solo AI-native development context; the batch is ready for Phase 1 decision review.
- Latest V3 roadmap alignment result: the top-level roadmap and V3 full-vision roadmap now treat Phase 1 as ready for decision review and keep Phase 2 blocked until that review explicitly selects `START_PHASE_2`.
- Latest V3 Phase 1 decision result: `START_PHASE_2` is selected for shadow `V3_MISSION_RECORD` design only; no default-mode promotion, new V3 profile, required-gate integration, or enforcement is approved.
- Latest V3 Phase 2 shadow-record result: v0 mission-record design and five trial-derived JSON examples exist; no validator, enforcement, gate integration, telemetry, or governance routing is approved.

## What Does NOT Exist Yet

- Factory v3 is not the default Factory mode.
- No Factory v3 profile beyond `V3-OP-001` is approved for operational use.
- Factory v3 user guidance is new and should be refined after real project trials.
- Factory v3 full-vision roadmap exists, but its later phases are not implemented or approved.
- Factory v3 roadmap pre-mortem exists, but its proposed fixtures are a backlog and not yet implemented.
- Phase 1 trial operating plan, index, capture template, two fallback trial records, three happy-path implementation trials, owner waiver, decision review, and Phase 2 v0 shadow mission-record design exist; Phase 2 does not yet have an advisory validator, malformed-record fixtures, enforcement, telemetry, governance routing, or operational promotion.
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
./scripts/factoryctl pack-lint --run RUN_20260522_1220_v3_release_user_guide

# Run your test suite
# (add your project's test command here)
```
