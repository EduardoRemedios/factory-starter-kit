# Factory Plugin Reference

Start with the [Factory Plugin Quick Start](CONDUCTOR_PLUGIN_QUICK_START.md), then
use this reference for exact cross-harness behavior and evidence rules.

Codex uses `$factory-<name>`. Claude uses `/conductor:<name>`. Invocation syntax differs; Factory semantics and gates do not.

| Journey | Codex | Claude | Repository writes |
|---|---|---|---|
| Diagnosis | `$conductor-doctor` | `/conductor:doctor` | Never |
| New repository setup | `$conductor-greenfield` | `/conductor:greenfield` | Preview first; exact-plan approval required |
| Existing repository setup | `$conductor-brownfield` | `/conductor:brownfield` | Preview first; exact-plan approval required |
| Run state | `$conductor-progress` | `/conductor:progress` | Never |
| Continue Factory | `$conductor-run` | `/conductor:run` | Only the next legal Factory action |
| Deterministic checks | `$conductor-validate` | `/conductor:validate` | Validator-defined evidence only |
| Update or rollback | `$conductor-update` | `/conductor:update` | Separate preview and approval for update or rollback |

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
5. after those checks, any `EXECUTION_CLOSEOUT.json` is revalidated against its
   exact identities, pins, enabled checks and retained evidence digests

Closeout absence preserves historical behavior. Presence opts into strict
`conductor.execution-closeout.v1`; an invalid record blocks and cannot fall back.
Valid outcomes are `REVIEW_READY`, `NO_GO`, and `BLOCKED`. None grants merge,
tag, publication, adapter, phase, or mission authority.

Progress is read-only.

## Stage A Project Preflight

Projects may opt in with `docs/Conductor/PROJECT_PREFLIGHT.json`. When declared, the
fixed `scripts/conductor_project_preflight --run RUN_ID --json` command runs after
Core knowledge lint and before context recall. Missing, malformed, timed-out,
oversized, non-zero, or failing results halt Stage A. Undeclared projects retain
the prior Core flow.

## Ownership

- `release-owned`: Factory Core content that may update only when it still matches the installation receipt
- `project-owned`: seeded only when absent and preserved after installation
- `generated/pinned`: lifecycle or platform-adapter files such as the receipt, rollback evidence, and Claude bridge

Generated lifecycle state is stored at `docs/Conductor/installation/INSTALLATION_STATE.json`. Durable transaction and recovery evidence is stored under `docs/Conductor/installation/receipts/`.

## Public Surface

The initial release intentionally exposes seven journeys. Internal Factory roles, stage contracts, validation commands, and artifact names remain in Factory Core. The plugin does not recreate GSD's full command catalogue and does not add automatic model fan-out.
