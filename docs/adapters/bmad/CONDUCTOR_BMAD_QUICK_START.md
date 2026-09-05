# Factory BMAD Companion — Claude Code Quick Start

Use Claude Code CLI. This technical pilot does not claim Claude Desktop support.
Keep Factory and the companion in the same Factory Starter Kit marketplace so
the versioned Factory dependency can resolve.

This page is written for self-service setup. You can copy and paste the command
blocks into the macOS Terminal. A "script" is just a command you run from
Terminal.

See `CONDUCTOR_BMAD_CLI_ROLLOUT_PLAYBOOK.md`,
`CONDUCTOR_BMAD_FIRST_TESTER_HANDOFF.md`,
`CONDUCTOR_BMAD_COMPATIBILITY_POLICY.md`, and
`CONDUCTOR_BMAD_BOOTSTRAP_RECOVERY.md`.

## Before You Start

You need:

- macOS
- Claude Code CLI
- Git
- Python 3.11 or newer
- `npx`
- a local copy of the project repository you want to use with Factory

Open Terminal and check the tools:

```bash
claude --version
claude plugin --help
git --version
python3 --version
npx --version
```

If any command says `command not found`, stop and ask the maintainer for that
tool to be installed.

## Install From the GitHub Marketplace (recommended)

```bash
claude plugin marketplace add EduardoRemedios/factory-starter-kit
claude plugin install conductor-bmad@factory-starter-kit --scope user
```

That is the whole install; `conductor` arrives as a dependency. Skip to
"Start" below unless you need the offline path.

## Offline Path: Clone the Factory Starter Kit

Use this only when the GitHub marketplace is not reachable. Run:

```bash
mkdir -p "$HOME/Code"
git clone https://github.com/EduardoRemedios/factory-starter-kit.git \
  "$HOME/Code/factory-starter-kit"
cd "$HOME/Code/factory-starter-kit"
git checkout main
```

If the folder already exists, update it instead:

```bash
cd "$HOME/Code/factory-starter-kit"
git pull --ff-only
git checkout main
```

This folder is the marketplace root:

```text
$HOME/Code/factory-starter-kit
```

Do not use a temporary folder, an extracted ZIP, or `/tmp`.

## Find Your Project Path

The project path is the folder for the application repository where you want to
use BMAD and Factory.

If you know the folder, open it in Terminal and run:

```bash
cd /path/to/your/project
pwd
```

Copy the full path printed by `pwd`. It should look similar to:

```text
<home-folder>/Code/your-project
```

In the commands below, replace `/absolute/path/to/your/project` with that full
path. Keep the quotes.

## Run the Preflight Check

The preflight check is read-only. It checks your Mac, Claude Code, the Factory
package, and the target project path before installation.

```bash
cd "$HOME/Code/factory-starter-kit"
PROJECT_ROOT="/absolute/path/to/your/project"

./scripts/conductor-python scripts/verify_conductor_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$PROJECT_ROOT" \
  --json
```

Read the `"state"` line near the end:

- `"state": "PASS"` means continue.
- `"state": "WARN"` means continue only if the warning is understood.
- `"state": "BLOCKED"` means stop and send the full Terminal output to the
  maintainer.

## Offline Path: Install From the Starter Kit Checkout

If either uninstall command reports that the plugin is not installed, continue
to prune and preflight. `claude plugin prune` may leave cached payload
directories on disk; the rollout preflight blocks if same-version cached bytes
do not match the checkout.

```bash
cd "$HOME/Code/factory-starter-kit"
PROJECT_ROOT="/absolute/path/to/your/project"

claude plugin marketplace list
# If factory-starter-kit points at an old or missing path:
# claude plugin marketplace remove factory-starter-kit
claude plugin uninstall conductor-bmad@factory-starter-kit
claude plugin uninstall conductor@factory-starter-kit
claude plugin prune
claude plugin marketplace add "$PWD"
./scripts/conductor-python scripts/verify_conductor_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$PROJECT_ROOT" \
  --json
claude plugin install conductor-bmad@factory-starter-kit --scope user
```

Use the durable checkout path above; do not register a temporary or scratchpad
path as the marketplace source.

This is one explicit user installation. The companion declares Factory
`~0.3.4` as an automatic dependency, so users do not separately install or
manage Factory. Missing, disabled, or incompatible dependency state halts
instead of duplicating Factory Core.

## Start

Start Claude Code from your project repository:

```bash
cd "$PROJECT_ROOT"
claude
```

Inside Claude Code, run:

```text
/reload-plugins
/conductor-bmad:doctor
```

Run `/conductor-bmad:doctor` and follow its single next action:

- New target: `/conductor:greenfield`
- Existing project without Factory: `/conductor:brownfield`
- Factory present without BMAD: `/conductor-bmad:bootstrap`
- Both present: `/conductor-bmad:audit`

