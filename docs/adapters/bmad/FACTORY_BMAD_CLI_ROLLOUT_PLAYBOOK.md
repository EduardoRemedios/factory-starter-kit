# Factory BMAD CLI Rollout Playbook

Use this playbook for the first two Claude Code CLI pilot teams. It is a
support path, not a release verdict. Publication, organization rollout, and
Product Owner sign-off remain separate decisions.

Before using this team playbook, run one trusted-colleague full-flow test with
`FACTORY_BMAD_FIRST_TESTER_HANDOFF.md`.

## Supported First-Team Surface

- macOS local development machine.
- Claude Code CLI with plugin marketplace support.
- Python 3.11 or newer available as both the current Factory interpreter and
  `python3` on the Claude hook PATH.
- `npx` available for the pinned BMAD bootstrap.
- Local Claude Code session, not Claude Desktop, cloud session, WSL, or Cowork.
- Factory and Factory-BMAD installed from the same checked-out `0.2.3`
  marketplace root.
- The marketplace root is a durable local checkout, not `/tmp`, a scratchpad, an
  extracted ZIP, or any path that can disappear between sessions.

## Maintainer Prep

Run this before a team starts:

```bash
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root /absolute/path/to/factory-starter-kit \
  --target-root /absolute/path/to/team/repo \
  --json
```

Do not start the pilot while the preflight state is `BLOCKED`. A `WARN` state is
allowed only when the maintainer has explained the warning to the team owner and
recorded why it does not affect the planned journey.

Prepare one 30-minute guided setup call. The maintainer, not the team, owns
interpreting blocked reason codes during the first use.

## Team Happy Path

1. Open a terminal in the intended repository or empty target directory.
2. Confirm the same Claude binary will be used throughout:

   ```bash
   which claude
   claude --version
   claude plugin --help
   ```

3. Install from the supplied marketplace root:

   ```bash
   claude plugin marketplace list
   # If factory-starter-kit points at an old or missing path:
   # claude plugin marketplace remove factory-starter-kit
   claude plugin marketplace add /absolute/path/to/factory-starter-kit
   claude plugin install factory-bmad@factory-starter-kit
   ```

4. Confirm `factory-starter-kit` now points at the supplied durable checkout.
5. Start a fresh Claude Code session in the target directory.
6. Invoke `/factory-bmad:doctor`.
7. Follow only the single next action returned by Doctor.
8. Approve setup or bootstrap only by quoting the exact full current plan ID.
9. After BMAD bootstrap applies, close and reopen Claude Code before invoking
   any BMAD skill.
10. Use only allowed upstream BMAD discovery workflows.
11. Promote reviewed evidence, draft the Factory brief from the promoted
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
- a preview plan changes after review
- BMAD bootstrap returns `FACTORY_BMAD_BOOTSTRAP_POST_AUDIT_FAILED`
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
