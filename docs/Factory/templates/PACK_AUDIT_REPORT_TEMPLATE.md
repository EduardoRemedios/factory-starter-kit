# docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/PACK_AUDIT_REPORT.md
- Produced ONLY by Purple Team stage: STAGE_I2.
- Verdict MUST be one of: PASS / CONDITIONAL PASS / FAIL.
- PACK_CHECKLIST.md is the single source-of-truth for checklist answers; do NOT duplicate the full checklist here.
- If any Critical item in PACK_CHECKLIST.md is NO, Verdict MUST be FAIL.
- Must include: verdict, references to checklist + manifest, deferral summary, scope expansion approval status, and sign-off.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial Purple audit report.

## Audit Inputs (LOAD)
- intent.md
- intent_lock_report.md
- <SPRINT_ID>_ENVELOPE.md
- traceability_matrix.md
- verification_plan.md
- micro_sprints.md
- PACK_CHECKLIST.md
- PACK_MANIFEST.md

## Verdict
- Verdict: PASS / CONDITIONAL PASS / FAIL

## Checklist Reference (source-of-truth)
- Checklist: PACK_CHECKLIST.md
- Manifest: PACK_MANIFEST.md

## Critical Failures (only if any Critical item is NO)
If any Critical checklist item is NO, list them with evidence:
- C?: <one sentence> — Evidence: <path/section>

## Deferrals Summary
List all deferrals (if any). If none, state “None”.

| Deferral ID | Description | Bounded? | Owner/Role | Micro-sprint Hook | Status |
|---|---|---|---|---|---|
| D-001 |  | YES/NO |  | MS-01 | Open/Closed |

Rules:
- Any unbounded deferral => FAIL.
- Any bounded deferral without a micro-sprint hook => FAIL.

## Scope Expansion Summary
- Any [SCOPE EXPANSION] items present? YES/NO
- If YES: list each item and approval status:
  - Item: <one sentence> — Status: APPROVED / BLOCKING — Evidence: <path>

Rule:
- Any BLOCKING scope expansion => FAIL.

## Quality Notes (only items that need explanation)
If any Quality item in PACK_CHECKLIST is NO, explain briefly:
- Q?: <explanation, 1–3 bullets>

## Cross-Document Consistency Notes (short)
Bullets confirming:
- scope boundaries match (intent ↔ envelope ↔ micro-sprints)
- verification obligations match constraint severity
- no drift introduced during envelope hardening

## Final Notes (short)
One paragraph maximum: what’s strongest, what’s riskiest during execution.

## Sign-off
- Purple Reviewer (role): 
- Date: YYYY-MM-DD
