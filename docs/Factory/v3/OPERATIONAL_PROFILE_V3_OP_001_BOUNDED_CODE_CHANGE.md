# Factory v3 Operational Profile Candidate: V3-OP-001 Bounded Code Change

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial bounded optional V3 operational profile candidate.

## Status
Approved for optional operational use under `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`. This document does not make Factory v3 the default, deprecate Factory v2, approve other V3 profiles, or wire V3 checks into required gates.

The prior research evidence remains the basis for approval; this profile remains non-enforcing with respect to repository gates unless a future integration run explicitly changes that.

## Purpose
Define the first narrow Factory v3 operational profile candidate so remaining readiness work can be judged against a concrete profile instead of abstract V3 ambition.

This profile is designed for ordinary software repositories. It does not assume a separate runtime governance kernel exists.

## Profile Identity
- Profile ID: `V3-OP-001`
- Profile name: Bounded Code Change
- Profile type: optional V3 operational profile
- Governing default outside this profile: Factory v2
- Required fallback: Factory v2

## Eligible Work
Work may be eligible for this profile only when all conditions are true:

- The requested change has a clear user-visible or codebase-visible outcome.
- The affected files or modules can be named before execution.
- The work is local to an existing architecture and does not require a new cross-cutting framework.
- Existing tests, focused fixtures, static checks, or deterministic command checks can verify the change.
- The change can be implemented without new external dependencies unless the human sponsor explicitly authorizes and justifies them.
- The change can preserve SIMPLE-CODE-GATE expectations.
- The mission can name explicit halt and reentry rules before execution.

Typical eligible work:

- Small bug fixes in an existing module.
- Narrow behavior changes with known tests or fixtures.
- Documentation updates tied to an approved process decision.
- Focused test or fixture additions.
- Local refactors that remove real duplication without changing architecture.

## Excluded Work
Work must not use this profile when any condition is true:

- Mission intent is ambiguous.
- Required file, command, dependency, or tool authority cannot be named.
- The work introduces a new platform, framework, plugin architecture, registry, broad strategy layer, or cross-cutting abstraction.
- The work affects production deployment, runtime action mediation, regulated action paths, payment flows, authentication policy, data migration, security boundary behavior, or infrastructure authority without a separate heavier Factory profile.
- Verification cannot be run or cannot produce evidence.
- The task requires broad product discovery, open-ended design, or multiple unresolved stakeholder decisions.
- The task needs a separate runtime kernel to prove safety.
- The task would make Factory v2 appear unavailable or unsupported.

## Required Mission Envelope Fields
A future V3 mission under this profile must record:

- mission objective and success criteria
- eligible work rationale
- explicit non-goals
- authorized file and directory scope
- forbidden file and directory scope
- allowed commands
- dependency policy
- verification commands and expected evidence paths
- halt-on-failure rules
- interruption and reentry rules
- V2 fallback triggers
- SIMPLE-CODE-GATE review status
- human sponsor approval for the profile use

## Authority Limits
This profile may govern coding-agent delivery work within the optional release scope approved in `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.

It does not authorize:

- runtime-kernel authority
- production action mediation
- separate governance kernel dependency
- CI or required-gate wiring
- V2 deprecation
- unbounded autonomous execution
- dependency additions without explicit approval
- continuation after failed halt-on-failure verification

## Verification Expectations
A future V3 mission under this profile must provide:

- pre-execution verification plan
- runnable verification commands where feasible
- command output evidence
- diff evidence
- advisory V3 operational-readiness eval output
- SIMPLE-CODE-GATE classification
- closeout residual-risk statement

Failed halt-on-failure verification must stop execution and preserve evidence.

## V2 Fallback Triggers
Route work to Factory v2, or return to Factory v2, when any trigger occurs:

- objective ambiguity remains after initial framing
- scope expands beyond the authorized mission envelope
- file, command, dependency, or tool authority is missing
- verification fails
- verification evidence is missing or stale
- interruption or reentry state conflicts with authored artifacts
- SIMPLE-CODE-GATE blocker remains unresolved
- a dependency addition is proposed without explicit authorization
- architecture or ownership boundaries become unclear
- runtime-kernel, production-action, security, regulatory, payment, authentication, migration, or infrastructure authority is implicated
- the human sponsor requests V2 fallback

## Evidence Requirements
Closeout for a future operational use of this profile must name:

- profile ID and revision
- mission envelope path
- branch and commit
- model and harness
- verification commands and outputs
- advisory eval outputs
- accepted findings and residual risks
- V2 fallback review result
- human release or closeout decision

## Promotion Dependencies
This profile can be used operationally within the approved optional `V3-OP-001` scope.

Completed decision-prep evidence:

- false-positive and false-negative review
- external-kernel boundary review
- operational-readiness decision report

Required ongoing condition:

- Factory v2 fallback remains available for every mission.
