---
name: seed-contracts
description: Preview or seed the inert adapter contracts (adapter config schema, lane policy schema and JSON, authority policy) so contract-lint can validate a declared BMAD adapter before intake.
---

# Conductor BMAD Seed Contracts

Preview only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . seed-contracts
```

Show every destination, action, digest, and plan ID. Apply only after exact
`--approve-plan` approval. The seed writes only inert files under
`docs/adapters/bmad/`: `contracts/bmad_adapter_config.schema.json`,
`contracts/lane_policy.schema.json`, `lane_policy.json`, and `BMAD_POLICY.md`.
It does not require the capability audit to be READY, because these files carry
no authority and change nothing about enforcement: they let `conductorctl
contract-lint intent` validate `PROJECT_CONFIG.json -> adapters.bmad` (for
example a declared non-root BMAD installation) before intake is possible.

Existing different files are conflicts requiring human reconciliation. Run this
right after declaring `adapters.bmad` in the Project Config, or when G1 lint
reports `CONDUCTOR_CONTRACT_ADAPTER_SCHEMA_MISSING: adapters.bmad`.
