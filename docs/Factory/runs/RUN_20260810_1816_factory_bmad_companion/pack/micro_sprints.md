# Micro-sprints — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Sequenced the bounded companion implementation.

## Global Ordering

Execute MS-00 through MS-06 in order. A failed exit gate halts all later work.
No micro-sprint may access the live application-pilot repository, a real Claude profile, or customer
material.

## MS-00 — Verification Scaffold and Baseline

- Objective: freeze allowed paths/digests and land planned fixtures/test shells.
- Inputs: locked intent, traceability matrix, verification manifest, current 0.2.0 packages.
- Outputs: baseline evidence root, executable test inventory, protected-path digests.
- Entry: exact human execution authorization matches the final pack digest.
- Exit: every VM command resolves to a test/script location; baseline privacy and no-touch scans pass.
- Stop/go: stop on dirty in-scope drift, private data, missing source pin, or unclassified external command.

## MS-01 — Companion Source, Packaging, and Dependency

- Objective: create one authored `factory-bmad` source and deterministic Claude/Codex package generation.
- Inputs: plugin-creator rules, Factory build architecture, current official Claude dependency schema.
- Outputs: manifests, skills, runtime skeleton, ownership, marketplace entries, build tests.
- Entry: MS-00 PASS.
- Exit: deterministic builds, strict schemas, namespace checks, and Factory non-duplication pass.
- Stop/go: stop if dependency constraints or same-marketplace composition cannot be validated.

## MS-02 — Diagnose and BMAD Bootstrap

- Objective: implement five-state routing and pinned BMAD install preview/audit/recovery.
- Inputs: state and pinned-install fixtures; official 6.10.0 package metadata.
- Outputs: diagnose/bootstrap skills, runtime evaluators, receipts, focused tests.
- Entry: MS-01 PASS.
- Exit: VM-002 passes; preview is zero-write; unexpected/partial state halts safely.
- Stop/go: stop on any write outside approved prefixes or uncertain automatic cleanup.

## MS-03 — Policy and Project Adapter

- Objective: implement authority policy, module/workflow classification, companion ownership, and seed-only project adapter setup.
- Inputs: module matrix; Factory project-preflight contract.
- Outputs: one-page policy, adapter setup preview/receipt, policy validator, documentation.
- Entry: MS-02 PASS.
- Exit: VM-003 passes; existing user policy/preflight files conflict rather than overwrite.
- Stop/go: stop if BMM downstream availability cannot be separated from companion routing.

## MS-04 — Promotion and Intake

- Objective: implement immutable snapshot promotion, embedded-checklist brief intake, and fail-closed preflight.
- Inputs: promotion/preflight fixtures; `docs/upstream` index contract.
- Outputs: promotion/intake skills, snapshot manifest/receipt schemas, rollback, preflight command and tests.
- Entry: MS-03 PASS.
- Exit: VM-004 and VM-005 pass, including symlink/traversal/stale/interruption/reuse cases.
- Stop/go: stop on mutable evidence, direct draft citation, unsafe path, or incomplete human review evidence.

## MS-05 — UX, Canonical Docs, and Regression

- Objective: make outputs concise and align public policy, onboarding, state, roadmap, changelog, and packages.
- Inputs: summary-output fixture; actual completed behavior.
- Outputs: concise formatter, JSON mode, updated canonical docs, exact generated doc mirrors/ownership digests, current generated packages.
- Entry: MS-04 PASS.
- Exit: VM-007–VM-010 pass; public status says technical `REVIEW_READY` only.
- Stop/go: stop on private data, support overclaim, stale package, regression, or unapproved dependency.

## MS-06 — Isolated Live Claude/BMAD Proof and Closeout

- Objective: prove dependency composition and a full pinned BMAD upstream journey in disposable state.
- Inputs: final packages, Claude Code supported binary/auth, official BMAD 6.10.0 package.
- Outputs: VM-006/VM-011 evidence, scoped diff, closeout draft and recorded closeout.
- Entry: MS-05 PASS and explicit authorization for isolated live checks.
- Exit: all VM checks PASS; closeout validates as `REVIEW_READY`; no real-profile or application-pilot mutation.
- Stop/go: stop on auth/network ambiguity, profile mutation, dependency error, unexpected installer write, or evidence gap.

## Completion Boundary

Completion permits maintainer review and a later application-pilot decision. It
does not permit merge, tag, publication, organization rollout, or downstream
application execution.
