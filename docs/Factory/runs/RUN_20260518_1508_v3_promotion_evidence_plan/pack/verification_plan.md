# Verification Plan

## Version
v1

## Change Log
- v1 (2026-05-18): Initial verification plan for promotion-evidence advisory lint planning.

## Strategy
This is a `PLANNING_ONLY` pack. Verification proves that the future pilot remains reversible, advisory, non-blocking, and separate from Factory v2 required gates.

## Checks

### V1-CHECK-001 - Non-empty Promotion Warning Capture
- Tier: V1
- Covers: R-001, R-006
- Method: Future pilot runs `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json` while temporary promotion wording is present.
- Expected: Output includes a non-blocking promotion-evidence finding, preferably `V3-A006`, with `blocking_effect: none`.

### V1-CHECK-002 - Required Gate No-touch Review
- Tier: V1
- Covers: R-002, R-003
- Method: Review final diff to confirm no changes to `scripts/factoryctl`, `scripts/knowledge_lint.sh`, `scripts/factory_stage_lint.py`, `scripts/factory_pack_lint.py`, mission lint, mission cursor lint, CI, or merge preflight.
- Expected: No required gate or CI wiring changes.

### V1-CHECK-003 - Final Clean Advisory Run
- Tier: V1
- Covers: R-001, R-002
- Method: After removing temporary unsafe text, run `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`.
- Expected: Final docs return `ADVISORY_PASS` with 0 findings.

### V0-REVIEW-001 - No Promotion Review
- Tier: V0
- Covers: R-002
- Method: Human review of pilot report and final docs.
- Expected: Report states evidence does not promote Factory v3.

### V0-REVIEW-002 - Matcher Tuning Decision
- Tier: V0
- Covers: R-004
- Method: Review finding classifications.
- Expected: No matcher tuning unless false positive, false negative, ambiguous warning, or missed signal is documented.

### V0-REVIEW-003 - AEGIS Boundary Review
- Tier: V0
- Covers: R-005
- Method: Review final docs against `docs/Factory/AEGIS_BOUNDARY.md`.
- Expected: No AEGIS dependency or runtime-kernel authority claim.

### V0-REVIEW-004 - Classification Completeness
- Tier: V0
- Covers: R-006
- Method: Confirm pilot report classifies each finding as `accepted`, `false_positive`, `needs_more_context`, or `deferred`.
- Expected: Every finding has exactly one classification.

## Fixture Sketch
- `pack/fixtures/verification/promotion_evidence_warning/input.md`
- `pack/fixtures/verification/promotion_evidence_warning/expected_findings.json`
- `pack/fixtures/verification/promotion_evidence_warning/notes.md`

## Manifest Decision
No `verification_manifest.yaml` is created because this is a planning-only pack.

