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
- Optional machine-readable verification manifests for execution-enabled and Mission Mode runs
- SIMPLE-CODE-GATE v2 mandatory guardrail for small, direct, behavior-preserving implementation across Factory v2 and v3
- Optional Mission Cursor continuity guard for long Codex/agent sessions
- Tool-agnostic merge authorization protocol guidance
- Optional task-memory runbook helper through `factoryctl`
- Optional repo cartographer advisory scan
- Generic review-only Agent Loop Bridge harness pattern
- Factory v3 external-kernel boundary crosswalk for repos that also use a lower-level autonomy governance kernel
- Harness adapter guidance for Codex and other AI coding tools
- Optional Product Owner pre-Factory process
- Factory v3 optional `V3-OP-001` operational profile, user guide, starter templates, full-vision roadmap, and research/evidence docs under `docs/Factory/v3/`
- Starter lint scripts
- Starter project-state placeholders

You drop it into your own repository and adapt the project-specific spine.

## Maturity

This is a pre-1.0 starter kit.

It is intentionally generic. It should contain the process layer, not your private run history or your product-specific docs.

## Factory Version Posture

This repository currently ships the Factory v2 operating core:
- the `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2` planning pipeline
- Mission Mode as an additive wrapper for bounded multi-sprint chains
- deterministic stage-lint, pack-lint, context recall, verification manifest, and merge authorization guidance
- optional support helpers such as task memory, Repo Cartographer, Mission Cursor continuity, and Agent Loop Bridge

The repository also includes Factory v3. The first narrow profile, `V3-OP-001 Bounded Code Change`, is approved for optional operational use. It does not replace the v2 pipeline, make V3 the default mode, or wire V3 checks into required gates. V2 remains supported and available as fallback.

In short:
- Factory v2 remains the default and fallback process in this starter kit.
- Factory v3 `V3-OP-001` is approved for optional bounded-code-change use.
- Recent updates generalize lessons from downstream Factory usage back into the starter kit.
- Factory v3 operating guidance lives in `docs/Factory/v3/USER_GUIDE.md`, with release approval at `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.
- Factory v3 is compatible with external governance kernels but does not require one.
- No V3 profile beyond `V3-OP-001` is approved. Broader V3 promotion still requires evidence, human approval, and Factory governance.

## Quick Start

First 30 seconds:
1. Copy this repository into your own repository as the starting framework layer.
2. Edit `AGENTS.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md` first.
3. Install the script dependency with `python3 -m pip install -r requirements.txt`.
4. Run `bash scripts/knowledge_lint.sh`.
5. Build the continuity index with `./scripts/factoryctl context-index`.
6. Optional: initialize task memory with `./scripts/factoryctl memory-init`.
7. Optional: run an advisory repo scan with `./scripts/cartographer`.
8. If you will use Mission Mode, run `bash scripts/mission_lint.sh <MISSION_ID>`.
9. If you will use Mission Cursor continuity, run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before resuming from the cursor.

Dependency command:

```bash
python3 -m pip install -r requirements.txt
```

## What This Is

The Factory is a planning and governance pipeline for agentic development.

It does not write code by itself. It produces the sprint contract that should govern coding:
- locked intent
- explicit constraints
- risk analysis
- verification plan
- optional verification manifest for runnable checks
- traceability
- execution envelope

The core operating order is:
1. intent first
2. constraints second
3. verification third
4. executable verification inventory when the run will execute code
5. continuity recall before each gate that depends on prior decisions
6. execution last

## Process Layers

The public starter kit now models ten generic layers:
1. Core Factory pipeline: `raw_brief.md -> A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`
2. Context recall layer: indexed recall reports before Stage A, mission checkpointing, and PO brief review
3. Product Owner lane (optional): Phase Brief -> Phase Intent -> PO sprint brief -> Brief Review PASS -> Factory
4. Mission Mode (optional): ordered multi-sprint execution under one consolidated checkpoint
5. Verification manifest (optional): compact runnable check inventory for execution-enabled and Mission Mode units
6. Mission Cursor continuity (optional): derived resume cursor plus lint gate for long-running agent sessions
7. Task memory (optional): local runbook suggestion and outcome journal for repeat work
8. Repo Cartographer (optional): advisory snapshot reports for repository state, drift, verification, and traceability
9. Agent Loop Bridge (optional): review-only structured handoffs between agent lanes
10. External governance-kernel boundary (optional): SDLC mission governance for repos with separate governance kernels, without duplicating runtime enforcement

See `docs/Factory/ARCHITECTURE.md` for the portable layer model: Factory Core, harness adapters, validators, extension packs, and project adapters.

## What This Starter Kit Includes

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
│       ├── README.md
│       └── run.py
├── docs/
│   ├── PROJECT_STATE.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   ├── onboarding/
│   │   └── ONBOARDING_GUIDE.md
│   └── Factory/
│       ├── ARCHITECTURE.md
│       ├── EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY.md
│       ├── MERGE_PROTOCOL.md
│       ├── ORCHESTRATION.md
│       ├── MISSION_MODE.md
│       ├── SCRATCHPAD.md
│       ├── TASK_MEMORY.md
│       ├── Harnesses/
│       │   ├── AGENT_LOOP_BRIDGE.md
│       │   ├── AGENT_LOOP_BRIDGE_MANUAL_RUNBOOK.md
│       │   ├── CODEX.md
│       │   └── README.md
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
│       ├── templates/
│           ├── CONTEXT_RECALL_REPORT_TEMPLATE.md
│           ├── EXECUTION_PROMPT_TEMPLATE.md
│           ├── HANDOFF_STAGE_TEMPLATE.md
│           ├── INTENT_LOCK_REPORT_TEMPLATE.md
│           ├── MISSION_CHECKPOINT_TEMPLATE.md
│           ├── MISSION_COMPLETION_REPORT_TEMPLATE.md
│           ├── MISSION_CURSOR_TEMPLATE.json
│           ├── MISSION_EXECUTION_PROMPT_TEMPLATE.md
│           ├── MISSION_MANIFEST_TEMPLATE.md
│           ├── PACK_AUDIT_REPORT_TEMPLATE.md
│           ├── PACK_CHECKLIST_TEMPLATE.md
│           ├── PACK_MANIFEST_TEMPLATE.md
│           ├── SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md
│           ├── SPRINT_ENVELOPE_TEMPLATE.md
│           ├── TRACEABILITY_MATRIX_TEMPLATE.md
│       │   └── VERIFICATION_MANIFEST_TEMPLATE.yaml
│       └── v3/
│           ├── README.md
│           ├── VISION.md
│           ├── ROADMAP_TO_FULL_VISION.md
│           ├── ROADMAP_PREMORTEM.md
│           ├── PHASE1_TRIAL_PLAN.md
│           ├── USER_GUIDE.md
│           ├── OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md
│           ├── OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md
│           ├── STRATEGY.md
│           ├── NON_GOALS_AND_BOUNDARIES.md
│           ├── CONCEPT_CANDIDATES.md
│           ├── SHADOW_SCHEMA_CANDIDATES.md
│           ├── ADVISORY_VALIDATOR_PLAN.md
│           ├── PILOT_PROFILE_PLAN.md
│           ├── PROMOTION_CRITERIA.md
│           └── templates/
│               ├── V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md
│               ├── V3_MISSION_ENVELOPE_TEMPLATE.md
│               ├── V3_CLOSEOUT_TEMPLATE.md
│               ├── V3_FALLBACK_REVIEW_TEMPLATE.md
│               └── V3_SIMPLE_CODE_GATE_REVIEW_TEMPLATE.md
│           └── trials/
│               └── TRIAL_INDEX.md
```

