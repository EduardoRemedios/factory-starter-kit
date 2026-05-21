# Changelog

## 2026-05-21
- Added standalone Factory v3 operational-readiness eval runner, golden fixtures, and decision report template; the runner is advisory and not wired into required Factory gates.
- Added an execution-enabled Factory v2 implementation-plan pack for the standalone V3 operational-readiness eval suite; code changes still require post-I2 human GO.
- Added a Factory v2 planning pack for the V3 operational-readiness eval suite, with `pack-lint` passing and V3 remaining research-only.
- Added Factory v3 operational-readiness pre-mortem and eval planning for future optional V3 operational use while keeping Factory v2 supported.

## 2026-05-19
- Added promotion-evidence advisory lint pilot evidence that classifies a missed `V3-A006` signal and recommends bounded matcher tuning in a later run.
- Tuned `V3-A006` promotion-evidence matching to catch local release claims masked by target-wide evidence language, with a regression fixture.
- Added post-tuning `V3-A006` real-doc smoke evidence confirming local release claims are caught while final Factory v3 docs remain clean.

## 2026-05-18
- Added Factory v3 Level 0 research evidence and advisory validator design packs.
- Added optional standalone Factory v3 advisory lint prototype at `scripts/factory_v3_advisory_lint.py`.
- Added deterministic advisory lint fixtures for clean, warning, and promotion-claim cases.
- Added execution closeout evidence and a deterministic pilot usage fixture for Factory v3 advisory lint.
- Recorded canonical tracking state for the advisory lint prototype, closeout evidence, pilot result, and next blocked/allowed steps.
- Added the first real-branch advisory lint pilot report with zero findings and no matcher tuning.
- Added a non-empty real-branch advisory lint pilot report with 2 accepted findings, remediation, and no matcher tuning.
- Added a planning-only Factory v2 pack for the next promotion-evidence advisory lint pilot.
- Kept Factory v3 advisory lint non-blocking and outside all required Factory v2 gates.
