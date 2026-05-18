# Intent Red Team

## Version
v1

## Change Log
- v1 (2026-05-18): Initial red-team review of the Factory v3 research intent.

## Iteration
- Iteration: 1 of max 2

## Findings

### F-001 - Critical - v3 could be mistaken for a replacement pipeline
- Why it matters: Public docs already contain document version numbers such as v3.5, so a new Factory v3 track may confuse users unless the operating split is explicit.
- Fix recommendation: Every v3 research doc should include a research-only banner, and README language should state that Factory v2 remains the usable process.

### F-002 - Critical - Shadow schemas could become accidental contracts
- Why it matters: If shadow schemas are added near `Spec/` or templates, adopters may treat them as required.
- Fix recommendation: Keep candidates under `docs/Factory/v3/shadow_schemas/` and forbid references from `stage-lint`, `pack-lint`, and required knowledge-lint checks until promotion.

### F-003 - High - AEGIS vocabulary could imply a dependency
- Why it matters: Terms such as authority lease and evidence replay overlap with AEGIS-style kernels.
- Fix recommendation: Mark AEGIS as an optional compatibility target and keep kernel-owned behavior out of Factory.

### F-004 - High - Evaluation criteria could be too subjective
- Why it matters: v3 promotion needs evidence, not confidence by narrative.
- Fix recommendation: Require advisory validator results, eval fixture outcomes, pilot feedback, false-positive tracking, and explicit promotion criteria.

## Verification Holes
- No current validator protects the exact v2 stage order from accidental documentation drift.
- No current check prevents v3 research docs from being listed as required v2 pack artifacts.
- No current advisory profile exists for evaluating v3 concepts against historical or live Factory runs.

## Scope Concerns
- None require scope expansion. All findings harden the requested planning scope.

