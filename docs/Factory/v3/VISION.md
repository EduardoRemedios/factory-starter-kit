# Factory v3 Vision

## Version
v0.2

## Change Log
- v0.2 (2026-05-22): Removed private-kernel naming from the public vision, defined the governance-runtime boundary, and made the document self-contained for readers without private system context.
- v0.1 (2026-05-22): Initial vision document for the path from optional `V3-OP-001` use to the full mission-governance runtime vision.

## Status
Strategic direction and research roadmap context only. This document is non-enforcing: it does not make Factory v3 the default Factory mode, approve any profile beyond `V3-OP-001`, deprecate Factory v2, or wire V3 checks into required gates.

## Purpose
Factory v3 exists because coding models and harnesses are improving toward longer, more autonomous execution. As that happens, some Factory v2 orchestration work should collapse into smaller mission-governance primitives.

The durable Factory value is not more project-management ceremony. The durable value is governance of autonomous coding work:

- clear mission authority,
- bounded scope,
- executable constraints,
- verification discipline,
- halt and escalation semantics,
- evidence integrity,
- replayability,
- V2 fallback when the mission is not safe for V3.

## Core Thesis
Factory v3 should evolve from:

```text
human -> task -> orchestration pipeline -> implementation
```

to:

```text
human -> mission definition -> governed autonomous execution
```

The goal is not to replace human judgment. The goal is to let better coding harnesses handle more local decomposition and repair while Factory preserves the governance properties that keep the work bounded, testable, and auditable.

## Current Position
Factory v3 has achieved the first operational bridgehead:

- optional `V3-OP-001 Bounded Code Change`,
- mission envelopes for bounded code-changing work,
- explicit authority, forbidden scope, commands, verification, halt rules, dependency policy, and V2 fallback,
- starter templates and user guidance,
- advisory eval scripts and fixtures,
- pilot evidence for halt behavior, reentry, V2 fallback, natural-language drift detection, and SIMPLE-CODE-GATE coverage.

This is enough for careful optional use on bounded code changes.

It is not yet the full Factory v3 platform.

## Full Vision
The full Factory v3 vision is a harness-agnostic mission-governance runtime for autonomous coding workers.

In this document, runtime means repo-local governance records, validators, routing rules, verification state, and evidence replay for coding missions. It does not mean a production autonomy runtime, policy engine, payment system, regulated-action mediator, or deployed product control plane.

At that point, Factory v3 should provide:

1. Mission runtime
   - persistent mission state,
   - pause and resume semantics,
   - current objective state,
   - active authority boundaries,
   - verification checkpoints,
   - escalation state,
   - completion and termination state.

2. Authority lease engine
   - allowed and forbidden paths,
   - allowed commands,
   - runtime and retry budgets,
   - dependency-change rules,
   - required verification,
   - revocation and renewal semantics.

3. Execution telemetry layer
   - structured record of actions, commands, retries, repairs, file touches, verification, failures, human interventions, and closeout decisions.

4. Constraint registry
   - concrete, enforceable controls first,
   - higher-level invariants only when they map to testable evidence,
   - no speculative framework or abstract policy layer without enforcement value.

5. Continuous verification runtime
   - verification freshness tracking,
   - halt-on-failure behavior,
   - repeated repair-loop detection,
   - rollback or reentry triggers.

6. Eval harness
   - golden fixtures,
   - real-run shadows,
   - seeded drift cases,
   - false-positive and false-negative tracking,
   - capability thresholds for V3 promotion decisions.

7. Capability profiler
   - reliability profiles for Codex, Claude Code, Cursor, and future harnesses,
   - measured execution quality rather than generic model benchmarking,
   - governance intensity tied to actual harness performance.

8. Governance router
   - route work across autonomous, light, standard, and heavy governance modes,
   - preserve V2 fallback,
   - block V3 when authority, scope, verification, or evidence is weak.

9. Evidence and replay layer
   - machine-readable mission records,
   - evidence-linked command and decision records,
   - replayable closeout,
   - diffable governance history.

10. Cross-harness adapters
    - no vendor lock-in,
    - Codex, Claude Code, Cursor, and future harnesses can all emit or consume the same governance artifacts.

## Boundary
Factory v3 governs coding missions.

Factory v3 does not become:

- a production policy engine,
- a payment or regulated-action mediator,
- a runtime autonomy kernel,
- a persistent cognition memory system,
- a second ledger for any private or project-specific governance kernel,
- a replacement for project-specific tests or domain review.

If a repository has a private or project-specific autonomy governance kernel, Factory v3 remains the SDLC mission-governance layer and maps to that kernel through a project adapter. The kernel remains the authority and proof layer for runtime system behavior.

If a repository has no such kernel, Factory v3 should still be useful through ordinary documents, templates, validators, command evidence, and project-specific tests.

## Governance Continuity Versus Cognition Continuity
Factory v3 should persist governance continuity, not cognition continuity.

Factory-owned state:

- mission objective,
- active authority boundaries,
- allowed and forbidden paths,
- allowed commands,
- runtime budgets,
- verification requirements,
- escalation state,
- human approvals,
- evidence links,
- completion state.

Harness-owned state:

- chat history,
- internal planning,
- tool history,
- chain-of-thought,
- generic repo memory,
- vendor-specific session state.

This boundary keeps Factory portable and prevents it from competing with harness memory systems.

## Decision Standard
Factory v3 can become the default operational mode only when it has evidence that it preserves the important V2 guarantees with less unnecessary ceremony for a defined class of work.

Default-mode promotion requires:

- multiple approved V3 profiles, not only `V3-OP-001`,
- machine-readable mission records,
- telemetry evidence from real projects,
- measured false-positive and false-negative behavior,
- reliable halt and reentry behavior,
- clear V2 fallback,
- harness capability thresholds,
- human approval.

Until then, Factory v2 remains the default and fallback.
