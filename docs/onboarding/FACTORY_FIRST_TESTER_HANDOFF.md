# Factory First Tester Handoff

Use this checklist for one trusted colleague before the first team rollout. The
goal is to test the Factory-only Claude Code CLI path with a small disposable
repository, not to test optional upstream companions or a production project.

## Scope

- Factory-only plugin release candidate: `0.2.5` on `main`
- Surface: Claude Code CLI on macOS
- Test target: disposable empty Git repository
- Out of scope: optional upstream companions, Claude Desktop, production code changes,
  execution-enabled Factory runs

## Prerequisites

The tester needs:

- macOS
- Git
- Python 3.11 or newer
- Claude Code CLI with `claude plugin --help`
- access to `https://github.com/EduardoRemedios/factory-starter-kit`

## Maintainer Prep

Ask the tester to start from a clean terminal and run:

```bash
git clone https://github.com/EduardoRemedios/factory-starter-kit.git
cd factory-starter-kit
git checkout main

./scripts/factory-python scripts/verify_factory_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$HOME/factory-first-tester-greenfield" \
  --json | tee factory-first-tester-preflight.json
```

The preflight state must be `PASS`, or `WARN` with a warning the maintainer
understands and accepts. Stop on `BLOCKED`.

## Install Factory

Install from the checked-out release candidate:

```bash
claude plugin uninstall factory@factory-starter-kit
claude plugin prune
./scripts/factory-python scripts/verify_factory_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$HOME/factory-first-tester-greenfield" \
  --json | tee factory-first-tester-preflight.json
claude plugin marketplace add "$PWD"
claude plugin install factory@factory-starter-kit --scope user
claude plugin list
```

If uninstall reports that the plugin is not installed, continue to prune and
preflight. If the tester already has an older Factory plugin installed,
uninstall or update it before continuing so only one Factory candidate is being
tested.

## Greenfield Test

Create a disposable target repository:

```bash
mkdir -p "$HOME/factory-first-tester-greenfield"
cd "$HOME/factory-first-tester-greenfield"
git init
claude
```

Inside Claude Code, run:

```text
/reload-plugins
/factory:greenfield
```

Review the preview. Apply only by quoting the exact full current plan ID shown
by Factory. A generic approval such as `approve` is not valid.

After setup completes, run:

```text
/factory:doctor
/factory:validate
/factory:progress
```

The expected result is no blocked setup state and a clear next legal action. Do
not start an execution-enabled Factory run during this first test.

## Evidence To Return

Ask the tester to return:

- `factory-first-tester-preflight.json`
- `claude --version`
- `claude plugin list`
- the Greenfield preview and apply result
- Doctor, Validate, and Progress output
- final `git status --short` from the disposable target repository
- a short friction log listing every moment where the next step was unclear

## Stop Conditions

Stop and preserve output when:

- preflight is `BLOCKED`
- `claude plugin --help` is unavailable
- the Factory plugin does not appear after `/reload-plugins`
- the preview writes outside the disposable target repository
- the exact plan ID changes before apply
- any reason code is unclear
