# Factory BMAD CLI Rollout Playbook

Use this playbook for the first two Claude Code CLI pilot teams. It is a
support path, not a release verdict. Publication, organization rollout, and
Product Owner sign-off remain separate decisions.

Before using this team playbook, run one trusted-colleague full-flow test with
`CONDUCTOR_BMAD_FIRST_TESTER_HANDOFF.md`.

## Supported First-Team Surface

- macOS local development machine.
- Claude Code CLI with plugin marketplace support.
- Python 3.11 or newer available as both the current Factory interpreter and
  `python3` on the Claude hook PATH.
- `npx` available for the pinned BMAD bootstrap.
- Local Claude Code session, not Claude Desktop, cloud session, WSL, or Cowork.
- Factory and Factory-BMAD installed from the same checked-out `0.2.5`
  marketplace root.
- The marketplace root is a durable local checkout, not `/tmp`, a scratchpad, an
  extracted ZIP, or any path that can disappear between sessions.

## Maintainer Prep

Run this before a team starts:

```bash
cd "$HOME/Code/factory-starter-kit"
PROJECT_ROOT="/absolute/path/to/team/repo"

./scripts/conductor-python scripts/verify_conductor_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root "$PROJECT_ROOT" \
  --json
```

Do not start the pilot while the preflight state is `BLOCKED`. A `WARN` state is
allowed only when the maintainer has explained the warning to the team owner and
recorded why it does not affect the planned journey.

The setup is self-service. Team members should copy and paste the command
blocks exactly, replacing only the project path. A script is a Terminal command;
no separate programming knowledge is required.
If either uninstall command below reports that the plugin is not installed,
continue to prune and preflight. Treat `claude plugin prune` as dependency-state
cleanup; the rollout preflight is the cache-content authority because cached
payload directories may remain on disk.

## Team Happy Path

1. Open Terminal.
2. Confirm the same Claude binary will be used throughout:

   ```bash
   which claude
   claude --version
   claude plugin --help
   ```

3. Clone the Factory Starter Kit and record the project path:

   ```bash
   mkdir -p "$HOME/Code"
   git clone https://github.com/EduardoRemedios/factory-starter-kit.git \
     "$HOME/Code/factory-starter-kit"
   cd "$HOME/Code/factory-starter-kit"
   git checkout main

   PROJECT_ROOT="/absolute/path/to/team/repo"
   ```

   If the folder already exists, update it instead:

   ```bash
   cd "$HOME/Code/factory-starter-kit"
   git pull --ff-only
   git checkout main
   ```

   To find the project path, open the project folder in Terminal and run
   `pwd`. Copy the full path printed by `pwd` into `PROJECT_ROOT`.

4. Install from the checked-out marketplace root:

   ```bash
   cd "$HOME/Code/factory-starter-kit"
   PROJECT_ROOT="/absolute/path/to/team/repo"

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

5. Confirm the rollout preflight has no `BLOCKED` result and
   `factory-starter-kit` now points at the supplied durable checkout.
6. Start a fresh Claude Code session in the target directory:

   ```bash
   cd "$PROJECT_ROOT"
   claude
   ```

7. Invoke `/conductor-bmad:doctor`.
8. Follow only the single next action returned by Doctor.
9. Approve setup or bootstrap only by quoting the exact full current plan ID.
10. After BMAD bootstrap applies, close and reopen Claude Code before invoking
   any BMAD skill.
11. Use only allowed upstream BMAD discovery workflows.
12. Promote reviewed evidence, draft the Factory brief from the promoted
    snapshot, and stop at Factory human review gates.

Use `ODYSSEY_V3_INITIAL_BMAD_BRIEF.md` as the default first-test product seed
unless the sponsor explicitly approves a different bounded seed. The first
trusted-colleague test may be greenfield to isolate BMAD-to-Factory friction.
Before team rollout, also rehearse both brownfield states expected in team use:
one repository with neither Factory nor BMAD, and one repository with BMAD
already present but Factory absent.

## Stop Conditions

Stop and preserve output when any of these happen:

- the rollout preflight reports `BLOCKED`
- the team cannot run `claude plugin --help`
- `python3` is missing or older than 3.11
- `npx` is missing
- `factory-starter-kit` points at an old, missing, or non-durable marketplace
  source
- rollout preflight reports a stale `claude_cache_*` result
- a preview plan changes after review
- BMAD bootstrap returns `CONDUCTOR_BMAD_BOOTSTRAP_POST_AUDIT_FAILED`
- any unexpected file appears outside the reported mutation set
- the user is unsure whether a BMAD command is allowed after Factory is present

## Maintainer Evidence

For each pilot, retain:

- rollout preflight JSON
- `claude --version`
- `claude plugin list --json` after installation
- Doctor result before and after setup
- any preview/apply JSON used for exact approval
- BMAD bootstrap receipt, if bootstrap is used
- final `git status --short`
- a short friction log with every point where the team asked what to do next

## Pass Bar

The first-team CLI path is acceptable only when both pilots complete setup and
the BMAD-to-Factory handoff without maintainer shell surgery, unexpected writes,
or unexplained blocked states.
