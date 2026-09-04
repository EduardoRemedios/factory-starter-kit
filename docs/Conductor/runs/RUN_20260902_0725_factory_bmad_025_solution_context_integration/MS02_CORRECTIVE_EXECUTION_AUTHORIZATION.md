# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-02): Recorded digest-bound MS-02 corrective-only activation.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `ff8c1cd65f486b7083b133c099776b13257b1c36791d1e35a2f14e3d010bc251`
- Authorized Pack Audit SHA-256: `6b6221830ef0556b75ffd4f150af9a263b9a11f7c8a6a630cb66f4ebf02ba8cf`

## Human Decision Reference

- Exact approval received in the active Codex task on 2026-09-02 for the repaired pack and MS-02 corrective activation only.
- The approval authorizes the one-line activation-test expectation correction, exact 53-test authored gate, no-touch verification, control archival, restoration of planning mode, final pack lint, and stop before MS-03.

## Activation Pins

- Run ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Repository: `/Users/eduardodosremedios/factory-bmad-0.2.5-solution-context`
- Branch: `codex/factory-bmad-0.2.5-solution-context`
- HEAD: `7f4b6b15c96eb1c7fbbf330f1b0f3855cce5abf6`
- Locked Intent SHA-256: `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`
- Source Coupling SHA-256: `cec8080693bafb36e946c0263b2d71a9bbfbd9d1d8b2bc800ca10d605dd66fbf`
- Evidence Root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/MS-02-CORRECTIVE`
- Evidence Budget: maximum 40 files and 10 MiB.

## Preserved Candidate Pins

- `plugin-src/factory-bmad/runtime/factory_bmad.py`: `792e4e03a013a64f2bef3b0c19bd2ef85181b9e4c165c1e9664c6c6b7697e99c`
- `plugin-src/factory-bmad/runtime/factory_bmad_policy.py`: `e72762ede0d0b92313d1fc7d3aff24fc79c05b66d447dee8398b3eb9200fe548`
- `tests/test_factory_bmad_activation.py`: `d37eeb9d3d0330dd3f6db206406e2439aa6761b60ce52a3ce92943f42067962f`
- `tests/test_factory_bmad_capabilities.py`: `39396c3d5669042bb0c8c7f5bdc3684205aac3d14ac22ec409c302bf6b8a4aed`
- `tests/test_factory_bmad_enforcement.py`: `c5eee508c52d0dacf34e03eb2b37b2c27a1c9d3ae749935b75c87b286e99b1f5`
- `tests/test_factory_bmad_support.py`: `30dd90d7555860d33ae5151989484dd26d345d50dd91d09aa5acb465b97f6e26`
- Generated roots aggregate: `6b617c3b03da85efc3c3554d2b670b71a9388c9ae56e96372492179e526299a0`.

## Authorized Write Set

- Modified maximum: 1; created maximum: 0; deleted maximum: 0 implementation files.
- `tests/test_factory_bmad_activation.py` only: replace the stale expected next action with `review_zero_write_remediation_preview`.

## Authorized Verification

- Run MS-02 Gate A and Gate B exactly as written in `pack/verification_plan.md` and require exactly 53 passing tests.
- Verify the five other preserved candidate files, generated packages, donors, protected paths, registrations, pack pins, and every unlisted base path remain unchanged.
- Archive controls, restore `PLANNING_ONLY`, run final `pack-lint`, and stop for evidence review before MS-03.

## Authority Boundary

- No fixture, generated-package, dependency, Factory Core, donor, protected-path, registration, or other implementation change is authorized.
- No builder or BMAD invocation, MS-03 execution, Git action, AuditEdge access, publication, pilot, rollout, MS-06, or downstream fan-out is authorized.
- Any pin, preimage, one-file write-set, test-count, test-result, no-touch, evidence-budget, or control-lifecycle mismatch requires immediate stop and preserved failure evidence.

