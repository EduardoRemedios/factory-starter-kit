# docs/Factory/templates/MISSION_COMPLETION_REPORT_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/missions/<MISSION_ID>/MISSION_COMPLETION_REPORT.md
- Must include outcome for each mission unit (completed/failed/skipped).
- Must include HALT reason if mission did not complete.
- Must include evidence reconciliation links for all executed units.
- Must include restart recommendation when halted.
- No placeholders may remain in final artifacts.
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial mission completion report.

## Mission Metadata
- Mission ID:
- Start:
- End:
- Final State: MISSION_COMPLETED / MISSION_HALTED

## Unit Outcome Summary
| Order | RUN_ID | SPRINT_ID | Outcome | Verification Status | Evidence Paths |
|---:|---|---|---|---|---|
| 1 | RUN_... | SPRINT_... | completed | PASS | <paths> |
| 2 | RUN_... | SPRINT_... | failed | FAIL | <paths> |
| 3 | RUN_... | SPRINT_... | skipped | N/A | <paths> |

## HALT Summary (required if halted)
- Halt trigger:
- Halted at unit:
- Policy violation ID (if applicable):
- Evidence:

## Evidence Reconciliation
- Mission manifest reference:
- Checkpoint reference:
- Per-unit audit references:

## Scope and Authorization Integrity Check
- Scope ledger unchanged? YES/NO
- Authorization still valid at termination? YES/NO
- Any unapproved scope expansion detected? YES/NO

## Restart Recommendation
- Resume from:
- Preconditions:
  - 

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None
