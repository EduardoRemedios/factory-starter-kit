# Operational Readiness Decision Report For V3-OP-001

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial C-10 decision report for `V3-OP-001`.

## Status
Decision report complete. Operational release approval is recorded in `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.

This document supports optional operational use of `V3-OP-001` only. It does not make Factory v3 the default, deprecate Factory v2, approve any other V3 profile, or wire V3 checks into required gates.

## Decision Metadata
- Decision: APPROVED FOR OPTIONAL OPERATIONAL USE
- Release approval: `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`
- Promotion target: `V3-OP-001 Bounded Code Change`
- Promotion level: optional operational profile, not default Factory mode
- Date: 2026-05-22
- Human approver: Eduardo Remedios
- Evidence baseline branch: `main`
- Evidence baseline revision before this report: `c91398e`
- Approval commit: `f07fa11`

## Scope
- V3 profile evaluated: `V3-OP-001 Bounded Code Change`
- V2 fallback retained: YES
- separate governance kernel dependency introduced: NO
- Runtime-kernel authority introduced: NO
- Required-gate integration introduced: NO
- Factory v2 deprecation introduced: NO

## Decision Summary
The evidence supports a human release decision for narrow, optional Factory v3 operational use under `V3-OP-001`.

The evidence does not support making Factory v3 the default, removing Factory v2, wiring V3 checks into required gates, applying V3 to broad or ambiguous missions, or claiming runtime proof or production mediation from Factory artifacts.

Operational use is approved only within this release scope:

- `V3-OP-001` is approved for optional operational use,
- Factory v2 remains supported and available as fallback,
- approval applies at commit `f07fa11`,
- the residual risks in this report are accepted.

## Evidence Inputs

| Checklist ID | Evidence | Result |
|---|---|---|
| C-01 | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/halt_failed_command/result.json`; `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md` | Real failed-command halt behavior proven for the pilot. |
| C-02 | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/reentry_valid/result.json`; `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/reentry_stale_cursor/result.json` | Authored-artifact reentry and stale-cursor halt proven for the pilot. |
| C-03 | `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/execution_evidence/NL_DETECTION_MEASUREMENT_REPORT.md` | Natural-language advisory detection measured with 0 false positives across 10 clean artifacts and expected drift IDs detected. |
| C-04 | `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`; `docs/Factory/runs/RUN_20260522_0948_v3_g011_severity_policy/EXECUTION_CLOSEOUT.md` | SIMPLE-CODE-GATE severity policy decided for V2 and V3. |
| C-05 | `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md` | Profile is named and bounded. |
| C-06 | `docs/Factory/v3/OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md` | V2 fallback triggers are explicit. |
| C-07 | `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1019_v3_operational_profile_matrix/EXECUTION_CLOSEOUT.md` | V2 guarantees are preserved for the narrow profile definition. |
| C-08 | `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1052_v3_fp_fn_rollup/EXECUTION_CLOSEOUT.md` | Finding classifications complete for current evidence set. |
| C-09 | `docs/Factory/v3/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY_REVIEW_V3_OP_001.md`; `docs/Factory/runs/RUN_20260522_1120_v3_boundary_review/EXECUTION_CLOSEOUT.md` | Boundary review passes for decision-prep purposes. |

## Pilot Results

| Area | Evidence | Result |
|---|---|---|
| Real shadow scans | `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md` | 3 accepted clean real-shadow scans; 0 known false positives. |
| Seeded drift | `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md` | 9 accepted seeded findings across V3-G003, V3-G005, V3-G006, V3-G007, V3-G009, V3-G010, V3-G011, and V3-G014. |
| Positive routing | `docs/Factory/v3/FINDING_CLASSIFICATION_ROLLUP_V3_OP_001.md` | V3-G012 and V3-G013 accepted positive routing cases. |
| Natural-language pilot | `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/execution_evidence/NL_DETECTION_MEASUREMENT_REPORT.md` | 10 clean artifacts measured with 0 findings; 7 drift IDs detected in curated corpus. |
| Current V3 docs scan | `docs/Factory/runs/RUN_20260522_1120_v3_boundary_review/execution_evidence/verification/docs_v3_nl_pilot.json` | `ADVISORY_PASS`, 0 findings after C-09. |

## Required Checks

| Check | Status | Evidence |
|---|---|---|
| V2 guarantee preservation matrix has no unresolved Critical gaps. | YES | `docs/Factory/v3/V2_GUARANTEE_PRESERVATION_MATRIX_V3_OP_001.md` |
| Golden fixtures pass and include negative cases. | YES | `tests/fixtures/factory_v3_operational_readiness_eval/expected.json`; `docs/Factory/runs/RUN_20260521_0833_v3_eval_suite_impl_plan/EXECUTION_CLOSEOUT.md` |
| Verification failure behavior tested. | YES | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md` |
| Interruption and reentry behavior tested. | YES | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md` |
| V2 fallback behavior tested. | YES | `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/pilots/v3g012_v2_fallback/REPORT.md`; `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/pilots/v3g013_v3_with_fallback/REPORT.md` |
| external-kernel boundary review passes. | YES | `docs/Factory/v3/EXTERNAL_GOVERNANCE_KERNEL_BOUNDARY_REVIEW_V3_OP_001.md` |
| SIMPLE-CODE-GATE remains mandatory for code-changing work. | YES | `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md` |
| Human release approval recorded. | YES | `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md` |

## Residual Risks

| Risk | Treatment |
|---|---|
| Broad production false-negative discovery is not measured. | Accept only for narrow `V3-OP-001`; collect more real-use evidence after optional release. |
| Current release target is optional profile use, not default Factory mode. | Keep V2 authoritative and available as fallback. |
| V3 checks remain standalone advisory only. | Do not wire into required gates without a later Factory run and explicit approval. |
| No live external governance kernel adapter was tested. | Accept because `V3-OP-001` does not require external governance kernel and does not claim kernel behavior. |
| User-facing operating instructions are new. | Use `docs/Factory/v3/USER_GUIDE.md` for initial trials and update it from real project feedback. |

## Release Conditions
Operational use must stay within these conditions:

- profile approved: `V3-OP-001 Bounded Code Change`,
- release scope: optional use only,
- fallback: Factory v2 remains supported and available,
- approval commit: `f07fa11`,
- accepted residual risks,
- first-use monitoring expectations,
- rollback rule: return to Factory v2 on ambiguity, failed verification, stale evidence, missing authority, or human request.

## Decision Rationale
C-01 through C-09 provide enough evidence for optional operational use of `V3-OP-001`: real halt and reentry behavior have been tested, natural-language detection has been measured, SIMPLE-CODE-GATE severity is defined, the profile is bounded, V2 fallback is explicit, V2 guarantees are mapped, finding classifications are complete for the current evidence set, and the external-kernel boundary passes. The explicit release approval is now recorded.

## No-Go Carry-Forward
If release approval is not granted, carry forward:

- record the human reason for no-go,
- keep V3 at research and decision-prep status,
- continue using Factory v2 as the authoritative process,
- collect any requested additional evidence through a new Factory run.

## Recommended Next Step
Use `docs/Factory/v3/USER_GUIDE.md` for initial trials in real projects and capture feedback in follow-up Factory evidence.
