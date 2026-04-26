# Factory Starter Kit

A generic, open-source starter kit for the latest Factory planning process.

Conventional sprint planning assumes humans will recover context, notice drift, and tighten weak contracts during execution. Agentic execution amplifies those gaps instead. The Factory is the planning and governance layer that forces explicit intent, explicit constraints, explicit verification, and explicit continuity before coding starts.

This is a pre-1.0 starter kit. It intentionally ships generic process docs, templates, and starter scripts that adopters must adapt to their own repository. It is licensed under Apache-2.0.

## What This Starter Kit Includes

The reusable framework layer:
- Factory runner guide and stage/spec contracts
- Mission Mode for bounded multi-sprint chains
- Context recall tooling and report templates
- Deterministic pack-lint validation after the final pack audit
- Optional Product Owner pre-Factory process
- Starter lint scripts
- Starter project-state placeholders

You drop it into your own repository and adapt the project-specific spine.

## Maturity

This is a pre-1.0 starter kit.

It is intentionally generic. It should contain the process layer, not your private run history or your product-specific docs.

## Quick Start

First 30 seconds:
1. Copy this repository into your own repository as the starting framework layer.
2. Edit `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md` first.
3. Run `bash scripts/knowledge_lint.sh`.
4. Build the continuity index with `./scripts/factoryctl context-index`.
5. If you will use Mission Mode, run `bash scripts/mission_lint.sh <MISSION_ID>`.

## What This Is

The Factory is a planning and governance pipeline for agentic development.

It does not write code by itself. It produces the sprint contract that should govern coding:
- locked intent
- explicit constraints
- risk analysis
- verification plan
- traceability
- execution envelope

The core operating order is:
1. intent first
2. constraints second
3. verification third
4. continuity recall before each gate that depends on prior decisions
5. execution last

## Process Layers

The public starter kit now models four generic layers:
1. Core Factory pipeline: `raw_brief.md -> A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`
2. Context recall layer: indexed recall reports before Stage A, mission checkpointing, and PO brief review
3. Product Owner lane (optional): Phase Brief -> Phase Intent -> PO sprint brief -> Brief Review PASS -> Factory
4. Mission Mode (optional): ordered multi-sprint execution under one consolidated checkpoint

See `docs/Factory/ARCHITECTURE.md` for the portable layer model: Factory Core, harness adapters, validators, extension packs, and project adapters.

## What This Starter Kit Includes

```text
your-repo/
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── scripts/
│   ├── factoryctl
│   ├── factory_context_index.py
│   ├── factory_pack_lint.py
│   ├── knowledge_lint.sh
│   └── mission_lint.sh
├── docs/
│   ├── PROJECT_STATE.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   ├── onboarding/
│   │   └── ONBOARDING_GUIDE.md
│   └── Factory/
│       ├── ARCHITECTURE.md
│       ├── ORCHESTRATION.md
│       ├── MISSION_MODE.md
│       ├── SCRATCHPAD.md
│       ├── ProductOwner/
│       │   ├── PO_PROCESS.md
│       │   ├── PO_ROLE_DEFINITION.md
│       │   ├── PHASE_INTENT_REVIEW_CHECKLIST.md
│       │   ├── BRIEF_REVIEW_CHECKLIST.md
│       │   └── templates/
│       │       ├── PHASE_BRIEF_TEMPLATE.md
│       │       ├── PHASE_INTENT_TEMPLATE.md
│       │       └── PHASE_STATE_TEMPLATE.md
│       ├── Spec/
│       │   ├── DEFINITIONS.md
│       │   ├── STAGE_CONTRACTS.md
│       │   ├── NAMING_CONVENTIONS.md
│       │   └── PURPLE_GATE_CHECKLIST.md
│       └── templates/
│           ├── CONTEXT_RECALL_REPORT_TEMPLATE.md
│           ├── EXECUTION_PROMPT_TEMPLATE.md
│           ├── HANDOFF_STAGE_TEMPLATE.md
│           ├── INTENT_LOCK_REPORT_TEMPLATE.md
│           ├── MISSION_CHECKPOINT_TEMPLATE.md
│           ├── MISSION_COMPLETION_REPORT_TEMPLATE.md
│           ├── MISSION_EXECUTION_PROMPT_TEMPLATE.md
│           ├── MISSION_MANIFEST_TEMPLATE.md
│           ├── PACK_AUDIT_REPORT_TEMPLATE.md
│           ├── PACK_CHECKLIST_TEMPLATE.md
│           ├── PACK_MANIFEST_TEMPLATE.md
│           ├── SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md
│           ├── SPRINT_ENVELOPE_TEMPLATE.md
│           └── TRACEABILITY_MATRIX_TEMPLATE.md
```

This starter kit intentionally does not ship product-specific run packs, finished state docs, historical missions, or real PO phase artifacts.

The root `CHANGELOG.md` tracks starter-kit releases. The `docs/CHANGELOG.md` file is a placeholder project changelog adopters are expected to replace with their own project history.

## Setup

1. Copy or clone the starter kit into your repo.
2. Adapt `AGENTS.md` to your project.
3. Fill in `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md`.
4. Review `docs/Factory/ORCHESTRATION.md` and `docs/Factory/MISSION_MODE.md`.
5. If you will use the optional PO lane, review `docs/Factory/ProductOwner/`.
6. Adapt `scripts/knowledge_lint.sh` and `scripts/mission_lint.sh` if your project uses different canonical docs or naming.
7. Run:

```bash
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
```

If you plan to use Mission Mode, also verify:

```bash
bash scripts/mission_lint.sh <MISSION_ID>
```

## Project-Specific Adaptation

You are expected to adapt:
- `AGENTS.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`
- `scripts/knowledge_lint.sh`
- `scripts/mission_lint.sh` if you use Mission Mode
- the default recall source patterns in `scripts/factory_context_index.py` if your repo uses materially different canonical paths

You should usually keep unchanged:
- `docs/Factory/Spec/`
- `docs/Factory/templates/`
- `docs/Factory/MISSION_MODE.md`
- `docs/Factory/ProductOwner/` unless your governance model differs

You may lightly adapt:
- `docs/Factory/ORCHESTRATION.md`
- `docs/Factory/SCRATCHPAD.md`

## Minimal Run Loops

For a single sprint:
1. write or receive `raw_brief.md`
2. run knowledge lint
3. refresh the continuity index
4. generate `CONTEXT_RECALL_REPORT.md`
5. initialize a Factory run
6. execute stages `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`
7. run `./scripts/factoryctl pack-lint --run <RUN_ID>`
8. review the pack
9. approve or reject execution

For a multi-sprint mission:
1. lock the mission unit list and checkpoint
2. keep `MISSION_MANIFEST.md` as the only authored mission ledger
3. refresh mission recall before checkpointing or authorizing the next unit
4. run mission lint before advancing each already-authorized mission unit
5. update mission and project state docs in the same closure cycle

For a PO-authored planning lane:
1. lock a Phase Intent
2. check sprint budget in `PHASE_STATE.md`
3. generate the brief-cycle recall artifact
4. run the brief review cycle
5. only then hand the passed brief into the Factory as `raw_brief.md`

## What This Repo Should Not Become

- not a copy of another project's product docs
- not a dump of private run history
- not a codegen framework
- not a second source of truth for your project state
- not a place where generic process docs silently fork from the tooling and lint contracts

Keep it generic. Keep it reusable. Keep project-specific content in the adopting repo.

## License

This repository is licensed under Apache-2.0. See [LICENSE](LICENSE).
