# Factory Starter Kit

A generic, open-source starter kit for the Factory planning pipeline.

This is a pre-1.0 starter kit. It intentionally ships generic templates and placeholder project-state docs that must be adapted in the adopting repository. It is licensed under Apache-2.0.

This repo is the reusable framework layer:
- the Factory runner guide
- the stage/spec contracts
- the mission wrapper contract
- the templates
- starter lint scripts
- starter context docs

You drop it into your own repository and adapt the project-specific spine.

## Maturity

This is a pre-1.0 starter kit.

It intentionally ships generic templates and placeholder project-state docs that must be adapted in the adopting repository.

## Quick Start

First 30 seconds:
1. Copy this repository into your own repository as the starting framework layer.
2. Edit `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md` first.
3. Run `bash scripts/knowledge_lint.sh`.
4. If you will use Mission Mode, run `bash scripts/mission_lint.sh <MISSION_ID>`.

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
4. execution last

## What This Starter Kit Includes

```text
your-repo/
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── scripts/
│   ├── knowledge_lint.sh
│   └── mission_lint.sh
├── docs/
│   ├── PROJECT_STATE.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   ├── onboarding/
│   │   └── ONBOARDING_GUIDE.md
│   └── Factory/
│       ├── ORCHESTRATION.md
│       ├── MISSION_MODE.md
│       ├── SCRATCHPAD.md
│       ├── Spec/
│       │   ├── DEFINITIONS.md
│       │   ├── STAGE_CONTRACTS.md
│       │   ├── NAMING_CONVENTIONS.md
│       │   └── PURPLE_GATE_CHECKLIST.md
│       └── templates/
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

This starter kit intentionally does not ship product-specific run packs or finished project-specific state docs. It ships generic templates and placeholder state docs so adopters can adapt them in their own repository.

The root `CHANGELOG.md` tracks starter-kit releases. The `docs/CHANGELOG.md` file is the project changelog template adopters are expected to replace with their own project history.

## Setup

1. Copy or clone the starter kit into your repo.
2. Adapt `AGENTS.md` to your project.
3. Fill in `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md`.
4. Review `docs/Factory/ORCHESTRATION.md` and `docs/Factory/MISSION_MODE.md`.
5. Adapt `scripts/knowledge_lint.sh` and `scripts/mission_lint.sh` if your project uses different canonical docs or naming.
6. Run:

```bash
bash scripts/knowledge_lint.sh
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

You should usually keep unchanged:
- `docs/Factory/Spec/`
- `docs/Factory/templates/`
- `docs/Factory/MISSION_MODE.md`

You may lightly adapt:
- `docs/Factory/ORCHESTRATION.md`
- `docs/Factory/SCRATCHPAD.md`

## Minimal Run Loop

For a single sprint:
1. write a raw brief
2. run knowledge lint
3. initialize a Factory run
4. execute stages A → B → C → D → E → F → G → H → I → J → I2
5. review the pack
6. approve or reject execution

For a multi-sprint mission:
1. lock the mission unit list and checkpoint
2. keep `MISSION_MANIFEST.md` as the only authored mission ledger
3. run mission lint before advancing each already-authorized mission unit
4. update mission and project state docs in the same closure cycle

## What This Repo Should Not Become

- not a copy of another project's product docs
- not a dump of private run history
- not a codegen framework
- not a second source of truth for your project state

Keep it generic. Keep it reusable. Keep project-specific content in the adopting repo.

## License

This repository is licensed under Apache-2.0. See [LICENSE](LICENSE).
