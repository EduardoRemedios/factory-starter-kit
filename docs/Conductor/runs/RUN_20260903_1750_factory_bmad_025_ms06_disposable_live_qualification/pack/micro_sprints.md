# Micro-sprints — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Sequenced provision, live proof, and closeout gates.

## Global Rules
- The pack is planning-only; every micro-sprint requires a later exact, digest-bound activation.
- Execute in order and stop at the first mismatch, failure, containment breach, unexported-evidence teardown attempt, missing human review, or authority ambiguity.
- The qualified candidate, Factory Core, donors, registrations, and unrelated paths remain no-touch; every live action happens inside the disposable repository.
- AuditEdge, candidate mutation, commit, merge, push, publication, pilot, release, and rollout remain outside all micro-sprints.

## MS-01 — Pin, contain, and provision the disposable repository
- Objective: prove the exact inputs and create a contained disposable repository seeded from the qualified candidate.
- Inputs: locked pack; candidate commit `c23be98034215c17c9c49a7e9b6302cb2ad1f18d`; pinned driver digests; pinned local BMAD 6.10.0 tree; `fixtures/live/qualification_contract/`.
- Outputs: pin revalidation evidence, containment preflight evidence, seeded disposable repository, protected preimages including harness caches and registrations.
- Entry criteria: fresh human authorization pins pack/audit hashes, candidate commit, driver digests, BMAD tree, disposable root, evidence roots, and the `EXECUTION_ENABLED` transition.
- Exit criteria: VM-001 and VM-002 PASS; preimages captured; no protected path touched.
- Stop or go gate: STOP on any pin mismatch, non-empty or symlinked disposable root, or preimage anomaly.

## MS-02 — Live proofs and human-reviewed promotion
- Objective: run the live authoring, typed-output, and denial proofs, then perform one human-reviewed promotion and export all evidence.
- Inputs: MS-01 PASS; pinned drivers; activation-pinned environment.
- Outputs: driver logs for both hook paths, typed-output validations, sentinel non-execution evidence, one hash-pinned immutable promotion with claim dispositions, digest-pinned exports in the external evidence root.
- Entry criteria: containment intact; pins unchanged; human available for promotion review during the activation window.
- Exit criteria: VM-003 through VM-007 PASS; every export exists externally with digests before any teardown action.
- Stop or go gate: STOP on any driver failure, untyped or binding output, sentinel execution, missing human review, or unexported evidence.

## MS-03 — Teardown, residue proof, governance, and closeout
- Objective: destroy the disposable repository, prove residue absence, run governance checks, and record the canonical closeout.
- Inputs: MS-02 PASS; preimages; external evidence.
- Outputs: teardown evidence, residue comparison, governance logs, bounded in-repo closeout evidence, canonical `EXECUTION_CLOSEOUT.json`, archived controls, final `PLANNING_ONLY` state.
- Entry criteria: all exports complete; pins unchanged.
- Exit criteria: VM-008 through VM-010 PASS; closeout recorded through the canonical validator while `EXECUTION_ENABLED` with live controls, then mode restored and controls archived; maximum status `FACTORY_BMAD_025_MS06_DISPOSABLE_LIVE_QUALIFIED`.
- Stop or go gate: STOP after first failure or after closeout. Completion grants no merge, publication, pilot, release, or rollout authority; human evidence review is mandatory.

## Sequence Summary
`MS-01 provision gate, then MS-02 live-proof and promotion gate, then MS-03 teardown and closeout gate, then human evidence review and STOP.`

## Bounded Deferrals
- None.
