# Factory SIMPLE-CODE-GATE Severity Policy

## Version
v0.2

## Change Log
- v0.2 (2026-05-25): Removed split-out next-generation policy references after they moved to their dedicated repository.
- v0.1 (2026-05-22): Initial severity policy for SIMPLE-CODE-GATE findings.

## Status
Mandatory policy for Factory-controlled planning, execution, and review.

## Purpose
Define when SIMPLE-CODE-GATE issues are blockers, advisory-high findings, or no findings.

The default policy protects implementation quality and governance clarity for Factory-controlled code-changing work.

## Default Rule
For Factory-controlled code-changing work, SIMPLE-CODE-GATE findings block operational execution or closeout when they materially increase bloat, brittleness, hidden coupling, dependency risk, silent failure risk, or unclear ownership.

For planning, research, and pre-execution review, the same issues may be recorded as advisory-high findings before code is changed, but they must be resolved or explicitly accepted before operational execution or closeout.

## Severity Classes

### BLOCKER
Use `BLOCKER` when the proposed or implemented change includes any of these conditions:

- Code bloat: duplicated chunks, broad multi-purpose helpers, or extra layers that do not reduce real current complexity.
- Spooky action: hidden side effects, brittle request-path mutation, or unvalidated data passed through middleware or boundary layers.
- Dependency creep: a new external package or tool where standard library code or existing repo utilities are sufficient, unless explicitly authorized and justified.
- Silent failure: swallowed exceptions, ambiguous `None` or empty fallbacks, or runtime policy paths that fail open instead of failing closed with evidence.
- Speculative abstraction: generic frameworks, registries, strategy layers, plugin seams, or broad indirection added only for possible future variation.
- Ownership confusion: helpers or abstractions that do not have a clear owner or boundary in the current architecture.
- Verification evasion: complexity that makes existing tests, fixtures, or review surfaces unable to show the behavior being changed.

Operational closeout must not mark the work ready while a blocker remains unresolved unless a human sponsor explicitly accepts the residual risk and the acceptance is recorded with evidence.

### ADVISORY_HIGH
Use `ADVISORY_HIGH` when the issue appears in planning, research, or pre-execution review and code has not yet been changed.

Advisory-high findings are non-blocking for planning evidence collection, but they are not ignorable. Before operational execution or closeout, each advisory-high SIMPLE-CODE-GATE finding must be:

- fixed,
- reclassified as no finding with rationale, or
- explicitly accepted by the human sponsor with residual risk.

### NO_FINDING
Use `NO_FINDING` when the change is small, direct, local, behavior-preserving, and uses existing repo utilities or standard library support.

An abstraction may still be acceptable when it passes all four abstraction-firewall checks from `AGENTS.md`:

1. It removes real, existing duplication.
2. It names a stable domain concept.
3. It reduces branching or call-site complexity.
4. It has a clear owner or boundary in the current architecture.

## Human Acceptance Requirements
Human acceptance of a SIMPLE-CODE-GATE blocker must name:

- the exact finding,
- the reason the risk is accepted,
- the affected files or boundaries,
- the verification evidence that still passed,
- the residual risk,
- the follow-up trigger for remediation or refactor.

If that evidence is missing, keep the finding blocking.
