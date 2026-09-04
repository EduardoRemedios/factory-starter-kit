# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-02): Recorded digest-bound MS-02-only execution activation.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `9796ab6eb1161000cf0abedecd062d3a28066e41fa7f267f1a21ba0ac63b4d19`
- Authorized Pack Audit SHA-256: `09a828a56414e4ad2f35f190e3ed964bb4f93b5953d6471ca79c1fe98f65908b`

## Human Decision Reference

- Exact decision received in the active Codex task on 2026-09-02: "I authorize that exact MS-02 activation."
- The decision incorporates the immediately preceding exact MS-02 proposal, including its six-path write set, focused verification, exclusions, evidence limits, archive-and-stop requirement, and MS-01 evidence-manifest pin.

## Activation Pins

- Run ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Repository: `/Users/eduardodosremedios/factory-bmad-0.2.5-solution-context`
- Branch: `codex/factory-bmad-0.2.5-solution-context`
- HEAD: `7f4b6b15c96eb1c7fbbf330f1b0f3855cce5abf6`
- Locked Intent SHA-256: `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`
- Source Coupling SHA-256: `cec8080693bafb36e946c0263b2d71a9bbfbd9d1d8b2bc800ca10d605dd66fbf`
- MS-01 Evidence Manifest SHA-256: `277c1d1447547c2c708a2dfc05d19ec96a97f54170acb931616edcc160ebf58d`
- Evidence Root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/MS-02`
- Evidence Budget: maximum 40 files and 10 MiB.

## Authorized Write Set

- Modified maximum: 6; created maximum: 0; deleted maximum: 0.
- `plugin-src/factory-bmad/runtime/factory_bmad.py`
- `plugin-src/factory-bmad/runtime/factory_bmad_policy.py`
- `tests/test_factory_bmad_activation.py`
- `tests/test_factory_bmad_capabilities.py`
- `tests/test_factory_bmad_enforcement.py`
- `tests/test_factory_bmad_support.py`

## Authorized Operation

- MS-02 only: revalidate MS-01 preimages; semantically reconcile the two runtime files and four named test/helper files; preserve both donors' required behavior without textual donor precedence; run the MS-02-focused VM-003 through VM-007 and applicable VM-012/VM-014 checks; capture bounded evidence; archive controls; restore `PLANNING_ONLY`; rerun `pack-lint`; stop for evidence review.
- Focused command: `./scripts/factory-python -m unittest -v tests.test_factory_bmad_activation tests.test_factory_bmad_capabilities tests.test_factory_bmad_enforcement tests.test_factory_bmad_policy tests.test_factory_bmad_policy_parity tests.test_factory_bmad_support tests.test_factory_bmad_output tests.test_factory_bmad_runtime_no_bytecode tests.test_factory_bmad_cli_rollout tests.test_factory_bmad_live_preflight`.

## Authority Boundary

- Donors remain read-only. Generated packages, dependencies, Factory Core, protected paths, registrations, documentation, AuditEdge, and every unlisted path remain no-touch.
- No BMAD invocation, MS-03, builder invocation, commit, merge, push, publication, pilot, rollout, MS-06, AuditEdge access, or downstream fan-out is authorized.
- Any preimage drift, lost regression, new abstraction or dependency, generated write, test failure, evidence-budget breach, BMAD invocation, or unlisted write requires immediate stop, control archival, restoration of `PLANNING_ONLY`, and preservation of evidence.

