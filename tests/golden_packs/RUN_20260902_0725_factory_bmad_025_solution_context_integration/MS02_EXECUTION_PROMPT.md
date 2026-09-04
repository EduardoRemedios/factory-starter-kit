# Execution Prompt — MS-02 Semantic Runtime Reconciliation Only

## Version

v1

## Change Log

- v1 (2026-09-02): Activated the approved six-file MS-02 integration boundary.

## Run Metadata

- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Created: `2026-09-02 08:44 WEST`
- Source Pack: `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/`
- Human Go: RECORDED

## Purpose

Semantically combine the approved 0.2.5 safeguards and solution-context runtime behavior in exactly two authored runtime files and four test/helper files, prove the MS-02 collision and fail-closed behavior, then archive controls and stop before MS-03.

## Skill Routing Contract

- Use the `factory-run` skill for activation and micro-sprint sequencing.
- Use the `factory-execution-closeout` skill for scope, diff, verification, residual-risk, and evidence checks.

## Hard Guardrails

- Execute MS-02 only; maximum six modified files, zero created, and zero deleted implementation files.
- Make the smallest direct semantic reconciliation. Add no dependency, framework, registry, strategy layer, generic gateway, hidden mutation, silent fallback, or speculative abstraction.
- Preserve Factory/Conductor and explicit human Go as the sole implementation authority.
- Preserve Factory and Factory-BMAD command passthrough, 0.2.5 identity/cache/approval behavior, stable public layout compatibility, granular layout evidence, unsafe-layout deny-before-allowlist, default-deny unknown paths, permanent delivery/loop/TEA-authority denial, and exact-version `EVIDENCE_ONLY` solution profiles.
- Donors are read-only evidence. Do not copy either donor wholesale or use textual donor precedence.
- Do not modify generated packages, dependencies, Factory Core, protected paths, registrations, documentation, AuditEdge, or any unlisted path.
- Do not invoke BMAD, MS-03, the package builder, Git commit/merge/push, publication, pilot, rollout, MS-06, AuditEdge, or downstream fan-out.

## Authorized Paths

1. `plugin-src/factory-bmad/runtime/factory_bmad.py`
2. `plugin-src/factory-bmad/runtime/factory_bmad_policy.py`
3. `tests/test_factory_bmad_activation.py`
4. `tests/test_factory_bmad_capabilities.py`
5. `tests/test_factory_bmad_enforcement.py`
6. `tests/test_factory_bmad_support.py`

## Execution Sequence

1. Revalidate the unchanged pack, MS-01 evidence, base, donors, generated roots, protected paths, Git state, and worktree registrations.
2. Inspect both donor deltas and reconcile the five collision-contract behaviors plus the approved support helper semantically.
3. Verify the actual implementation write set equals a subset of the six authorized paths with no created or deleted implementation file.
4. Run the exact focused verification command from `EXECUTION_AUTHORIZATION.md` using `./scripts/factory-python` and preserve its complete log externally.
5. Recheck generated roots, protected paths, donors, registrations, and every unlisted base path against preimages.
6. Persist the exact control-lifecycle delta and an MS-02 PASS or FAIL verdict within 40 files and 10 MiB.
7. Archive controls, restore `PLANNING_ONLY`, rerun `pack-lint`, and stop for human MS-02 evidence review.

## Stop Conditions

- Stop on donor/preimage drift, an unlisted write, generated or dependency change, lost 0.2.5 or solution-context regression, malformed/unknown/prohibited path execution, authority escalation, test failure, residue, or evidence-budget breach.
- Preserve failure evidence; do not repair outside the authorized six paths and do not enter MS-03.

## Exit Checklist

- [ ] VM-003 through VM-007 and applicable VM-012/VM-014 checks PASS.
- [ ] Actual implementation writes are at most six modified, zero created, zero deleted.
- [ ] Donors and all protected/unlisted/generated state remain unchanged.
- [ ] SIMPLE-CODE-GATE v2 passes with no dependency or speculative abstraction.
- [ ] Evidence is within 40 files and 10 MiB and includes the exact control lifecycle.
- [ ] Controls archived, live controls absent, and `PLANNING_ONLY` restored.
- [ ] Final `pack-lint` PASS.
- [ ] Stopped before MS-03.