This starter kit intentionally does not ship product-specific run packs, finished state docs, historical missions, or real PO phase artifacts.

The root `CHANGELOG.md` tracks starter-kit releases. The `docs/CHANGELOG.md` file is a placeholder project changelog adopters are expected to replace with their own project history.

## Setup

1. Copy or clone the starter kit into your repo.
2. Adapt `AGENTS.md` to your project.
3. Fill in `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md`.
4. Review `docs/Factory/ORCHESTRATION.md` and `docs/Factory/MISSION_MODE.md`.
5. If your repository uses a separate autonomy governance kernel, review `docs/Factory/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY.md`.
6. Review `docs/Factory/Harnesses/` for AI coding tool guidance.
7. If you will use the optional PO lane, review `docs/Factory/ProductOwner/`.
8. Adapt `scripts/knowledge_lint.sh`, `scripts/mission_lint.sh`, and `scripts/mission_cursor_lint.sh` if your project uses different canonical docs or naming.
9. Run:

```bash
python3 -m pip install -r requirements.txt
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
```

If you plan to use Mission Mode, also verify:

```bash
bash scripts/mission_lint.sh <MISSION_ID>
```

If you plan to use Mission Cursor continuity, verify before every cursor-based resume:

```bash
bash scripts/mission_cursor_lint.sh <MISSION_ID>
```

## Project-Specific Adaptation

You are expected to adapt:
- `AGENTS.md`
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`
- `scripts/knowledge_lint.sh`
- `scripts/mission_lint.sh` if you use Mission Mode
- `scripts/mission_cursor_lint.sh` if you use Mission Cursor continuity with a customized mission table
- the default recall source patterns in `scripts/factory_context_index.py` if your repo uses materially different canonical paths

You should usually keep unchanged:
- `docs/Factory/Spec/`
- `docs/Factory/templates/`
- `docs/Factory/Harnesses/` unless your AI tool stack differs materially
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
7. for execution-enabled or mission units, create `pack/verification_manifest.yaml` when runnable checks exist
8. run `./scripts/factoryctl pack-lint --run <RUN_ID>`
9. review the pack
10. approve or reject execution

For a multi-sprint mission:
1. lock the mission unit list and checkpoint
2. keep `MISSION_MANIFEST.md` as the only authored mission ledger
3. refresh mission recall before checkpointing or authorizing the next unit
4. run mission lint before advancing each already-authorized mission unit
5. run mission cursor lint before resuming from `MISSION_CURSOR.json`, if using the optional cursor adapter
6. update mission and project state docs in the same closure cycle

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
- not a second autonomy governance kernel when your repo already has one
- not a place where generic process docs silently fork from the tooling and lint contracts

Keep it generic. Keep it reusable. Keep project-specific content in the adopting repo.

## License

This repository is licensed under Apache-2.0. See [LICENSE](LICENSE).
