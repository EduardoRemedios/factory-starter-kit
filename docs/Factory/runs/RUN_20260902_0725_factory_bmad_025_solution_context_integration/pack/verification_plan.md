# Verification Plan — Factory-BMAD 0.2.5 Integration

## Version
v5

## Change Log
- v1 (2026-09-02): Defined deterministic integration, collision, authority, parity, and no-touch checks.
- v2 (2026-09-02): Added explicit protected paths and pre-write builder call-topology inspection after envelope Red review.
- v3 (2026-09-02): Separated authored, release-fixture, generated-package, and full-suite gates after the stopped MS-02 exposed cross-milestone test coupling.
- v4 (2026-09-02): Human-authorized arithmetic/evidence-ledger correction of MS-03 write, evidence-allowance, and control accounting; test ownership unchanged.
- v5 (2026-09-03): Human-authorized manifest repair after the MS-05 pre-activation blocker: added the executable verification manifest binding VM-001 through VM-015; check meaning, ownership, and budgets unchanged.

## Posture
- Audited mode: `PLANNING_ONLY`; no command below is execution authority.
- Locked intent SHA-256: `14e4716d4df41bb5e9b05a59c1f8fac6406b4c69c9fe3fa206f1dec9066cc17c`.
- `verification_manifest.yaml` binds VM-001 through VM-015 for canonical closeout recording. A later activation must pin exact current hashes and commands without changing this audited pack.
- Evidence root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260902_0725_factory_bmad_025_solution_context_integration/`, maximum 40 files and 10 MiB per micro-sprint activation; 58 files are already retained through the MS-02 corrective closeout, and the remaining 102-file allowance within the 160-file/40 MiB ceiling is MS-03 maximum 40, MS-04 maximum 30, MS-05 maximum 32.

## Checks
- VM-001 — V4 source revalidation: exact base HEAD/branch and complete donor path/type/mode/digest/Git-status/worktree-registration inventories match activation pins before writes and after closeout.
- VM-002 — V3 status contract: no prior 0.2.3 verdict is accepted as combined 0.2.5 qualification; final vocabulary is bounded and independently scanned.
- VM-003 — V3 fixture/static: collision fixture covers every overlapping runtime/test file and forbids textual donor precedence or generated-byte transplant.
- VM-004 — V3 focused regression: retain 0.2.5 identity, cache/approval behavior, Factory and Factory-BMAD command passthrough, CLI rollout, and existing nested capability evidence.
- VM-005 — V3 focused regression: Doctor/Audit public `FACTORY_BMAD_NON_CANONICAL_LAYOUT`, subordinate `layout_reason_code`, and enforcement `FACTORY_BMAD_ENFORCEMENT_ACTIVE_UNSAFE_LAYOUT` coexist for nested, both, partial, ambiguous, and symlink layouts.
- VM-006 — V3 negative regression: malformed, unknown, loop, delivery, quick-dev, sprint, code-review, unattended, and TEA-authority paths deny before causal sentinels through both hook paths.
- VM-007 — V3 policy regression: architecture, UX, and spec require exact BMAD 6.10.0 skill/customization/manifest/override profiles and receive only non-authority solution context.
- VM-008 — V3 promotion/preflight regression: multi-file immutable promotion, tamper/traversal/symlink rejection, supersession, claim accepted/rejected/modified/deferred/conflict outcomes, and no Factory authority pass.
- VM-009 — V3 package regression: exactly one replacement builder updates only two generated roots; ownership, parity, package-current, modes, and topology match source.
- VM-010 — V4 no-touch: Factory Core/generated Factory, donors, Git/config, dependencies, unrelated docs/tests, pilot roots, and registrations remain byte-equal.
- VM-011 — V3 isolated index regression: generic legacy marker yields zero recall while selected promoted marker is positively indexed; no AuditEdge claim is made.
- VM-012 — V3 regression: the 53-test MS-02 authored gate, MS-03 release-fixture/promotion gate, post-builder generated gate, and final full suite cover privacy, no-bytecode, runtime path safety, dependency, cache-integrity, and CLI preflight without premature generated parity.
- VM-013 — V3 lifecycle audit: MS-02 and MS-03 authored gates precede one replacement builder; generated-package checks run only after that replacement; the final full regression contains the single check-only builder invocation; residue is absent.
- VM-014 — V3 coupling audit: actual authored/generated write sets equal fixture allowlists and exact topology/budgets; unexpected paths halt.
- VM-015 — V3 governance audit: knowledge lint, diff check, stage/pack lints, SIMPLE-CODE-GATE, status ceiling, and explicit MS-06/AuditEdge/Git/rollout exclusions pass.

## Planned Commands After Separate Authorization

### MS-02 authored runtime gate

- Gate A (6 tests): `./scripts/factory-python -m unittest -v tests.test_factory_bmad_activation`.
- Gate B (47 tests):

```bash
./scripts/factory-python -m unittest -v \
  tests.test_factory_bmad_capabilities \
  tests.test_factory_bmad_policy \
  tests.test_factory_bmad_output \
  tests.test_factory_bmad_runtime_no_bytecode \
  tests.test_factory_bmad_cli_rollout \
  tests.test_factory_bmad_live_preflight \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_exact_upstream_allowlist \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_prohibited_and_unknown_default_deny \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_unqualified_solution_context_is_blocked_before_expansion \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_exact_solution_profiles_pass_both_hook_paths_with_non_authority_context \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_solution_profile_drift_and_overrides_fail_closed \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_model_skill_is_denied_before_execution \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_allowed_and_unrelated_invocations_have_no_decision \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_nested_bmad_layout_blocks_even_allowed_upstream_invocation \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_normal_namespaced_companion_promote_is_unrelated_to_bmad_guard \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_factory_slash_command_passes_when_cwd_contains_bmad_marker \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_denial_says_doctor_was_not_run \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_malformed_active_bmad_skill_fails_closed \
  tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_hook_cli_returns_structured_decision_and_invalid_json_exit_two \
  tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_runtime_and_ci_lint_share_verdict \
  tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_unknown_returns_same_stable_reason \
  tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_ci_callable_policy_lint_cli \
  tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_seeded_project_lint_uses_same_reason \
  tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_seeded_project_lint_does_not_write_bytecode
