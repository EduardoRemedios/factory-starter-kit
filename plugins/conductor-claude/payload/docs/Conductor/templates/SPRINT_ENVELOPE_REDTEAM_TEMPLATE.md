# docs/Conductor/templates/SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

<!--
VALIDATION:
- Create at: docs/Conductor/runs/<RUN_ID>/pack/<SPRINT_ID>_ENVELOPE_REDTEAM.md
- Must not propose implementation details; findings + fix recommendations only.
- Must include severity-ranked findings table and agent failure modes.
- Must include cross-reference check against intent_redteam.md (resurfaced issues).
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial envelope red team report.

## Inputs Reviewed (LOAD)
- <SPRINT_ID>_ENVELOPE.md
- verification_plan.md
- traceability_matrix.md
- micro_sprints.md

## Cross-Reference: Intent Red Team
- Any intent_redteam.md findings resurfaced here? YES/NO
- If YES: list IDs and why they resurfaced:
  - 

## Executive Verdict
- PASS / CONDITIONAL PASS / FAIL
- Rationale (one paragraph)

## Severity-Ranked Findings
| ID | Severity | Category | Finding | Why it matters | Fix recommendation |
|---|---|---|---|---|---|
| ER-01 | Critical |  |  |  |  |

## Agent Failure Modes (Envelope)
Trigger → symptom → mitigation (bullets).
- 

## Verification Holes
What must be verifiable but isn’t (bullets).
- 

## Scope / Drift Checks
- Any scope expansion detected? YES/NO
- If YES: list items and whether properly tagged `[SCOPE EXPANSION]` and BLOCKING.

## Minimal Patch Set
Smallest changes required to move to PASS (bullets).
- 
