# Execution Prompt — MS-03 Only

## Version

v1

## Change Log

- v1 (2026-09-02): Activated the approved MS-03 boundary.

## Run Metadata

- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Created: `2026-09-02 15:05 WEST`
- Source Pack: `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/`
- Human Go: RECORDED

## Purpose

Semantically integrate the solution-context donor's promotion, preflight, adapter, and skill behavior plus the uplift donor's bounded doc updates onto the 0.2.5 base within the exact 15-modified/1-created MS-03 write set, create the release-owned solution-context contract fixture, replace the enforcement test's transient donor-run fixture reference, pass the rerun MS-02 authored gate and the MS-03 gate, prove all no-touch boundaries, and close back to planning mode before MS-04.

## Authorized Paths and Changes

- Integrate donor `/Users/eduardodosremedios/factory-bmad-0.2.2-repair` authored deltas into: `plugin-src/factory-bmad/project-adapter/BMAD_POLICY.md`, `plugin-src/factory-bmad/project-adapter/RAW_BRIEF_TEMPLATE.md`, `plugin-src/factory-bmad/project-adapter/factory_project_preflight`, `plugin-src/factory-bmad/skills/audit/SKILL.md`, `plugin-src/factory-bmad/skills/promote/SKILL.md`, `tests/test_factory_bmad_preflight.py`, `tests/test_factory_bmad_promotion.py`, `tests/test_factory_bmad_reconciliation.py`.
- Integrate donor `/Users/eduardodosremedios/factory-starter-kit-0.2.3-uplift` authored deltas into: `docs/CHANGELOG.md`, `docs/adapters/bmad/BMAD_POLICY.md`, `docs/adapters/bmad/FACTORY_BMAD_QUICK_START.md`.
- Author bounded integration-owned updates to `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `tests/plugin_fixtures/factory_bmad_025_source_coupling.json` with no MS-06/AuditEdge/rollout readiness claim.
- Create `tests/plugin_fixtures/factory_bmad_solution_context_contract.json` from the reviewed candidate (`02604c452081fcad3181b8689860414d3e836ac7e53db628e42f58239cfcd364`).
- Apply the reviewed one-line fixture-reference swap to `tests/test_factory_bmad_enforcement.py` (candidate `f26c0419cbef70f2b8fa80db948e010a3beec54306fd0c891f523c7c02267f8e`).
- Maximum implementation delta during this activation: 15 modified, 1 created, 0 deleted.

## Execution Sequence

1. Revalidate activation pins, preserved MS-02 candidate hashes, generated aggregate, donors, protected paths, and the safe empty `MS-03` evidence root.
2. Capture preimages of the 15 authorized modified paths.
3. Integrate donor deltas semantically; halt on any unresolvable conflict.
4. Create the release fixture and apply the enforcement-test swap.
5. Rerun MS-02 Gate A and Gate B exactly as written; require exactly 53 PASS.
6. Run the MS-03 gate: `./scripts/factory-python -m unittest -v tests.test_factory_bmad_preflight tests.test_factory_bmad_promotion tests.test_factory_bmad_reconciliation tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_parent_permission_is_non_transitive_and_must_deny_fixture_stays_denied`.
7. Verify the parent-permission test consumes only `tests/plugin_fixtures/factory_bmad_solution_context_contract.json` and no donor-run fixture reference remains.
8. Revalidate every no-touch surface (donors, protected paths, generated aggregate, unlisted base paths, pack pins); record evidence within 40 files and 10 MiB.
9. Archive controls byte-identically as `MS03_EXECUTION_AUTHORIZATION.md` / `MS03_EXECUTION_PROMPT.md`, restore `PLANNING_ONLY`.
10. Run final `pack-lint` and stop for human evidence review before MS-04.

## Hard Guardrails

- Preserve Factory/Conductor and explicit human approval as the sole implementation authority; SIMPLE-CODE-GATE v2 applies.
- Do not change runtime files, the activation/capabilities/support tests, generated packages, dependencies, Factory Core, donors, protected paths, registrations, or any unlisted path.
- Do not invoke the builder, BMAD, MS-04/MS-05 tests beyond their exclusions, Git mutation, publication, pilot, rollout, MS-06, AuditEdge, or downstream fan-out.
- Stop on the first pin, write-set, test-count, test-result, no-touch, residue, evidence-budget, or lifecycle mismatch; preserve evidence and do not attempt another repair.

## Exit Checklist

- [ ] Exactly 15 implementation files modified and 1 created during this activation; zero deleted.
- [ ] MS-02 gate reruns at exactly 53 PASS.
- [ ] MS-03 gate passes with the release-owned fixture only.
- [ ] Donors, protected paths, generated aggregate, and every unlisted surface remain unchanged.
- [ ] Controls archived byte-identically, live controls absent, and `PLANNING_ONLY` restored.
- [ ] Final `pack-lint` PASS with zero warnings.
- [ ] Stopped before MS-04.
