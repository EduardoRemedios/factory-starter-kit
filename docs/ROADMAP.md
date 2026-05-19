# ROADMAP.md — Development Roadmap

> **Purpose:** Sprint-level plan and milestone sequence.
>
> **Last updated:** 2026-05-19

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

## Next Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| `V3-A006` matcher tuning | Next | Pilot evidence shows a false negative from target-wide promotion-evidence matching; tune only this check in a bounded implementation run. |
| Advisory check expansion | Blocked | Wait for additional real-branch evidence across more finding classes before adding more checks. |
| `factoryctl` integration or CI usage | Blocked | Requires a new Factory pack, false-positive review evidence, and explicit human release approval. |
