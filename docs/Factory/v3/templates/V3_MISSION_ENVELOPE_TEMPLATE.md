# V3 Mission Envelope Template

## Status
Template for optional `V3-OP-001` use. It is based on approved research evidence and remains non-enforcing for required repository gates.

## Profile
- Profile ID: `V3-OP-001`
- Profile name: Bounded Code Change
- Factory v2 fallback retained: YES

## Objective
-

## Success Criteria
-

## Eligible-Work Rationale
-

## Non-Goals
-

## Authorized Scope
Files and directories:
-

## Forbidden Scope
Files, directories, systems, or concerns:
-

## Allowed Commands
-

## Dependency Policy
- New dependencies allowed: YES/NO
- If YES, human approval path:

## Verification
Commands and expected evidence:
-

## Halt Rules
Stop if:
-

## Interruption And Reentry
- Resume only from authored artifacts and current repository state.
- Halt if derived state conflicts with authored artifacts.

## V2 Fallback Triggers
Fallback to Factory v2 if:
- objective ambiguity remains,
- scope expands,
- authority is missing,
- verification fails,
- evidence is stale or missing,
- dependency approval is missing,
- SIMPLE-CODE-GATE blocker remains unresolved,
- payment, authentication, compliance, deployment, runtime-kernel, or infrastructure authority is implicated,
- human sponsor requests V2.

## SIMPLE-CODE-GATE Expectations
- Smallest clear behavior-preserving change.
- No code bloat.
- No spooky action.
- No dependency creep.
- No silent failures.
- No speculative abstraction.
