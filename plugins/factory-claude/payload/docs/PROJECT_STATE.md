# PROJECT_STATE.md - Canonical Build State

> **Purpose:** Single source of truth for the current starter-kit state.
>
> **Last updated:** 2026-08-13

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
- Factory plugin `0.1.0` now has one authored source that generates Codex and Claude Code packages with Doctor, Greenfield, Brownfield, Progress, Run, Validate, and Update entry points.
- Codex app loading, Brownfield adoption, Greenfield setup, validation, update, and exact rollback restoration have passed pre-pilot verification.
- Claude Code CLI and Desktop Doctor, Brownfield, Progress, and Validate journeys have passed live cross-surface verification.
- Public golden fixtures live under `tests/plugin_fixtures/`; private run and pilot evidence are not part of the public release package.
- Project-specific Factory installation state is excluded from distributable plugin payloads and covered by a regression test.
- The public README now provides plugin-first installation for the ChatGPT/Codex desktop app, Claude Code desktop, and Claude Code CLI, plus an evidence-based developer FAQ.
- Factory now preserves I2 audited mode as immutable pack evidence and validates any later cross-mode execution activation through a separate, exact manifest-and-audit digest-bound authorization record.
- Factory now treats `verification_manifest.yaml` as executable verification authority, requires exact VM-ID agreement with plan and traceability, and binds no-touch checks to SHA-pinned preimage manifests.
- Proxy-review hardening now makes absent audited mode fail closed, reads VM coverage from the canonical traceability column, rejects symlinked preimage manifests, and validates optional execution ordering.

## Current Tracking Snapshot

- Current repository scope: Factory V2, starter-kit content, and the dual-platform Factory plugin release candidate.
- Latest verified milestone: activation and verification-contract repairs, proxy-review hardening, protected-baseline checks, all 83 repository tests, knowledge lint, and deterministic package checks pass.
- Current release state: the privacy-safe release candidate is prepared for `main`; the independent two-user pilot, stable release tag, and Product Owner sign-off remain pending.

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
