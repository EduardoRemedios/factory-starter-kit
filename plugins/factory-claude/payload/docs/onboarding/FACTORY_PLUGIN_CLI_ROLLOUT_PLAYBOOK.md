# Factory Plugin CLI Rollout Playbook

Use this playbook for the first Claude Code CLI teams that adopt Factory only.
It does not require any upstream companion or external discovery workflow.

## Supported First-Team Surface

- macOS local development machine.
- Claude Code CLI with plugin marketplace support.
- Python 3.11 or newer available as both the current interpreter and `python3`.
- Git available on PATH.
- Local Claude Code session, not Desktop, cloud session, WSL, or Cowork.
- Factory installed from the checked-out starter-kit marketplace root.

## Maintainer Prep

Run this before a team starts:

```bash
python3 scripts/verify_factory_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
```

Do not start while the preflight state is `BLOCKED`. A `WARN` state is allowed
only when the maintainer has explained the warning to the project owner and it
does not affect the intended journey.

## Team Happy Path

1. Open a terminal in the intended empty project directory or existing Git
   repository.
2. Confirm the same Claude binary will be used throughout:

   ```bash
   which claude
   claude --version
   claude plugin --help
   ```

3. Install Factory from the supplied marketplace root:

   ```bash
   claude plugin marketplace add /absolute/path/to/factory-starter-kit
   claude plugin install factory@factory-starter-kit
   ```

4. Start a fresh Claude Code session in the target directory.
5. For a new project, invoke `/factory:greenfield` first.
6. For an existing Git repository, invoke `/factory:doctor`, then
   `/factory:brownfield` if Doctor reports Factory is not configured.
7. Approve setup only by quoting the exact full current plan ID.
8. After setup, run `/factory:doctor`, `/factory:validate`, and
   `/factory:progress`.
9. Start the first Factory run as `PLANNING_ONLY` unless execution is explicitly
   authorized in the brief.

## Stop Conditions

Stop and preserve output when any of these happen:

- the rollout preflight reports `BLOCKED`
- the team cannot run `claude plugin --help`
- `python3` is missing or older than 3.11
- a preview plan changes after review
- a write appears outside the reported allowed path list
- a blocked reason code is unclear to the team

## Maintainer Evidence

For each pilot, retain:

- rollout preflight JSON
- `claude --version`
- `claude plugin list --json` after installation
- Doctor result before and after setup
- preview/apply JSON used for exact approval
- final `git status --short`
- a short friction log with every point where the team asked what to do next
