# Risk Register — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Registered live-proof risks with mitigations and verification hooks.

| Risk ID | Severity | Risk | Mitigation | Verification |
|---|---|---|---|---|
| R-001 | Critical | Live proof is simulated instead of driven through the pinned drivers. | Only the three digest-pinned dedicated drivers produce valid live claims. | VM-001, VM-003 |
| R-002 | Critical | Disposable root overlaps or symlinks into a protected path. | Freshness, emptiness, non-symlink, outside-protected verification before seeding. | VM-002 |
| R-003 | Critical | Teardown destroys unexported promotion or log evidence. | Digest-pinned export to the external root strictly before teardown. | VM-007 |
| R-004 | Critical | Candidate or BMAD bytes drift from the qualified/pinned state. | Activation pins candidate commit, package digests, and the local BMAD 6.10.0 tree. | VM-001 |
| R-005 | Critical | BMAD output alters the disposable repository's Factory authority chain. | Authority-boundary live check after each workflow; deny-by-default enforcement. | VM-005 |
| R-006 | High | An allowed workflow emits binding or untyped context. | Typed `EVIDENCE_ONLY` validation of each emitted solution context. | VM-004 |
| R-007 | High | A prohibited or malformed path executes its causal sentinel live. | Sentinel non-execution proof through both hook paths. | VM-005 |
| R-008 | High | Promotion proceeds without the human review. | Halt on missing review during the activation window. | VM-006 |
| R-009 | High | Residue survives in harness caches or registrations. | Residue inventory includes caches and registrations; postimage comparison. | VM-008 |
| R-010 | High | Live output leaks secrets or floods the harness. | External full logs, bounded digests inline, secret scan before retention. | VM-009 |
| R-011 | Medium | Partial success is claimed as qualification. | Partial-success rule maps any gap to `NO_GO`/`BLOCKED`. | VM-010 |
| R-012 | Medium | Evidence volume exceeds reviewable bounds. | External ceiling and bounded in-repo closeout evidence set. | VM-009, VM-010 |

## Notes
- Every Critical risk maps to at least one V3-or-higher verification check at Stage F.
- No risk is accepted without mitigation; none is deferred.
