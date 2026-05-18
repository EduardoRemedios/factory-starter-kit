# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-18): Initial red-team review of implementation-plan intent.

## Iteration
- Iteration: 1 of max 2

## Findings

### F-001 - Critical - Planning may drift into coding
- Why it matters: The user said "go", but the current run is planning-only.
- Fix recommendation: State that implementation remains future work unless a separate implementation run is authorized.

### F-002 - Critical - `factoryctl` integration is tempting but premature
- Why it matters: `factoryctl` integration implies core tooling surface.
- Fix recommendation: Start with `scripts/factory_v3_advisory_lint.py` only.

### F-003 - High - Fixtures must prove non-blocking behavior
- Why it matters: The useful invariant is advisory output without gate failure.
- Fix recommendation: Require clean, warning, and promotion-claim fixtures.

## Verification Holes
- The future script needs JSON output tests.
- The future script needs markdown report output tests or at least text formatting checks.

## Scope Concerns
- None require scope expansion.

