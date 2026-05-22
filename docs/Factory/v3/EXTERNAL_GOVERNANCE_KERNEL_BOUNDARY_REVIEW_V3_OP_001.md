# External Governance Kernel Boundary Review For V3-OP-001

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial C-09 boundary review for `V3-OP-001`.

## Status
Research-only, non-enforcing decision-prep evidence. This document does not promote Factory v3, deprecate Factory v2, authorize operational use, or wire V3 checks into required gates.

## Purpose
Complete the C-09 boundary review for `V3-OP-001 Bounded Code Change`.

The review checks whether the profile remains an SDLC coding-governance profile and avoids duplicating any lower-level autonomy governance kernel.

## Scope
- Profile: `V3-OP-001`
- Profile document: `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`
- Boundary source: `docs/Factory/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY.md`
- Default authority until release: Factory v2
- Gate effect: none
- Promotion decision: not authorized

## Boundary Summary
`V3-OP-001` passes the external-kernel boundary review for decision-prep purposes.

The profile is suitable for ordinary repositories without a separate governance kernel because it uses process artifacts, verification commands, evidence paths, halt rules, and V2 fallback. It is also compatible with repositories that have a separate governance kernel because it does not duplicate kernel-owned runtime authority, policy, leases, proof, or production action behavior.

Optional operational release approval for `V3-OP-001` is recorded separately at `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.

## Source Review

| Source | Boundary-Relevant Content | Review Result |
|---|---|---|
| `docs/Factory/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY.md` | Factory governs coding missions; external kernels govern autonomous system behavior at runtime. | PASS |
| `docs/Factory/ARCHITECTURE.md` | Factory Core includes external governance-kernel boundary rules and is not a second runtime governance kernel. | PASS |
| `docs/Factory/ORCHESTRATION.md` | External governance kernel boundary is hard when present; Factory artifacts may map to kernel inputs through adapters. | PASS |
| `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md` | Profile excludes runtime-kernel authority, production action mediation, separate governance kernel dependency, CI wiring, V2 deprecation, and unbounded autonomous execution. | PASS |
| `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md` | Runtime-kernel authority is a preserved V2 guarantee for the profile only when boundary review and advisory eval output show no authority claim. | PASS |
| `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md` | Current measured evidence has no known false positives and no measured seeded or natural-language false negatives, but broad production discovery is not measured. | PASS |

## Ownership Matrix

| Concern | Factory V3-OP-001 Ownership | External Kernel Ownership | Result |
|---|---|---|---|
| Coding objective | Defines bounded software-delivery objective and success criteria. | None required. | PASS |
| Repo scope | Defines authorized files, forbidden files, commands, dependency policy, and verification expectations. | May consume these as inputs if a kernel exists. | PASS |
| Verification evidence | Records command output, advisory eval output, diff evidence, and closeout residual risk. | May attach Factory evidence to a kernel evidence bundle if a kernel exists. | PASS |
| Halt and reentry | Requires failed verification halt, authored-artifact reentry, and stale-state halt for coding work. | Owns runtime revocation, rollback, or domain action controls. | PASS |
| Runtime authority | No ownership. The profile does not approve deployed autonomous behavior. | Owns runtime leases, policy gates, safety checks, and domain action permissions. | PASS |
| Production action behavior | No ownership. The profile excludes production action mediation. | Owns production action admission and mediation. | PASS |
| Audit-grade runtime proof | No ownership. Factory evidence is delivery evidence only. | Owns proof bundles or offline verification where applicable. | PASS |
| Separate governance kernel dependency | No dependency. Ordinary repositories can use Factory process governance without a separate governance kernel. | Optional substrate only when an adopting repository already has one. | PASS |

## Ordinary Repository Review
Most adopting repositories will not have a separate governance kernel. `V3-OP-001` remains useful in those repositories because it requires only:

- an explicit mission objective,
- authorized and forbidden repo scope,
- allowed commands,
- dependency policy,
- verification commands and evidence paths,
- halt and reentry rules,
- SIMPLE-CODE-GATE review,
- V2 fallback triggers,
- human sponsor approval for profile use.

These are process-governance controls. They do not imply runtime enforcement.

## Separate-Kernel Repository Review
For repositories with a separate lower-level governance kernel, `V3-OP-001` should remain above the kernel as the SDLC mission-governance layer.

Allowed relationship:
- Factory mission envelope fields may become kernel policy inputs.
- Factory verification outputs may be attached to kernel evidence bundles.
- Factory escalation events may trigger kernel reentry or revocation workflows through a project adapter.

Forbidden relationship:
- Factory must not become the kernel ledger.
- Factory must not become the policy engine.
- Factory must not become the runtime action gate.
- Factory must not become the proof authority.
- Factory must not create a second source of truth for runtime authority, evidence, or mission state.

## Forbidden-Claim Checklist

| Claim Type | Review |
|---|---|
| `V3-OP-001` approves Factory v3 operational use. | Not present. C-10 remains required. |
| `V3-OP-001` removes Factory v2 fallback. | Not present. V2 fallback is mandatory. |
| `V3-OP-001` makes a separate governance kernel mandatory. | Not present. A separate governance kernel is optional. |
| `V3-OP-001` provides runtime authority. | Not present. Factory v3 does not claim runtime authority. |
| `V3-OP-001` provides production action mediation. | Not present. Production action mediation is excluded. |
| `V3-OP-001` provides audit-grade runtime proof. | Not present. Factory evidence is delivery evidence only. |
| `V3-OP-001` changes validators, gates, CI, or required checks. | Not present. Current checks remain standalone advisory only. |

## Boundary Decision
C-09 is complete for `V3-OP-001`.

Decision basis:
- `V3-OP-001` is coding-governance only.
- A separate governance kernel remains optional.
- Ordinary non-kernel repositories remain supported.
- Repositories with a lower-level kernel can map Factory artifacts through adapters without duplicating kernel authority.
- Factory v2 remains authoritative until a future release decision.
- Operational use remains limited to optional `V3-OP-001`.

## Residual Risk
- This review is document and evidence based. It does not test a live external governance kernel adapter.
- Broad production false-negative discovery remains outside the current measured evidence set.
- Future expansion beyond optional `V3-OP-001` requires explicit human approval.

## Next Step
Collect real-project trial feedback for optional `V3-OP-001` use.
