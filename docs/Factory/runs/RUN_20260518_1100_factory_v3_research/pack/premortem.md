# Premortem

## Version
v1

## Change Log
- v1 (2026-05-18): Initial premortem for Factory v3 research planning.

## Failure Scenarios

### PM-001 - v3 docs overwrite v2 authority
- Failure: v3 strategy language is merged into core specs before evals prove readiness.
- Mitigation: Keep v3 under `docs/Factory/v3/` and require separate promotion criteria before touching `Spec/`.

### PM-002 - advisory validators become accidental required gates
- Failure: a v3 advisory check is wired into `knowledge_lint`, `stage-lint`, or `pack-lint`.
- Mitigation: Advisory validators must be opt-in commands with non-blocking output until promotion.

### PM-003 - AEGIS compatibility becomes AEGIS dependency
- Failure: Starter-kit users think AEGIS is required.
- Mitigation: README and v3 boundary docs must say AEGIS is optional and lower-level kernels remain external.

### PM-004 - runtime governance leaks into Factory
- Failure: Factory v3 tries to mediate production actions or act as a proof engine.
- Mitigation: `NON_GOALS_AND_BOUNDARIES.md` must exclude runtime authority, policy engines, ledgers, and cryptographic proof.

### PM-005 - promotion happens by confidence instead of evidence
- Failure: v3 release is declared before shadow runs and eval data exist.
- Mitigation: `PROMOTION_CRITERIA.md` must require eval evidence, pilot review, and explicit release approval.

## Early Warning Signals
- v3 docs are referenced from required v2 run structure.
- A proposed schema uses mandatory language before advisory validation exists.
- A README edit says v3 is current instead of future research.
- A v3 artifact claims runtime proof from Factory evidence alone.

