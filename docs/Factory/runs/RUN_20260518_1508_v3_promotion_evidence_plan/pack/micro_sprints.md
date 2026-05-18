# Micro-sprints - Promotion-Evidence Advisory Lint Pilot

## Version
v1

## Change Log
- v1 (2026-05-18): Initial micro-sprint sequence for a future promotion-evidence pilot.

## MS-00 - Verification Scaffold
- Objective: Confirm baseline docs and advisory lint are clean before any temporary mutation.
- Inputs: `docs/Factory/v3/`, `scripts/factory_v3_advisory_lint.py`, `verification_plan.md`.
- Outputs: Baseline command output recorded in future pilot report.
- Entry criteria: Human approval to execute the future pilot exists.
- Exit criteria: `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json` returns `ADVISORY_PASS`.
- Stop or go gate: STOP if baseline docs emit findings unrelated to the planned promotion-evidence mutation.

## MS-01 - Promotion-Evidence Warning Pilot
- Objective: Temporarily introduce the smallest real-doc promotion/release wording that lacks evidence and explicit human release approval, then capture advisory output.
- Inputs: `PROMOTION_CRITERIA.md` or another bounded `docs/Factory/v3/` target, fixture sketch, verification plan.
- Outputs: Non-empty advisory output and finding classification table.
- Entry criteria: MS-00 passed and temporary mutation target is named.
- Exit criteria: Finding classifications are recorded as `accepted`, `false_positive`, `needs_more_context`, or `deferred`.
- Stop or go gate: STOP if findings imply required-gate wiring, AEGIS dependency, runtime-kernel authority, or broader scope than promotion evidence.

## MS-02 - Remediation And Closeout
- Objective: Remove temporary unsafe wording and record final pilot evidence.
- Inputs: Advisory output from MS-01 and current docs diff.
- Outputs: Pilot report, final clean advisory result, matcher tuning decision.
- Entry criteria: MS-01 findings are classified.
- Exit criteria: Final `docs/Factory/v3` advisory run returns `ADVISORY_PASS`, no required gate files were touched, and no matcher tuning is performed unless justified by evidence.
- Stop or go gate: STOP if final docs retain release/promotion claims or if matcher edits are proposed without separate approval.

## Bounded Deferral Hooks
- Matcher tuning decision is deferred to a later implementation run if and only if future pilot evidence identifies false positive, false negative, ambiguity, or missed signal.
- Required-gate integration remains blocked pending a separate Factory v2 pack and explicit human release approval.

