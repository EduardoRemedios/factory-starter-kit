# Changelog

## Unreleased

- Add SIMPLE-CODE-GATE v2 to root agent guidance, Factory orchestration, stage contracts, sprint envelope templates, execution prompts, and mission execution prompts.
- Add optional Mission Cursor continuity support: `MISSION_CURSOR_TEMPLATE.json`, `mission_cursor_lint.sh`, manifest `Unit ID` support, and generic Codex goal/bookmark guidance.
- Add generic tool-agnostic merge authorization protocol guidance in `docs/Factory/MERGE_PROTOCOL.md`.
- Add optional task-memory support through `factoryctl memory-init`, `memory-suggest`, `memory-log`, and `memory-review`.
- Add generic Repo Cartographer advisory scans under `scripts/cartographer` and `tools/repo_cartographer/`.
- Add generic Agent Loop Bridge review-only handoff docs and deterministic JSON fixture validator.
- Add `docs/Factory/AEGIS_BOUNDARY.md` to align Factory v3 mission governance with AEGIS-style autonomy-kernel primitives without duplicating runtime enforcement.
- Add verification-left-shift v1: verification tiers, optional `verification_manifest.yaml`, manifest template, and `pack-lint` manifest validation.
- Add `factoryctl metrics-init` to instantiate `RUN_METRICS.md` from the canonical template.
- Add `RUN_METRICS_TEMPLATE.md` for lightweight Factory process telemetry after real runs.
- Add `factoryctl stage-lint` for immediate per-stage handoff and output validation.
- Add generic Factory role skills for root planning, Purple gate review, pack consolidation, and execution closeout.
- Harden `factoryctl pack-lint` for non-`SPRINT_` sprint IDs and fixture `notes.md` files.
- Add `docs/Factory/ARCHITECTURE.md` to define the portable Factory Core, harness adapter, validator, extension pack, and project adapter layer model.
- Add `factoryctl pack-lint` for deterministic completed-pack validation after Stage I2.
- Add `docs/Factory/Harnesses/` with Codex-first harness adapter guidance for GPT-5.5 local work, Codex CLI terminal runs, Codex Cloud, plugins, skills, hooks, and connector-backed evidence.

## v0.2.0 - 2026-03-21

- Refresh the starter-kit docs and specs to the latest generic Factory, Mission Mode, and optional Product Owner process shape.
- Add the continuity-recall contract across Stage A, mission checkpointing, and PO brief review.
- Replace the dead `AgentArchitecture` handoff reference with a generic execution-profile field.

## v0.1.0 - 2026-03-10

- Add Apache-2.0 licensing at the repo root.
- Clarify pre-1.0 maturity, starter-kit adaptation expectations, and first-step adoption guidance in the root README.
