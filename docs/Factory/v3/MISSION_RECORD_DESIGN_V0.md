# Factory v3 Mission Record Design v0

## Version
v0.2

## Change Log
- v0.2 (2026-05-24): Added malformed-record fixture coverage and a standalone advisory mission-record validator with deterministic expected outputs.
- v0.1 (2026-05-24): Initial shadow mission-record design derived from the first five Phase 1 `V3-OP-001` trials.

## Status
Research-only shadow design. This document is non-enforcing: it does not make Factory v3 the default, approve new V3 profiles, deprecate Factory v2, wire V3 into required gates, or implement runtime authority.

## Purpose
Define the smallest useful machine-readable mission record for optional `V3-OP-001` work.

The record is a replay aid for bounded coding missions. It is not a runtime governance kernel, not a proof ledger, not a telemetry system, and not a replacement for Factory v2.

## Source Evidence
This design is derived from:

- `docs/Factory/v3/PHASE1_DECISION_REVIEW_V3_OP_001.md`
- `docs/Factory/v3/trials/TRIAL_INDEX.md`
- the five Phase 1 trial records under `docs/Factory/v3/trials/`

## Primary Artifact
Template:

```text
docs/Factory/v3/templates/V3_MISSION_RECORD_TEMPLATE.json
```

Backfilled examples:

```text
tests/fixtures/factory_v3_mission_record/
```

Advisory validator:

```text
scripts/factory_v3_mission_record_lint.py
```

## Design Principles

1. Capture observed Phase 1 evidence before adding new concepts.
2. Represent pre-envelope rejection as a valid terminal decision state.
3. Represent thread-local mission envelopes without forcing file-scope expansion.
4. Keep local command evidence first-class.
5. Preserve V2 fallback as an explicit field.
6. Keep advisory checks optional because adopting repos may not have starter-kit scripts.
7. Avoid chain-of-thought, full chat transcripts, and vendor-private cognition state.
8. Avoid runtime-kernel authority, production proof, lease enforcement, telemetry, or governance routing.

## Decision States

| State | Meaning |
|---|---|
| `pre_envelope_fallback` | V3 was considered but stopped before mission-envelope creation because authority, scope, commands, verification, or profile eligibility was missing. |
| `completed_with_v3` | V3 executed within `V3-OP-001` scope and verification completed without fallback. |
| `halted` | V3 started and then stopped because verification did not pass, scope expanded, authority was missing, or another halt rule fired. No further execution is implied by this state. |
| `blocked` | The work could not safely proceed and no execution occurred. |

Phase 1 produced `pre_envelope_fallback` and `completed_with_v3` records. `halted` and `blocked` remain design states for future valid-record fixtures.

## Required Field Groups

| Group | Purpose |
|---|---|
| `record` | Schema identity, status, profile, decision state, and source evidence. |
| `mission` | Objective, repository, harness, user, and envelope mode. |
| `authority` | Authorized files, forbidden scope, allowed commands, dependency policy, and V2 fallback requirement. |
| `execution` | Files changed, verification commands, command results, halt/fallback result, and advisory checks. |
| `reviews` | SIMPLE-CODE-GATE, fallback/halt review, friction notes, and false-positive/false-negative notes. |
| `phase2_design_signals` | Lessons that should shape later schema, validator, or fixture work. |

## Envelope Modes

| Mode | Meaning |
|---|---|
| `not_created_pre_envelope_fallback` | No mission envelope was created because V3 was rejected before authority was granted. |
| `thread_local` | The envelope stayed in the chat thread because creating an artifact would have expanded the authorized file scope. |
| `file_artifact` | A repository file contains the mission envelope and is inside the authorized artifact scope. |

## Shadow Record Rules

- A mission record may be created after the fact from closeout evidence.
- A mission record must not imply enforcement.
- A mission record must not expand authorized files during execution.
- A mission record must identify missing evidence with explicit `not_recorded` or `not_run` values.
- A mission record must preserve whether V2 fallback was used or retained.

## Advisory Validator

The standalone advisory validator reads one mission-record JSON file or a directory of JSON files:

```bash
python3 scripts/factory_v3_mission_record_lint.py --target tests/fixtures/factory_v3_mission_record --json
```

It emits JSON with `blocking_effect: none` and only advisory statuses:

- `ADVISORY_PASS`
- `ADVISORY_WARN`
- `ADVISORY_FAIL_NON_BLOCKING`

The validator is a replay and fixture aid only. It is not wired into `factoryctl`, CI, merge preflight, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, or any required Factory v2 gate.

Deterministic expected outputs live under:

```text
tests/fixtures/factory_v3_mission_record/expected/
```

Malformed-record fixtures currently cover missing authorized files, missing allowed commands, missing verification result, fallback without reason code, thread-local envelope without reference, and unsafe approval-scope flags.

## Out Of Scope For v0

- JSON Schema validation.
- `factoryctl` integration.
- CI or merge-preflight checks.
- Continuous telemetry.
- Runtime authority enforcement.
- Governance routing.
- Capability profiling.
- External governance-kernel adapters.

## Next Step
Use the advisory validator against future shadow records and add valid halted, blocked, stale-reentry, and verification-failure examples only when real evidence or an approved Phase 2 design task justifies them.
