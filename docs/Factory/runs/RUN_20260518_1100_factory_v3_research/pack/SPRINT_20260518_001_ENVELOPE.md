# SPRINT_20260518_001 Envelope

## Version
v1

## Change Log
- v1 (2026-05-18): Initial envelope for Factory v3 research planning.

## Sprint Objective
Create the first research-design slice for Factory v3 while leaving Factory v2 behavior intact.

## Execution Mode
- Mode: PLANNING_ONLY
- Implementation is not authorized by this pack.

## Scope
- Plan a v3 research namespace.
- Plan strategic and research-only v3 docs.
- Plan shadow schema candidates without enforcement.
- Plan advisory validators without v2 gate wiring.
- Plan eval capture, pilot profile, promotion criteria, and README split language.

## Out Of Scope
- Editing v2 stage contracts.
- Editing `stage-lint`, `pack-lint`, or required knowledge-lint behavior.
- Adding runtime action execution, policy engines, ledgers, cryptographic proof, or production mediation.
- Making AEGIS required.

## Proposed Files
- `docs/Factory/v3/README.md`
- `docs/Factory/v3/STRATEGY.md`
- `docs/Factory/v3/NON_GOALS_AND_BOUNDARIES.md`
- `docs/Factory/v3/CONCEPT_CANDIDATES.md`
- `docs/Factory/v3/SHADOW_SCHEMA_CANDIDATES.md`
- `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`
- `docs/Factory/v3/PILOT_PROFILE_PLAN.md`
- `docs/Factory/v3/PROMOTION_CRITERIA.md`
- README wording after the research docs exist.

## Strategic Or Research-only Docs
- All files under `docs/Factory/v3/` start as research-only.
- `docs/Factory/v3/PROMOTION_CRITERIA.md` is a release gate candidate, not an active gate.
- Shadow schema docs are candidates, not enforced schemas.

## Keep Out Of v3
- AEGIS ledger duplication.
- Constitutional policy engine duplication.
- Runtime autonomy gate duplication.
- Domain-action mediation.
- Cryptographic evidence authority.
- Persistent cognition or world-model memory.
- Production rollback or revocation execution.

## Schema Candidates Later
- `mission_envelope`
- `authority_lease`
- `governance_profile`
- `verification_freshness`
- `evidence_receipt`
- `escalation_event`
- `reentry_request`
- `revocation_request`
- `rollback_request`
- `capability_profile`
- `kernel_adapter_mapping`
- `advisory_validation_report`

## v2 Protection Lint Candidates
- Check that v2 stage order remains unchanged in README and `STAGE_CONTRACTS.md`.
- Check that v3 docs are not listed in required v2 run-root or pack files.
- Check that shadow schemas are not imported by required validators.
- Check that README states v2 is current and v3 is research-only.
- Check that no Factory doc claims runtime proof from Factory evidence alone.

## README Language
Recommended public language: Factory v2 is the current operating process in this starter kit. Factory v3 is a research and design track for future mission-governed autonomous execution. v3 artifacts do not replace the v2 `A -> I2` pipeline, do not make AEGIS required, and do not add runtime-kernel behavior to Factory.

## File-touch Budget
- MS-01: max files modified 1, created 3, deleted 0.
- MS-02: max files modified 0, created 2, deleted 0.
- MS-03: max files modified 0, created 1, deleted 0.
- MS-04: max files modified 0, created 2, deleted 0.
- MS-05: max files modified 1, created 0, deleted 0.
- MS-06: max files modified 1, created 1, deleted 0.
- Sprint total: max files modified 3, created 9, deleted 0.

## Verification Before Merge
- Run `bash scripts/knowledge_lint.sh`.
- Run any future advisory v3 lint as non-blocking evidence only.
- Confirm `git diff` does not change v2 stage order or required validator behavior.
- Review new v3 docs for AEGIS boundary compliance.

## Risks
- Users confuse Factory document versions with Factory v3 posture.
- Advisory validators become required too early.
- AEGIS-compatible language implies an AEGIS dependency.
- Promotion criteria remain too subjective.

## Open Questions
- Choose `docs/Factory/v3/` or `docs/Factory/research/v3/`.
- Decide whether shadow schemas should become JSON examples after prose review.
- Define the minimum number of pilot runs before release.

