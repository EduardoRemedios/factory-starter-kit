# V2 Guarantee Preservation Matrix For V3-OP-001

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial preservation matrix for `V3-OP-001` bounded code change profile candidate.

## Status
Research-only, non-enforcing decision-prep evidence. This document does not promote Factory v3, deprecate Factory v2, authorize operational use, or wire V3 checks into required gates.

## Purpose
Map the Factory v2 guarantees that would be collapsed or compressed by `V3-OP-001` to the V3 controls that must preserve them.

## Scope
- Profile: `V3-OP-001 Bounded Code Change`
- Profile evidence: `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`
- Default authority until release: Factory v2
- Fallback authority: Factory v2

## Matrix

| V2 Guarantee | V3-OP-001 Control | Preservation Decision | Required Evidence |
|---|---|---|---|
| Intent is explicit and hardened before execution. | Mission objective, success criteria, eligible-work rationale, explicit non-goals, and fallback triggers are required mission envelope fields. | PRESERVED FOR PROFILE | Mission envelope names objective, success criteria, non-goals, and no ambiguity remains. |
| Constraints are locked before work. | Authorized scope, forbidden scope, allowed commands, dependency policy, and authority limits are required before execution. | PRESERVED FOR PROFILE | Mission envelope lists file, command, tool, and dependency boundaries. |
| Risk is considered before work. | Profile exclusions and fallback triggers reject high-risk work before execution. | PRESERVED FOR PROFILE | Closeout records whether any exclusion or fallback trigger appeared. |
| Verification is designed before execution. | Verification commands, expected evidence paths, and halt-on-failure rules are required fields. | PRESERVED FOR PROFILE | Verification plan and command outputs exist before closeout. |
| Execution envelope is reviewable. | V3 mission envelope must contain objective, scope, authority, verification, evidence, halt, reentry, and fallback rules. | PRESERVED FOR PROFILE | Mission envelope is inspectable before execution. |
| Red/Blue/Purple hardening catches drift. | Profile requires advisory eval output, SIMPLE-CODE-GATE classification, and fallback on ambiguity, scope expansion, stale evidence, or unresolved blocker findings. | PRESERVED FOR PROFILE | Advisory findings are classified before operational closeout. |
| Pack audit gates human Go/No-go. | Profile use requires human sponsor approval and future operational-readiness release approval. | PRESERVED FOR PROFILE | Decision report names profile revision and human release approval. |
| Closeout evidence is replayable. | Profile requires branch, commit, model, harness, verification outputs, advisory eval outputs, findings, residual risks, and closeout decision. | PRESERVED FOR PROFILE | Closeout evidence bundle names exact paths and revisions. |
| SIMPLE-CODE-GATE remains mandatory. | Profile inherits `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`; unresolved blocker-class findings require remediation, explicit acceptance, or V2 fallback. | PRESERVED FOR PROFILE | SIMPLE-CODE-GATE classification appears in closeout. |
| Verification failure halts work. | Failed halt-on-failure verification must stop execution and preserve evidence. | PRESERVED FOR PROFILE | Halt evidence records failed command and no continuation. |
| Interruption and reentry do not invent state. | Reentry must resume from authored artifacts and halt on stale or conflicting state. | PRESERVED FOR PROFILE | Reentry evidence cites authored mission artifacts. |
| V2 remains available. | V2 fallback triggers are mandatory and include human sponsor request, ambiguity, scope expansion, missing authority, failed verification, and unresolved blocker findings. | PRESERVED FOR PROFILE | Mission envelope and closeout record fallback review. |
| Runtime-kernel authority is not claimed. | Profile excludes production action mediation, runtime-kernel authority, and separate governance kernel dependency. | PRESERVED FOR PROFILE | Boundary review and advisory eval output show no runtime-authority claim. |

## Result
The relevant Factory v2 guarantees are preserved for the narrow `V3-OP-001` profile definition when all listed controls are present.

This result is not an operational promotion. It only means the profile definition is sufficiently bounded for the next readiness steps.

## Remaining Decision Work
Completed decision-prep evidence now includes false-positive and false-negative classification, external-kernel boundary review, and the operational-readiness decision report for the profile.

Release approval is recorded at `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.
