# docs/Factory/templates/SPRINT_ENVELOPE_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/<SPRINT_ID>_ENVELOPE.md
- Sprint ID MUST match ../SPRINT_ID.txt and NAMING_CONVENTIONS.md §4 format.
- Must include file-touch budgets (per micro-sprint AND total) and they MUST be non-empty (DEFINITIONS.md §7).
- Any budgets outside DEFINITIONS.md guidance ranges MUST include a one-line justification.
- Must list required verification steps before merge and reference verification_plan.md and traceability_matrix.md.
- Must include explicit stop/go gates aligned to micro_sprints.md.
- Must not introduce new requirements; any new requirement MUST be tagged [SCOPE EXPANSION] and marked BLOCKING.
- Domain Areas must list only concrete values from intent.md Scope → Domain Areas; no ellipsis or placeholder lists allowed.
- Must include Iteration metadata for envelope review: Iteration: k of max 2 (used in STAGE_I cycles).
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial sprint envelope created for this run.

## Sprint Metadata
- RUN_ID: RUN_YYYYMMDD_HHMM_TAG
- Sprint ID: SPRINT_YYYYMMDD_NNN
- Owner: Project owner
- Created: YYYY-MM-DD HH:MM (local)

## Iteration (for envelope review cycles)
- Iteration: 1 of max 2

## Inputs (LOAD)
- intent.md
- micro_sprints.md
- verification_plan.md
- traceability_matrix.md

## Inputs (DISK)
- risk_register.md
- premortem.md
- intent_lock_report.md

## Purpose
One paragraph: what this sprint will achieve, in plain language.

## Scope
### In Scope
- 

### Out of Scope
- 

### Domain Areas (for fixtures)
List only values explicitly allowed by intent.md Scope → Domain Areas.
- None

## Acceptance Criteria (binary)
- AC-01: 
- AC-02: 

## Constraints (must/must-not)
Every Critical/High constraint must appear in traceability_matrix.md.
- C-01 (Critical/High/Medium/Low): 
- C-02: 

## Evidence / Receipts Expectations (if applicable)
- None

## File-Touch Budgets (HARD)
### Per Micro-sprint Budgets
| Micro-sprint ID | Modified (max) | Created (max) | Deleted (max) | Justification if outside guidance |
|---|---:|---:|---:|---|
| MS-01 |  |  |  |  |
| MS-02 |  |  |  |  |

Guidance reference: DEFINITIONS.md §7.

### Sprint Total Budget
| Modified (max) | Created (max) | Deleted (max) | Justification if outside guidance |
|---:|---:|---:|---|
|  |  |  |  |

## Execution Plan (micro-sprint sequencing)
Reference micro_sprints.md; list stop/go points explicitly.
- Gate 1 (after MS-01): 
- Gate 2 (after MS-02): 

## Verification Plan (must run before merge)
References:
- verification_plan.md
- traceability_matrix.md

Required checks:
- VP-01: 
- VP-02: 

Fixture coverage confirmation:
- “All Critical/High constraints have at least one fixture/test/check.” (YES/NO at execution time)

## Rollback / Abort Criteria
Abort if:
- 
Rollback approach:
- 

## Risks to Watch
Top risks from risk_register.md:
- R-01: 
- R-02: 

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None

## Scope Expansion Log
- None