```

- Gate A plus Gate B must report exactly 53 PASS. They explicitly exclude one MS-03 release-fixture test and three MS-04 generated-package tests.

### MS-03 release-fixture and authored-feature gate

- MS-03 activation-relative write budget: 15 modified (the 14 authored allowlist paths untouched in MS-02 plus a second `tests/test_factory_bmad_enforcement.py` touch), 1 created, 0 deleted; the 20-path authored allowlist is unchanged.
- Run the MS-02 authored gates again after MS-03 changes.
- Then run: `./scripts/factory-python -m unittest -v tests.test_factory_bmad_preflight tests.test_factory_bmad_promotion tests.test_factory_bmad_reconciliation tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_parent_permission_is_non_transitive_and_must_deny_fixture_stays_denied`.
- The parent-permission test must read `tests/plugin_fixtures/factory_bmad_solution_context_contract.json`; references to a donor or transient `docs/Factory/runs/` fixture are prohibited.

### MS-04 generated-package gate

- Replacement builder: `./scripts/factory-python scripts/build_factory_bmad_plugins.py` exactly once.
- Only after replacement run: `./scripts/factory-python -m unittest -v tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_generated_package_pretooluse_sentinel_matrix tests.test_factory_bmad_enforcement.FactoryBmadEnforcementTests.test_generated_package_contract_rejects_ambiguous_commands tests.test_factory_bmad_policy_parity.FactoryBmadPolicyParityTests.test_generated_policy_copies_match_authored_source tests.test_factory_bmad_plugin_build`.

### MS-05 qualification gate

- Full regression: `./scripts/factory-python -m unittest discover -s tests -p 'test_*.py' -v`; its package-current test is the single check-only builder invocation.
- Knowledge and structure: `bash scripts/knowledge_lint.sh`, `git diff --check`, Stage F-I2 lints, and `pack-lint`.

## Lifecycle
1. Revalidate activation pins, statically confirm the one replacement and one full-suite check-only builder call sites, and capture complete external preimages.
2. Semantically integrate authored collisions and donor-only behavior within the allowlist.
3. Run the exact 53-test MS-02 authored gate; then create and consume the release-owned fixture in the MS-03 authored-feature gate. Halt on either failure.
4. Run one replacement builder; then run the generated-package gate and verify exact generated topology.
5. Run the full regression and remaining checks; compare all protected postimages.
6. Archive authorization, return to `PLANNING_ONLY`, record bounded closeout, and stop for human evidence review before MS-06.

## Evidence Rules
- Preserve full logs externally; conversation receives bounded summaries only.
- Every negative test proves sentinel non-execution.
- Donor or activation drift, extra builder call, test failure, residue, unexpected path, or status overclaim halts.
