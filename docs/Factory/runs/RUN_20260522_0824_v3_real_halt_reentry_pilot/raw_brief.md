# Raw Brief - V3 Real Halt And Reentry Pilot

## Source
Human sponsor approved the advised next step on 2026-05-22: proceed with the real operational behavior pilot for V3 halt and reentry behavior.

## Execution Authorization
- Execution Mode: EXECUTION_ENABLED
- Execution Authorization: Human sponsor message "agree please proceed" on 2026-05-22.
- Downstream Fan-Out: NOT APPROVED

## Problem
Factory v3 cannot be considered for operational use until real operational behavior is proven, not only seeded text detection. The current decision checklist still has two critical open items:
- C-01: real failed-command halt behavior
- C-02: real interruption/reentry behavior from authored artifacts

## Goal
Run a bounded, run-local pilot that proves:
1. a failed halt-on-failure command stops the pilot and preserves evidence
2. reentry accepts matching authored state
3. reentry halts when a derived cursor conflicts with authored source artifacts

## Scope
- Create run-local harness and evidence under this run root.
- Do not modify production Factory validators or V3 advisory runner code.
- Update the V3 operational decision checklist and canonical tracking docs after closeout.

## Out of Scope
- No V3 operational promotion.
- No required-gate integration.
- No CI integration.
- No runtime-kernel, AEGIS authority, production mediation, or proof claims.
- No broader natural-language detection work.

## Acceptance Criteria
- Pack reaches Stage I2 PASS.
- Human GO is recorded.
- Run-local pilot executes and writes evidence.
- Failed-command scenario records halt and no continuation.
- Valid reentry scenario records resume from authored artifacts.
- Stale reentry scenario records halt on conflict.
- Verification and pack checks pass.
