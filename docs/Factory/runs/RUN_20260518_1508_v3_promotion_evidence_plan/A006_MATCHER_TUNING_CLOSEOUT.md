# A006 Matcher Tuning Closeout - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-19): Recorded bounded `V3-A006` matcher tuning after promotion-evidence pilot false negative.

## Closeout Decision
- Decision: READY
- Branch: `codex/factory-v3-a006-matcher-tune`
- Trigger evidence: `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/PROMOTION_EVIDENCE_PILOT_REPORT.md`

## Authorization Note
- Original planning pack mode: `PLANNING_ONLY`.
- Human approval for follow-up implementation occurred after the pilot report recommendation.
- This closeout records the bounded matcher tuning completed after that approval. It does not promote Factory v3 or change required Factory v2 gates.

## Scope Alignment
- Tuned only `V3-A006` promotion-evidence matching in `scripts/factory_v3_advisory_lint.py`.
- Added masked promotion-claim regression fixture under `tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/`.
- Updated existing advisory lint expected outputs to use precise file paths for local `V3-A006` findings.
- Updated `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md` to describe local promotion or release claim behavior.
- Updated canonical tracking docs after verification.

## Protected Boundary Review
- No changes were made to `scripts/factoryctl`.
- No changes were made to `scripts/knowledge_lint.sh`.
- No changes were made to `scripts/factory_stage_lint.py`.
- No changes were made to `scripts/factory_pack_lint.py`.
- No changes were made to mission lint, mission cursor lint, CI, or merge preflight.
- No Factory v3 release or promotion was claimed.
- Advisory lint remains standalone, optional, and non-blocking with `blocking_effect: none`.

## Implementation Notes
- Previous behavior evaluated promotion evidence target-wide, so valid evidence language elsewhere in `docs/Factory/v3` could mask a local unsafe release claim.
- New behavior evaluates explicit local promotion or release claim paragraphs and reports the specific file path.
- The matcher remains intentionally narrow to avoid warning on normal promotion criteria, no-go decisions, or governance text.

## Verification Evidence
- Temporary real-doc smoke: adding `Factory v3 release is ready for review.` to `docs/Factory/v3/PROMOTION_CRITERIA.md` produced `V3-A006` at `docs/Factory/v3/PROMOTION_CRITERIA.md`; the temporary wording was removed before commit.
- `bash scripts/knowledge_lint.sh`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: PASS, `ADVISORY_PASS`, 9 files checked, 0 findings.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/expected.json --json`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan`: PASS.
- `git diff --check`: PASS.

## Residual Risk
- `V3-A006` remains pattern-based and advisory; it is not a semantic release-policy verifier.
- Broader promotion phrasing may still require future evidence-driven matcher expansion.
- Required-gate integration remains blocked without a new Factory v2 pack and explicit human release approval.
