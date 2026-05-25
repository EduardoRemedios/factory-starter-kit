# PROJECT_STATE.md - Canonical Build State

> **Purpose:** Single source of truth for the current starter-kit state.
>
> **Last updated:** 2026-05-25

## What Exists

- Factory V2 remains the canonical planning process in this repository.
- Factory V3 content has moved to `https://github.com/EduardoRemedios/Factory_V3`.
- Mission Mode exists as an additive wrapper for ordered multi-sprint chains.
- Context recall, stage-lint, pack-lint, verification manifest, mission lint, mission cursor lint, task memory, Repo Cartographer, and Agent Loop Bridge helpers remain available.
- SIMPLE-CODE-GATE v2 remains the implementation guardrail for Factory-controlled code-changing work.
- Product Owner process docs and templates remain available under `docs/Factory/ProductOwner/`.

## Current Tracking Snapshot

- Current repository scope: Factory V2 and earlier starter-kit content.
- Factory V3 docs, scripts, fixtures, and run evidence are no longer maintained here.
- Latest structural change: V3 content was split into the dedicated `Factory_V3` repository.

## What Does NOT Exist Here

- Factory V3 docs, scripts, fixtures, or V3 run evidence.
- Product-specific run history for adopters.
- Project-specific test commands beyond starter-kit validation helpers.

## How To Verify

```bash
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
python3 scripts/agent_loop_bridge_validate.py tests/fixtures/agent_loop_bridge/valid_handoff.json --json
```
