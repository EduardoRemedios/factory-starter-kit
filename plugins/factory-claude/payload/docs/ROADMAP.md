# ROADMAP.md - Development Roadmap

> **Purpose:** Track starter-kit V2 and earlier process work.
>
> **Last updated:** 2026-07-26

## Sprints

| Sprint | Title | Status | Date | Evidence |
|--------|-------|--------|------|----------|
| SPRINT_20260525_001 | Restore V2-only starter-kit scope | Done | 2026-05-25 | `docs/PROJECT_STATE.md` |
| SPRINT_20260624_001 | Add review/merge handoff discipline | Done | 2026-06-24 | `docs/Factory/MERGE_PROTOCOL.md` |
| SPRINT_20260624_002 | Add non-technical onboarding path | Done | 2026-06-24 | `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` |
| SPRINT_20260625_001 | Add Kilo model-routed stage lanes | Done | 2026-06-25 | `docs/Factory/Harnesses/KILO.md`; `./scripts/factoryctl kilo-stage` |
| SPRINT_20260702_001 | Formalize Stage A direct-source recall repair | Done | 2026-07-02 | `docs/Factory/ORCHESTRATION.md`; `scripts/factory_pack_lint.py`; `tests/test_context_recall_repair.py` |
| SPRINT_20260724_001 | Build and pilot dual-platform Factory plugin | Cross-surface technical verification passed; independent pilot pending | 2026-07-24 | `tests/plugin_fixtures/`; `tests/test_factory_plugin_*.py` |

## Current Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Factory V2 starter-kit maintenance | Ongoing | Keep this repo focused on V2 and earlier content. |
| Required gate maintenance | Ongoing | Preserve knowledge lint, stage-lint, pack-lint, mission lint, and mission cursor lint behavior for V2 workflows. |
| Context recall repair discipline | Ongoing | Keep direct-source repair explicit, source-backed, and invalid for material unresolved refs. |
| Async contributor handoff hygiene | Ongoing | Use `REVIEW_READY` for review handoffs and reserve `MERGE_READY` for the final sync window after merge preflight passes. |
| Beginner adopter enablement | Ongoing | Keep the non-technical setup guide accurate as agent tools and installer flows change. |
| Harness model routing | Ongoing | Validate Kilo, Cursor, Codex, and Claude Code adapters without changing Factory Core stage contracts. |
| Factory plugin rollout | In verification | Publish a privacy-safe release candidate, complete the first-time-user pilot, freeze the release candidate, and obtain Product Owner sign-off. |
