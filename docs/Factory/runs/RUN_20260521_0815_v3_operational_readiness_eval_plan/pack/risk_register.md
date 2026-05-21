# Risk Register - V3 Operational Readiness Eval Suite

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E risk register.

| Risk ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-01 | Critical | Eval suite becomes narrative-only. | Require fixture inventory and expected output schema. | VP-01, VP-02 |
| R-02 | Critical | V3 collapses V2 stages without equivalent guarantees. | Require V2 guarantee preservation matrix. | VP-03 |
| R-03 | Critical | V3 promotion language slips into planning artifacts. | Add no-promotion checks and audit review. | VP-04 |
| R-04 | High | Golden fixtures overfit to clean-pass cases. | Require negative fixtures for ambiguity, scope, authority, halt, and boundary failures. | VP-02 |
| R-05 | High | Harness reliability is assumed rather than measured. | Require harness capability fields in pilot templates. | VP-05 |
| R-06 | High | AEGIS boundary is blurred by mission authority terms. | Include boundary fixture and adapter-safe positive case. | VP-06 |
| R-07 | High | SIMPLE-CODE-GATE is omitted from V3 code-work evals. | Include over-abstraction and dependency-creep fixture. | VP-07 |
| R-08 | Medium | Planning pack is too broad for a first implementation sprint. | Sequence work into fixture contract, report schema, and runner implementation micro-sprints. | VP-08 |

## Residual Risk
First eval implementation may still need tuning after real pilots. That risk is acceptable only if the first implementation remains advisory and does not promote V3.
