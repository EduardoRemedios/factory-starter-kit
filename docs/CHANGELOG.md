# Changelog

## 2026-05-24
- Added Factory v3 Phase 1 trial operating plan and trial index for real-project `V3-OP-001` evidence collection.

## 2026-05-22
- Added Factory v3 Phase 1 trial capture template for real-project `V3-OP-001` evidence collection.
- Added Factory v3 roadmap pre-mortem with failure modes, Phase 1 watchpoints, and a golden-fixture backlog.
- Added Factory v3 vision and phased roadmap documents for moving from optional `V3-OP-001` use toward the full mission-governance runtime vision.
- Updated the top-level and V3 README files so adopters can discover optional `V3-OP-001` operational use and the V3 user guide.
- Recorded optional operational release approval for `V3-OP-001` and added the V3 Codex user guide with starter templates.
- Added `V3-OP-001` operational-readiness decision report; C-10 is now ready for explicit human release approval.
- Added `V3-OP-001` external-kernel boundary review; C-09 is now marked DONE in the V3 operational checklist.
- Added `V3-OP-001` finding classification rollup for real shadow, seeded drift, positive routing, and natural-language evidence; C-08 is now marked DONE in the V3 operational checklist.
- Added bounded `V3-OP-001` operational profile candidate and V2 guarantee preservation matrix; C-05, C-06, and C-07 are now marked DONE in the V3 operational checklist.
- Added cross-version SIMPLE-CODE-GATE severity policy for ordinary Factory V2/V3 repos and marked V3 operational checklist C-04 DONE.
- Added opt-in V3 natural-language advisory detection pilot with zero false positives across 10 clean artifacts and expected drift IDs detected; C-03 is now marked DONE in the operational decision checklist.
- Added execution-enabled V3 real halt and reentry pilot evidence; C-01 and C-02 are now marked DONE in the operational decision checklist.

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
