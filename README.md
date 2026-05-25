# Factory Starter Kit

A generic, open-source starter kit for Factory V2 and earlier planning workflows.

The starter kit is the reusable process layer for agentic software delivery: explicit intent, explicit constraints, explicit verification, and explicit continuity before coding starts.

## What This Starter Kit Includes

- Factory runner guide and stage/spec contracts.
- Mission Mode for bounded multi-sprint chains.
- Context recall tooling and report templates.
- Deterministic stage-lint and pack-lint validation.
- Optional machine-readable verification manifests for execution-enabled and Mission Mode runs.
- SIMPLE-CODE-GATE v2 for small, direct, behavior-preserving implementation.
- Optional Mission Cursor continuity guard for long Codex/agent sessions.
- Tool-agnostic merge authorization protocol guidance.
- Optional task-memory runbook helper through `factoryctl`.
- Optional repo cartographer advisory scan.
- Generic review-only Agent Loop Bridge harness pattern.
- Harness adapter guidance for Codex and other AI coding tools.
- Optional Product Owner pre-Factory process.
- Starter lint scripts and project-state placeholders.

You drop it into your own repository and adapt the project-specific spine.

## Factory Version Posture

This repository is for Factory V2 and earlier content.

Factory V2 remains the default starter-kit process:

- `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`
- Mission Mode as an additive wrapper for bounded multi-sprint chains.
- deterministic stage-lint, pack-lint, context recall, verification manifest, and merge authorization guidance.
- optional support helpers such as task memory, Repo Cartographer, Mission Cursor continuity, and Agent Loop Bridge.

## Quick Start

1. Copy this repository into your own repository as the starting framework layer.
2. Edit `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md`.
3. Install script dependencies with `python3 -m pip install -r requirements.txt`.
4. Run `bash scripts/knowledge_lint.sh`.
5. Build the continuity index with `./scripts/factoryctl context-index`.
6. Optional: initialize task memory with `./scripts/factoryctl memory-init`.
7. Optional: run an advisory repo scan with `./scripts/cartographer`.
8. If you will use Mission Mode, run `bash scripts/mission_lint.sh <MISSION_ID>`.
9. If you will use Mission Cursor continuity, run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before resuming from the cursor.

## Process Layers

1. Core Factory pipeline: `raw_brief.md -> A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`
2. Context recall layer: indexed recall reports before Stage A, mission checkpointing, and PO brief review.
3. Product Owner lane: Phase Brief -> Phase Intent -> PO sprint brief -> Brief Review PASS -> Factory.
4. Mission Mode: ordered multi-sprint execution under one consolidated checkpoint.
5. Verification manifest: compact runnable check inventory for execution-enabled and Mission Mode units.
6. Mission Cursor continuity: derived resume cursor plus lint gate for long-running agent sessions.
7. Task memory: local runbook suggestion and outcome journal for repeat work.
8. Repo Cartographer: advisory snapshot reports for repository state, drift, verification, and traceability.
9. Agent Loop Bridge: review-only structured handoffs between agent lanes.

See `docs/Factory/ARCHITECTURE.md` for the portable layer model.

## Repository Map

```text
your-repo/
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── requirements.txt
├── scripts/
│   ├── factoryctl
│   ├── factory_context_index.py
│   ├── factory_pack_lint.py
│   ├── factory_run_metrics.py
│   ├── factory_stage_lint.py
│   ├── factory_task_memory.py
│   ├── agent_loop_bridge_validate.py
│   ├── cartographer
│   ├── knowledge_lint.sh
│   ├── mission_cursor_lint.sh
│   └── mission_lint.sh
├── tools/
│   └── repo_cartographer/
└── docs/
    ├── PROJECT_STATE.md
    ├── ROADMAP.md
    ├── CHANGELOG.md
    └── Factory/
        ├── ARCHITECTURE.md
        ├── MERGE_PROTOCOL.md
        ├── ORCHESTRATION.md
        ├── MISSION_MODE.md
        ├── SCRATCHPAD.md
        ├── TASK_MEMORY.md
        ├── Harnesses/
        ├── ProductOwner/
        ├── Spec/
        └── templates/
```

This starter kit intentionally does not ship product-specific run packs, finished state docs, historical missions, or real PO phase artifacts.

## Verification

```bash
python3 -m pip install -r requirements.txt
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
```
