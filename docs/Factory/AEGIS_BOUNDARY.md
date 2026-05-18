# docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial boundary and crosswalk for aligning Factory v3 mission governance with AEGIS-style autonomy governance without duplicating a runtime kernel.

## Purpose

Factory v3 is moving toward mission-governed autonomous execution: bounded authority, executable constraints, continuous verification, escalation semantics, and replayable evidence for long-running coding agents.

AEGIS-style systems already define many of those primitives at a deeper runtime layer. This document prevents Factory from becoming a second governance kernel by defining the boundary between:
- Factory as an SDLC mission-governance profile for software delivery work
- AEGIS as a constitutional autonomy kernel or runtime enforcement layer for consequential systems

## Core Boundary

Factory governs coding missions.

AEGIS governs autonomous system behavior at runtime.

Factory should define portable repo-level contracts for agentic software delivery:
- mission objective
- authorized repo scope
- file and command boundaries
- verification requirements
- evidence requirements
- escalation and halt rules
- merge and closeout gates

Factory should not implement a general runtime autonomy kernel:
- no domain action executor
- no constitutional ledger
- no production policy engine
- no persistent world model
- no regulated-action mediation runtime
- no cryptographic proof infrastructure unless an adopting repo already provides it

## Strategic Rule

Factory v3 should be AEGIS-compatible but not AEGIS-dependent.

This means:
1. Factory may reuse compatible vocabulary such as mission envelope, authority lease, gates, evidence, reentry, revocation, and rollback.
2. Factory artifacts should stay lightweight enough for any repository to adopt.
3. If an adopting repository has AEGIS or another governance kernel, Factory should treat it as the lower-level enforcement substrate.
4. If an adopting repository does not have AEGIS, Factory should still provide useful SDLC governance through documents, templates, validators, and harness adapters.

## Crosswalk

| Factory v3 concept | AEGIS-style concept | Factory ownership | Kernel ownership |
| --- | --- | --- | --- |
| Mission primitive | Operational Contract / Mission Envelope | Define the coding objective, repo scope, execution mode, and completion conditions | Enforce runtime action authority for consequential system operations |
| Authority lease | Autonomy Lease | Bound agent authority over files, commands, tools, time, cost, and dependencies | Bound autonomous runtime authority over domain actions |
| Governance router | Autonomy Gates / AAI state machine | Choose Factory governance intensity for a coding mission | Decide whether runtime action is allowed, blocked, or escalated |
| Continuous verification | Verification, simulation promotion, production guard | Require checks, regressions, no-touch scans, and evidence freshness during delivery | Prove runtime safety, simulation readiness, and production admissibility |
| Evidence / replay | Evidence ledger, proof bundles, offline verifier | Preserve run artifacts, diffs, commands, decisions, and merge evidence | Produce audit-grade runtime evidence and offline-verifiable proof bundles |
| Escalation semantics | Reentry contract, revocation, rollback | Halt or escalate when coding authority, confidence, verification, or scope boundaries fail | Restore human control, revoke runtime leases, and roll back domain actions |
| Capability profiler | Harness scoring / autonomy-level evaluation | Measure coding-agent reliability and tune Factory governance intensity | Measure autonomous-system readiness for higher runtime autonomy |

## Do Not Duplicate

Factory must not duplicate kernel behavior when a lower-level governance runtime exists.

Do not add Factory features that attempt to become:
- a second AEGIS ledger
- a second constitutional policy engine
- a second runtime autonomy gate
- a second domain-action mediation layer
- a second cryptographic evidence authority
- a second persistent cognition or world-model memory layer

Instead, use adapters:
- Factory artifact -> kernel policy input
- Factory authority lease -> kernel autonomy lease profile
- Factory verification manifest -> kernel verification or proof requirement
- Factory closeout evidence -> kernel evidence bundle attachment
- Factory escalation event -> kernel reentry or revocation trigger

## Factory-Owned State

Factory owns governance continuity for software delivery:
- mission objective and current delivery status
- source artifact references
- active repo authority boundaries
- authorized paths, forbidden paths, and file-touch budgets
- allowed commands and required verification commands
- unresolved ambiguities
- escalation state
- human approvals
- pack, closeout, and merge evidence

Factory does not own cognition continuity:
- chain-of-thought
- internal planner state
- full chat history
- generic long-term repo memory
- vendor-specific harness internals
- persistent world-model state

## Governance Intensity Guidance

When a coding mission changes or integrates with an AEGIS-like kernel, default to heavier Factory governance:
- kernel, policy, evidence, safety, sandbox, ledger, verification, authority, or runtime-action paths require HEAVY governance
- generated docs, examples, and non-execution research may use LIGHT or STANDARD governance if they do not change contracts
- schema changes to authority, evidence, lease, or mission-envelope artifacts require explicit compatibility review

The goal is not to slow all work. The goal is to prevent accidental mutation of the lower-level governance substrate while still allowing normal product delivery to move.

## Adoption Pattern

For repos that use AEGIS or a similar kernel:
1. Keep Factory as the SDLC mission-governance layer.
2. Keep the kernel as the runtime authority and proof layer.
3. Add a project adapter that maps Factory artifact fields to kernel primitives.
4. Treat kernel-policy changes as critical or high-risk Factory constraints.
5. Never claim runtime proof from Factory evidence alone unless the kernel verifier produced that proof.

For repos without a kernel:
1. Use Factory's authority, verification, and evidence contracts as process governance.
2. Avoid implying that process artifacts are runtime enforcement.
3. Add deterministic validators before adding heavier runtime concepts.
4. Introduce kernel integration only when there is a real enforcement need.

## Decision Test

Before adding a Factory v3 feature, ask:

1. Does this govern coding-agent delivery work?
2. Does this enforce runtime behavior of a deployed autonomous system?
3. Is there already a lower-level kernel that should own this?
4. Can this be represented as a lightweight repo artifact or validator instead of a runtime service?
5. Would this create a second source of truth for authority, evidence, or mission state?

If the answer to question 2 or 5 is yes, stop and define an adapter boundary before proceeding.
