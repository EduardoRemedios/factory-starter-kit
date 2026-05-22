# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-22): Stage G micro-sprint sequence.

## MS-01 - Failed-command Halt Pilot
- Objective: Prove nonzero halt-on-failure command stops execution.
- Inputs: run-local harness.
- Outputs: `execution_evidence/halt_failed_command/result.json`.
- Entry Criteria: Stage I2 PASS and human GO.
- Exit Criteria: Result records `halted: true`, nonzero exit, and no continuation marker.
- Stop or Go Gate: Stop if continuation marker exists.

## MS-02 - Reentry Pilot
- Objective: Prove authored artifacts govern reentry.
- Inputs: source and derived cursor fixture JSON.
- Outputs: valid and stale reentry result JSON.
- Entry Criteria: MS-01 complete.
- Exit Criteria: valid resume allowed; stale cursor halted.
- Stop or Go Gate: Stop if stale cursor is allowed.

## MS-03 - Checklist And Closeout
- Objective: Update decision checklist and record closeout.
- Inputs: pilot evidence.
- Outputs: checklist update and `EXECUTION_CLOSEOUT.md`.
- Entry Criteria: MS-02 complete.
- Exit Criteria: C-01 and C-02 evidence status accurately recorded.
- Stop or Go Gate: Stop if closeout implies V3 promotion.

## MS-04 - Verification
- Objective: Run governance and verification checks.
- Inputs: completed evidence and docs.
- Outputs: verification artifacts.
- Entry Criteria: MS-03 complete.
- Exit Criteria: required checks pass.
- Stop or Go Gate: Stop if any check fails.
