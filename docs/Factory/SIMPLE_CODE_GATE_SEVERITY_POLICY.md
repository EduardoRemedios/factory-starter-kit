# Factory SIMPLE-CODE-GATE Severity Policy

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial cross-version severity policy for SIMPLE-CODE-GATE findings.

## Status
Mandatory cross-version policy for Factory-controlled planning, execution, and review. This document does not promote Factory v3 or deprecate Factory v2.

## Purpose
Define when SIMPLE-CODE-GATE issues are blockers, advisory-high findings, or no findings.

Factory is used across ordinary software repositories, most of which do not have AEGIS or another runtime governance kernel. The default policy therefore protects general implementation quality and governance clarity for both Factory v2 and Factory v3. Runtime-kernel boundary concerns are an optional additional case for repos that have such a kernel.

## Default Rule
For Factory-controlled code-changing work, SIMPLE-CODE-GATE findings block operational execution or closeout when they materially increase bloat, brittleness, hidden coupling, dependency risk, silent failure risk, or unclear ownership.

For planning, research, and shadow work, the same issues may be recorded as advisory-high findings before code is changed, but they must be resolved, explicitly accepted with rationale, or routed back to Factory v2 before operational execution or closeout.

## Severity Classes

### BLOCKER
Use `BLOCKER` for Factory v2 or Factory v3 operational code-changing work when the proposed or implemented change includes any of these conditions:

- Code bloat: duplicated chunks, broad multi-purpose helpers, or extra layers that do not reduce real current complexity.
- Spooky action: hidden side effects, brittle request-path mutation, or unvalidated data passed through middleware or boundary layers.
- Dependency creep: a new external package or tool where standard library code or existing repo utilities are sufficient, unless explicitly authorized and justified.
- Silent failure: swallowed exceptions, ambiguous `None` or empty fallbacks, or runtime policy paths that fail open instead of failing closed with evidence.
- Speculative abstraction: generic frameworks, registries, strategy layers, plugin seams, or broad indirection added only for possible future variation.
- Ownership confusion: helpers or abstractions that do not have a clear owner or boundary in the current architecture.
- Verification evasion: complexity that makes existing tests, fixtures, or review surfaces unable to show the behavior being changed.

Operational closeout must not mark the work ready while a blocker remains unresolved unless a human sponsor explicitly accepts the residual risk and the acceptance is recorded with evidence.

### ADVISORY_HIGH
Use `ADVISORY_HIGH` when the issue appears in planning, research, shadow evaluation, or pre-execution review and code has not yet been changed under an operational profile.

Advisory-high findings are non-blocking for research evidence collection, but they are not ignorable. Before operational execution or closeout, each advisory-high SIMPLE-CODE-GATE finding must be:

- fixed,
- reclassified as no finding with rationale,
- explicitly accepted by the human sponsor with residual risk, or
- routed back to Factory v2 when V3 profile authority or verification is not strong enough.

### NO_FINDING
Use `NO_FINDING` when the change is small, direct, local, behavior-preserving, and uses existing repo utilities or standard library support.

An abstraction may still be acceptable when it passes all four abstraction-firewall checks from `AGENTS.md`:

1. It removes real, existing duplication.
2. It names a stable domain concept.
3. It reduces branching or call-site complexity.
4. It has a clear owner or boundary in the current architecture.

## Factory v2 And Factory v3 Application
Factory v2 remains the authoritative default process. Factory v3 may become an optional operational profile only when it preserves this policy for the selected work type.

The policy applies equally to:

- V2 planning packs and execution envelopes.
- V2 execution closeout and review.
- V3 mission profiles, mission envelopes, and V3 operational-readiness evidence.
- V3 shadow and advisory runs, with advisory-high severity until a profile is operationally authorized.

## Optional Runtime-Kernel Addendum
If an adopting repo has AEGIS or another runtime governance kernel, also treat a SIMPLE-CODE-GATE issue as a blocker when it creates duplicate authority, duplicate evidence state, duplicate runtime gates, duplicate leases, or confusing ownership between Factory and the kernel.

Repos without such a kernel do not need AEGIS concepts to apply this policy.

## V3-G011 Policy Decision
For the current Factory v3 operational-readiness checklist, `V3-G011` remains `advisory_high` in the standalone research eval runner because the runner is advisory and has no gate effect.

For a future approved operational V3 profile, a `V3-G011` finding becomes an operational blocker when it matches the `BLOCKER` class above. The profile may keep planning-only or shadow findings advisory-high, but it must resolve or explicitly accept them before operational closeout.

## Human Acceptance Requirements
Human acceptance of a SIMPLE-CODE-GATE blocker must name:

- the exact finding,
- the reason the risk is accepted,
- the affected files or boundaries,
- the verification evidence that still passed,
- the residual risk,
- the follow-up trigger for remediation or refactor.

If that evidence is missing, keep the finding blocking.
