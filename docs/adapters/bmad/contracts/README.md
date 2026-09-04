# BMAD adapter contracts

Adapter-specific schemas. They are shipped with the `conductor-bmad` plugin, not with the core `conductor` plugin, which must stay domain-neutral.

| Schema | Artifact | Validated at |
|---|---|---|
| `bmad_adapter_config.schema.json` | `PROJECT_CONFIG.json` → `adapters.bmad` | G1 (core contract-lint delegates adapter blocks to adapter schemas) |
| `lane_policy.schema.json` | `docs/adapters/bmad/lane_policy.json` | BMAD hook decision, audit, policy lint |

Templates: `../templates/`. Tests: `tests/test_schemas.py`. Design rationale: `docs/Conductor/DESIGN_PACK/04_LANE_POLICY.md`.
