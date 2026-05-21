# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-21): Stage G micro-sprint sequence.

## MS-01 - Confidence Threshold Lock
- Objective: Lock the evidence threshold for operational V3 use.
- Inputs: `intent.md`, `OPERATIONAL_READINESS_EVIDENCE_ROLLUP.md`.
- Outputs: threshold language in envelope and decision report inputs.
- Entry Criteria: Intent lock PASS.
- Exit Criteria: Thresholds include real pilots, fallback, halt behavior, reentry, false-positive budget, and human approval.
- Stop or Go Gate: Stop if thresholds imply V3 promotion in this run.

## MS-02 - Detection Strategy Decision
- Objective: Choose the staged combined path for deterministic and broader detection.
- Inputs: `risk_register.md`, `verification_plan.md`, current pilot reports.
- Outputs: documented approach for trigger-marker backbone plus bounded natural-language detection design.
- Entry Criteria: MS-01 complete.
- Exit Criteria: False-positive control and V3-G011 severity decision are carried forward.
- Stop or Go Gate: Stop if broader detection is proposed without review budget.

## MS-03 - Pilot Plan
- Objective: Define the next pilots required for confidence.
- Inputs: `fixtures/README.md`, `traceability_matrix.md`.
- Outputs: prioritized pilot list for interruption/reentry, V2 fallback, failed-verification, and additional real shadows.
- Entry Criteria: MS-02 complete.
- Exit Criteria: Each pilot has expected evidence and decision value.
- Stop or Go Gate: Stop if any pilot would make V3 authoritative before approval.

## MS-04 - Decision Pack Closure
- Objective: Package the plan for human review.
- Inputs: all pack artifacts.
- Outputs: manifest, checklist, audit report.
- Entry Criteria: MS-01 through MS-03 complete.
- Exit Criteria: Stage I2 PASS or CONDITIONAL PASS and pack-lint PASS.
- Stop or Go Gate: Stop if any unresolved critical finding remains.
