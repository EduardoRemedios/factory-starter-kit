# Factory BMAD Compatibility Policy

Use this policy before each Claude Code CLI pilot and before any broader
rollout.

## Pinned Surfaces

- Factory: `0.2.5`
- Factory-BMAD: `0.2.5`
- BMAD installer: `bmad-method@6.10.0`
- BMAD modules: Core and BMM only
- Claude surface: Claude Code CLI local macOS session
- Hook interpreter: `python3` resolving to Python 3.11 or newer

Claude Code may be newer than the last verified build, but a newer build is a
compatibility event, not an assumption. Run the rollout preflight and at least
one maintainer smoke before putting a team on it.

## Required Checks

Before a first-team pilot:

```bash
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
```

Then run the normal package and policy checks from the marketplace root:

```bash
./scripts/factory-python -m unittest tests.test_factory_bmad_cli_rollout -v
./scripts/factory-python -m unittest tests.test_factory_bmad_plugin_build -v
./scripts/factory-python -m unittest tests.test_factory_bmad_enforcement -v
./scripts/factory-python scripts/build_factory_bmad_plugins.py --check
```

Run authenticated live lanes only as a maintainer release qualification activity,
not as an adopter setup step.

## Compatibility Events

Requalify before continuing if any of these changes:

- Claude Code major or minor version prefix
- Claude plugin marketplace behavior
- Claude hook event schema or hook command execution environment
- `python3` PATH or version on managed Macs
- Node/npm/npx availability
- BMAD package version, module names, skill names, or manifest shape
- Factory or Factory-BMAD package version/dependency declaration
- Claude plugin cache behavior or any stale `factory-starter-kit` cache finding

## Unsupported Until Proved

- Claude Desktop Code tab
- Claude Desktop cloud sessions
- Claude Desktop Cowork
- Windows, Linux, and WSL
- BMAD loop module
- TEA as a write-capable downstream authority

These surfaces can become supported only after a separate validation lane and
explicit documentation update.
