# Verification Plan — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Bound live-proof checks, drivers, evidence rules, and the executable manifest.

## Posture
- Audited mode: `PLANNING_ONLY`; no command below is execution authority.
- Locked intent SHA-256: `40d281e56319c05782a74b288e3b8cdf1393d040fac454d1cbccac127623c6d8`.
- `verification_manifest.yaml` binds VM-001 through VM-010 for canonical closeout recording. A later activation must pin exact current hashes, driver digests, environment values, the disposable root, and the local BMAD 6.10.0 tree without changing this audited pack.
- All disposable-root, harness-binary, and evidence-root locations reach the pinned drivers only through activation-pinned environment values; no absolute path appears in any planned command.

## Checks
- VM-001 — V4 source revalidation: candidate commit, plugin package digests, driver digests, BMAD 6.10.0 tree digests, and the live qualification contract fixture match activation pins before any live action and after closeout.
- VM-002 — V3 containment preflight: the disposable root is fresh, empty, non-symlinked, outside every protected root, and contains no symlink into protected paths, verified through the pinned preflight driver before seeding.
- VM-003 — V4 live authoring proof: architecture, UX, and spec workflows run through the pinned drivers across both hook paths and complete without touching Factory state.
- VM-004 — V3 typed-output validation: every emitted solution context is typed `SOLUTION_CONTEXT` with `EVIDENCE_ONLY` authority, non-binding, and unable to alter the disposable repository's Factory authority chain.
- VM-005 — V4 live denial proof: prohibited, unknown, malformed, and unsafe-layout paths deny before causal sentinels through both hook paths; sentinel non-execution is evidenced.
- VM-006 — V4 promotion review: the human reviews the concrete snapshot during the activation window and one immutable, hash-pinned promotion with explicit claim dispositions is recorded; a missing review halts.
- VM-007 — V3 evidence export: promotion evidence and complete live logs are exported to the external evidence root with digests strictly before teardown.
- VM-008 — V4 teardown and residue: the disposable repository is removed with evidence, and protected paths, harness plugin caches, and worktree registrations are preimage-equal.
- VM-009 — V3 evidence bounds: external evidence stays within its ceiling, harness output stays bounded, and live logs pass the secret scan before retention.
- VM-010 — V3 governance audit: knowledge lint, stage F-I2 lints, pack-lint, the partial-success rule, and the status ceiling hold; exclusions (AuditEdge, candidate mutation, delivery authority) are respected.

## Planned Commands After Separate Authorization
- Containment preflight: `./scripts/factory-python scripts/verify_factory_bmad_live_preflight.py` with activation-pinned arguments.
- Live composition and authoring: `bash scripts/verify_factory_bmad_claude_composition.sh` with the activation-pinned environment.
- Live pilot and denial proof: `bash scripts/verify_factory_bmad_live_pilot.sh` with the activation-pinned environment.
- Governance: `bash scripts/knowledge_lint.sh`, stage F-I2 lints, and `pack-lint`.

## Lifecycle
1. Revalidate all pins and the contract fixture; verify containment; seed the disposable repository from the pinned candidate packages and BMAD tree.
2. Run the live authoring proofs, typed-output validation, and live denial proofs through the pinned drivers.
3. Perform the human-reviewed promotion; export promotion evidence and full logs with digests.
4. Tear down the disposable repository; prove residue absence against preimages.
5. Run governance checks; record the canonical closeout while `EXECUTION_ENABLED` with live controls; restore `PLANNING_ONLY`; archive controls; stop for human evidence review.

## Evidence Rules
- Complete live logs live only in the external evidence root; the harness receives bounded digests and verdicts.
- Every denial proof shows sentinel non-execution; every allowed proof shows typed non-binding output.
- Any missing or failed proof yields `NO_GO`, or `BLOCKED` when a proof could not run; the maximum status is `FACTORY_BMAD_025_MS06_DISPOSABLE_LIVE_QUALIFIED`.
