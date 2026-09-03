# Execution Prompt — MS-05 Corrective Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Instantiated for the digest-bound MS-05 corrective activation.

## Run Metadata
- RUN_ID: RUN_20260902_0725_factory_bmad_025_solution_context_integration
- Sprint ID: SPRINT_20260902_001
- Created: 2026-09-03 17:20 (WEST)
- Source Pack: docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/
- Human Go: RECORDED

## Purpose
Reconcile the single stale bootstrap test expectation to the locked layout contract, re-run the complete qualification, supersede the NO_GO closeout with the final canonical closeout, restore `PLANNING_ONLY`, archive controls, and stop before MS-06. Out of scope: any other implementation, source, generated, documentation, fixture, or pack change; MS-06; BMAD invocation; AuditEdge; Git actions; publication; pilot; rollout.

## Skill Routing Contract
- No dedicated skill applies; execute via stage contract only.

## Hard Guardrails
- Exactly one implementation write: `tests/test_factory_bmad_bootstrap.py` (`test_partial_state_blocks` expectation only).
- Halt at the first failing gate; preserve failure state.
- SIMPLE-CODE-GATE v2: smallest clear behavior-preserving change; assertions only, no new abstraction.

## Micro-sprint Execution Sequence
1. MS-05 corrective (only):
   - Objective: reconcile the stale expectation, fully qualify, record the final closeout.
   - Entry criteria: pins revalidated against the live authorization; preimage snapshot captured; first-attempt in-repo evidence archived externally.
   - Exit criteria: complete discovery suite PASS with the single check-only builder invocation; knowledge lint, git diff check, stage F-I2 lints, and pack-lint PASS; no-touch postimage equals preimage outside the authorized test file, control, and evidence paths; NO_GO closeout archived and superseded; final `EXECUTION_CLOSEOUT.json` recorded and valid; mode restored; controls archived.
   - Stop/Go gate: STOP after archival for human evidence review; completion grants no MS-06 or rollout authority.

## Verification Contract (must run before closeout)
- `./scripts/factory-python -m unittest -v tests.test_factory_bmad_bootstrap`
- `./scripts/factory-python -m unittest discover -s tests -p 'test_*.py' -v`
- `bash scripts/knowledge_lint.sh`
- `git diff --check`
- `./scripts/factoryctl stage-lint --run RUN_20260902_0725_factory_bmad_025_solution_context_integration --stage <F|G|H|I|J|I2>`
- `./scripts/factoryctl pack-lint --run RUN_20260902_0725_factory_bmad_025_solution_context_integration`

`pack/verification_manifest.yaml` checks are satisfied in order; any `halt_on_failure: true` failure is a stop condition; bounded evidence is written at each check's `evidence_path`.

Factory-controlled Python verification runs through `./scripts/factory-python` only. Complete high-volume evidence goes only to the pinned external MS-05 evidence root (maximum 30 files total); the harness receives bounded counts, digests, and verdicts only.

## Troubleshooting and Failure Policy
- Stop at the first failing gate; report the exact failing command and preserve failure state.
- Do not auto-rollback, delete evidence, or bypass failures with silent behavior changes.

## Final Exit Checklist
- [ ] Bootstrap module and complete discovery suite PASS.
- [ ] Knowledge lint, git diff check, stage F-I2 lints, and pack-lint PASS.
- [ ] No-touch postimage equals preimage outside authorized paths.
- [ ] First-attempt evidence archived; refreshed VM evidence and summary in place.
- [ ] NO_GO closeout archived externally with digest and superseded.
- [ ] Final `EXECUTION_CLOSEOUT.json` recorded through the canonical validator and valid.
- [ ] Mode restored to `PLANNING_ONLY`; controls archived as the MS05-corrective pair; run stopped before MS-06.
