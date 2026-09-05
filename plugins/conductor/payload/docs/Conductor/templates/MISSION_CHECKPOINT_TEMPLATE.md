# docs/Conductor/templates/MISSION_CHECKPOINT_TEMPLATE.md

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

<!--
VALIDATION:
- Create at: docs/Conductor/missions/<MISSION_ID>/MISSION_CHECKPOINT.md
- Must provide a single consolidated GO/NO-GO decision.
- Must reference mission manifest and locked scope ledger.
- Must include explicit authorization evidence (mode + human decision).
- Must include deterministic HALT and restart rules.
- No placeholders may remain in final artifacts.
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial mission checkpoint.

## Mission Metadata
- Mission ID: MISSION_YYYYMMDD_NNN
- Date: YYYY-MM-DD
- Decision owner: Project owner

## Inputs Reviewed
- MISSION_MANIFEST.md
- Mission scope ledger
- Referenced unit pack audit reports

## Consolidated Decision
- Decision: GO / NO-GO

## Critical Checks (all must be YES for GO)
| ID | Check | Answer (YES/NO) | Evidence |
|---|---|---|---|
| MC-01 | Mission unit ordering is explicit and deterministic |  | MISSION_MANIFEST.md |
| MC-02 | Scope ledger is locked and referenced |  | scope ledger path |
| MC-03 | Authorization chain is explicit (mode + human decision) |  | execution mode + decision record |
| MC-04 | No unresolved BLOCKING scope expansion remains |  | unit lock/audit reports |
| MC-05 | HALT semantics are documented and deterministic |  | this file |

## Authorization Record
- Execution mode:
- Human decision timestamp:
- Authorization reference:
- Fan-out policy:

## HALT / Restart Contract
- HALT triggers:
  - 
- Restart conditions:
  - 

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None

## Final Sign-off
- Signed by:
- Timestamp:
