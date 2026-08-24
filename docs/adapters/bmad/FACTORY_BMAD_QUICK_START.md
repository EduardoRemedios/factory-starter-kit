# Factory BMAD Companion — Claude Code Quick Start

Use Claude Code CLI. This technical pilot does not claim Claude Desktop support.
Keep Factory and the companion in the same Factory Starter Kit marketplace so
the versioned Factory dependency can resolve.

For the first two teams, run the CLI rollout preflight and use the guided
playbook before installing anything in a team repository:

```bash
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
```

See `FACTORY_BMAD_CLI_ROLLOUT_PLAYBOOK.md`,
`FACTORY_BMAD_FIRST_TESTER_HANDOFF.md`,
`FACTORY_BMAD_COMPATIBILITY_POLICY.md`, and
`FACTORY_BMAD_BOOTSTRAP_RECOVERY.md`.

## Install a checked-out release candidate

If either uninstall command reports that the plugin is not installed, continue
to prune and preflight. `claude plugin prune` may leave cached payload
directories on disk; the rollout preflight blocks if same-version cached bytes
do not match the checkout.

```bash
claude plugin marketplace list
# If factory-starter-kit points at an old or missing path:
# claude plugin marketplace remove factory-starter-kit
claude plugin uninstall factory-bmad@factory-starter-kit
claude plugin uninstall factory@factory-starter-kit
claude plugin prune
claude plugin marketplace add /absolute/path/to/factory-starter-kit
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
claude plugin install factory-bmad@factory-starter-kit
```

Use a durable checkout path such as `$HOME/Code/factory-bmad-candidate`; do not
register a temporary or scratchpad path as the marketplace source.

This is one explicit user installation. The companion declares Factory
`~0.2.5` as an automatic dependency, so users do not separately install or
manage Factory. Missing, disabled, or incompatible dependency state halts
instead of duplicating Factory Core.

## Start

Run `/factory-bmad:doctor` and follow its single next action:

- New target: `/factory:greenfield`
- Existing project without Factory: `/factory:brownfield`
- Factory present without BMAD: `/factory-bmad:bootstrap`
- Both present: `/factory-bmad:audit`

For a brownfield repository whose starting state is BMAD present and Factory
absent, Factory Brownfield apply is the first mutation. The desired target state
is always Factory and BMAD together, with Factory as downstream SDLC authority.
The bundled guard activates automatically as soon as Factory and BMAD coexist in
that Git worktree. Until then, the repository is treated only as an adoption
candidate, not as an approved BMAD-without-Factory operating mode.

Every setup command previews first. Apply only by quoting the exact full plan ID.

After BMAD bootstrap applies, close and open a fresh Claude Code session before
trying an installed BMAD skill. Then run `/factory-bmad:doctor` again and follow
its next action. This reload is required for predictable skill discovery.
If bootstrap blocks after post-audit, preserve the receipt and use
`FACTORY_BMAD_BOOTSTRAP_RECOVERY.md`; do not retry by deleting files.

After audit passes, run `/factory-bmad:intake`. This seeds the authority policy,
shared policy implementation, capability-audit evidence, brownfield
reconciliation, one raw-brief template with its checklist, and the existing
project-preflight adapter. Existing different files block instead of being
overwritten.

Create allowed BMAD discovery output, human-review the selected artifact, then
run `/factory-bmad:promote`. Draft the Factory brief only from the promoted
snapshot ID and aggregate hash; never cite `_bmad-output/` directly.

## Discovery routes

- **Fast pilot handover:** time-box discovery to one useful technique, converge
  to the product-brief synthesis shape, record limitations honestly, obtain
  human review, promote the selected evidence, and start the Factory brief.
- **Full discovery:** use additional allowed upstream workflows when the product
  decision genuinely needs them. Completeness is not required merely to hand
  control to Factory.

## Handover map

- Snapshot manifest → project preflight: validates review evidence, inventory,
  modes, and aggregate integrity.
- Promoted `artifact.md` → Stage A recall: resolves the human-readable upstream
  content. Do not use `SNAPSHOT_MANIFEST.json` as the Stage A required reference.
- Factory intent → authoritative only after Purple Gate PASS: BMAD remains
  non-binding evidence throughout.

Claude Code autocomplete is discovery UI: an autocomplete suggestion is not an
invocation. A hook denial means the requested command was blocked; Doctor was
not run. `/factory-bmad:doctor` is an optional suggested recovery action unless
you explicitly invoke it.

The Claude plugin automatically denies any non-allowlisted `bmad-*` direct
command or model-initiated skill in an enforcement-active repository. The exact
allowlist is in `docs/adapters/bmad/BMAD_POLICY.md`. Run the same authored
classifier in CI from the repository root with:

```bash
python3 scripts/factory_bmad_policy_lint
```
