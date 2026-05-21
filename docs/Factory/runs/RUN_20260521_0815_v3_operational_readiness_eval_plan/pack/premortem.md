# Pre-mortem - V3 Operational Readiness Eval Suite

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E pre-mortem for V3 eval-suite planning.

## Scenario
Six months from now, Factory v3 was moved into optional operational use too early. The eval suite looked complete, but it failed to catch drift in real mission-governed coding work.

## Failure Modes

### PM-01 - Narrative evals replaced deterministic checks
- Impact: V3 promotion remains subjective.
- Mitigation: Stage F requires fixture IDs, expected outcomes, and report fields.

### PM-02 - V2 ceremony collapsed without preserving guarantees
- Impact: V3 loses intent lock, adversarial hardening, or audit safety.
- Mitigation: Require a V2 guarantee preservation matrix and negative collapse fixture.

### PM-03 - Scope expansion hides inside long missions
- Impact: V3 agents execute unapproved requirements.
- Mitigation: Include scope-expansion fixtures and halt expectations.

### PM-04 - Authority lease is incomplete
- Impact: Agent uses unapproved files, commands, tools, or dependencies.
- Mitigation: Include missing-authority fixture and mission-envelope completeness eval.

### PM-05 - Verification failure does not halt execution
- Impact: Evidence shows failure but work continues.
- Mitigation: Include failed-verification pilot and halt-on-failure fixture.

### PM-06 - V3 creates runtime-kernel confusion
- Impact: Factory claims AEGIS-like proof or production authority.
- Mitigation: Include AEGIS boundary fixture and adapter-safe positive case.

### PM-07 - Reentry resumes from stale state
- Impact: Agent continues from derived memory instead of source artifacts.
- Mitigation: Include stale-continuity fixture and interruption pilot.

### PM-08 - V2 appears deprecated
- Impact: Users route unsuitable work to V3.
- Mitigation: Include V2 non-deprecation fixture and fallback routing eval.

### PM-09 - Simple-Code-Gate is bypassed
- Impact: V3 produces bloated or brittle code plans.
- Mitigation: Include SIMPLE-CODE-GATE negative fixture.

## Pre-mortem Conclusion
The eval suite must prove V3 preserves V2 safety properties before it reduces V2 ceremony. It must include negative fixtures, pilot reports, and a decision report template before any operational promotion.
