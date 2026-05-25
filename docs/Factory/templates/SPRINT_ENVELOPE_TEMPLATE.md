# docs/Factory/templates/SPRINT_ENVELOPE_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/<SPRINT_ID>_ENVELOPE.md
- Sprint ID MUST match ../SPRINT_ID.txt and NAMING_CONVENTIONS.md §4 format.
- Must include file-touch budgets (per micro-sprint AND total) and they MUST be non-empty (DEFINITIONS.md §7).
- Any budgets outside DEFINITIONS.md guidance ranges MUST include a one-line justification.
- Must list required verification steps before merge and reference verification_plan.md and traceability_matrix.md.
- If verification_manifest.yaml exists, must reference it and summarize how execution should consume it.
- Must include explicit stop/go gates aligned to micro_sprints.md.
- Must not introduce new requirements; any new requirement MUST be tagged [SCOPE EXPANSION] and marked BLOCKING.
- For Factory-controlled code-changing sprints, must include SIMPLE-CODE-GATE v2 as an implementation constraint.
- Domain Areas must list only concrete values from intent.md Scope → Domain Areas; no ellipsis or placeholder lists allowed.
- Must include Iteration metadata for envelope review: Iteration: k of max 2 (used in STAGE_I cycles).
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1.1

## Change Log
- v1.1 (2026-05-19): Added SIMPLE-CODE-GATE v2 implementation constraint for Factory-controlled code-changing sprints.
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
- verification_manifest.yaml (optional)

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

### SIMPLE-CODE-GATE (v2) Constraint (for code-changing sprints)
Mandatory guardrail for Factory-controlled implementation work.

- Implement the smallest clear, behavior-preserving change.
- Prefer direct, readable, local code over cleverness or premature abstraction.
- Avoid copy-paste chunks, awkward abstraction layers, bloated multi-purpose helpers, brittle request-path mutation, hidden side effects, dependency creep, and silent failure swallowing.
- Add abstractions only when they remove real duplication, name a stable domain concept, reduce branching or call-site complexity, and have a clear owner/boundary.
- Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection for speculative future variation.
- If future variation is uncertain, keep the code explicit and document the specific scale metric, repeated pattern, or business condition that will trigger a refactor.
- Comments must explain why, not what.

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
- Gate 0 (optional MS-00 verification scaffold):
- Gate 1 (after MS-01): 
- Gate 2 (after MS-02): 

## Verification Plan (must run before merge)
References:
- verification_plan.md
- traceability_matrix.md
- verification_manifest.yaml (optional; required to reference here if present)

Required checks:
- VP-01: 
- VP-02: 

Verification tier summary:
- V0 artifact proof:
- V1 static/mechanical:
- V2 focused fixture/test:
- V3 regression/conformance:
- V4 live/external/source revalidation:

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
