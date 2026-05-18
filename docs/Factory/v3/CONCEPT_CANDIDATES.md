# Factory v3 Concept Candidates

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial non-enforcing concept candidates for Factory v3 research.

## Status
Research only. These concepts are not Factory v2 contracts and are not enforced by any validator.

## Purpose
This document names candidate Factory v3 concepts before any schema or validator work begins. It keeps Factory-owned SDLC mission governance separate from kernel-owned runtime governance.

## Candidate Concepts

### Mission Envelope
- Candidate meaning: A compact description of a coding mission's objective, repository scope, allowed files, allowed commands, verification expectations, halt rules, and completion conditions.
- Factory-owned: coding mission boundaries and delivery conditions.
- Kernel-owned: runtime authorization for deployed autonomous-system actions.
- Enforcement status: not enforced.

### Authority Lease
- Candidate meaning: A bounded grant of coding-agent authority over files, commands, time, cost, tools, and dependency access.
- Factory-owned: repository work boundaries for software delivery.
- Kernel-owned: runtime autonomy leases for domain actions.
- Enforcement status: not enforced.

### Governance Profile
- Candidate meaning: A selected governance intensity for a coding mission, such as light, standard, heavy, or kernel-sensitive.
- Factory-owned: choosing planning depth, review requirements, and verification expectations.
- Kernel-owned: runtime gate decisions and production admissibility.
- Enforcement status: not enforced.

### Verification Freshness
- Candidate meaning: Evidence that required checks were run recently enough and against the relevant artifact, branch, or runtime target.
- Factory-owned: delivery verification freshness for code and docs.
- Kernel-owned: runtime proof freshness and production safety checks.
- Enforcement status: not enforced.

### Evidence Receipt
- Candidate meaning: A structured record that a command, review, human decision, or artifact check occurred.
- Factory-owned: SDLC evidence pointers and replayable delivery context.
- Kernel-owned: audit-grade runtime evidence or cryptographic proof.
- Enforcement status: not enforced.

### Escalation Event
- Candidate meaning: A recorded condition that requires human review, scope lock, halt, or re-planning.
- Factory-owned: coding mission escalation and halt semantics.
- Kernel-owned: runtime reentry, revocation, and production action intervention.
- Enforcement status: not enforced.

### Reentry Request
- Candidate meaning: A request to resume a halted coding mission after evidence, scope, and authority are revalidated.
- Factory-owned: SDLC mission resume conditions.
- Kernel-owned: runtime reentry into autonomous operation.
- Enforcement status: not enforced.

### Revocation Request
- Candidate meaning: A request to withdraw coding-agent authority for a mission, branch, file set, command class, or tool.
- Factory-owned: repository delivery authority withdrawal.
- Kernel-owned: runtime autonomy revocation.
- Enforcement status: not enforced.

### Rollback Request
- Candidate meaning: A request to reverse or abandon a coding delivery path after verification failure or scope breach.
- Factory-owned: code, doc, branch, or pack rollback planning.
- Kernel-owned: production domain rollback execution.
- Enforcement status: not enforced.

### Capability Profile
- Candidate meaning: A record of agent or harness reliability for a category of coding mission.
- Factory-owned: choosing planning depth and review intensity for software delivery.
- Kernel-owned: autonomy readiness for deployed systems.
- Enforcement status: not enforced.

### Kernel Adapter Mapping
- Candidate meaning: A project-specific map from Factory artifacts to an external governance kernel's accepted inputs.
- Factory-owned: adapter documentation and source artifact references.
- Kernel-owned: runtime acceptance, enforcement, and proof.
- Enforcement status: not enforced.

### Advisory Validation Report
- Candidate meaning: A non-blocking report that checks v3 research assumptions against repository artifacts.
- Factory-owned: advisory SDLC feedback.
- Kernel-owned: runtime validation or production proof.
- Enforcement status: not enforced.

## Candidate Promotion Rule
No concept in this file may become a required Factory contract until a later Factory v2-governed run defines schema shape, advisory validation evidence, pilot results, and explicit promotion approval.

