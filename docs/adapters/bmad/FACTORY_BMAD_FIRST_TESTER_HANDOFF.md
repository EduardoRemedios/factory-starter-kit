# Factory BMAD First Tester Handoff

Use this checklist for one trusted colleague before the first team rollout. The
goal is to test the complete BMAD-to-Factory transition in a disposable
greenfield repository, not to build a production application.

## Scope

- Candidate: coordinated Factory and Factory-BMAD `0.2.4`
- Surface: Claude Code CLI on macOS
- Primary test target: disposable Greenfield repository
- Follow-up rehearsal targets before team rollout:
  - brownfield repository with neither Factory nor BMAD
  - brownfield repository with BMAD already present and Factory absent
- Product brief seed: `ODYSSEY_V3_INITIAL_BMAD_BRIEF.md`
- Execution mode: `PLANNING_ONLY`
- Out of scope: Claude Desktop, production code changes, execution-enabled
  Factory runs, BMAD architecture/stories/implementation workflows, and any
  organization rollout decision

## Prerequisites

The tester needs:

- macOS
- Git
- Python 3.11 or newer
- `npx`
- Claude Code CLI with `claude plugin --help`
- access to the Factory-BMAD candidate repository cloned to a durable path such
  as `$HOME/Code/factory-bmad-candidate`

Do not run the first-tester flow from `/tmp`, a scratchpad, an extracted ZIP, or
any path that may disappear between Claude sessions. Claude records the
marketplace source path by marketplace name; a deleted checkout can leave
`factory-starter-kit` registered but unloadable.

## Maintainer Prep

Ask the tester to start from a clean terminal and run this from the candidate
repository:

```bash
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$HOME/factory-bmad-first-tester-greenfield" \
  --json | tee factory-bmad-first-tester-preflight.json
```

The preflight state must be `PASS`, or `WARN` with a warning the maintainer
understands and accepts. Stop on `BLOCKED`.

## Install Factory-BMAD

Install only the companion. Factory is resolved as the protected dependency.
Before each candidate retest, remove both the companion and its Factory
dependency from Claude Code, then prune the cache. Claude Code can retain an
auto-installed dependency under the same version, and a reinstall may otherwise
reuse stale package bytes. If either uninstall command reports that the plugin
is not installed, continue to prune and preflight.

```bash
claude plugin marketplace list
# If factory-starter-kit already points at an old or missing path, remove it
# before adding the durable candidate checkout:
# claude plugin marketplace remove factory-starter-kit
claude plugin uninstall factory-bmad@factory-starter-kit
claude plugin uninstall factory@factory-starter-kit
claude plugin prune
claude plugin marketplace add "$PWD"
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$HOME/factory-bmad-first-tester-greenfield" \
  --json | tee factory-bmad-first-tester-preflight.json
claude plugin install factory-bmad@factory-starter-kit --scope user
claude plugin list
```

If the tester already has older Factory or Factory-BMAD plugins installed,
uninstall or update them before continuing so only this candidate is being
tested. If `claude plugin marketplace list` still shows `factory-starter-kit`
pointing anywhere except the durable candidate checkout, stop and fix the
marketplace registration before installing. If the rollout preflight reports a
`claude_cache_*` blocker, prune again or remove only the stale
`~/.claude/plugins/cache/factory-starter-kit` cache directory, then rerun
preflight before installing.

## Primary Test: Greenfield

Create a disposable empty target. Mark knows the Factory flow already; this test
is intended to expose friction in BMAD bootstrap, discovery, promotion, and
handoff.

```bash
mkdir -p "$HOME/factory-bmad-first-tester-greenfield"
cd "$HOME/factory-bmad-first-tester-greenfield"
claude
```

Inside Claude Code, run:

```text
/reload-plugins
/factory-bmad:doctor
```

Follow only the single next action returned by Doctor. For this target the path
should lead through Factory Greenfield and then `/factory-bmad:bootstrap`.