If Doctor reports `CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT`, do not run
`/conductor-bmad:bootstrap`, because that can create a second BMAD install beside
an existing nested one such as `bmad/_bmad`. Two options, both human decisions:

- Declare the existing tree as the active root in
  `docs/Conductor/PROJECT_CONFIG.json` under `adapters.bmad.declared_root`
  (repo-relative, directory named `_bmad`, not under `docs/`). Every version and
  digest check then applies at that root and Doctor reports a canonical layout.
  Then run `/conductor-bmad:seed-contracts` (preview, then apply by exact plan
  ID) so `contract-lint intent` can validate the declared adapter; it writes
  only inert schema and policy files and does not need the audit to be READY.
- Or preserve the tree as inert history under
  `docs/adapters/bmad/legacy-evidence/` using the zero-write preview from
  `/conductor-bmad:audit`, then bootstrap a fresh canonical install.

While the layout is unresolved, discovery workflows and helpers still run and
carry a `LAYOUT WARNING` in their context; intake, promotion, and
architecture/spec/UX authoring are blocked. If the nested BMAD tree has its own
`AGENTS.md`, do not overwrite it.

For a brownfield repository whose starting state is BMAD present and Factory
absent, Factory Brownfield apply is the first mutation. The desired target state
is always Factory and BMAD together, with Factory as downstream SDLC authority.
The bundled guard activates automatically as soon as Factory and BMAD coexist in
that Git worktree. Until then, the repository is treated only as an adoption
candidate, not as an approved BMAD-without-Factory operating mode.

Every setup command previews first. Apply only by quoting the exact full plan ID.
If the repository already has a project `CLAUDE.md`, Brownfield previews a
`migrate_bridge` action: the guide's content moves into the project-owned body
of `AGENTS.md` (under the Conductor managed block, or appended as "Migrated from
CLAUDE.md" when an `AGENTS.md` already exists) and `CLAUDE.md` becomes exactly
the one-line bridge `@AGENTS.md`. Review the preview and apply by exact plan ID;
nothing is deleted.

After BMAD bootstrap applies, close and open a fresh Claude Code session before
trying an installed BMAD skill. Then run `/conductor-bmad:doctor` again and follow
its next action. This reload is required for predictable skill discovery.
If bootstrap blocks after post-audit, preserve the receipt and use
`CONDUCTOR_BMAD_BOOTSTRAP_RECOVERY.md`; do not retry by deleting files.

After audit passes, run `/conductor-bmad:intake`. This seeds the authority policy,
shared policy implementation, capability-audit evidence, brownfield
reconciliation, one raw-brief template with its checklist, and the existing
project-preflight adapter. Existing different files block instead of being
overwritten.

Create allowed BMAD discovery output, human-review the selected artifact, then
run `/conductor-bmad:promote`. Draft the Factory brief only from the promoted
snapshot ID and aggregate hash; never cite `_bmad-output/` directly.

## Discovery routes

- **Fast pilot handover:** time-box discovery to one useful technique, converge
  to the product-brief synthesis shape, record limitations honestly, obtain
  human review, promote the selected evidence, and start the Factory brief.
- **Full discovery:** use additional allowed upstream workflows when the product
  decision genuinely needs them. Completeness is not required merely to hand
  control to Factory.

## Handover map

(0.2-era wording kept because the plugin tests pin it. In 0.3 the promoted snapshot enters the Intent Pack as an `upstream_snapshot` source and G1 Intent Lock replaces Stage A recall and Purple Gate PASS.)

- Snapshot manifest → project preflight: validates review evidence, inventory,
  modes, and aggregate integrity.
- Promoted `artifact.md` → Stage A recall: resolves the human-readable upstream
  content. Do not use `SNAPSHOT_MANIFEST.json` as the Stage A required reference.
- Factory intent → authoritative only after Purple Gate PASS: BMAD remains
  non-binding evidence throughout.

Claude Code autocomplete is discovery UI: an autocomplete suggestion is not an
invocation. A hook denial names its cause in one line: the reason code, the lane
of the skill you invoked (`product_context`, `helper`, `evidence_only`,
`delivery`, or `unknown`), the layout state, an `Allowed here:` list of what
still works, and a `Next:` command. `/conductor-bmad:doctor` is an optional
suggested recovery action unless you explicitly invoke it.

The Claude plugin denies delivery-lane and unknown `bmad-*` direct commands or
model-initiated skills in an enforcement-active repository. Party mode, review,
editorial review, and elicitation are helpers in the product-context lane and
are allowed. The lane definitions are in `docs/adapters/bmad/BMAD_POLICY.md` and
`docs/adapters/bmad/lane_policy.json`. Run the same authored
classifier in CI from the repository root with:

```bash
python3 scripts/conductor_bmad_policy_lint
```
