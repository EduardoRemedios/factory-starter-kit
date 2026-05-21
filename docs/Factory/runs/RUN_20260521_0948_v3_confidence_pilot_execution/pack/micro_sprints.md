# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-21): Stage G micro-sprint sequence.

## MS-01 - Real Shadow Scans
- Objective: Run two additional real-run shadow scans.
- Inputs: existing V2-authoritative run roots.
- Outputs: output JSON and reports.
- Entry Criteria: Stage I2 PASS and human GO.
- Exit Criteria: Findings classified.
- Stop or Go Gate: Stop if a scan emits an unexpected finding.

## MS-02 - Seeded And Positive Routing Pilots
- Objective: Run remaining seeded and routing cases.
- Inputs: run-local fixture directories.
- Outputs: JSON outputs and pilot reports.
- Entry Criteria: MS-01 complete.
- Exit Criteria: Expected finding IDs or positive passes are recorded.
- Stop or Go Gate: Stop if output differs from expected status.

## MS-03 - Natural-language Detection Design
- Objective: Document a bounded design for broader advisory detection.
- Inputs: current trigger-marker limitation and pilot evidence.
- Outputs: `NATURAL_LANGUAGE_DETECTION_DESIGN.md`.
- Entry Criteria: MS-02 complete.
- Exit Criteria: False-positive budget and no-gate effect are explicit.
- Stop or Go Gate: Stop if design implies implementation in this run.

## MS-04 - Batch Rollup
- Objective: Summarize confidence gained and remaining gaps.
- Inputs: all pilot reports and design note.
- Outputs: `CONFIDENCE_PILOT_BATCH_ROLLUP.md`.
- Entry Criteria: MS-03 complete.
- Exit Criteria: Rollup states whether V3 is operationally ready.
- Stop or Go Gate: Stop if rollup implies promotion without decision report.

## MS-05 - Closeout
- Objective: Verify and close execution.
- Inputs: execution evidence and pack.
- Outputs: `EXECUTION_CLOSEOUT.md` and tracking doc updates.
- Entry Criteria: MS-04 complete.
- Exit Criteria: verification commands pass.
- Stop or Go Gate: Stop if any required check fails.
