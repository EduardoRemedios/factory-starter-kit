# Premortem

## Version
v1

## Change Log
- v1 (2026-05-18): Initial premortem for v3 advisory lint implementation plan.

## Failure Scenarios

### PM-001 - Prototype becomes required gate
- Failure: Future script is invoked by `knowledge_lint`, `stage-lint`, or `pack-lint`.
- Mitigation: Keep standalone script and explicitly forbid required-gate wiring.

### PM-002 - Output semantics are ambiguous
- Failure: Users treat advisory output as a failed Factory pack.
- Mitigation: Require `ADVISORY_*` status and `blocking_effect: none`.

### PM-003 - Scope expands into parser complexity
- Failure: Prototype tries to deeply parse all Factory documents.
- Mitigation: Start with simple deterministic text and path checks.

### PM-004 - Docs and tests diverge
- Failure: Advisory plan says non-blocking but fixtures do not prove it.
- Mitigation: Add fixtures for every initial check category.

## Early Warning Signals
- Future patch edits protected v2 validators.
- Future test output includes plain `FAIL` without advisory wording.
- Future implementation adds schema files before prose candidates are promoted.

