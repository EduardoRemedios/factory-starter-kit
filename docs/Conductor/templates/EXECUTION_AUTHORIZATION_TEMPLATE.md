# Execution Authorization

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

<!--
VALIDATION:
- Create only for a post-I2 PLANNING_ONLY to EXECUTION_ENABLED transition.
- Create at docs/Conductor/runs/<RUN_ID>/EXECUTION_AUTHORIZATION.md.
- Compute both SHA-256 values from the unchanged reviewed pack artifacts.
- Each required authorization field must occur exactly once.
- The record must be a regular non-symlink file.
- Do not rewrite PACK_MANIFEST.md, PACK_AUDIT_REPORT.md, the sprint envelope, or verification_manifest.yaml during activation.
- Confirm closeout producibility before activation: when verification_plan.md declares runnable VM checks, pack/verification_manifest.yaml must already exist in the audited pack (pack-lint fails an execution-enabled run without it), and the closeout must be recorded while this authorization is live and EXECUTION_MODE.txt is EXECUTION_ENABLED.
-->

## Version

v1

## Change Log

- v1 (YYYY-MM-DD): Recorded digest-bound execution activation.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `<64-character lowercase SHA-256>`
- Authorized Pack Audit SHA-256: `<64-character lowercase SHA-256>`

## Human Decision Reference

- Record the exact human approval or its immutable local reference here.

## Authority Boundary

- This record activates only the reviewed pack whose exact manifest and audit hashes appear above.
- It grants no merge, publication, release, rollout, downstream fan-out, or customer authority unless separately explicit.
