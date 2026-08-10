# ROADMAP.md - Development Roadmap

> **Purpose:** Track starter-kit V2 and earlier process work.
>
> **Last updated:** 2026-08-10

## Sprints

| Sprint | Title | Status | Date | Evidence |
|--------|-------|--------|------|----------|
| SPRINT_20260525_001 | Restore V2-only starter-kit scope | Done | 2026-05-25 | `docs/PROJECT_STATE.md` |
| SPRINT_20260624_001 | Add review/merge handoff discipline | Done | 2026-06-24 | `docs/Factory/MERGE_PROTOCOL.md` |
| SPRINT_20260624_002 | Add non-technical onboarding path | Done | 2026-06-24 | `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` |
| SPRINT_20260625_001 | Add Kilo model-routed stage lanes | Done | 2026-06-25 | `docs/Factory/Harnesses/KILO.md`; `./scripts/factoryctl kilo-stage` |
| SPRINT_20260702_001 | Formalize Stage A direct-source recall repair | Done | 2026-07-02 | `docs/Factory/ORCHESTRATION.md`; `scripts/factory_pack_lint.py`; `tests/test_context_recall_repair.py` |
| SPRINT_20260724_001 | Build and pilot dual-platform Factory plugin | Codex pre-pilot passed; Claude and formal pilot pending | 2026-07-24 | `docs/onboarding/FACTORY_PLUGIN_PILOT_RUNBOOK.md` |
| SPRINT_20260805_002 | Harden generic Factory plugin prerequisites and RC 0.2.0 | REVIEW_READY | 2026-08-05 | `docs/CHANGELOG.md` |
| SPRINT_20260805_003 | Finalize Factory plugin RC 0.2.0 and execution closeout | REVIEW_READY | 2026-08-05 | `scripts/factory_execution_closeout.py`; `tests/test_factory_execution_closeout.py` |
| SPRINT_20260805_004 | Repair Factory plugin run-root path safety | REVIEW_READY | 2026-08-05 | `tests/test_factory_execution_closeout.py`; `tests/test_factory_project_preflight.py` |
| SPRINT_20260805_005 | Reverify release evidence and public release scope | REVIEW_READY | 2026-08-05 | `python3 -m unittest discover -s tests -v`; `python3 scripts/build_factory_plugins.py --check` |
| SPRINT_20260810_001 | Repair Greenfield CLI empty-target bootstrap | REVIEW_READY | 2026-08-10 | `tests/test_factory_plugin_cli.py`; `docs/onboarding/FACTORY_PLUGIN_QUICK_START.md` |
| SPRINT_20260810_002 | Preserve exact Claude-local metadata during Greenfield bootstrap | REVIEW_READY | 2026-08-10 | `tests/test_factory_plugin_setup_plan.py`; `tests/test_factory_plugin_lifecycle.py` |
| SPRINT_20260810_003 | Plan separate upstream-evidence companion plugin | I2 PASS — awaiting execution authorization | 2026-08-10 | `docs/CHANGELOG.md` |

## Current Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Factory V2 starter-kit maintenance | Ongoing | Keep this repo focused on V2 and earlier content. |
| Required gate maintenance | Ongoing | Preserve knowledge lint, stage-lint, pack-lint, mission lint, and mission cursor lint behavior for V2 workflows. |
| Context recall repair discipline | Ongoing | Keep direct-source repair explicit, source-backed, and invalid for material unresolved refs. |
| Async contributor handoff hygiene | Ongoing | Use `REVIEW_READY` for review handoffs and reserve `MERGE_READY` for the final sync window after merge preflight passes. |
| Beginner adopter enablement | Ongoing | Keep the non-technical setup guide accurate as agent tools and installer flows change. |
| Harness model routing | Ongoing | Validate Kilo, Cursor, Codex, and Claude Code adapters without changing Factory Core stage contracts. |
| Factory plugin rollout | REVIEW_READY | The maintainer Claude Code Greenfield/Doctor/Progress/Validate slice passed; complete remaining formal journeys, the independent first-time-user pilot, release decisions, and Product Owner sign-off. |
| Upstream-evidence companion | I2 PASS — PLANNING_ONLY | Reviewed pack pins the enterprise upstream tool, Factory authority, immutable promotion, existing project preflight, concise Claude UX, and isolated live proof; implementation awaits exact human authorization. |
