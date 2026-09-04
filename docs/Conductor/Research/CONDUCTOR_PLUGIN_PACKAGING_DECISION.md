# Factory Plugin Packaging Decision

## Version
v1

## Change Log
- v1 (2026-07-24): Selected two generated platform packages from one authored source.

## Status
- Decision: APPROVED FOR IMPLEMENTATION
- Decision value: `generated_platform_packages`
- Run: `RUN_20260724_1448_factory_plugin`

## Decision
Maintain one authored Factory skill source and generate two platform packages:

- Authored source: `plugin-src/conductor/`
- Codex package: `plugins/conductor/`
- Claude package: `plugins/conductor-claude/`
- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude marketplace: `.claude-plugin/marketplace.json`

Both package manifests use plugin identifier `factory`. The package folders may differ because each marketplace owns its own source path.

## Why
- Vendor manifest and marketplace schemas differ.
- Claude's desired command `/conductor:doctor` uses skill name `doctor`.
- Codex's desired skill `$conductor-doctor` uses skill name and directory `conductor-doctor`.
- Agent Skills requires the Codex name to match its directory.
- Generating the two frontmatter/directory variants keeps one authored body while preserving the approved user experience.

## Generation Contract
- A standard-library build script reads the seven authored skill definitions.
- It validates the fixed semantic IDs: doctor, greenfield, brownfield, progress, run, validate, update.
- It writes both packages in deterministic sorted order.
- It fails on unknown mappings, duplicate names, unsafe paths, or invalid metadata.
- A second clean generation must produce no diff.
- Platform package files are generated; edits must occur in `plugin-src/conductor/`.

## Validation Commands
- Codex schema: `python3 <plugin-creator-skill-root>/scripts/validate_plugin.py plugins/conductor`
- Claude schema: `claude plugin validate plugins/conductor-claude --strict`
- Build regression: `python3 -m unittest tests.test_conductor_plugin_build -v`
- Live Codex: install from `.agents/plugins/marketplace.json` in the Codex app and start a new task.
- Live Claude: update Claude Code, run `claude --plugin-dir ./plugins/conductor-claude`, then invoke `/conductor:doctor`.

## Rejected Alternatives
- Two authored skill trees: rejected because drift is inevitable.
- One unchanged dual-manifest root: rejected because the approved Claude and Codex public skill names differ.
- Standalone `.claude/` plus repo `.agents/skills` only: rejected because it does not provide the requested installable team distribution.
