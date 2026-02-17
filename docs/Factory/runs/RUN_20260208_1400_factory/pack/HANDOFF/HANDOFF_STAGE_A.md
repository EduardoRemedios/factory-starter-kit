## Version
v1

## Change Log
- v1 (2026-02-08): Initial handoff file for Stage A.

## Stage
- Stage ID: STAGE_A
- Stage Name: Intent Contracting
- Timestamp: 2026-02-08 14:00 (local)

## Inputs (LOAD)
- raw_brief.md (358 lines, APPROVED status, authored 2026-02-08)

## Inputs (DISK)
- docs/HARMONY_STATE.md
- docs/ROADMAP.md
- docs/AUTH_MODEL.md
- docs/HARMONY_V2_SYSTEM_INVARIANTS.md
- docs/RISK_REGISTER.md
- runtime/policy_engine.py
- runtime/schemas.py

## Outputs Produced (paths)
- pack/intent.md (v1)

## Changes Made
- Converted raw brief into contract-grade intent with all required sections
- Sourced every requirement with [SOURCE:RAW] or [SOURCE:REF:path] tags
- Classified 17 constraints by impact severity (9 Critical, 5 High, 3 Medium)
- Defined 9 binary acceptance criteria
- Identified 2 NON-BLOCKING open questions (legacy path unification, action_id naming)
- Defined 3 domain areas for fixtures: routing, policy, verification
- No BLOCKING open questions identified

## Assumptions
- Sprint A builds on Phase 0 closure; all 43 tests and CI are green
- The adapter contract shape in the raw brief is authoritative (not the fuller shape from AUTH_MODEL.md §9 which includes player-auth hooks — those are explicitly out of scope per the brief)
- `action_type` vs `action_id` distinction is documented but not a rename task for Sprint A
- Confirmation stub is intentionally minimal to avoid building a mini-UVS

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- OQ-01: Legacy path unification (decide() vs evaluate_request()) — recommended for Sprint A but not mandated by brief
- OQ-02: action_id/action_type naming inconsistency — document distinction, no rename

## Verification Steps Recommended
- Confirm intent.md has all required sections: Purpose, Goal, Non-goals, Principles, Roles, Acceptance Criteria, Go/No-Go
- Confirm all requirements are sourced or tagged [INFERRED]
- Confirm open questions labeled BLOCKING/NON-BLOCKING
- Confirm size cap (≤1,200 words) is met

## Exit Criteria Status
- PASS
