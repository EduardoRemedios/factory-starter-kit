## Version
- v1

## Change Log
- v1 (2026-08-10): Attacked intent v1.

## Stage
- Stage ID: STAGE_B
- Stage Name: Intent Red Team
- Timestamp: 2026-08-10 18:25 WEST
- Execution profile used: High-reasoning
- Contradiction status: Hardening required; no scope contradiction.
- Applicable hard rules: Findings include severity, impact, fixes, agent failures, and verification holes.

## Iteration
- Iteration: 1 of max 2

## Inputs (LOAD)
- `pack/intent.md` v1.

## Inputs (DISK)
- `../CONTEXT_RECALL_REPORT.md`

## Skill Routing Contract
- Skill used: NONE
- Use when: no more specific intent Red Team skill exists.
- Do not use when: Purple adjudication.
- Expected output artifact: `pack/intent_redteam.md`.

## Outputs Produced (paths)
- `pack/intent_redteam.md` v1.

## Changes Made
- Identified seven bounded weaknesses.

## Assumptions
- The upstream installer is third-party state.

## Open Issues
### BLOCKING
- None after required Blue hardening.
### NON-BLOCKING
- Codex live support remains deferred.

## Verification Steps Recommended
- Live dependency, partial install, ownership conflict, and concise-output golden checks.

## Exit Criteria Status
- PASS
