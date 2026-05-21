# ROADMAP.md — Development Roadmap

> **Purpose:** Sprint-level plan and milestone sequence.
>
> **Last updated:** 2026-05-21

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

## Next Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| V3 natural-language advisory detection pilot | Next | Implement only a bounded candidate layer with false-positive corpus and no gate effect, if approved. |
| V3 real reentry and failed-command halt pilot | Next | Prove operational behavior from authored artifacts and actual halt-on-failure execution before any operational profile decision. |
| Additional real-branch evidence collection | Next | Collect future advisory findings only as real changes arise; do not expand matchers or integrate gates yet. |
| Advisory check expansion | Blocked | Wait for additional real-branch evidence across more finding classes before adding more checks. |
| `factoryctl` integration or CI usage | Blocked | Requires a new Factory pack, false-positive review evidence, and explicit human release approval. |
