# Real-Branch Warning Pilot Report - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-18): Recorded a non-empty real-branch advisory lint pilot and finding classifications.

## Purpose
Exercise the standalone Factory v3 advisory lint prototype against a real Factory v3 documentation branch that temporarily contains plausible boundary drift, then classify the emitted findings before deciding whether matcher tuning is justified.

## Pilot Branch
- Branch: `codex/factory-v3-nonempty-advisory-pilot`
- Base revision: `1312dd2`
- Target path: `docs/Factory/v3`
- Pilot file: `docs/Factory/v3/PILOT_PROFILE_PLAN.md`

## Boundary Conditions
- Factory v2 remains the canonical process.
- Factory v3 remains Level 0 research only.
- Advisory lint remains standalone, optional, and non-blocking.
- Required blocking effect remains `none`.
- AEGIS/runtime-kernel authority remains external.
- The temporary drift draft was removed after the advisory run and is not retained as authoritative documentation.

## Temporary Draft Mutation
The pilot temporarily appended this draft text to `docs/Factory/v3/PILOT_PROFILE_PLAN.md`:

```text
For this draft, stage-lint must call v3 advisory lint before every Factory handoff.

For this draft, Factory v3 requires AEGIS before any repository can use the v3 profile.
```

This wording was intentionally unacceptable because it implied required v2 gate wiring and an AEGIS dependency.

## Advisory Command
```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

## Non-empty Pilot Result
- Status: `ADVISORY_FAIL_NON_BLOCKING`
- Blocking effect: `none`
- Promotion level: `research`
- Files checked: 9
- Findings: 2
- Warnings: 0
- Review status: `needs_human_review`

## Findings Emitted

| ID | Severity | Path | Message | Classification | Notes |
| --- | --- | --- | --- | --- | --- |
| `V3-A003` | `advisory_critical` | `docs/Factory/v3/PILOT_PROFILE_PLAN.md` | possible required v2 gate wiring language found | `accepted` | The draft incorrectly said `stage-lint must call v3 advisory lint`, which violates the non-blocking boundary. |
| `V3-A004` | `advisory_critical` | `<target>` | AEGIS optionality is missing or contradicted | `accepted` | The draft incorrectly said Factory v3 requires AEGIS, which violates the AEGIS-compatible but not AEGIS-dependent boundary. |

## Finding Classification Summary

| Classification | Count | Notes |
| --- | ---: | --- |
| `accepted` | 2 | Both findings identified real boundary drift in the temporary draft. |
| `false_positive` | 0 | No emitted finding was rejected. |
| `needs_more_context` | 0 | Both findings were clear from the draft text. |
| `deferred` | 0 | No finding was deferred. |

## Remediation
The temporary draft mutation was removed from `docs/Factory/v3/PILOT_PROFILE_PLAN.md`.

Final advisory result after remediation:
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: `ADVISORY_PASS`, `blocking_effect: none`, 9 files checked, 0 findings.

## Matcher Tuning Decision
Decision: no matcher tuning.

Rationale: both emitted findings were accepted as useful and accurate. The pilot did not produce false positives, ambiguous warnings, or evidence that matching rules should change.

## Verification Evidence
- `bash scripts/knowledge_lint.sh`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json`: PASS, `ADVISORY_PASS`, 9 files checked, 0 findings after remediation.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json`: PASS.
- `python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json`: PASS.
- `./scripts/factoryctl pack-lint --run RUN_20260518_1235_v3_advisory_lint_impl_plan`: PASS.
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
This pilot adds the missing non-empty real-branch signal-quality evidence. The advisory lint correctly caught required-gate wiring and AEGIS dependency drift while preserving non-blocking output. This supports continued standalone advisory use, but it does not justify integration into required gates or Factory v3 promotion.

## Residual Risk
- The pilot exercised two critical boundary classes but did not test promotion-evidence warnings in a real-doc branch.
- More real-branch evidence is still needed before adding new checks or considering any optional workflow integration.
- Required-gate adoption remains blocked without a new Factory v2-governed pack and explicit human release approval.
