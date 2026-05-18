# PROJECT_STATE.md — Canonical Build State

> **Purpose:** Single source of truth for the current state of the build. Updated after every sprint.
>
> **Last updated:** 2026-05-18

---

## What Exists

- Factory v2 remains the canonical planning process.
- Factory v3 exists as a research-only documentation track under `docs/Factory/v3/`.
- A standalone, optional Factory v3 advisory lint prototype exists at `scripts/factory_v3_advisory_lint.py`.
- Advisory lint fixtures exist under `tests/fixtures/factory_v3_advisory_lint/` for clean, warning, and promotion-claim cases.

## What Does NOT Exist Yet

- Factory v3 is not promoted for release.
- Factory v3 advisory lint is not wired into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, mission cursor lint, merge preflight, or any required Factory v2 gate.
- Factory v3 does not implement runtime-kernel authority, proof, leases, sandboxing, policy, or production action mediation.

## How to Verify

```bash
# Run the knowledge lint preflight
bash scripts/knowledge_lint.sh

# Run the optional Factory v3 advisory lint prototype
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json

# Run deterministic advisory lint fixture checks
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json

# Run your test suite
# (add your project's test command here)
```
