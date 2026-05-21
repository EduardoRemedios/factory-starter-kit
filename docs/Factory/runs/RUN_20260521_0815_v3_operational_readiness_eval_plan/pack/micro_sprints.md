# Micro-sprints - V3 Operational Readiness Eval Suite

## Version
v1

## Change Log
- v1 (2026-05-21): Stage G micro-sprint sequence.

## MS-01 - Pre-mortem To Fixture Contract
- Objective: Convert V3 pre-mortem failures into exact fixture IDs, inputs, expected outcomes, and reason codes.
- Inputs: `premortem.md`, `risk_register.md`, `OPERATIONAL_READINESS_EVAL_PLAN.md`.
- Outputs: fixture inventory and expected output contract.
- Entry criteria: locked intent PASS.
- Exit criteria: every Critical and High failure mode maps to fixture or pilot evidence.
- Stop/Go gate: stop if any Critical failure mode lacks coverage.

## MS-02 - Eval Report And Pilot Templates
- Objective: Define report schema and pilot evidence templates for shadow runs, interruption, failed verification, and V2 fallback.
- Inputs: fixture contract, `PROMOTION_CRITERIA.md`, `PILOT_PROFILE_PLAN.md`.
- Outputs: decision report template and pilot evidence template.
- Entry criteria: MS-01 passed.
- Exit criteria: templates include model, harness, revision, artifacts, fixture results, false positives, false negatives, overhead, decision, and residual risks.
- Stop/Go gate: stop if evidence fields cannot support a promotion decision.

## MS-03 - Future Runner Planning Only
- Objective: Plan later implementation boundaries without selecting technology in this run.
- Inputs: fixture contract and report template.
- Outputs: future execution brief for eval runner implementation.
- Entry criteria: MS-02 passed.
- Exit criteria: implementation remains separate, advisory first, and SIMPLE-CODE-GATE compliant.
- Stop/Go gate: stop if implementation would wire V3 into required gates without a new approval.
- Deferral hook: D-001 future eval-runner implementation language.

## MS-04 - Red/Blue/Purple Operational Readiness Review
- Objective: Review the eval suite design before any future implementation.
- Inputs: all prior outputs.
- Outputs: review notes and decision report readiness status.
- Entry criteria: MS-03 passed.
- Exit criteria: no unresolved Critical findings and no V3 promotion language.
- Stop/Go gate: stop if V2 fallback, AEGIS boundary, or verification halt behavior is unclear.
