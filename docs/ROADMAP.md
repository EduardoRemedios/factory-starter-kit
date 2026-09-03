# ROADMAP.md - Development Roadmap

> **Purpose:** Track starter-kit V2 and earlier process work.
>
> **Last updated:** 2026-08-24

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
| SPRINT_20260810_003 | Build separate upstream-evidence companion plugin | REVIEW_READY | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_001 | Enforce uniform single-repository upstream-evidence adoption | BLOCKED at stochastic model-choice proof; superseded by SPRINT_20260811_002 | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_002 | Repair deterministic packaged PreToolUse verification | REVIEW_READY | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_003 | Repair companion release failure and evidence preservation | REVIEW_READY | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_004 | Reconcile companion evidence-budget governance prospectively | REVIEW_READY; predecessor budget remains FAIL | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_005 | Verify exact public companion boundary | BLOCKED before candidate on volatile Codex turn-diff refs | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_006 | Repair publication ref classifier | Focused implementation tests pass; candidate revalidation pending | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260811_007 | Close final snapshot, protected-inventory, and clone-integrity gaps | Focused checks pass; one frozen candidate/clone gate pending | 2026-08-11 | `docs/CHANGELOG.md` |
| SPRINT_20260812_006 | Repair the Factory and Factory-BMAD 0.2.1 lifecycle | REVIEW_READY; final Factory contract repairs integrated | 2026-08-13 | `scripts/factory_pack_lint.py`; `tests/test_factory_pack_lint_activation_verification.py` |
| SPRINT_20260814_001 | Repair and qualify Factory and Factory-BMAD 0.2.2 | FIXED_AWAITING_RETEST; deterministic qualification passed | 2026-08-14 | `docs/adapters/bmad/FACTORY_BMAD_PILOT_BACKLOG.md`; `tests/test_factory_pack_lint_core.py` |
| SPRINT_20260815_001 | Recover and qualify Factory and Factory-BMAD 0.2.3 | AMENDED_SOURCE_LIVE_QUALIFIED; publication pending | 2026-08-15 | `artifacts/verification/factory_bmad_023_recovery/LIVE_REQUALIFICATION_ADAPTER_REPAIR.md` |
| SPRINT_20260822_001 | Repair Factory-BMAD first-tester cache integrity blocker | REVIEW_READY; first-tester matrix passed, F10 repaired and tester-smoked in 0.2.4 | 2026-08-22 | `scripts/verify_factory_bmad_cli_rollout.py`; `docs/adapters/bmad/FACTORY_BMAD_FIRST_TESTER_HANDOFF.md` |
| SPRINT_20260824_001 | Prepare Claude Code CLI first-team rollout polish | REVIEW_READY | 2026-08-24 | `plugin-src/factory/runtime/factory_plugin.py`; `plugin-src/factory-bmad/runtime/factory_bmad.py`; `docs/adapters/bmad/FACTORY_BMAD_CLI_ROLLOUT_PLAYBOOK.md` |
| SPRINT_20260902_001 | Integrate 0.2.5 solution-context authoring boundary | QUALIFIED; MS-01 through MS-05 closed, canonical closeout `REVIEW_READY`, human review accepted 2026-09-03, status `FACTORY_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`; MS-06 and rollout separately gated | 2026-09-03 | `plugin-src/factory-bmad/project-adapter/factory_project_preflight`; `tests/plugin_fixtures/factory_bmad_solution_context_contract.json` |

## Current Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Factory V2 starter-kit maintenance | Ongoing | Keep this repo focused on V2 and earlier content. |
| Required gate maintenance | Ongoing | Preserve knowledge lint, stage-lint, pack-lint, mission lint, and mission cursor lint behavior for V2 workflows. |
| Context recall repair discipline | Ongoing | Keep direct-source repair explicit, source-backed, and invalid for material unresolved refs. |
| Async contributor handoff hygiene | Ongoing | Use `REVIEW_READY` for review handoffs and reserve `MERGE_READY` for the final sync window after merge preflight passes. |
| Beginner adopter enablement | Ongoing | Keep the non-technical setup guide accurate as agent tools and installer flows change. |
| Harness model routing | Ongoing | Validate Kilo, Cursor, Codex, and Claude Code adapters without changing Factory Core stage contracts. |
| Factory plugin rollout | REVIEW_READY | The maintainer Claude Code Greenfield/Doctor/Progress/Validate slice passed; first-team CLI rollout now has a preflight and guided support path. Complete remaining formal journeys, the independent first-time-user pilot, release decisions, and Product Owner sign-off. |
| Upstream-evidence companion | 0.2.5 REVIEW_READY + CLI rollout hardening | The 0.2.3 first-tester matrix passed for greenfield, brownfield-neither, and BMAD-only brownfield. The 0.2.4 candidate bumped both plugin identities and added same-version Claude cache comparison so stale dependency bytes block before retest or rollout; Mark smoke-tested that guard. The 0.2.5 candidate keeps that guard and adds clearer approval-plan labels plus corrected prune/cache guidance for first-team operators. Claude Desktop remains unsupported until separately validated. Merge, publication, and rollout remain separate decisions. |
| Solution-context integration | Authored integration in progress | BMAD PRD/UX/architecture/spec authoring may produce non-binding `SOLUTION_CONTEXT` evidence; human promotion freezes hash-pinned snapshots and claim dispositions; Factory/Conductor retains all implementation planning, verification, and execution authority. BMAD implementation, sprint execution, code review authority, unattended development, quick-dev, and bmad-loop remain prohibited. Generated-package regeneration, full-suite qualification, MS-06, and any rollout decision remain separately gated. |
