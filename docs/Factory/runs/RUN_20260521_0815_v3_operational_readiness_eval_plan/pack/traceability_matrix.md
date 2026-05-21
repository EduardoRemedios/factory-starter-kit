# Traceability Matrix - V3 Operational Readiness Eval Suite

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F traceability matrix.

| Constraint | Severity | Verification | Tier | Evidence |
|---|---|---|---|---|
| C-01 V3 remains research-only in this run. | Critical | VP-04 | V1 | `intent.md`; `SPRINT_20260521_013_ENVELOPE.md` |
| C-02 V2 remains supported and available as fallback. | Critical | VP-04 | V1 | `intent.md`; `SPRINT_20260521_013_ENVELOPE.md` |
| C-03 V3 collapse of V2 ceremony requires equivalent guarantee preservation. | Critical | VP-03 | V2 | this matrix |
| C-04 Eval design starts from pre-mortem failure modes. | High | VP-01 | V1 | `premortem.md`; fixture inventory |
| C-05 Golden fixtures include negative cases. | High | VP-02 | V2 | fixture inventory |
| C-06 AEGIS and runtime-kernel boundaries remain intact. | High | VP-06 | V2 | fixture inventory |
| C-07 SIMPLE-CODE-GATE v2 is represented for code-changing V3 work. | High | VP-07 | V2 | fixture inventory |

## V2 Guarantee Preservation Matrix
| V2 Guarantee | V3 Candidate | Required Eval Signal |
|---|---|---|
| Intent lock | Mission objective and success criteria | ambiguity fixture fails |
| Constraint lock | Authority lease and mission boundaries | missing authority fixture fails |
| Risk analysis | Mission pre-mortem hooks | every failure mode maps to fixture or pilot |
| Verification plan | Continuous verification contract | failed verification halts |
| Envelope review | Mission envelope | incomplete envelope fails |
| Red/Blue/Purple review | Mission review and audit gates | unresolved critical finding blocks |
| Pack audit | Operational readiness decision | missing human approval fails |
| Closeout evidence | Mission evidence bundle | missing command or decision evidence fails |
