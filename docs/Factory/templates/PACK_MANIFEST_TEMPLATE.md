# docs/Factory/templates/PACK_MANIFEST_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/pack/PACK_MANIFEST.md
- Validation scope is completeness only: existence + non-empty checks; no content parsing required.
- Required pack files MUST match docs/Factory/Spec/NAMING_CONVENTIONS.md §5.
- Required run-root files MUST match docs/Factory/Spec/NAMING_CONVENTIONS.md §2.
- Every listed path MUST exist relative to the run root and MUST be non-empty.
- Sprint ID in this manifest MUST match ../SPRINT_ID.txt.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1

## Change Log
- v1 (YYYY-MM-DD): Initial manifest for this run.

## Run Metadata
- RUN_ID: RUN_YYYYMMDD_HHMM_TAG
- Sprint ID: SPRINT_YYYYMMDD_NNN
- Created: YYYY-MM-DD HH:MM (local)
- Owner: Project owner
- Spec Versions:
  - NAMING_CONVENTIONS: v?
  - DEFINITIONS: v?
  - STAGE_CONTRACTS: v?
  - PURPLE_GATE_CHECKLIST: v?

## Required Files (Run Root)
- ../raw_brief.md
- ../SPRINT_ID.txt

## Required Files (Pack)
Core:
- intent.md
- intent_redteam.md
- intent_synthesis.md
- intent_lock_report.md
- premortem.md
- risk_register.md
- verification_plan.md
- micro_sprints.md

Envelope:
- <SPRINT_ID>_ENVELOPE.md
- <SPRINT_ID>_ENVELOPE_REDTEAM.md

Verification Assets:
- fixtures/ (directory; must exist; must contain at least 1 fixture directory)
- traceability_matrix.md

Pack Gates:
- PACK_AUDIT_REPORT.md
- PACK_CHECKLIST.md
- PACK_MANIFEST.md

Handoffs:
- HANDOFF/ (directory; must exist)
  - HANDOFF_STAGE_A.md
  - HANDOFF_STAGE_B.md
  - HANDOFF_STAGE_C.md
  - HANDOFF_STAGE_D.md
  - HANDOFF_STAGE_E.md
  - HANDOFF_STAGE_F.md
  - HANDOFF_STAGE_G.md
  - HANDOFF_STAGE_H.md
  - HANDOFF_STAGE_I.md
  - HANDOFF_STAGE_I2.md
  - HANDOFF_STAGE_J.md
  - (optional) HANDOFF_SUMMARY.md

## Non-Empty Confirmation (Checklist)
Mark each item YES/NO. If NO, the pack is invalid.

Run root:
- ../raw_brief.md: YES/NO
- ../SPRINT_ID.txt: YES/NO

Pack core:
- intent.md: YES/NO
- intent_redteam.md: YES/NO
- intent_synthesis.md: YES/NO
- intent_lock_report.md: YES/NO
- premortem.md: YES/NO
- risk_register.md: YES/NO
- verification_plan.md: YES/NO
- micro_sprints.md: YES/NO

Envelope:
- <SPRINT_ID>_ENVELOPE.md: YES/NO
- <SPRINT_ID>_ENVELOPE_REDTEAM.md: YES/NO

Verification assets:
- fixtures/ exists: YES/NO
- fixtures/ contains ≥1 fixture: YES/NO
- traceability_matrix.md: YES/NO

Pack gates:
- PACK_AUDIT_REPORT.md: YES/NO
- PACK_CHECKLIST.md: YES/NO
- PACK_MANIFEST.md: YES/NO

Handoffs:
- HANDOFF/ exists: YES/NO
- HANDOFF_STAGE_A.md: YES/NO
- HANDOFF_STAGE_B.md: YES/NO
- HANDOFF_STAGE_C.md: YES/NO
- HANDOFF_STAGE_D.md: YES/NO
- HANDOFF_STAGE_E.md: YES/NO
- HANDOFF_STAGE_F.md: YES/NO
- HANDOFF_STAGE_G.md: YES/NO
- HANDOFF_STAGE_H.md: YES/NO
- HANDOFF_STAGE_I.md: YES/NO
- HANDOFF_STAGE_I2.md: YES/NO
- HANDOFF_STAGE_J.md: YES/NO

## Notes
- Any missing or empty required file = FAIL (pack invalid).
