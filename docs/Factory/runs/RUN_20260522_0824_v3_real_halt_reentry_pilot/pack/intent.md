# Intent - V3 Real Halt And Reentry Pilot

## Version
v2

## Change Log
- v1 (2026-05-22): Initial Stage A intent.
- v2 (2026-05-22): Stage C synthesis clarified proof scenarios and non-promotion limits.

## Purpose
Prove the real operational behavior needed for V3 decision-checklist items C-01 and C-02.

## Goal
Execute a run-local pilot harness that demonstrates failed-command halt behavior and authored-artifact reentry behavior.

## Non-goals
- Do not promote V3 operationally.
- Do not deprecate or discourage V2.
- Do not modify Factory production validators.
- Do not wire V3 checks into required gates.
- Do not implement natural-language detection.
- Do not claim runtime-kernel authority or production proof.

## Proof Scenarios
1. Failed-command halt: a halt-on-failure command exits nonzero, the pilot records halt, and no continuation action is performed.
2. Valid reentry: authored source state and derived cursor agree, so resume is allowed from authored artifacts.
3. Stale reentry: derived cursor conflicts with authored source state, so resume halts and evidence records the conflict.

## Acceptance Criteria
- Evidence JSON exists for all three proof scenarios.
- Closeout maps evidence to checklist C-01 and C-02.
- Operational decision checklist is updated from OPEN to PARTIAL or DONE only according to the evidence.
- All verification commands pass.

## Open Issues
### BLOCKING
- None.

### NON-BLOCKING
- This pilot proves run-local behavior, not full V3 operational profile promotion.
