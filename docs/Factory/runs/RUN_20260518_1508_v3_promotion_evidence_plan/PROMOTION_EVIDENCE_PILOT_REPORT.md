# Promotion-Evidence Pilot Report - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-19): Recorded the promotion-evidence real-doc pilot and discovered missed `V3-A006` signal.

## Purpose
Exercise promotion-evidence warning behavior in the standalone Factory v3 advisory lint prototype against a bounded real-doc mutation, then remove the unsafe wording and record whether matcher tuning is justified.

## Authorization Note
- Original pack mode: `PLANNING_ONLY`.
- Pack reviewed: `docs/Factory/runs/RUN_20260518_1508_v3_promotion_evidence_plan/pack/PACK_AUDIT_REPORT.md`.
- Human approval: user said, "ok I agree with your approach, plese also use any skills that you deem relevant for this work and proceed".
- This report records execution after that approval. It does not change the original planning-only pack.

## Pilot Branch
- Branch: `codex/factory-v3-promotion-evidence-pilot`
- Target path: `docs/Factory/v3`
- Temporary mutation target: `docs/Factory/v3/PROMOTION_CRITERIA.md`
- Final retained doc changes: none in `docs/Factory/v3`.

## Boundary Conditions
- Factory v2 remains the canonical process.
- Factory v3 remains Level 0 research only.
- Advisory lint remains standalone, optional, and non-blocking.
- Required blocking effect remains `none`.
- AEGIS/runtime-kernel authority remains external.
- No matcher tuning was performed in this run.

## Baseline Command
```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

## Baseline Result
- Status: `ADVISORY_PASS`
- Blocking effect: `none`
- Files checked: 9
- Findings: 0

## Temporary Draft Mutation
The pilot temporarily appended this draft text to `docs/Factory/v3/PROMOTION_CRITERIA.md`:

```text
## Temporary Pilot Draft - Do Not Keep
Factory v3 release is ready for review.
```

This wording was intentionally unacceptable because it made a release claim without local evidence paths or explicit human release approval.

## Non-empty Warning Capture Result
Command:

```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

Observed result:
- Status: `ADVISORY_PASS`
- Blocking effect: `none`
- Files checked: 9
- Findings: 0
- Expected finding: `V3-A006`
- Actual finding: none

## Finding Classification
No findings were emitted, so no emitted finding could be classified as `accepted`, `false_positive`, `needs_more_context`, or `deferred`.

## Missed-Signal Classification

| Expected ID | Expected Behavior | Actual Behavior | Classification | Notes |
| --- | --- | --- | --- | --- |
| `V3-A006` | Promotion or release language without local evidence and explicit human release approval should produce a non-blocking advisory finding. | No finding emitted. | `false_negative` | The current check evaluates evidence and human release approval target-wide, so valid promotion-governance language elsewhere in `docs/Factory/v3` masks an unsafe local release claim. |

## Remediation
The temporary draft mutation was removed from `docs/Factory/v3/PROMOTION_CRITERIA.md`.

Final advisory result after remediation:
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: `ADVISORY_PASS`, `blocking_effect: none`, 9 files checked, 0 findings.

## Matcher Tuning Decision
Decision: no matcher tuning in this run.

Rationale: the approved pack authorized evidence capture and explicitly deferred matcher tuning to a later implementation run if pilot evidence identified a missed signal. This pilot does identify a missed signal, so the recommended next step is a bounded matcher-tuning run for `V3-A006`.

## Verification Evidence
- `bash scripts/knowledge_lint.sh`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: PASS, `ADVISORY_PASS`, 9 files checked, 0 findings after remediation.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan`: PASS.
- `git diff --check`: PASS.

## Protected Boundary Review
- No changes were made to `scripts/factory_v3_advisory_lint.py`.
- No changes were made to `scripts/factoryctl`.
- No changes were made to `scripts/knowledge_lint.sh`.
- No changes were made to `scripts/factory_stage_lint.py`.
- No changes were made to `scripts/factory_pack_lint.py`.
- No changes were made to mission lint, mission cursor lint, CI, or merge preflight.
- No Factory v3 release or promotion was claimed.

## Interpretation
The promotion-evidence pilot produced a useful negative result. It shows the advisory lint can miss a local unsafe release claim when the broader target directory contains valid promotion-governance language. This is strong evidence for a small, evidence-driven `V3-A006` matcher tune in a later implementation run, likely by evaluating promotion claims at file or local-section granularity instead of target-wide.

## Residual Risk
- Until `V3-A006` is tuned, advisory lint may miss local release claims in otherwise well-governed v3 docs.
- Matcher tuning remains unimplemented and requires separate approval.
- Required-gate integration remains blocked without a new Factory v2 pack and explicit human release approval.
