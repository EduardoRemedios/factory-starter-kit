# Pilot Usage Report - Factory v3 Advisory Lint

## Version
v1

## Change Log
- v1 (2026-05-18): Added first deterministic pilot usage report for the advisory lint prototype.

## Purpose
Exercise the standalone advisory lint against a deliberately unsafe Factory v3 documentation fixture to confirm that warnings remain non-blocking while still surfacing useful review signals.

## Target
- Fixture path: `tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3`
- Expected report: `tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json`

## Command
```bash
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/pilot_usage/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/pilot_usage/expected.json --json
```

## Result
- Status: `ADVISORY_FAIL_NON_BLOCKING`
- Blocking effect: `none`
- Files checked: 2
- Findings: 7
- Useful warnings: 7
- Known false positives: 0

## Finding Classes Exercised
- Missing research-only or non-enforcing posture.
- Required Factory v2 gate wiring language.
- Missing shadow schema isolation language.
- AEGIS optionality contradiction.
- Runtime-kernel authority claim.
- Promotion or release language without evidence and explicit human release approval.

## Interpretation
The pilot confirms that the prototype catches the intended boundary-stressor signals while preserving non-blocking output. The result is useful as fixture evidence only; it does not prove real-document false-positive quality.

## Next Step
Use the advisory lint on a real Factory v3 documentation branch and record accepted, false-positive, needs-more-context, and deferred classifications before expanding checks or integrating the tool into optional workflows.
