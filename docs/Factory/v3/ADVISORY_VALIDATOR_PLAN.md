# Factory v3 Advisory Validator Plan

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial non-enforcing validator plan for Factory v3 research.

## Status
Research only. This plan does not implement a validator and does not change Factory v2 gates.

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

## Candidate Command
Potential future command:

```bash
./scripts/factoryctl v3-advisory-lint --target <path>
```

This command is a candidate only. It is not implemented by this plan.

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

### V3-A004 - AEGIS Optionality
- Check: Confirm public docs do not make AEGIS a dependency.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if docs imply AEGIS is required.

### V3-A005 - Runtime Kernel Boundary
- Check: Confirm v3 docs do not claim runtime authority, production action mediation, cryptographic proof, or autonomous system enforcement.
- Severity: advisory critical.
- Blocks v2: no.
- Expected output: warning if Factory claims kernel-owned behavior.

### V3-A006 - Promotion Evidence
- Check: Confirm any v3 release or promotion claim references eval evidence and explicit human release approval.
- Severity: advisory high.
- Blocks v2: no.
- Expected output: warning if promotion language lacks evidence.

## Candidate Output Shape
The future advisory report may include:
- `status`: `ADVISORY_PASS`, `ADVISORY_WARN`, or `ADVISORY_FAIL`
- `checked_artifacts`
- `findings`
- `warnings`
- `non_blocking_result`
- `recommended_next_steps`

The output must clearly say it is advisory and non-blocking.

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
- the change must not make AEGIS required
- human release approval must name the promoted check

## Out Of Scope
- Implementing the command.
- Adding JSON schemas.
- Editing required validators.
- Blocking v2 runs.
- Enforcing runtime behavior.

