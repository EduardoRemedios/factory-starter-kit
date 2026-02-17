# docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/PACK_CHECKLIST.md
- This file is the run-specific instantiation of docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md.
- Items MUST match the spec 1:1 in IDs and wording (C1–C9, K1–K2, Q1–Q3).
- Each checklist item MUST be one sentence and answerable YES/NO (or YES/NO/NA where specified).
- Each item MUST include an Evidence field pointing to an artifact path (and section if applicable).
- If any Critical item is NO, overall outcome MUST be FAIL.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1.1

## Change Log
- v1.1 (2026-02-11): Added C9 knowledge-lint critical item and run-root evidence reference.
- v1 (YYYY-MM-DD): Initial checklist for this run.

## Overall Outcome
- Outcome: PASS / CONDITIONAL PASS / FAIL
- Determined By: Purple Audit (PACK_AUDIT_REPORT.md)

## Critical (must all be YES for PASS/CONDITIONAL PASS)
C1. All required artifacts exist and are non-empty. | Answer: YES/NO | Evidence: PACK_MANIFEST.md
C2. intent.md is contract-grade per DEFINITIONS.md §8. | Answer: YES/NO | Evidence: intent.md
C3. No unresolved Critical findings remain from intent or envelope red teams. | Answer: YES/NO | Evidence: intent_redteam.md; <SPRINT_ID>_ENVELOPE_REDTEAM.md
C4. Every Critical/High constraint has verification coverage (traceability complete). | Answer: YES/NO | Evidence: traceability_matrix.md
C5. Sprint envelope includes file-touch budgets and they are non-empty. | Answer: YES/NO | Evidence: <SPRINT_ID>_ENVELOPE.md
C6. Micro-sprints include entry/exit criteria and stop/go gates. | Answer: YES/NO | Evidence: micro_sprints.md
C7. No unbounded deferrals exist. | Answer: YES/NO | Evidence: intent_lock_report.md; PACK_AUDIT_REPORT.md
C8. No [SCOPE EXPANSION] items remain unapproved (none BLOCKING). | Answer: YES/NO | Evidence: intent.md; intent_synthesis.md; PACK_AUDIT_REPORT.md
C9. Knowledge lint preflight passed and evidence artifact is present in run root (`KNOWLEDGE_LINT.txt`). | Answer: YES/NO | Evidence: ../KNOWLEDGE_LINT.txt

## Conditional (required for CONDITIONAL PASS)
K1. Every deferral is bounded per DEFINITIONS.md §5. | Answer: YES/NO/NA | Evidence: intent_lock_report.md
K2. Each bounded deferral is hooked in micro_sprints.md with a micro-sprint ID. | Answer: YES/NO/NA | Evidence: micro_sprints.md

## Quality (can be NO, but must be explained in PACK_AUDIT_REPORT.md)
Q1. Size caps are satisfied for all artifacts. | Answer: YES/NO | Evidence: HANDOFF/HANDOFF_STAGE_J.md
Q2. Scope boundaries match across intent, envelope, and micro-sprints. | Answer: YES/NO | Evidence: intent.md; <SPRINT_ID>_ENVELOPE.md; micro_sprints.md
Q3. No [INFERRED] requirements remain unapproved. | Answer: YES/NO | Evidence: intent.md; intent_synthesis.md; PACK_AUDIT_REPORT.md

## Notes (optional)
- Keep notes short; explanations belong in PACK_AUDIT_REPORT.md.
