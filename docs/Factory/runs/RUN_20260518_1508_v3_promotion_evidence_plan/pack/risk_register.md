# Risk Register - Promotion-Evidence Advisory Lint Planning

## Version
v1

## Change Log
- v1 (2026-05-18): Initial risk register for promotion-evidence advisory lint planning.

| ID | Risk | Severity | Mitigation | Verification Hook |
| --- | --- | --- | --- | --- |
| R-001 | Temporary promotion or release wording remains in final docs. | High | Require remediation and final clean advisory run. | V1-CHECK-001, V1-CHECK-003 |
| R-002 | Pilot evidence is misread as Factory v3 promotion. | Critical | State no promotion in envelope, report, and checklist. | V0-REVIEW-001 |
| R-003 | Advisory lint is wired into required gates. | Critical | Exclude required gate files from file-touch budget. | V1-CHECK-002 |
| R-004 | Matcher tuning happens without clear evidence. | High | Keep matcher tuning out of scope and require later approval. | V0-REVIEW-002 |
| R-005 | AEGIS dependency or runtime-kernel claim appears. | Critical | Require boundary review against `AEGIS_BOUNDARY.md`. | V0-REVIEW-003 |
| R-006 | Finding classification is incomplete. | High | Require classification table with four allowed statuses. | V0-REVIEW-004 |

