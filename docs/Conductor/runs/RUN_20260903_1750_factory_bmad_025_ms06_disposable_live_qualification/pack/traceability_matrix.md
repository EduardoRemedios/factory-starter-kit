# Traceability Matrix — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Mapped locked constraints and registered risks to exact verification.

| Constraint ID | Severity | Statement | Source | Scope Tag | Tier | Verification | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical | Factory/Conductor plus human Go retain all implementation and delivery authority. | [SOURCE:RAW] | OK | V4 | VM-004, VM-005, VM-010 | `fixtures/live/qualification_contract/` |
| C-002 | Critical | Qualified candidate, Factory Core, donors, and unrelated state remain byte-identical. | [SOURCE:RAW] | OK | V4 | VM-001, VM-008 | `fixtures/live/qualification_contract/` |
| C-003 | Critical | Prohibited, unknown, malformed, and unsafe paths fail closed live. | [SOURCE:RAW] | OK | V4 | VM-005 | `fixtures/live/qualification_contract/` |
| C-004 | Critical | Promotion is immutable, human-reviewed, provenance-bound, and non-authorizing. | [SOURCE:RAW] | OK | V4 | VM-004, VM-006 | `fixtures/live/qualification_contract/` |
| C-005 | Critical | The disposable repository is contained, pinned, and destroyed with evidence. | [SOURCE:RAW] | OK | V4 | VM-002, VM-007, VM-008 | `fixtures/live/qualification_contract/` |
| C-006 | High | Live proofs cover both allowed authoring and denial families. | [SOURCE:RAW] | OK | V4 | VM-003, VM-005 | `fixtures/live/qualification_contract/` |
| C-007 | High | Evidence, budgets, commands, and status claims remain exact and bounded. | [SOURCE:RAW] | OK | V3 | VM-007, VM-009, VM-010 | `verification_plan.md` |

## Risk Coverage
- R-001: VM-001, VM-003; R-002: VM-002; R-003: VM-007; R-004: VM-001.
- R-005: VM-005; R-006: VM-004; R-007: VM-005; R-008: VM-006.
- R-009: VM-008; R-010: VM-009; R-011: VM-010; R-012: VM-009, VM-010.

## Coverage Summary
- Critical: 5/5 covered at V3-V4; High: 2/2 covered at V3-V4.
- Verification inventory is VM-001 through VM-010 and exactly matches `verification_plan.md` and `verification_manifest.yaml`.
- No Critical/High V0 coverage and no unbounded deferral.
