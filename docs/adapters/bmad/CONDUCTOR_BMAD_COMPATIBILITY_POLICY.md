# Factory BMAD Compatibility Policy

Use this policy before each Claude Code CLI pilot and before any broader
rollout.

## Pinned Surfaces

- Factory (plugin id `conductor`): local `0.3.6` candidate; published baseline `0.3.5`
- Factory-BMAD (plugin id `conductor-bmad`): local `0.3.6` candidate with `~0.3.6` dependency
- BMAD installer: `bmad-method@6.10.0`
- BMAD compatibility: exact Core/BMM `6.10.0` and candidate `6.12.1-next.0` profiles; no floating versions
- Optional TEA: legacy `v1.21.1` on the legacy profile; new `main` label only with commit `7ba2130193c473b53d2e323b4da9a80697eef88e` and matching public dependency bytes
- New authoring profile requires Python 3.11+, complete supporting files, safe declared roots and checked effective configuration
- Claude surface: Claude Code CLI local macOS session
- Hook interpreter: `python3` resolving to Python 3.11 or newer

Claude Code may be newer than the last verified build, but a newer build is a
compatibility event, not an assumption. Run the rollout preflight and at least
one maintainer smoke before putting a team on it.

## Required Checks

Before a first-team pilot:

```bash
./scripts/conductor-python scripts/verify_conductor_bmad_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
```

Then run the normal package and policy checks from the marketplace root:

```bash
./scripts/conductor-python -m unittest tests.test_conductor_bmad_cli_rollout -v
./scripts/conductor-python -m unittest tests.test_conductor_bmad_plugin_build -v
./scripts/conductor-python -m unittest tests.test_conductor_bmad_enforcement -v
./scripts/conductor-python scripts/build_conductor_bmad_plugins.py --check
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

## New-version qualification boundary

The 0.3.6 candidate adds version-specific inventories, checked internal skill aliases and Spec/companion closure. The legacy bootstrap pin is unchanged. Deterministic tests, guarded MCP protocol checks and authenticated Claude hooks are separate evidence lanes; none substitutes for another. See [the executable handoff](BMAD_6121_HANDOFF.md). No current publication, installation, native Codex or desktop activation claim is implied.
