# Factory v3 Advisory Validator Plan

## Version
v0.3

## Change Log
- v0.3 (2026-05-19): Tuned `V3-A006` to evaluate local promotion or release claims and added masked promotion-claim fixture coverage.
- v0.2 (2026-05-18): Recorded the standalone advisory lint prototype and fixture verification command shape.
- v0.1 (2026-05-18): Initial non-enforcing validator plan for Factory v3 research.

## Status
Research only. The standalone prototype is advisory and does not change Factory v2 gates.

## Purpose
Define optional Factory v3 advisory checks before any code is written. The checks should help evaluate v3 concepts without blocking Factory v2 runs.

## Non-blocking Rule
Any future v3 validator must be advisory until separately promoted.

It must not be called by:
- `bash scripts/knowledge_lint.sh`
- `./scripts/factoryctl stage-lint`
- `./scripts/factoryctl pack-lint`
- Mission lint
- Mission cursor lint
- merge preflight

## Prototype Command
Current standalone advisory prototype:

```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
```

This command is optional and non-blocking. It is not called by `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, mission cursor lint, or merge preflight.

## Candidate Checks

### V3-A001 - v2 Core Preservation
- Check: Confirm core docs still state the v2 stage order as `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if drift appears.

### V3-A002 - Research-only Posture
- Check: Confirm files under `docs/Factory/v3/` say they are research-only or non-enforcing.
- Severity: advisory high.
- Blocks v2: no.
- Expected output: warning if a v3 doc uses mandatory operating language without promotion.

### V3-A003 - Shadow Schema Isolation
- Check: Confirm shadow schema candidates are not required by `knowledge_lint`, `stage-lint`, or `pack-lint`.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if a v3 candidate is wired into required v2 validators.

### V3-A004 - External Governance Kernel Optionality
- Check: Confirm public docs do not make external governance kernel a dependency.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if docs imply external governance kernel is required.

### V3-A005 - Runtime Kernel Boundary
- Check: Confirm v3 docs do not claim runtime authority, production action mediation, cryptographic proof, or autonomous system enforcement.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if Factory claims kernel-owned behavior.

### V3-A006 - Promotion Evidence
- Check: Confirm local v3 release or promotion claims reference eval evidence and explicit human release approval.
- Severity: advisory high.
- Blocks v2: no.
- Expected output: warning if local promotion or release language lacks evidence and explicit human release approval.

## Candidate Output Shape
The advisory report includes:
- `status`: `ADVISORY_PASS`, `ADVISORY_WARN`, or `ADVISORY_FAIL_NON_BLOCKING`
- `blocking_effect`: always `none`
- `promotion_level`: currently `research`
- `checked_artifacts`
- `findings`
- `warnings`
- `recommended_next_steps`
- review fields for later human classification

The output must clearly say it is advisory and non-blocking.

## Fixture Verification
The prototype includes deterministic fixtures:

```bash
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/clean/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/clean/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/warning/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/warning/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/promotion_claim/expected.json --json
python3 scripts/factory_v3_advisory_lint.py --target tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/input/docs/Factory/v3 --expect tests/fixtures/factory_v3_advisory_lint/masked_promotion_claim/expected.json --json
```

## Evidence To Capture
For each advisory run, capture:
- target path or run id
- repository revision
- checked files
- warnings
- false positives after review
- false negatives discovered later
- time overhead
- reviewer decision

## Promotion Requirements
Before any advisory check becomes required:
- at least one Factory v2 planning pack must approve the change
- pilot evidence must show useful signal
- false-positive and false-negative behavior must be reviewed
- public docs must explain the behavior
- the change must not make external governance kernel required
- human release approval must name the promoted check

## Out Of Scope
- Adding JSON schemas.
- Editing required validators.
- Blocking v2 runs.
- Enforcing runtime behavior.
- Adding a `factoryctl` subcommand.
