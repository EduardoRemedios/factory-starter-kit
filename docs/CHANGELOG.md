# Changelog

## 2026-05-21
- Added Factory v3 operational decision checklist capturing the remaining evidence gates before any V3 operational-use decision.
- Added execution-enabled V3 confidence pilot batch with two additional clean real shadows, seeded V3-G003/G006/G010/G014 evidence, controlled V3-G005 halt evidence, V3-G012/V3-G013 positive routing passes, and a bounded natural-language detection design.
- Added a Factory v2 planning pack for the V3 eval evolution decision; the pack selects a staged confidence path toward future operational V3 use while keeping V2 authoritative.
- Added Factory v3 operational-readiness evidence rollup across the clean shadow pilot and seeded drift pilots; V3 remains research-only and V2 remains authoritative.
- Added seeded V3 operational-readiness drift pilot reports for `V3-G005` verification halt behavior and `V3-G011` SIMPLE-CODE-GATE detection.
- Added second seeded V3 operational-readiness drift pilot report with accepted `V3-G009` runtime-boundary detection and non-blocking output.
- Added first seeded V3 operational-readiness drift pilot report with accepted `V3-G007` detection and non-blocking output.
- Added the first real-run V3 operational-readiness shadow pilot report; the standalone eval returned `ADVISORY_PASS` and did not authorize promotion.
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
