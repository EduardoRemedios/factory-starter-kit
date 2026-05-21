# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-21): Stage F verification plan.

## Verification Items

| ID | Tier | Check | Pass Criteria |
|---|---|---|---|
| VP-01 | V0 | Readiness thresholds are explicit. | `intent.md` and envelope list thresholds before operational V3 use. |
| VP-02 | V0 | V2 fallback remains mandatory. | Pack states V2 remains authoritative and supported. |
| VP-03 | V1 | False-positive budget is required for natural-language detection. | Envelope includes a measurable review budget before broader detection can influence confidence. |
| VP-04 | V0 | Trigger-marker coverage remains regression backbone. | Micro-sprints preserve deterministic fixture coverage. |
| VP-05 | V0 | Missing confidence pilots are named. | Interruption/reentry, V2 fallback, failed-verification, and additional shadow pilots are required. |
| VP-06 | V0 | SIMPLE-CODE-GATE severity policy is carried forward. | Risk register and micro-sprints include severity decision before promotion. |
| VP-07 | V1 | Pack validates. | `stage-lint` and `pack-lint` pass. |

## No Runnable Manifest
This is a `PLANNING_ONLY` run and does not include `verification_manifest.yaml`.

## Exit Criteria Status
- PASS
