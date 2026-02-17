# docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/intent_lock_report.md
- Verdict MUST be one of: PASS / CONDITIONAL PASS / FAIL.
- Any deferral MUST be classified bounded/unbounded per DEFINITIONS.md §5.
- Any bounded deferral MUST include a micro-sprint hook ID; if not yet known, mark BLOCKING and set Verdict to FAIL.
- Any [SCOPE EXPANSION] must be listed with approval status; any BLOCKING scope expansion forces FAIL.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial intent lock report.

## Inputs Reviewed (LOAD)
- intent.md
- intent_redteam.md
- intent_synthesis.md

## Verdict
- Verdict: PASS / CONDITIONAL PASS / FAIL

## Lock Summary
- What is locked (1–5 bullets):
  - 
- Scope boundaries confirmed (1–5 bullets):
  - 
- Key definitions relied on (list):
  - DEFINITIONS.md: 

## Outstanding Findings (must be empty for PASS)
- Critical:
  - None / 
- High:
  - None / 

## Deferrals
| Deferral ID | Description (one sentence) | Bounded? (YES/NO) | Owner/Role | Micro-sprint Hook ID | Why safe to defer (one sentence) |
|---|---|---|---|---|---|
| D-001 |  | YES/NO |  | MS-01 |  |

Rules:
- Any unbounded deferral => Verdict must be FAIL.
- Any missing hook ID => BLOCKING => Verdict must be FAIL.

## Scope Expansion Check
- Any [SCOPE EXPANSION] present? YES/NO
- If YES: list each item and approval status (APPROVED / BLOCKING):
  - 

Rule:
- Any BLOCKING scope expansion => Verdict must be FAIL.

## Decision Rationale (short)
One paragraph: why this verdict is correct and what would flip it.

## Next Required Actions
- If FAIL: list what must change before re-lock.
- If CONDITIONAL PASS: list exactly what must be completed downstream.
