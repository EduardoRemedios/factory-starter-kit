# ROADMAP.md - Development Roadmap

> **Purpose:** Track starter-kit V2 and earlier process work.
>
> **Last updated:** 2026-08-15

## Sprints

| Sprint | Title | Status | Date | Evidence |
|--------|-------|--------|------|----------|
| SPRINT_20260525_001 | Restore V2-only starter-kit scope | Done | 2026-05-25 | `docs/PROJECT_STATE.md` |
| SPRINT_20260624_001 | Add review/merge handoff discipline | Done | 2026-06-24 | `docs/Factory/MERGE_PROTOCOL.md` |
| SPRINT_20260624_002 | Add non-technical onboarding path | Done | 2026-06-24 | `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` |
| SPRINT_20260625_001 | Add Kilo model-routed stage lanes | Done | 2026-06-25 | `docs/Factory/Harnesses/KILO.md`; `./scripts/factoryctl kilo-stage` |
| SPRINT_20260702_001 | Formalize Stage A direct-source recall repair | Done | 2026-07-02 | `docs/Factory/ORCHESTRATION.md`; `scripts/factory_pack_lint.py`; `tests/test_context_recall_repair.py` |
| SPRINT_20260724_001 | Build and pilot dual-platform Factory plugin | Public release candidate prepared for `main`; independent pilot pending | 2026-07-24 | `README.md`; `tests/plugin_fixtures/`; `tests/test_factory_plugin_*.py` |
| SPRINT_20260805_002 | Harden generic Factory plugin prerequisites and RC 0.2.0 | REVIEW_READY | 2026-08-05 | `docs/CHANGELOG.md` |
| SPRINT_20260815_002 | Uplift Factory-only plugin to 0.2.3 and harden CLI rollout | REVIEW_READY | 2026-08-15 | `scripts/verify_factory_cli_rollout.py`; `docs/onboarding/FACTORY_PLUGIN_CLI_ROLLOUT_PLAYBOOK.md` |

## Current Candidates

| Candidate | Status | Notes |
|-----------|--------|-------|
| Factory V2 starter-kit maintenance | Ongoing | Keep this repo focused on V2 and earlier content. |
| Required gate maintenance | Ongoing | Preserve knowledge lint, stage-lint, pack-lint, mission lint, and mission cursor lint behavior for V2 workflows. |
| Context recall repair discipline | Ongoing | Keep direct-source repair explicit, source-backed, and invalid for material unresolved refs. |
| Async contributor handoff hygiene | Ongoing | Use `REVIEW_READY` for review handoffs and reserve `MERGE_READY` for the final sync window after merge preflight passes. |
| Beginner adopter enablement | Ongoing | Keep the non-technical setup guide accurate as agent tools and installer flows change. |
| Harness model routing | Ongoing | Validate Kilo, Cursor, Codex, and Claude Code adapters without changing Factory Core stage contracts. |
| Factory plugin rollout | REVIEW_READY | Factory-only plugin source and generated packages are uplifted to 0.2.3. Claude Code CLI rollout now has a read-only preflight and first-team playbook. Complete the first-time-user pilot, maintainer review, release decisions, and Product Owner sign-off. |
| Codex Agent Plugins v1 compatibility | Planned after 0.2.3 rollout decision | Deliver as Factory plugin 0.3.0: generate the portable root `plugin.json` from the existing authored source, retain the native Codex manifest during transition, and prove both standard-only and dual-manifest loading in Codex App. |
| Optional upstream-evidence adapter | Deferred | Plan as a separate Factory run only after Codex compatibility passes; do not add MCP, portable dependency claims, adapter policy, or upstream-promotion writes to the 0.3.0 compatibility release. |

## Planned Codex Agent Plugins Compatibility Release

Decision: adopt Agent Plugins v1 as a Codex-first distribution and interoperability advancement, without changing Factory workflow behavior or reopening the 0.2.x rollout candidate.

- Release sequence: preserve and finish the `0.2.3` rollout decision; implement Agent Plugins compatibility as `0.3.0` so two different artifacts never share the same version.
- In scope: generate the portable root `plugin.json` from `plugin-src/`, retain `.codex-plugin/plugin.json` for transitional compatibility, and add schema, deterministic-build, privacy, package-content, and version-alignment checks.
- Required live proof: validate an isolated standard-only package in Codex App so the legacy manifest cannot mask a loader failure, then validate the dual-manifest package for backward compatibility.
- Support boundary: claim only the Codex surfaces and operating systems exercised by live verification.
- Out of scope: MCP servers, plugin dependency semantics, adapter skills or policy, upstream-evidence promotion, and broad cross-client portability claims.
- Go/no-go rule: do not release `0.3.0` if the standard-only package cannot load and execute the existing Factory entry points correctly without repository mutation outside their current contracts.
- Upstream-evidence follow-on prerequisite: any later write-capable promotion flow must have deterministic source and output digests, review evidence, an allowed destination, explicit human approval, a rollback receipt, and project-preflight verification. Until then, upstream promotion remains preview-only.
