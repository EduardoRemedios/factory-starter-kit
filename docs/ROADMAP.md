# ROADMAP.md — Development Roadmap

> **Purpose:** Sprint-level plan and milestone sequence.
>
> **Last updated:** 2026-05-18

---

## Sprints

| Sprint | Title | Status | Date | Evidence |
|--------|-------|--------|------|----------|
| SPRINT_20260518_001 | Factory v3 research track | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260518_002 | Factory v3 advisory validator design | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_AUDIT_REPORT.md` |
| SPRINT_20260518_003 | Factory v3 advisory lint prototype | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/pack/PACK_AUDIT_REPORT.md`; `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/EXECUTION_CLOSEOUT.md`; `scripts/factory_v3_advisory_lint.py` |
| SPRINT_20260518_004 | Factory v3 advisory lint pilot evidence | Done | 2026-05-18 | `docs/Factory/runs/RUN_20260518_1235_v3_advisory_lint_impl_plan/PILOT_USAGE_REPORT.md`; `tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json` |

## Next Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Real-branch advisory lint pilot | Next | Run the standalone advisory lint on an actual Factory v3 docs branch and classify accepted, false-positive, needs-more-context, and deferred findings. |
| Advisory check expansion | Blocked | Wait for real-branch pilot evidence before adding more checks. |
| `factoryctl` integration or CI usage | Blocked | Requires a new Factory pack, false-positive review evidence, and explicit human release approval. |
