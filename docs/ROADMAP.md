# ROADMAP.md — Development Roadmap

> **Purpose:** Sprint-level plan and milestone sequence.
>
> **Last updated:** 2026-05-24

---

## Sprints

| Sprint | Title | Status | Date | Evidence |
|--------|-------|--------|------|----------|
| SPRINT_20260518_001 | Factory v3 research track | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260518_002 | Factory v3 advisory validator design | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260518_003 | Factory v3 advisory lint prototype | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/pack/PACK_AUDIT_REPORT.md`; `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md`; `scripts/factory_v3_advisory_lint.py` |
| SPRINT_20260518_004 | Factory v3 advisory lint pilot evidence | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/PILOT_USAGE_REPORT.md`; `tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json` |
| SPRINT_20260518_005 | Factory v3 real-branch advisory lint pilot | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_PILOT_REPORT.md`; `docs/Factory/v3/PILOT_PROFILE_PLAN.md` |
| SPRINT_20260518_006 | Factory v3 non-empty advisory lint pilot | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/REAL_BRANCH_WARNING_PILOT_REPORT.md` |
| SPRINT_20260518_007 | Factory v3 promotion-evidence advisory lint pilot plan | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260519_008 | Factory v3 promotion-evidence advisory lint pilot | Done | 2026-05-19 | `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/PROMOTION_EVIDENCE_PILOT_REPORT.md` |
| SPRINT_20260519_009 | Factory v3 `V3-A006` matcher tuning | Done | 2026-05-19 | `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/A006_MATCHER_TUNING_CLOSEOUT.md`; `tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/expected.json` |
| SPRINT_20260519_010 | Factory v3 post-tuning `V3-A006` smoke pilot | Done | 2026-05-19 | `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/POST_TUNING_A006_SMOKE_REPORT.md` |
| SPRINT_20260519_011 | Cross-version SIMPLE-CODE-GATE v2 mandatory guidance | Done | 2026-05-19 | `AGENTS.md`; `docs/Factory/ORCHESTRATION.md`; `docs/Factory/Spec/STAGE_CONTRACTS.md`; `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md`; `docs/Factory/templates/MISSION_EXECUTION_PROMPT_TEMPLATE.md`; `docs/Factory/templates/SPRINT_ENVELOPE_TEMPLATE.md` |
| SPRINT_20260521_012 | Factory v3 operational-readiness eval planning | Done | 2026-05-21 | `docs/Factory/v3/OPERATIONAL_READINESS_EVAL_PLAN.md` |
| SPRINT_20260521_013 | Factory v3 operational-readiness eval suite planning pack | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0815_v3_operational_readiness_eval_plan/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260521_014 | Standalone V3 operational-readiness eval suite implementation | Done | 2026-05-21 | `scripts/factory_v3_operational_readiness_eval.py`; `tests/fixtures/factory_v3_operational_readiness_eval/expected.json`; `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260521_015 | V3 operational-readiness real-run shadow pilot | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/shadow_pilot/OPERATIONAL_READINESS_SHADOW_PILOT_REPORT.md` |
| SPRINT_20260521_016 | V3 operational-readiness seeded drift pilot | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot/SEEDED_DRIFT_PILOT_REPORT.md` |
| SPRINT_20260521_017 | V3 runtime-boundary seeded drift pilot | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g009/SEEDED_DRIFT_PILOT_V3G009_REPORT.md` |
| SPRINT_20260521_018 | V3 halt-behavior and SIMPLE-CODE-GATE seeded drift pilots | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g005/SEEDED_DRIFT_PILOT_V3G005_REPORT.md`; `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/seeded_drift_pilot_v3g011/SEEDED_DRIFT_PILOT_V3G011_REPORT.md` |
| SPRINT_20260521_019 | V3 operational-readiness evidence rollup | Done | 2026-05-21 | `docs/Factory/v3/OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md` |
| SPRINT_20260521_020 | V3 eval evolution decision pack | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0939_v3_eval_evolution_decision_plan/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260521_021 | V3 confidence pilot batch execution | Done | 2026-05-21 | `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260521_022 | V3 operational decision checklist | Done | 2026-05-21 | `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md` |
| SPRINT_20260522_023 | V3 real halt and reentry pilot | Done | 2026-05-22 | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_024 | V3 natural-language advisory detection pilot | Done | 2026-05-22 | `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_025 | V3-G011 SIMPLE-CODE-GATE severity policy | Done | 2026-05-22 | `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`; `docs/Factory/runs/RUN_20260522_0948_v3_g011_severity_policy/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_026 | V3 operational profile and guarantee matrix | Done | 2026-05-22 | `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`; `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1019_v3_operational_profile_matrix/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_027 | V3-OP-001 finding classification rollup | Done | 2026-05-22 | `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1052_v3_fp_fn_rollup/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_028 | V3-OP-001 external-kernel boundary review | Done | 2026-05-22 | `docs/Factory/v3/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY_REVIEW_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1120_v3_boundary_review/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_029 | V3-OP-001 operational-readiness decision report | Done | 2026-05-22 | `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1150_v3_decision_report/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_030 | V3-OP-001 release approval and user guide | Done | 2026-05-22 | `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`; `docs/Factory/v3/USER_GUIDE.md`; `docs/Factory/runs/RUN_20260522_1220_v3_release_user_guide/EXECUTION_CLOSEOUT.md` |
| SPRINT_20260522_031 | V3 full-vision roadmap | Done | 2026-05-22 | `docs/Factory/v3/VISION.md`; `docs/Factory/v3/ROADMAP_TO_FULL_VISION.md` |
| SPRINT_20260522_032 | V3 roadmap pre-mortem | Done | 2026-05-22 | `docs/Factory/v3/ROADMAP_PREMORTEM.md` |
| SPRINT_20260522_033 | V3 Phase 1 trial capture template | Done | 2026-05-22 | `docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md` |
| SPRINT_20260524_034 | V3 Phase 1 trial operating plan | Done | 2026-05-24 | `docs/Factory/v3/PHASE1_TRIAL_PLAN.md`; `docs/Factory/v3/trials/TRIAL_INDEX.md` |
| SPRINT_20260524_035 | V3 Phase 1 first fallback trial | Done | 2026-05-24 | `docs/Factory/v3/trials/TRIAL_20260524_001_no_bounded_code_change.md`; `docs/Factory/v3/trials/TRIAL_INDEX.md` |
| SPRINT_20260524_036 | V3 Phase 1 trial guide refinement | Done | 2026-05-24 | `docs/Factory/v3/USER_GUIDE.md`; `docs/Factory/v3/PHASE1_TRIAL_PLAN.md`; `docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md` |
| SPRINT_20260524_037 | V3 Harmony placeholder fallback trial | Done | 2026-05-24 | `docs/Factory/v3/trials/TRIAL_20260524_002_harmony_placeholder_fallback.md`; `docs/Factory/v3/USER_GUIDE.md` |

## Next Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Phase 1 V3 real-project trial batch | Next | Record 5 trials with `PHASE1_TRIAL_PLAN.md`; 2 of 5 are recorded, both fallback cases. The next trial should be a completed bounded implementation. |
| Phase 2 V3 structured mission record | Next | Design a shadow `V3_MISSION_RECORD` format only after trial evidence clarifies what must be captured, including pre-envelope fallback decisions. |
| V3-OP-001 trial feedback | Next | Test optional V3 use in real projects, capture friction, missed fallback triggers, and guide/template improvements. |
| V3 user guide refinement | Next | Update the user guide after trial evidence, especially for Codex task prompts and fallback ergonomics. |
| Additional real-branch evidence collection | Next | Collect future advisory findings only as real changes arise; do not expand matchers or integrate gates yet. |
| Advisory check expansion | Blocked | Wait for additional real-branch evidence across more finding classes before adding more checks. |
| `factoryctl` integration or CI usage | Blocked | Requires a new Factory pack and explicit human release approval for gate integration. |
