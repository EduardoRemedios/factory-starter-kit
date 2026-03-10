# docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md

<!--
VALIDATION:
- Each stage MUST create: docs/Factory/runs/<RUN_ID>/pack/HANDOFF/HANDOFF_STAGE_<STAGE_ID>.md
- Word cap: ≤ 500 words, bullets only (DEFINITIONS.md).
- Must include: Outputs, Changes, Assumptions, Open issues (BLOCKING/NON-BLOCKING), Verification steps, Exit criteria PASS/FAIL.
- Must include: Skill Routing Contract (skill name or `NONE`, use-when, do-not-use-when, expected outputs).
- Must include: Model tier used, Contradiction status, Applicable hard rules (per AgentArchitecture/MODEL_ROUTING_POLICY.md and GATE_ENFORCEMENT_CONTRACT.md).
- Must include Stage ID and timestamp.
- If the stage is a cycle stage (STAGE_B, STAGE_C, STAGE_I), must include: Iteration: k of max 2.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1.2

## Change Log
- v1.2 (2026-02-18): Added Model tier used, Contradiction status, and Applicable hard rules per AgentArchitecture (MODEL_ROUTING_POLICY, GATE_ENFORCEMENT_CONTRACT).
- v1.1 (2026-02-12): Added required Skill Routing Contract section to make skill invocation boundaries explicit in stage handoffs.
- v1 (YYYY-MM-DD): Initial handoff file for this stage.

## Stage
- Stage ID: STAGE_<...>
- Stage Name: 
- Timestamp: YYYY-MM-DD HH:MM (local)
- Model tier used: High-reasoning | Medium | Cost-optimized (per docs/Factory/AgentArchitecture/MODEL_ROUTING_POLICY.md)
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

## Exit Criteria Status
- PASS / FAIL

## If FAIL (required only if FAIL)
- Why it failed:
  - 
- What must change before retry:
  - 
