# Traceability Matrix — Factory-BMAD 0.2.5 Integration

## Version
v2

## Change Log
- v1 (2026-09-02): Mapped locked Critical/High constraints and risks to exact verification.
- v2 (2026-09-03): Manifest-repair correction: VM-011 was listed only under risk coverage; it now also appears in the C-004 verification cell so the matrix column matches the plan and manifest inventories.

| Constraint ID | Severity | Statement | Source | Scope Tag | Tier | Verification | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical | Factory/Conductor plus human Go retains implementation authority. | [SOURCE:RAW] | OK | V3 | VM-007, VM-008, VM-015 | `fixtures/policy/authority_boundary/` |
| C-002 | Critical | 0.2.5 safeguards and command compatibility do not regress. | [SOURCE:RAW] | OK | V3 | VM-003, VM-004 | `fixtures/integration/collision_contract/` |
| C-003 | Critical | Unsafe, unknown, and prohibited BMAD paths fail closed. | [SOURCE:RAW] | OK | V3 | VM-005, VM-006 | `fixtures/policy/authority_boundary/` |
| C-004 | Critical | Solution-context promotion is immutable and non-authorizing. | [SOURCE:RAW] | OK | V3 | VM-007, VM-008, VM-011 | `fixtures/policy/authority_boundary/` |
| C-005 | Critical | Donor, Core, Git/config, dependency, and unrelated state remains protected. | [SOURCE:RAW] | OK | V4 | VM-001, VM-010 | `fixtures/integration/donor_contract/` |
| C-006 | High | Generated packages derive through one canonical rebuild. | [SOURCE:RAW] | OK | V3 | VM-009, VM-013 | `fixtures/verification/source_coupling/` |
| C-007 | High | Public layout compatibility and granular evidence coexist. | [SOURCE:RAW] | OK | V3 | VM-005 | `fixtures/integration/collision_contract/` |
| C-008 | High | Both donors' non-equivalent regressions remain covered. | [SOURCE:RAW] | OK | V3 | VM-003, VM-004, VM-012 | `fixtures/integration/collision_contract/` |
| C-009 | High | Documentation claims stay within deterministic evidence. | [SOURCE:RAW] | OK | V3 | VM-002, VM-015 | `verification_plan.md` |
| C-010 | High | Paths, budgets, commands, builder counts, evidence, and status are fixed. | [SOURCE:RAW] | OK | V3 | VM-013, VM-014, VM-015 | `fixtures/verification/source_coupling/` |

## Risk Coverage
- R-001: VM-001; R-002: VM-002, VM-015; R-003: VM-003, VM-004; R-004: VM-004.
- R-005: VM-005; R-006: VM-005, VM-006; R-007: VM-006; R-008: VM-007, VM-008.
- R-009: VM-009; R-010: VM-010; R-011: VM-008; R-012: VM-011.
- R-013: VM-012; R-014: VM-013; R-015: VM-014; R-016: VM-015.

## Coverage Summary
- Critical: 5/5 covered at V3-V4.
- High: 5/5 covered at V3-V4.
- Verification inventory is VM-001 through VM-015 and exactly matches `verification_plan.md`.
- No Critical/High V0 coverage and no unbounded deferral.
