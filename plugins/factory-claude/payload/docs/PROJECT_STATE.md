# PROJECT_STATE.md - Canonical Build State

> **Purpose:** Single source of truth for the current starter-kit state.
>
> **Last updated:** 2026-08-10

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
- Factory plugin technical RC `0.2.0` has one authored source that generates Codex and Claude Code packages with Doctor, Greenfield, Brownfield, Progress, Run, Validate, and Update entry points.
- Greenfield setup now supports an absent or empty target through an exact root/Git/payload/metadata/validation transaction with fail-closed Git ownership recovery.
- Greenfield CLI root selection now defaults only Greenfield to the invocation
  current directory; Doctor and every established-project command retain Git-root
  discovery, and explicit absent or spaced targets remain preview-only.
- Claude Greenfield now tolerates only the exact harness-created
  `.claude/settings.local.json` shape in an otherwise new target. Its path,
  bytes, modes, types, and directory entries are plan-bound read-only evidence,
  excluded from Factory writes and management, and preserved through lifecycle recovery.
- Promoted upstream Markdown is indexed as generic evidence, while project-specific Stage A preflight is optional, schema-locked, bounded, and ordered after Core knowledge lint and before context recall.
- Codex app loading, Brownfield adoption, Greenfield setup, validation, update, and exact rollback restoration have passed pre-pilot verification.
- Project-specific Factory installation state is excluded from distributable plugin payloads and covered by a regression test.
- Execution-enabled runs now close through the schema-locked, non-authorizing
  `factory.execution-closeout.v1` record; progress revalidates its identities,
  pins, complete verification coverage, retained evidence, and digests on every read.
- Execution-closeout and project-preflight evidence paths now reject symlinks in
  every run-root ancestor before external reads or writes; focused regression
  covers `docs`, `docs/Factory`, and `docs/Factory/runs` with no-damage assertions.

## Current Tracking Snapshot

- Current repository scope: Factory V2, starter-kit content, and the dual-platform Factory plugin release candidate.
- Latest verified milestone: `SPRINT_20260810_002` repaired the Claude-created
  local-settings false Brownfield classification with exact-shape, ownership,
  stale-before-Git, apply, recovery, rollback, and cross-runtime proof.
- Current release state: corrected technical `REVIEW_READY`; the maintainer
  Claude Code CLI journey must be rerun from the existing harness-initialized
  directory. The independent first-time-Factory-user pilot,
  merge/tag/publication decisions, and Product Owner sign-off remain pending.

## What Does NOT Exist Here

- Product-specific run history for adopters.
- Project-specific test commands beyond starter-kit validation helpers.

## How To Verify

```bash
bash scripts/knowledge_lint.sh
./scripts/factoryctl context-index
./scripts/factoryctl kilo-stage --help
python3 -m unittest tests.test_context_recall_repair
python3 -m unittest discover -s tests -v
python3 scripts/build_factory_plugins.py --check
python3 scripts/agent_loop_bridge_validate.py tests/fixtures/agent_loop_bridge/valid_handoff.json --json
```
