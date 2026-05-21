# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-21): Stage B red-team review of eval-suite planning intent.

## Iteration
- Iteration: 1 of max 2

## Summary
The intent is directionally correct, but the first-order risk is that a V3 eval-suite plan becomes too conceptual and fails to produce executable fixture contracts.

## Findings

### RT-01 - Eval suite could become narrative-only
- Severity: Critical
- Why it matters: V3 promotion would remain confidence-based if fixtures, expected outputs, and pilot report shapes are not specified.
- Fix recommendation: Require Stage F to define concrete fixture IDs, expected outcomes, and report fields.
- Agent failure mode: Agent writes persuasive docs without machine-checkable criteria.
- Verification hole: No fixture inventory or traceability to pre-mortem failures.

### RT-02 - V2 collapse criteria need stronger traceability
- Severity: High
- Why it matters: V3 could compress V2 stages while losing intent lock, adversarial review, verification, or audit guarantees.
- Fix recommendation: Require a V2 guarantee preservation matrix in the eval-suite design.
- Agent failure mode: Agent labels a V3 primitive as equivalent without proof.
- Verification hole: No negative fixture for unsafe ceremony collapse.

### RT-03 - Operational promotion could leak into this planning run
- Severity: High
- Why it matters: The run must plan evals, not authorize V3 operations.
- Fix recommendation: Keep promotion and implementation explicitly out of scope in the envelope and audit.
- Agent failure mode: Agent treats a well-designed eval plan as operational approval.
- Verification hole: No no-go check for premature promotion language.

### RT-04 - Harness capability threshold is underspecified
- Severity: Medium
- Why it matters: V3 depends on model and harness maturity, so evals need to capture tool reliability and continuity.
- Fix recommendation: Add harness capability as a required eval family and pilot report field.
- Agent failure mode: Agent assumes future harness reliability without evidence.
- Verification hole: No interruption or reentry pilot.

## Scope Expansion Review
- No scope expansion required.

## Recommended Hardening
- Add fixture contracts for ambiguous intent, missing authority, halt failure, V2 deprecation language, AEGIS boundary violation, and SIMPLE-CODE-GATE violation.
- Add pilot evidence requirements for real shadow runs, failed verification, interruption, and V2 fallback.
