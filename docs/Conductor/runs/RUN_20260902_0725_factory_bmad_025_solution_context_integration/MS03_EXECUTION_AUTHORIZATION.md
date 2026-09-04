# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-02): Recorded digest-bound MS-03-only activation.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `1f9b7d34eea9af5b48e2d3170bf29a736c1b19d63136c397463d7e26e02e4e88`
- Authorized Pack Audit SHA-256: `4f9f09823ff57e2ca2b9fa08f93b3c1f268810dc5157ec4b57c9d520337c063b`

## Human Decision Reference

- Approval received in the active Claude Code session on 2026-09-02: Go for the next legal action of the corrected pack conditioned on the Purple-adjudicated PASS, followed by an explicit second confirmation ("yes I can confirm you can proceed") after the harness surfaced the control-creation gate.
- The approval authorizes only the MS-03 write set (15 modified, 1 created, 0 deleted), the MS-02 authored gate rerun, the MS-03 release-fixture/authored-feature gate, no-touch verification, bounded evidence, control archival, restoration of planning mode, final pack lint, and stop before MS-04.

## Activation Pins

- Run ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Repository: `/Users/eduardodosremedios/factory-bmad-0.2.5-solution-context`
- Branch: `codex/factory-bmad-0.2.5-solution-context`
- HEAD: `7f4b6b15c96eb1c7fbbf330f1b0f3855cce5abf6`
- Locked Intent SHA-256: `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`
- Source Coupling SHA-256: `cec8080693bafb36e946c0263b2d71a9bbfbd9d1d8b2bc800ca10d605dd66fbf`
- Micro-sprints (v3) SHA-256: `746a44cfb53e39032d091cf6cd84b94057569069e474d2262b86f5a7f8a3a919`
- Verification Plan (v4) SHA-256: `8c62af18449abc46ac46bad1e1de35c595865f46c3b83018acb3f9c68b1e66eb`
- Envelope (v4) SHA-256: `3d76ace83070edc5eff47ef687a04404a03f1a4760ff786dc995deb17bbe9782`
- Evidence Root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/MS-03`
- Evidence Budget: maximum 40 files and 10 MiB; run-total ceiling 160 files with 58 already retained.

## Preserved MS-02 Candidate Pins

- `plugin-src/factory-bmad/runtime/factory_bmad.py`: `792e4e03a013a64f2bef3b0c19bd2ef85181b9e4c165c1e9664c6c6b7697e99c`
- `plugin-src/factory-bmad/runtime/factory_bmad_policy.py`: `e72762ede0d0b92313d1fc7d3aff24fc79c05b66d447dee8398b3eb9200fe548`
- `tests/test_factory_bmad_activation.py`: `8290ae0aa24de8a049f1db2b8403a9d1ec7159f75c6cae72cf7b9cfcc3d9969b`
- `tests/test_factory_bmad_capabilities.py`: `39396c3d5669042bb0c8c7f5bdc3684205aac3d14ac22ec409c302bf6b8a4aed`
- `tests/test_factory_bmad_enforcement.py` (pre-MS-03): `c5eee508c52d0dacf34e03eb2b37b2c27a1c9d3ae749935b75c87b286e99b1f5`
- `tests/test_factory_bmad_support.py`: `30dd90d7555860d33ae5151989484dd26d345d50dd91d09aa5acb465b97f6e26`
- The runtime files and the activation/capabilities/support tests remain no-touch during MS-03; only the enforcement test is authorized for its second touch.

## Reviewed Candidate Pins

- Candidate enforcement test (fixture-reference swap only): `f26c0419cbef70f2b8fa80db948e010a3beec54306fd0c891f523c7c02267f8e`
- Candidate release fixture `factory_bmad_solution_context_contract.json`: `02604c452081fcad3181b8689860414d3e836ac7e53db628e42f58239cfcd364`

## Preimage Revalidation (performed before this activation)

- Donor `/Users/eduardodosremedios/factory-bmad-0.2.2-repair`: 959/959 records MATCH the MS-01 preimage.
- Donor `/Users/eduardodosremedios/factory-starter-kit-0.2.3-uplift`: 640/640 records MATCH the MS-01 preimage.
- Protected paths: 280/280 records MATCH the MS-01 preimage.
- Generated roots pre-write aggregate (canonical sorted path/sha256 JSON, both roots, 36 files): `3cdb58bfafea35e64b46a99276246aa841d0a444a7ab28db835118c3317ce91d`; must be byte-equal after MS-03.

## Authorized Write Set

- Modified maximum: 15; created maximum: 1; deleted maximum: 0 implementation files.
- Modified: `docs/CHANGELOG.md`, `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, `docs/adapters/bmad/BMAD_POLICY.md`, `docs/adapters/bmad/FACTORY_BMAD_QUICK_START.md`, `plugin-src/factory-bmad/project-adapter/BMAD_POLICY.md`, `plugin-src/factory-bmad/project-adapter/RAW_BRIEF_TEMPLATE.md`, `plugin-src/factory-bmad/project-adapter/factory_project_preflight`, `plugin-src/factory-bmad/skills/audit/SKILL.md`, `plugin-src/factory-bmad/skills/promote/SKILL.md`, `tests/plugin_fixtures/factory_bmad_025_source_coupling.json`, `tests/test_factory_bmad_enforcement.py`, `tests/test_factory_bmad_preflight.py`, `tests/test_factory_bmad_promotion.py`, `tests/test_factory_bmad_reconciliation.py`.
- Created: `tests/plugin_fixtures/factory_bmad_solution_context_contract.json`.

## Authorized Verification

- Rerun MS-02 Gate A and Gate B exactly as written in `pack/verification_plan.md` and require exactly 53 passing tests.
- Run the MS-03 gate exactly as written: `tests.test_factory_bmad_preflight`, `tests.test_factory_bmad_promotion`, `tests.test_factory_bmad_reconciliation`, and the parent-permission/non-transitivity enforcement test consuming only `tests/plugin_fixtures/factory_bmad_solution_context_contract.json`.
- Verify donors, protected paths, generated roots, registrations, pack pins, and every unlisted base path remain unchanged.
- Archive controls as `MS03_*`, restore `PLANNING_ONLY`, run final `pack-lint`, and stop for evidence review before MS-04.

## Authority Boundary

- No generated-package write, builder invocation, BMAD invocation, dependency, Factory Core, donor, protected-path, registration, or unlisted implementation change is authorized.
- No MS-04/MS-05 execution, Git action, AuditEdge access, publication, pilot, rollout, MS-06, or downstream fan-out is authorized.
- Any pin, preimage, write-set, test-count, test-result, no-touch, evidence-budget, or control-lifecycle mismatch requires immediate stop and preserved failure evidence.
