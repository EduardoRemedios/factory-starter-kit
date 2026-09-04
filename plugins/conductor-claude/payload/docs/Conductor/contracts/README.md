# Conductor contracts

JSON Schema 2020-12 definitions for every artifact the Conductor core validates. These are the hard layer: prose in AGENTS.md, skills, and guides explains them, but only these schemas plus `contract-lint` decide validity.

| Schema | Artifact | Written by | Validated at |
|---|---|---|---|
| `intent_pack.schema.json` | `runs/<RUN_ID>/intent_pack.json` | agent drafts, human locks | G1 |
| `countersign.schema.json` | `runs/<RUN_ID>/countersign/{INTENT_LOCK,EXECUTION_GO,COMPLETION}.json` | human only | G1, G2 entry, G3 |
| `verification_manifest_v2.schema.json` | `runs/<RUN_ID>/verification_manifest.yaml` | agent declares checks; runner writes `result` | G2 |
| `evidence_receipt.schema.json` | `runs/<RUN_ID>/receipts/<CHECK_ID>.json` | receipts runner only | G2, G3 |
| `statement_of_completion.schema.json` | `runs/<RUN_ID>/statement_of_completion.json` | agent drafts; lint derives state | G3 |
| `gap_request.schema.json` | `runs/<RUN_ID>/gap_requests/<GAP_ID>.json` | agent authors; human resolves | G3 → upstream lane |
| `project_config.schema.json` | `docs/Conductor/PROJECT_CONFIG.json` | maintainer | G1 |

The core is adapter-neutral. Adapter-specific settings live under `adapters.<name>` in the Project Config and are validated by that adapter's own schema in `docs/adapters/<name>/contracts/`, shipped with that adapter's plugin.

Conventions: `schema_version` is an integer on every document and is bumped only for breaking changes; ids match `^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$` (run ids in the wild are ~70 characters); digests are lowercase SHA-256 hex; paths are repository-relative with no `..` segments; timestamps are UTC ISO-8601 with a literal `Z`, enforced by pattern rather than by the optional `date-time` format checker.

Templates that validate against these schemas live in `../templates/` (`*.template.json`, `*_TEMPLATE_V2.yaml`). `tests/test_schemas.py` checks every schema against the metaschema, every template against its schema, and a set of negative fixtures that must be rejected.

Design rationale: `../DESIGN_PACK/03_CONTRACTS.md`.
