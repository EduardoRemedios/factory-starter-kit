# docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md

<!--
VALIDATION:
- Each stage MUST create: docs/Factory/runs/<RUN_ID>/pack/HANDOFF/HANDOFF_STAGE_<STAGE_ID>.md
- Word cap: ≤ 500 words, bullets only (DEFINITIONS.md).
- Must include: Outputs, Changes, Assumptions, Open issues (BLOCKING/NON-BLOCKING), Verification steps, Exit criteria PASS/FAIL.
- Must include: Skill Routing Contract (skill name or `NONE`, use-when, do-not-use-when, expected outputs).
- Must include: execution profile used, contradiction status, and applicable hard rules.
- If this handoff is also a branch/PR handoff, must include Repository Handoff State using REVIEW_READY or MERGE_READY per MERGE_PROTOCOL.md.
- Must include Stage ID and timestamp.
- If the stage is a cycle stage (STAGE_B, STAGE_C, STAGE_I), must include: Iteration: k of max 2.
- No placeholders may remain.
-->

## Version
v1.4

## Change Log
- v1.4 (2026-06-24): Added optional Repository Handoff State section for branch/PR review versus merge readiness.
- v1.3 (2026-03-21): Removed the dead AgentArchitecture dependency and replaced it with a generic execution-profile field.
- v1.2 (2026-02-18): Added execution profile used, contradiction status, and applicable hard rules.
- v1.1 (2026-02-12): Added required Skill Routing Contract section to make skill invocation boundaries explicit in stage handoffs.
- v1 (YYYY-MM-DD): Initial handoff file for this stage.

## Stage
- Stage ID: STAGE_<...>
- Stage Name:
- Timestamp: YYYY-MM-DD HH:MM (local)
- Execution profile used: Standard | High-reasoning | Cost-optimized
- Contradiction status: No contradiction with locked intent detected | Contradiction detected: <description> — BLOCKING, escalate.
- Applicable hard rules: STAGE_CONTRACTS <Stage ID> exit criteria satisfied (or list any not satisfied).

## Iteration (required for cycle stages only)
- Iteration: k of max 2

## Inputs (LOAD)
-

## Inputs (DISK)
-

## Skill Routing Contract
- Skill used (or `NONE`):
- Use when:
- Do not use when:
- Expected output artifact(s):

## Outputs Produced (paths)
-

## Changes Made
-

## Assumptions
-

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None

## Verification Steps Recommended
-

## Repository Handoff State (required only for branch/PR handoff)
- Handoff state: NOT_APPLICABLE | REVIEW_READY | MERGE_READY
- Final sync window: NOT_APPLICABLE | CLOSED | OPEN
- Base ref / SHA: NOT_APPLICABLE
- Head SHA: NOT_APPLICABLE
- Merge preflight summary path: NOT_APPLICABLE
- Review evidence summary:
  -
- Known stale or open items:
  - None

## Exit Criteria Status
- PASS / FAIL

## If FAIL (required only if FAIL)
- Why it failed:
  -
- What must change before retry:
  -
