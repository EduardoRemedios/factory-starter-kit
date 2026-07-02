# PROJECT_STATE.md - Canonical Build State

> **Purpose:** Single source of truth for the current starter-kit state.
>
> **Last updated:** 2026-07-02

## What Exists

- Factory V2 remains the canonical planning process in this repository.
- Mission Mode exists as an additive wrapper for ordered multi-sprint chains.
- Context recall, stage-lint, pack-lint, verification manifest, mission lint, mission cursor lint, task memory, Repo Cartographer, and Agent Loop Bridge helpers remain available.
- SIMPLE-CODE-GATE v2 remains the implementation guardrail for Factory-controlled code-changing work.
- Merge handoff discipline now separates `REVIEW_READY` from `MERGE_READY` repository handoffs, with final sync window guidance in `docs/Factory/MERGE_PROTOCOL.md`.
- Product Owner process docs and templates remain available under `docs/Factory/ProductOwner/`.
- Non-technical onboarding now exists at `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` for first-time local setup with Cursor, Claude, or Codex.
- Kilo Code CLI stage routing now exists as an optional harness adapter with `./scripts/factoryctl kilo-stage`.
- Stage A context recall now has a formal direct-source repair path for generated `WEAK` reports when unresolved refs are concrete local sources that can be read and summarized directly.

## Current Tracking Snapshot

- Current repository scope: Factory V2 and earlier starter-kit content.
- Latest structural change: direct-source repair was added for locally verifiable Stage A context recall gaps without weakening the raw `WEAK` halt.

## What Does NOT Exist Here

- Product-specific run history for adopters.
- Project-specific test commands beyond starter-kit validation helpers.

## How To Verify

```bash
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
./scripts/factoryctl kilo-stage --help
python3 -m unittest tests.test_context_recall_repair
python3 scripts/agent_loop_bridge_validate.py tests/fixtures/agent_loop_bridge/valid_handoff.json --json
```
