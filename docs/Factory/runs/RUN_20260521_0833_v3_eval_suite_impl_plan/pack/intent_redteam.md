# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-21): Stage B red-team review.

## Iteration
- Iteration: 1 of max 2

## Findings

### RT-01 - Runner may become a generic policy framework
- Severity: Critical
- Why it matters: That would violate SIMPLE-CODE-GATE and create bloat.
- Fix recommendation: Require explicit local checks for the first fixture set.
- Agent failure mode: Agent adds plugin registries or strategy layers.
- Verification hole: No check for dependency creep.

### RT-02 - Eval output could imply promotion
- Severity: Critical
- Why it matters: Advisory PASS must not equal operational approval.
- Fix recommendation: Output must include `blocking_effect: none` and `promotion_decision: not_authorized`.
- Agent failure mode: Agent markets clean fixtures as release readiness.
- Verification hole: No promotion-language fixture.

### RT-03 - Fixture set may miss V2 fallback
- Severity: High
- Why it matters: User wants V2 retained as an option.
- Fix recommendation: Require V3-G007, V3-G012, and V3-G013 in first implementation.
- Agent failure mode: Agent focuses only on V3 mission envelope fields.
- Verification hole: No deprecation negative case.

### RT-04 - Report fields may be empty shells
- Severity: Medium
- Why it matters: A report schema without source-backed fields is weak evidence.
- Fix recommendation: Require fixture output to list checked files and finding reasons.
- Agent failure mode: Agent emits structured but content-free JSON.
- Verification hole: No expected JSON assertion.
