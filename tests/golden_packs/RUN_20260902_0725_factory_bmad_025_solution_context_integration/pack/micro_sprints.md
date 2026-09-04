# Micro-sprints — Factory-BMAD 0.2.5 Integration

## Version
v3

## Change Log
- v1 (2026-09-02): Sequenced preimage, semantic integration, generation, qualification, and closeout gates.
- v2 (2026-09-02): Assigned source, release-fixture, generated-package, and full-suite tests to the milestones that own their prerequisites.
- v3 (2026-09-02): Human-authorized arithmetic/evidence-ledger correction: MS-03 activation-relative budget, cumulative-touch count, evidence allocation, and control accounting; no design or ownership change.

## Global Rules
- The pack is planning-only; every micro-sprint requires a later exact activation.
- Execute in order and stop at the first mismatch, failure, unexpected write, extra builder call, donor drift, or authority ambiguity.
- Existing checkouts, worktree registrations, Factory Core, dependencies, Git/config, and unrelated paths remain no-touch.
- MS-06, BMAD workflow invocation, AuditEdge, commit, merge, push, publication, pilot, and rollout remain outside all micro-sprints.
- MS-01 and MS-02 are complete under archived activations (MS-02 via a corrective activation, 53/53 PASS, mode restored to `PLANNING_ONLY`); the next legal action is human review followed by a fresh digest-bound MS-03 activation only.

## MS-01 — Freeze base, donors, and execution boundary
- Objective: prove the exact integration base and freeze complete donor/protected preimages before any implementation write.
- Inputs: unchanged I2 pack; exact branch/HEAD; donor roots; `fixtures/integration/donor_contract/`; source-coupling fixture.
- Outputs: external base/donor/protected inventories, Git/status/registration evidence, activation identity record, privacy and budget preflight.
- Entry criteria: fresh human authorization pins pack/audit hashes, repository/ref, evidence root, donor roots, source-coupling hash, and `EXECUTION_ENABLED` transition.
- Exit criteria: VM-001, pre-write portion of VM-010, and VM-014 PASS; evidence roots are safe, external, bounded, and non-symlinked.
- Stop or go gate: STOP on any base/donor/registration mismatch or existing evidence-root conflict; otherwise request confirmation before MS-02 if activation does not cover the exact next write set.

## MS-02 — Reconcile overlapping 0.2.5 runtime and tests
- Objective: semantically combine overlapping runtime policy/CLI and activation/capability/enforcement tests without losing either donor’s behavior.
- Inputs: MS-01 PASS; collision fixture; exact authored allowlist; locked intent.
- Outputs: reconciled `factory_bmad.py`, `factory_bmad_policy.py`, activation/capability/enforcement/support tests, and focused collision evidence.
- Entry criteria: donor hashes still match; generated roots remain preimage-equal; write authorization covers only named paths.
- Exit criteria: VM-003-VM-007 and applicable VM-012/VM-014 checks PASS through the exact 53-test authored gate; 0.2.5 identity, command passthrough, public/granular layout reasons, unsafe-layout denial, and solution-profile classification coexist. The MS-03 release-fixture test and all three MS-04 generated-package tests are excluded by exact test ID.
- Stop or go gate: STOP on a lost donor regression, new abstraction/dependency, generated write, BMAD invocation, or unlisted path.

## MS-03 — Reconcile promotion, preflight, adapters, skills, fixtures, and docs
- Objective: integrate immutable multi-file solution-context promotion, claim adjudication, source coupling, and only directly affected operator/project-adapter documentation.
- Activation-relative budget: 15 modified (the 14 authored allowlist paths untouched in MS-02 plus a second `tests/test_factory_bmad_enforcement.py` touch replacing its transient donor-run fixture reference), 1 created, 0 deleted; external evidence maximum 40 files.
- Inputs: MS-02 PASS; authority/source-coupling fixtures; repair MS-05 evidence; exact remaining authored allowlist.
- Outputs: reconciled project adapters, audit/promote skills, promotion/preflight/reconciliation tests, release-owned solution-context fixture including responsibility-boundary fields, source-coupling fixture, the enforcement test's removal of donor-run fixture coupling, and bounded state/policy/quick-start/changelog updates.
- Entry criteria: runtime collision gate remains PASS and donor/protected roots remain equal.
- Exit criteria: VM-002, VM-007, VM-008, VM-011, applicable VM-012, VM-014, and VM-015 PASS; the MS-02 authored gate is rerun; the parent-permission/non-transitivity test consumes only `tests/plugin_fixtures/factory_bmad_solution_context_contract.json`; no donor-run fixture reference or doc claim of MS-06/AuditEdge/rollout readiness remains.
- Stop or go gate: STOP on authority escalation, floating evidence, public-contract drift, index overclaim, unrelated documentation, or unlisted write.

## MS-04 — Regenerate the Factory-BMAD packages once
- Objective: replace only the two derived Factory-BMAD package roots from reconciled authored 0.2.5 source.
- Activation-relative budget: 18 modified, 0 created, 0 deleted; external evidence maximum 30 files.
- Inputs: MS-02-MS-03 authored PASS; exact builder hash; generated preimages; source-coupling fixture.
- Outputs: regenerated Codex/Claude packages, ownership/parity/topology evidence, builder receipt.
- Entry criteria: source-only focused gate passes; generated roots match preimages; replacement invocation count is zero.
- Exit criteria: VM-009, builder portion of VM-013, and generated portion of VM-014 PASS; exactly 18 files modified, none created/deleted, exactly one replacement invocation; packaged-hook sentinel, generated command-contract, policy-copy parity, and package-build/currentness tests run only after replacement and PASS.
- Stop or go gate: STOP on builder/source drift, topology mismatch, additional invocation, manual generated edit, or protected-root change.

## MS-05 — Deterministically qualify and close the integrated candidate
- Objective: run the full regression and governance checks, prove all no-touch postimages, archive activation, and return to planning mode.
- Activation-relative budget: 0 modified, 0 created, 0 deleted; external evidence maximum 32 files within the 160-file total.
- Inputs: MS-04 PASS; all verification assets; external evidence; unchanged pack.
- Outputs: full logs, postimage/no-touch comparison, bounded closeout, archived authorization/prompt, final `PLANNING_ONLY` state.
- Entry criteria: exact generated topology and all prior gates PASS; full suite contains the one allowed check-only builder invocation.
- Exit criteria: the complete discovery suite and VM-001-VM-015 PASS after MS-02-MS-04; no bytecode/residue/dependency/protected drift; Stage F-I2 and pack-lint PASS; maximum status `FACTORY_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`.
- Stop or go gate: STOP after first failure or qualification. Completion grants no MS-06 or rollout authority; human evidence review and separate MS-06 activation are mandatory.

## Sequence Summary
`MS-01 → evidence check → MS-02 → MS-03 → authored gate → MS-04 → MS-05 → human evidence review → STOP before MS-06`

## Bounded Deferrals
- None.
