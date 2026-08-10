# Traceability Matrix — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Mapped locked constraints to executable proof.

| Constraint | Severity | Statement | Source | Scope | Tier | Verification | Artifact |
|---|---|---|---|---|---|---|---|
| C-01 | Critical | Factory sole authority; no Core copy | [SOURCE:RAW] | OK | V2 | VM-001, VM-003 | `verification_plan.md` |
| C-02 | Critical | Five routes; diagnosis/preview no-write | [SOURCE:RAW] | OK | V2 | VM-002 | `fixtures/routing/state_matrix/` |
| C-03 | Critical | Pin 6.10.0 Core+BMM; exclude loop/TEA | [SOURCE:RAW] | OK | V4 | VM-002, VM-011 | `fixtures/bmad-bootstrap/pinned_install/` |
| C-04 | Critical | Exact install approval and proof-bounded recovery | [SOURCE:RAW] | OK | V2 | VM-002 | `verification_plan.md` |
| C-05 | Critical | No silent module changes; loop blocks; TEA evidence only | [SOURCE:RAW] | OK | V2 | VM-003 | `fixtures/authority-policy/module_matrix/` |
| C-06 | Critical | Promotion path, staleness, immutability safety | [SOURCE:RAW] | OK | V2 | VM-004 | `fixtures/upstream-promotion/promotion_matrix/` |
| C-07 | Critical | Snapshot provenance, digest, receipt, rollback | [SOURCE:RAW] | OK | V2 | VM-004 | `fixtures/upstream-promotion/promotion_matrix/` |
| C-08 | Critical | Existing Factory preflight fails closed | [SOURCE:RAW] | OK | V2 | VM-005 | `fixtures/factory-intake/preflight_matrix/` |
| C-09 | High | Installed BMM capability is not permitted authority | [SOURCE:RAW] | OK | V2 | VM-003, VM-005 | `fixtures/authority-policy/module_matrix/` |
| C-10 | High | Embedded brief checklist and frozen snapshot pins | [SOURCE:RAW] | OK | V2 | VM-005 | `fixtures/factory-intake/preflight_matrix/` |
| C-11 | High | Versioned Factory dependency; negative states halt | [SOURCE:RAW] | OK | V4 | VM-006 | `verification_plan.md` |
| C-12 | High | Companion ownership never overwrites project files | [SOURCE:RAW] | OK | V2 | VM-001, VM-005, VM-008 | `verification_plan.md` |
| C-13 | High | Concise default; JSON opt-in; no settings hash churn | [SOURCE:RAW] | OK | V2 | VM-009 | `fixtures/claude-code-ux/summary_output/` |
| C-14 | High | Public artifacts customer-neutral and private-safe | [SOURCE:RAW] | OK | V1 | VM-007 | `verification_plan.md` |
| C-15 | High | SIMPLE-CODE-GATE; no unapproved dependency | [SOURCE:RAW] | OK | V3 | VM-001, VM-008, VM-010 | `verification_plan.md` |

## Coverage Summary

- Critical constraints covered: 8 of 8.
- High constraints covered: 7 of 7.
- `[INFERRED]` requirements: none.
- `[SCOPE EXPANSION]` requirements: none.
