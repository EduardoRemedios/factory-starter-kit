# Post-Tuning A006 Smoke Report - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-19): Recorded real-doc smoke evidence for tuned `V3-A006` behavior.

## Purpose
Confirm that the bounded `V3-A006` matcher tuning catches a small real-doc promotion or release claim while leaving the final Factory v3 research docs clean.

## Authorization Note
- Original planning pack mode: `PLANNING_ONLY`.
- Human approval: user approved proceeding with the next post-tuning step.
- This report records bounded smoke evidence only. It does not promote Factory v3 or change required Factory v2 gates.

## Pilot Branch
- Branch: `codex/factory-v3-a006-matcher-tune`
- Target path: `docs/Factory/v3`
- Temporary mutation target: `docs/Factory/v3/PROMOTION_CRITERIA.md`
- Final retained doc changes: none in `docs/Factory/v3`.

## Boundary Conditions
- Factory v2 remains the canonical process.
- Factory v3 remains Level 0 research only.
- Advisory lint remains standalone, optional, and non-blocking.
- Required blocking effect remains `none`.
- AEGIS/runtime-kernel authority remains external.
- No additional matcher tuning was performed in this smoke pilot.

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
## Temporary Post-Tuning Smoke Draft - Do Not Keep
Factory v3 release is ready for review.
```

This wording was intentionally unacceptable because it made a local release claim without local evidence paths or explicit human release approval.

## Smoke Capture Result
Command:

```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

Observed result:
- Status: `ADVISORY_WARN`
- Blocking effect: `none`
- Files checked: 9
- Findings: 1
- Finding ID: `V3-A006`
- Finding path: `docs/Factory/v3/PROMOTION_CRITERIA.md`
- Finding severity: `advisory_high`
- Finding message: `promotion or release language lacks evidence and explicit human release approval`

## Finding Classification

| Finding ID | Path | Classification | Notes |
| --- | --- | --- | --- |
| `V3-A006` | `docs/Factory/v3/PROMOTION_CRITERIA.md` | `accepted` | Correctly caught the intentionally unsafe local release claim. |

Summary:
- `accepted`: 1
- `false_positive`: 0
- `needs_more_context`: 0
- `deferred`: 0

## Remediation
The temporary draft mutation was removed from `docs/Factory/v3/PROMOTION_CRITERIA.md`.

Final advisory result after remediation:
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: `ADVISORY_PASS`, `blocking_effect: none`, 9 files checked, 0 findings.

## Matcher Tuning Decision
Decision: no further matcher tuning in this smoke pilot.

Rationale: the tuned matcher produced the expected real-doc `V3-A006` finding without producing findings against the clean final Factory v3 docs. Further expansion should wait for additional real-branch evidence.

## Protected Boundary Review
- No changes were made to `scripts/factory_v3_advisory_lint.py`.
- No changes were made to `scripts/factoryctl`.
- No changes were made to `scripts/knowledge_lint.sh`.
- No changes were made to `scripts/factory_stage_lint.py`.
- No changes were made to `scripts/factory_pack_lint.py`.
- No changes were made to mission lint, mission cursor lint, CI, or merge preflight.
- No Factory v3 release or promotion was claimed.

## Verification Evidence
- `bash scripts/knowledge_lint.sh`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: PASS, `ADVISORY_PASS`, 9 files checked, 0 findings after remediation.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/expected.json --json`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1508_v3_promotion_evidence_plan`: PASS.
- `git diff --check`: PASS.

## Interpretation
The post-tuning real-doc smoke pilot confirms the original false negative is addressed for the tested local release-claim shape. The validator remains advisory only and should continue collecting real-branch evidence before any additional matcher expansion or required-gate proposal.

## Residual Risk
- `V3-A006` remains pattern-based and advisory; it is not a semantic release-policy verifier.
- Broader promotion phrasing may still require future evidence-driven matcher expansion.
- Required-gate integration remains blocked without a new Factory v2 pack and explicit human release approval.
