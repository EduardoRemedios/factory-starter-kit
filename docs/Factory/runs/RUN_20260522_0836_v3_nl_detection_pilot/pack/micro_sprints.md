# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-22): Stage G micro-sprint sequence.

## MS-01 - Opt-in Candidate Layer
- Objective: Add pilot-only natural-language candidate detection.
- Inputs: existing runner and design note.
- Outputs: runner changes behind explicit flag.
- Entry Criteria: Stage I2 PASS and human GO.
- Exit Criteria: default fixture regression still passes.
- Stop or Go Gate: Stop if default output changes.

## MS-02 - Corpus And Measurement
- Objective: Add clean and drift corpora and run pilot mode.
- Inputs: fixture plan.
- Outputs: JSON outputs and false-positive report.
- Entry Criteria: MS-01 complete.
- Exit Criteria: clean corpus has zero findings; drift corpus emits expected IDs.
- Stop or Go Gate: Stop if clean false positives exceed budget.

## MS-03 - Checklist And Closeout
- Objective: Update C-03 and record closeout.
- Inputs: pilot outputs.
- Outputs: checklist update and closeout.
- Entry Criteria: MS-02 complete.
- Exit Criteria: C-03 status accurately reflects evidence.
- Stop or Go Gate: Stop if closeout implies V3 promotion.

## MS-04 - Verification
- Objective: Run verification and package evidence.
- Inputs: completed changes.
- Outputs: verification artifacts.
- Entry Criteria: MS-03 complete.
- Exit Criteria: all required checks pass.
- Stop or Go Gate: Stop if any check fails.
