# Factory Plugin Quick Start

Use this path for the initial macOS pilot. The plugin makes Factory installable and discoverable; it does not bypass repository review, Factory validators, or human Go.

## Pilot Requirements

- macOS
- Git
- Python 3.11 or newer
- an absent or empty project path, or a Git repository you are allowed to change
- Codex app/Desktop, or a Claude Code build whose `claude plugin` command
  supports marketplace installation and strict validation (pilot-verified on
  Claude Code 2.1.218)

Windows, Linux, and Codex CLI are not part of the initial supported pilot.

## Codex App

1. Open the Factory plugin from the repo marketplace link supplied by the plugin owner.
2. Install `factory`.
3. Start a new Codex task so the new skills are loaded.
4. At the intended project path, invoke `$factory-doctor`.
5. For an absent or empty project path, invoke `$factory-greenfield`.
6. For an existing repository, invoke `$factory-brownfield`.
7. Review the exact per-file plan. Apply only after you approve its plan ID.
8. Invoke `$factory-validate`, then `$factory-progress`.

If a working Codex CLI is available, the equivalent non-default local-marketplace setup is:

```bash
codex plugin marketplace add <factory-starter-kit-root>
codex plugin add factory@factory-starter-kit
```

The initial pilot is app-first. A broken or unverified Codex CLI is not a reason to weaken the app flow.

## Claude Code

First update and check the supported version:

```bash
claude update
claude --version
claude plugin --help
```

If more than one `claude` executable is installed, use the same supported
executable for version checks, validation, installation, and the pilot.

Then validate and install the local marketplace:

```bash
cd <factory-starter-kit-root>
claude plugin validate --strict plugins/factory-claude
claude plugin validate --strict .claude-plugin/marketplace.json
claude plugin marketplace add <factory-starter-kit-root>
claude plugin install factory@factory-starter-kit
```

Restart Claude Code, open the project repository, and invoke:

```text
/factory:doctor
/factory:greenfield
```

Use `/factory:brownfield` instead of greenfield for an existing project.

Greenfield preview is read-only. After exact plan approval, it creates the target
directory when needed, initializes Git, installs Factory, records the transaction,
and validates the result. If setup fails, it removes Factory-created Git only when
the recorded Git digest is unchanged.

Claude setup previews a one-line `CLAUDE.md` containing `@AGENTS.md`. If `CLAUDE.md` already contains other instructions, setup halts for owner review.

## What Happens Before Any Write

Greenfield, brownfield, and update first return:

- the resolved Git worktree root
- installed and target versions
- an allowed-path list
- an ownership class for every file
- `create`, `no_change`, `preserve`, `modify`, `delete`, or `conflict`
- a deterministic plan ID
- a reason code and next legal action

No apply occurs until you explicitly approve the exact full current plan ID. A
generic response such as `approve`, `apply`, or `approve and apply` is
insufficient. A changed repository invalidates the plan.

## First Factory Run

After setup and validation:

1. Invoke doctor and resolve any blocker.
2. Run Core knowledge lint. If the project declares
   `docs/Factory/PROJECT_PREFLIGHT.json`, run the fixed project preflight next.
3. Refresh context recall, then invoke progress.
4. Invoke `$factory-run` in Codex or `/factory:run` in Claude.
5. Keep the first run `PLANNING_ONLY` unless the raw brief explicitly authorizes `EXECUTION_ENABLED`.
6. Stop after I2 and `pack-lint` for human review.
7. Implementation requires separate explicit human Go.
8. After approved execution, retain evidence for every enabled verification
   check, author a closeout draft from
   `docs/Factory/templates/EXECUTION_CLOSEOUT_TEMPLATE.json`, and record it with:

```bash
./scripts/factoryctl execution-closeout --run <RUN_ID> --input <DRAFT.json> --json
```

9. Invoke progress explicitly for that run and once with default selection.
   `REVIEW_READY` means maintainer review only; it is not release permission.

The selected session model serves Red, Blue, and Purple roles by default. Separate role-specific model routing is optional, not required.

## Recovery

Do not retry blindly after a blocked result. Use the reason code and the [troubleshooting guide](FACTORY_PLUGIN_TROUBLESHOOTING.md). For update recovery, use the [rollback guide](FACTORY_PLUGIN_ROLLBACK.md).
