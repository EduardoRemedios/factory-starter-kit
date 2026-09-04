# Install Conductor

One command per harness. No clone, no local marketplace path, no preflight to run yourself; the maintainer ran the read-only rollout preflight before publishing.

## Claude Code CLI

```bash
claude plugin marketplace add EduardoRemedios/factory-starter-kit
claude plugin install conductor@factory-starter-kit
```

If your repository already registers the marketplace in `.claude/settings.json` (`extraKnownMarketplaces` and `enabledPlugins`), Claude Code shows the plugin on open and the install line is the only step.

Then start Claude Code inside the repository and run `/conductor:doctor`. It tells you the one next legal action: `/conductor:greenfield` for an empty directory, `/conductor:brownfield` for an existing repository.

## Codex desktop app

The repository ships a marketplace file at `.agents/plugins/marketplace.json`. Open the Plugins Directory, select the `factory-starter-kit` source, install `conductor`, and start a new task so the skills load. The commands are `$conductor-doctor`, `$conductor-greenfield`, `$conductor-brownfield`, `$conductor-run`, `$conductor-validate`, `$conductor-progress`, `$conductor-update`.

## Cursor

Nothing to install. Cursor reads `AGENTS.md` at the repository root, which carries the Conductor managed block once the repository is adopted. Run the deterministic commands from the terminal (`./scripts/conductorctl ...`). Cursor Team Rules apply above project files; make sure none of them contradicts the managed block.

## Adopting a repository

Every setup command previews first and applies only when you quote the exact full plan ID it printed. Adoption writes only Conductor-owned paths. An existing `AGENTS.md` is never overwritten: the Conductor managed block is inserted after your first heading and everything else is preserved byte for byte.

After adoption: `/conductor:doctor`, `/conductor:validate`, `/conductor:progress`. Progress reports `READY_TO_INITIALIZE` until the first run exists.

## Requirements

- macOS (pilot surface), Git, Python 3.11 or newer.
- `python3 -m pip install -r requirements.txt` inside the adopted repository (installs `pyyaml` and `jsonschema`, which `conductorctl` needs).

## Rollback

`/conductor:update` previews and applies updates; `docs/onboarding/CONDUCTOR_PLUGIN_ROLLBACK.md` in the starter kit describes exact rollback from the transaction receipt.
