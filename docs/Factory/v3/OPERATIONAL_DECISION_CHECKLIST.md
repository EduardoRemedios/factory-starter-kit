# Factory v3 Operational Decision Checklist

## Version
v0.1

## Change Log
- v0.1 (2026-05-21): Initial high-level checklist of evidence still required before deciding whether Factory v3 can be used operationally.

## Status
Decision-prep checklist only. This document does not promote Factory v3, deprecate Factory v2, authorize operational use, or wire V3 checks into required gates.

## Purpose
Provide the high-level checklist that must be satisfied before making a decision on operational Factory v3 use.

Factory v3 can move out of research mode only when the remaining evidence shows that V3 preserves the relevant Factory v2 safety guarantees for a named operational profile, while Factory v2 remains supported and available as fallback.

## Current Posture
- Factory v3 status: Level 0 research only.
- V2 status: authoritative and supported.
- V3 eval runner status: standalone advisory only.
- Latest confidence signal: improved after the confidence pilot batch, but not sufficient for operational use.

## Decision Checklist

| ID | Check | Required Evidence | Status |
|---|---|---|---|
| C-01 | Real failed-command halt behavior is proven. | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/halt_failed_command/result.json` and closeout show nonzero command halt, preserved evidence, and no continuation marker. | DONE |
| C-02 | Real interruption/reentry behavior is proven. | `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/reentry_valid/result.json` and `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/execution_evidence/reentry_stale_cursor/result.json` show authored-artifact resume and stale cursor halt. | DONE |
| C-03 | Natural-language advisory detection is implemented and measured. | `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/execution_evidence/NL_DETECTION_MEASUREMENT_REPORT.md` shows opt-in pilot detection with 0 false positives across 10 clean artifacts and expected drift IDs detected. | DONE |
| C-04 | V3-G011 severity policy is decided. | `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md` defines cross-version blocker, advisory-high, and no-finding rules; V3-G011 remains advisory in research mode and becomes blocker-class for future operational V3 profiles when the policy's blocker conditions are met. | DONE |
| C-05 | Operational profile is named and bounded. | A concrete profile defining eligible work types, excluded work, authority limits, verification expectations, and V2 fallback triggers. | OPEN |
| C-06 | V2 fallback remains explicit. | Operational profile and decision report state when work must stay on or return to Factory v2. | OPEN |
| C-07 | V2 guarantee preservation matrix is complete. | Decision report maps collapsed V2 ceremony to equivalent V3 guarantees with no unresolved critical gaps. | OPEN |
| C-08 | False-positive and false-negative review is complete. | Human classification of real shadow, seeded, positive routing, and natural-language findings. | OPEN |
| C-09 | AEGIS/runtime-kernel boundary review passes. | Evidence that V3 remains coding-governance only and does not claim runtime proof, production mediation, or kernel authority. | OPEN |
| C-10 | Operational-readiness decision report is complete. | Report names exact artifact paths, revisions, pilot results, residual risks, and human release approval. | OPEN |

## Already Satisfied Or Partially Satisfied

| Area | Evidence | Status |
|---|---|---|
| Clean real-run shadow scans | Three clean V2-authoritative shadow scans exist across prior pilots and `RUN_20260521_0948_v3_confidence_pilot_execution`. | PARTIAL |
| Seeded negative detection | V3-G003, V3-G005, V3-G006, V3-G007, V3-G009, V3-G010, V3-G011, and V3-G014 have seeded evidence. | PARTIAL |
| Positive routing | V3-G012 and V3-G013 pass as positive routing cases. | PARTIAL |
| Natural-language design | Bounded design and false-positive budget exist at `docs/Factory/runs/RUN_20260521_0948_v3_confidence_pilot_execution/execution_evidence/NATURAL_LANGUAGE_DETECTION_DESIGN.md`. | PARTIAL |
| Real halt and reentry behavior | C-01 and C-02 evidence exists at `docs/Factory/runs/RUN_20260522_0824_v3_real_halt_reentry_pilot/EXECUTION_CLOSEOUT.md`. | DONE |
| Natural-language pilot measurement | C-03 evidence exists at `docs/Factory/runs/RUN_20260522_0836_v3_nl_detection_pilot/EXECUTION_CLOSEOUT.md`. | DONE |
| SIMPLE-CODE-GATE severity policy | C-04 evidence exists at `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md` and `docs/Factory/runs/RUN_20260522_0948_v3_g011_severity_policy/EXECUTION_CLOSEOUT.md`. | DONE |

## Decision Rule
Do not approve operational Factory v3 use until every `OPEN` checklist item is either:
- completed with evidence paths, or
- explicitly waived by the human sponsor with rationale and residual risk.

No waiver may remove these hard requirements:
- V2 remains supported and available as fallback.
- V3 must not claim runtime-kernel authority.
- Verification failure must halt for any operational profile.
- Human release approval must name the exact operational profile being promoted.

## Recommended Next Work
Prioritize in this order:

1. Operational profile boundary drafting.
2. V2 guarantee preservation matrix completion.
3. False-positive and false-negative review rollup.
4. AEGIS/runtime-kernel boundary review.
5. Operational-readiness decision report drafting.
