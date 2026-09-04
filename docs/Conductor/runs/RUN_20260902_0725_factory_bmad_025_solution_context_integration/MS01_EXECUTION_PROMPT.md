# Execution Prompt — MS-01 Preimage Freeze Only

## Version

v1

## Change Log

- v1 (2026-09-02): Activated the approved zero-implementation MS-01 evidence operation.

## Run Metadata

- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Created: `2026-09-02 07:45 WEST`
- Source Pack: `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/`
- Human Go: RECORDED

## Purpose

Capture the exact activation, base, donor, protected-path, Git-status, and worktree-registration preimages required by MS-01, then archive the controls, restore `PLANNING_ONLY`, and stop. No implementation or downstream qualification work is in scope.

## Required Read Order

1. `AGENTS.md`
2. `docs/PROJECT_STATE.md`
3. `docs/ROADMAP.md`
4. `docs/Factory/ARCHITECTURE.md`
5. `docs/Factory/ORCHESTRATION.md`
6. `docs/Factory/SCRATCHPAD.md` (only `## Active Pitfalls (Mandatory)`)
7. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/intent.md`
8. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/intent_lock_report.md`
9. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/risk_register.md`
10. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/verification_plan.md`
11. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/traceability_matrix.md`
12. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/micro_sprints.md`
13. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/SPRINT_20260902_001_ENVELOPE.md`
14. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/PACK_AUDIT_REPORT.md`
15. `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/EXECUTION_AUTHORIZATION.md`

## Skill Routing Contract

- Use the `factory-run` skill for MS-01 control and evidence sequencing.
- No dedicated implementation or closeout skill applies because MS-01 permits no implementation and ends with evidence review, not execution closeout.

## Hard Guardrails

- Execute MS-01 only and stop before MS-02.
- Preserve fail-closed behavior and deterministic evidence ordering.
- Do not modify implementation, generated packages, dependencies, donors, existing worktree registrations, or AuditEdge.
- Do not invoke BMAD, run the implementation test plan, build packages, commit, merge, push, publish, pilot, roll out, or fan out downstream work.
- Treat every source root as read-only except for the three authorized run-root control-state changes: create the two live controls, change `EXECUTION_MODE.txt`, then archive the controls and restore `PLANNING_ONLY`.
- Write complete inventory bodies only beneath the exact external MS-01 evidence root; keep them within 40 files and 10 MiB.
- Never emit file contents or secrets into evidence; record paths, types, modes, sizes, and cryptographic digests only.

## MS-01 Execution Sequence

1. Revalidate the unchanged pack digests, repository/branch/HEAD, live control hashes, and safe external evidence root.
2. Confirm builder call-site topology statically without invoking the builder or tests.
3. Capture exact base, donor, protected-path, Git-status, and worktree-registration preimages.
4. Verify evidence privacy, structure, count, size, deterministic ordering, and internal hashes.
5. Recheck all no-touch roots and registrations against their preimages.
6. Record an MS-01 PASS or FAIL verdict with exact evidence references.
7. Archive `EXECUTION_AUTHORIZATION.md` and `EXECUTION_PROMPT.md`, remove the live controls, restore `PLANNING_ONLY`, rerun `pack-lint`, and stop for human review.

## Stop Conditions

- Stop on any pack, activation, repository/ref, root-safety, donor, protected-path, Git-status, registration, privacy, evidence-budget, or no-touch mismatch.
- Preserve the failure evidence; do not repair, roll back user state, or enter MS-02.

## MS-01 Exit Checklist

- [ ] Activation identity and evidence-root safety PASS.
- [ ] Complete required preimages captured without content disclosure.
- [ ] Donors, protected paths, dependencies, generated packages, registrations, and AuditEdge remain untouched.
- [ ] Evidence remains within 40 files and 10 MiB.
- [ ] Controls archived and live controls absent.
- [ ] `EXECUTION_MODE.txt` restored to `PLANNING_ONLY`.
- [ ] Final `pack-lint` PASS.
- [ ] Stopped before MS-02.

