# Execution Prompt — MS-05 Deterministic Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Instantiated for the fresh digest-bound MS-05 activation of the repaired pack.

## Run Metadata
- RUN_ID: RUN_20260902_0725_factory_bmad_025_solution_context_integration
- Sprint ID: SPRINT_20260902_001
- Created: 2026-09-03 17:00 (WEST)
- Source Pack: docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/
- Human Go: RECORDED

## Purpose
Deterministically qualify the integrated 0.2.5 candidate: run the complete discovery suite and governance checks, prove the activation window touched nothing outside the authorized evidence and control paths, record the canonical schema-locked closeout through the validator, restore `PLANNING_ONLY`, archive controls, and stop before MS-06. Out of scope: any implementation, source, generated, documentation, fixture, or pack change; MS-06; BMAD invocation; AuditEdge; Git actions; publication; pilot; rollout.

## Skill Routing Contract
- No dedicated skill applies; execute via stage contract only.

## Hard Guardrails
- Preserve fail-closed behavior; halt at the first failing gate.
- Zero-write budget outside the authorized control and evidence paths.
- Keep schema-locked boundaries and evidence-chain integrity intact.
- SIMPLE-CODE-GATE v2 applies vacuously: no code-changing work is authorized.

## Micro-sprint Execution Sequence
1. MS-05 (only):
   - Objective: full qualification, no-touch proof, canonical closeout, restoration, archival, stop.
   - Entry criteria: pins revalidated against the live authorization; preimage snapshot captured.
   - Exit criteria: complete discovery suite PASS with the single check-only builder invocation; knowledge lint, git diff check, stage F-I2 lints, and pack-lint PASS (35 files, 0 errors, 0 warnings); no-touch postimage equals preimage outside authorized paths; `EXECUTION_CLOSEOUT.json` recorded and valid; mode restored; controls archived.
   - Stop/Go gate: STOP after archival for human evidence review; completion grants no MS-06 or rollout authority.

## Verification Contract (must run before closeout)
- `./scripts/factory-python -m unittest discover -s tests -p 'test_*.py' -v`
- `bash scripts/knowledge_lint.sh`
- `git diff --check`
- `./scripts/factoryctl stage-lint --run RUN_20260902_0725_factory_bmad_025_solution_context_integration --stage <F|G|H|I|J|I2>`
- `./scripts/factoryctl pack-lint --run RUN_20260902_0725_factory_bmad_025_solution_context_integration`

`pack/verification_manifest.yaml` exists: satisfy each manifest check in order, treat any `halt_on_failure: true` failure as a stop condition, write bounded evidence at each check's `evidence_path`, and do not replace manifest checks with weaker prose assertions.

Factory-controlled Python verification runs through `./scripts/factory-python` only.

Evidence output boundary: complete high-volume evidence goes only to the pinned external MS-05 evidence root (maximum 30 files); the harness receives bounded counts, digests, and verdicts only.

## Troubleshooting and Failure Policy
- Stop at the first failing gate; report the exact failing command and preserve failure state.
- Do not auto-rollback, delete evidence, or bypass failures with silent behavior changes.

## Final Exit Checklist
- [ ] Complete discovery suite PASS with the single check-only builder invocation.
- [ ] Knowledge lint, git diff check, stage F-I2 lints, and pack-lint PASS.
- [ ] No-touch postimage equals preimage outside authorized control and evidence paths.
- [ ] Fifteen VM evidence files plus one summary exist under the authorized in-repo evidence path.
- [ ] `EXECUTION_CLOSEOUT.json` recorded through the canonical validator and valid.
- [ ] Mode restored to `PLANNING_ONLY`; controls archived as the MS05 pair; run stopped before MS-06.
