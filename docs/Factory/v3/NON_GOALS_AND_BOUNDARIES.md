# Factory v3 Non-goals And Boundaries

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial non-goals and boundaries for Factory v3 research.

## Status
Research boundary note only. This document does not change Factory v2 behavior.

## Core Boundary
Factory governs coding missions.

External governance kernels govern autonomous system behavior at runtime.

Factory v3 research may define repository-level SDLC contracts for agentic software delivery. It must not become a second runtime governance kernel.

## Must Stay Out Of Factory v3
Factory v3 must not implement:
- runtime domain action execution
- production action mediation
- constitutional policy engines
- runtime autonomy gates
- cryptographic proof authorities
- second evidence ledgers for lower-level kernels
- persistent world-model or cognition memory
- production rollback execution
- regulated-action mediation runtime
- AEGIS-specific hard dependency

## Factory-owned Space
Factory may own lightweight coding-mission governance artifacts:
- mission objective
- repository scope
- file and command boundaries
- verification requirements
- evidence requirements
- escalation and halt rules
- merge and closeout gates
- adapter mappings to external systems

## Kernel-owned Space
A lower-level governance kernel owns:
- runtime authority
- production policy enforcement
- domain action approval
- cryptographic or audit-grade proof
- sandbox mediation
- runtime evidence verification
- production rollback or revocation execution

## Adapter Rule
When an adopting repo has AEGIS or a similar kernel, Factory artifacts may map to kernel inputs through a project adapter.

The adapter must not make Factory the runtime authority. Factory evidence may support a kernel decision, but it is not runtime proof unless the kernel verifier produced that proof.

## Decision Test
Before adding a v3 feature, ask:
1. Does it govern coding-agent delivery work?
2. Does it enforce deployed autonomous-system behavior?
3. Would it duplicate a lower-level kernel's authority, evidence, or policy?
4. Can it stay as a lightweight document, shadow schema, or advisory validator?
5. Would it create a second source of truth for authority, evidence, or mission state?

If the answer to question 2, 3, or 5 is yes, stop and define an adapter boundary instead.

