# Factory Plugin Reference

Codex uses `$factory-<name>`. Claude uses `/factory:<name>`. Invocation syntax differs; Factory semantics and gates do not.

| Journey | Codex | Claude | Repository writes |
|---|---|---|---|
| Diagnosis | `$factory-doctor` | `/factory:doctor` | Never |
| New repository setup | `$factory-greenfield` | `/factory:greenfield` | Preview first; exact-plan approval required |
| Existing repository setup | `$factory-brownfield` | `/factory:brownfield` | Preview first; exact-plan approval required |
| Run state | `$factory-progress` | `/factory:progress` | Never |
| Continue Factory | `$factory-run` | `/factory:run` | Only the next legal Factory action |
| Deterministic checks | `$factory-validate` | `/factory:validate` | Validator-defined evidence only |
| Update or rollback | `$factory-update` | `/factory:update` | Separate preview and approval for update or rollback |

Greenfield supports an absent path, an empty directory, or a repository containing
only `.git`. Its approved transaction orders root creation, Git initialization,
payload, lifecycle metadata, receipt, and validation. Recovery never removes
Factory-created `.git` after its recorded digest changes.

## Doctor Output

Doctor reports:

- harness and plugin version
- operating system, Python version, and repository root
- Factory project compatibility
- missing prerequisites
- repository/plugin skill coexistence
- selected-model policy for Red, Blue, and Purple
- state, reason code, blocker, and next legal action

Doctor is read-only.

## Progress Evidence Order

Progress uses disk evidence and fails closed:

1. missing output claimed by a passing handoff is a contradiction
2. unrepaired weak recall blocks
3. I2 and a passing Purple audit do not imply execution authorization
4. `EXECUTION_ENABLED` still requires explicit human Go

Progress is read-only.

## Stage A Project Preflight

Projects may opt in with `docs/Factory/PROJECT_PREFLIGHT.json`. When declared, the
fixed `scripts/factory_project_preflight --run RUN_ID --json` command runs after
Core knowledge lint and before context recall. Missing, malformed, timed-out,
oversized, non-zero, or failing results halt Stage A. Undeclared projects retain
the prior Core flow.

## Ownership

- `release-owned`: Factory Core content that may update only when it still matches the installation receipt
- `project-owned`: seeded only when absent and preserved after installation
- `generated/pinned`: lifecycle or platform-adapter files such as the receipt, rollback evidence, and Claude bridge

Generated lifecycle state is stored at `docs/Factory/installation/INSTALLATION_STATE.json`. Durable transaction and recovery evidence is stored under `docs/Factory/installation/receipts/`.

## Public Surface

The initial release intentionally exposes seven journeys. Internal Factory roles, stage contracts, validation commands, and artifact names remain in Factory Core. The plugin does not recreate GSD's full command catalogue and does not add automatic model fan-out.
