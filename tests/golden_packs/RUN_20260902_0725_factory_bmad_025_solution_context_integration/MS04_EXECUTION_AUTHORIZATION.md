# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-03): Recorded digest-bound MS-04-only activation with an
  explicitly accepted one-file protected-main pre-activation delta.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256:
  `1f9b7d34eea9af5b48e2d3170bf29a736c1b19d63136c397463d7e26e02e4e88`
- Authorized Pack Audit SHA-256:
  `4f9f09823ff57e2ca2b9fa08f93b3c1f268810dc5157ec4b57c9d520337c063b`

## Human Decision Reference

- Eduardo explicitly authorized this exact MS-04 activation in the active
  Codex session on 2026-09-03.
- The decision accepts exactly one pre-existing protected-main addition:
  `docs/Factory/Research/FACTORY_BMAD_SOLUTION_CONTEXT_COMPLETION_PLAN_2026-09-03.md`
  under `/Users/eduardodosremedios/factory-starter-kit`, SHA-256
  `bdebb1d4107cad28a782a1fe54c700f48576fa5470f382777082a957a7bd2728`.
- The original MS-01 protected-main preimage remains immutable historical
  evidence. The accepted current 45,473-record tree, SHA-256
  `6bbb0cd307a8567837e23eca4ed15c4f7d8a35fa9553f5b4d0213be91fd4f41f`,
  is the MS-04 activation preimage and must remain byte-identical through
  closeout.

## Activation Pins

- Run ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Repository:
  `/Users/eduardodosremedios/factory-bmad-0.2.5-solution-context`
- Branch: `codex/factory-bmad-0.2.5-solution-context`
- HEAD: `7f4b6b15c96eb1c7fbbf330f1b0f3855cce5abf6`
- Locked Intent SHA-256:
  `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`
- Source Coupling SHA-256:
  `cec8080693bafb36e946c0263b2d71a9bbfbd9d1d8b2bc800ca10d605dd66fbf`
- Micro-sprints SHA-256:
  `746a44cfb53e39032d091cf6cd84b94057569069e474d2262b86f5a7f8a3a919`
- Verification Plan SHA-256:
  `8c62af18449abc46ac46bad1e1de35c595865f46c3b83018acb3f9c68b1e66eb`
- Envelope SHA-256:
  `3d76ace83070edc5eff47ef687a04404a03f1a4760ff786dc995deb17bbe9782`
- Builder SHA-256:
  `14dc4e75a3e2087e146aa5bb14975ac117650e78144419f8b97f19250fb084a4`
- Generated-roots preimage aggregate:
  `3cdb58bfafea35e64b46a99276246aa841d0a444a7ab28db835118c3317ce91d`
  across 36 files.
- Evidence root:
  `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/MS-04`
- Evidence budget: maximum 30 files and 10 MiB; 67 files were retained before
  activation within the 160-file run ceiling.

## Authorized Write Set

- Invoke `./scripts/factory-python scripts/build_factory_bmad_plugins.py`
  exactly once.
- Only `plugins/factory-bmad` and `plugins/factory-bmad-claude` may change.
- Required activation-relative topology: exactly 18 modified, 0 created, and
  0 deleted generated files: nine per generated root.
- Generated files must derive mechanically from the accepted authored source;
  manual generated edits are prohibited.

## Authorized Verification and Closeout

- Run the exact MS-04 generated-package gate from `pack/verification_plan.md`.
- Verify ownership, modes, topology, donors, protected roots, registrations,
  dependencies, Git/configuration, all pack pins, and the accepted
  protected-main activation preimage.
- Retain no more than 30 external MS-04 evidence files.
- Archive these controls byte-identically as
  `MS04_EXECUTION_AUTHORIZATION.md` and `MS04_EXECUTION_PROMPT.md`, remove the
  live controls, restore `PLANNING_ONLY`, run `pack-lint`, and stop for human
  evidence review before MS-05.

## Authority Boundary

- No authored source, fixture, documentation, pack, dependency, donor,
  registration, Git, BMAD, AuditEdge, publication, rollout, or MS-05 action is
  authorized.
- Any pin, preimage, topology, builder-count, test, no-touch, evidence-budget,
  or control-lifecycle mismatch requires an immediate stop with preserved
  failure evidence.