Every setup step is preview-first. Apply only by quoting the exact full current
plan ID shown by Factory or Factory-BMAD. A generic approval such as `approve`
is not valid.

After BMAD bootstrap applies, close and reopen Claude Code from the same target
directory, then run:

```text
/reload-plugins
/factory-bmad:doctor
/factory-bmad:audit
/factory-bmad:intake
```

## Follow-Up Brownfield Rehearsal

After the greenfield first-tester pass, run a separate rehearsal for the two
team states expected in rollout:

1. brownfield repository with neither Factory nor BMAD;
2. brownfield repository with BMAD already present and Factory absent.

These should be disposable copies or fixtures, not production repositories.
Existing files must be preserved unless the preview explicitly classifies a
change and the exact plan ID is approved.

```bash
mkdir -p "$HOME/factory-bmad-first-tester-brownfield-neither"
cd "$HOME/factory-bmad-first-tester-brownfield-neither"
git init
printf '# Brownfield Fixture\n' > README.md
git add README.md
git commit -m "Create brownfield fixture"
claude
```

```text
/reload-plugins
/factory-bmad:doctor
```

For the second brownfield starting state, create or copy a disposable repository
where BMAD is already present and Factory is absent, then start from
`/factory-bmad:doctor`. This is an adoption source state only; the expected
target state is Factory and BMAD together, with Factory as downstream SDLC
authority. Doctor should route to Factory Brownfield first, then companion
bootstrap or audit depending on the detected BMAD state.

## BMAD Discovery

Use the application seed in `docs/adapters/bmad/ODYSSEY_V3_INITIAL_BMAD_BRIEF.md`
for the greenfield first test and any later brownfield rehearsal.
The test should use one fast allowed upstream BMAD workflow, preferably
brainstorming or product-brief synthesis, to produce a reviewed artifact.

The tester must not use BMAD architecture, stories, implementation, code-review,
loop, or correct-course workflows for this pilot.

Record:

- which BMAD workflow was invoked
- the raw draft location under `_bmad-output/`
- the reviewed artifact selected for promotion
- any limitations or assumptions retained from discovery

## Promote Reviewed Evidence

After human review, use:

```text
/factory-bmad:promote
```

Promote only the reviewed Markdown artifact. Capture the snapshot ID and
aggregate hash. Do not cite `_bmad-output/` directly in the Factory brief.

## Factory Handoff

Draft the Factory `raw_brief.md` only from:

- the promoted snapshot ID
- the aggregate hash
- the promoted Markdown content
- the explicit exclusions in the Odyssey v3 seed brief

Then run the normal Factory planning path in `PLANNING_ONLY` mode through I2:

```text
/factory:doctor
/factory:run
```

Stop after the final Factory pack and `pack-lint`. Do not approve
implementation.

## Expected Evidence

Ask the tester to return:

- `factory-bmad-first-tester-preflight.json`
- `claude --version`
- `claude plugin list`
- Doctor output before and after setup
- every setup preview/apply result and exact approved plan ID
- BMAD bootstrap receipt
- Audit and Intake output
- BMAD discovery transcript or saved output
- promoted snapshot ID and aggregate hash
- Factory `raw_brief.md`
- Stage A through I2 validator results
- final `git status --short`
- a short friction log listing every moment where the next step was unclear

For the follow-up brownfield rehearsal, also return confirmation that
user-owned brownfield files remained present.

## Stop Conditions

Stop and preserve output when:

- rollout preflight is `BLOCKED`
- `claude plugin --help` is unavailable
- `npx` is missing
- `factory-bmad` does not appear after `/reload-plugins`
- Factory dependency resolution fails
- bootstrap returns `FACTORY_BMAD_BOOTSTRAP_POST_AUDIT_FAILED`
- an unknown or prohibited `bmad-*` command is allowed
- raw `_bmad-output/` content is cited directly in the Factory brief
- `SNAPSHOT_MANIFEST.json` is used as the Stage A content reference
- Factory intent treats BMAD as authoritative before Purple Gate PASS
- any write appears outside the reported mutation set
