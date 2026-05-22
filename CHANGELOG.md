# Changelog

## Unreleased

- Add cross-version SIMPLE-CODE-GATE severity policy and mark V3 operational checklist C-04 complete.
- Add opt-in V3 natural-language advisory detection pilot with clean false-positive corpus and drift corpus measurement.
- Add execution-enabled V3 real halt and reentry pilot evidence; C-01 and C-02 are now marked DONE in the operational decision checklist.
- Add Factory v3 operational decision checklist capturing remaining evidence required before any V3 operational-use decision.
- Add execution-enabled V3 confidence pilot batch with additional real shadows, seeded drift evidence, positive routing pilots, and natural-language detection design.
- Add a Factory v2 planning pack for the V3 eval evolution decision, selecting a staged confidence path toward future operational V3 use.
- Add Factory v3 operational-readiness evidence rollup across the clean shadow pilot and seeded drift pilots, retaining NO-GO for V3 operational promotion.
- Add seeded V3 operational-readiness drift pilot reports for `V3-G005` verification halt behavior and `V3-G011` SIMPLE-CODE-GATE detection.
- Add second seeded V3 operational-readiness drift pilot report with accepted `V3-G009` runtime-boundary detection.
- Add first seeded V3 operational-readiness drift pilot report with accepted `V3-G007` detection.
- Add first real-run V3 operational-readiness shadow pilot report for the standalone eval runner.
- Add standalone Factory v3 operational-readiness eval runner, golden fixtures, and decision report template.
- Add an execution-enabled Factory v2 implementation-plan pack for the standalone V3 operational-readiness eval suite.
- Add a Factory v2 planning pack for the V3 operational-readiness eval suite, including pre-mortem, verification plan, golden fixture inventory, Red/Blue review, and Purple audit.
- Add Factory v3 operational-readiness pre-mortem and eval plan for judging optional V3 operational use while retaining V2.
- Add SIMPLE-CODE-GATE v2 as mandatory cross-version implementation guidance for Factory v2 and v3 in root agent guidance, Factory orchestration, stage contracts, sprint envelope templates, execution prompts, and mission execution prompts.
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
