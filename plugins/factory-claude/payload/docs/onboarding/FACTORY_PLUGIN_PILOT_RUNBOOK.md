# Factory Plugin Pilot Runbook

## Purpose

Decide whether Factory plugin 0.2.5 is ready for a team rollout using named
journeys, recovery evidence, and Product Owner sign-off.

## Entry Gates

- Claude Code has a `claude plugin` interface that passes the rollout preflight.
- `python3 scripts/verify_factory_cli_rollout.py --json` returns no `BLOCKED`
  checks for the marketplace root and pilot target.
- Claude plugin and marketplace pass strict validation.
- Codex package passes Plugin Creator validation.
- Factory is installed and invoked successfully in a fresh Claude session and a fresh Codex app task.
- The normalized live doctor/progress results show no unexplained semantic difference.
- A release candidate commit or tag is recorded.
- A rollback owner and prior package are available.

If an entry gate is missing, the pilot does not start.

## Cohort

- experienced Factory user: one named maintainer or trained adopter
- first-time Factory user: one named pilot-team member
- Product Owner and release decision: one named accountable owner

Do not substitute two experienced users for the first-time-user journey.

## Evidence Location

Use:

```text
artifacts/verification/factory_plugin/pilot/<YYYYMMDD>/<user>/
```

Capture version output, install result, doctor/progress JSON, preview plans, approvals, receipts, validator output, diffs, recovery result, journey timing, and defects.

## Required Journeys

Run all nine:

1. install
2. greenfield
3. doctor
4. brownfield
5. progress
6. validate
7. update
8. rollback
9. execution closeout and explicit/default progress

For the Claude Greenfield journey, also repeat the preview from an otherwise
empty disposable target containing only `.claude/settings.local.json`. Record
that the file is reported as preserved, absent from allowed writes and
mutations, and remains byte- and mode-identical after apply and rollback.

The first-time user follows only the published quick start and reference. Author coaching is recorded as a documentation defect.

## Live Cross-Harness Check

Use one bounded PLANNING_ONLY brief in both harnesses. Normalize only:

- invocation syntax
- plugin manifest
- harness metadata
- the documented Claude `CLAUDE.md` bridge

Compare stage order, required paths, execution mode, validator results, halt reasons, final state, and human authorization behavior.

## Stop Conditions

Stop immediately for:

- any destructive or unpreviewed mutation
- a write outside the allowed path list
- overwrite or deletion of a project-owned file
- unexplained Claude/Codex gate difference
- a present-invalid closeout falling back to an authorized execution state
- failed interruption recovery or rollback
- open Critical or High defect
- missing first-time-user journey

## Release Scorecard

| Measure | Required |
|---|---:|
| Open Critical defects | 0 |
| Open High defects | 0 |
| Destructive mutations | 0 |
| Recovery success rate | 100% |
| Journey completion rate | 100% |
| Experienced Factory user completed | Yes |
| First-time Factory user completed | Yes |
| Product Owner sign-off | Yes |

## Decision

- `PILOT_PASS`: every threshold is met and the accountable Product Owner signs off.
- `PILOT_NO_GO`: any threshold is missed.

No company-wide recommendation is made from a partial scorecard.
