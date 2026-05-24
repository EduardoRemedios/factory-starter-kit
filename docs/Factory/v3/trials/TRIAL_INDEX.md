# Factory v3 Phase 1 Trial Index

## Version
v0.2

## Change Log
- v0.2 (2026-05-24): Recorded first Phase 1 trial as a V3-unsuitable fallback decision before mission-envelope creation.
- v0.1 (2026-05-24): Initial empty index for Phase 1 `V3-OP-001` real-project trials.

## Status
Research trial evidence index only. This document is non-enforcing and does not approve new V3 profiles, make V3 the default, deprecate V2, or wire V3 checks into required gates.

## Purpose
Track Phase 1 real-project `V3-OP-001` trials.

Use `docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md` for each trial record.

## Trial Summary

| Trial ID | Repository | User | Outcome | V2 Fallback Used | Separate Kernel | Evidence |
|---|---|---|---|---|---|---|
| `TRIAL_20260524_001_no_bounded_code_change` | `factory-starter-kit` | Eduardo Remedios / Codex | FALLBACK_TO_V2 | yes | no | `docs/Factory/v3/trials/TRIAL_20260524_001_no_bounded_code_change.md` |

## Batch Requirements

| Requirement | Target | Current |
|---|---:|---:|
| Total real-project trials | 5 | 1 |
| Ordinary repos without separate governance kernel | 2 | 1 |
| Trial by user other than V3 doc author | 1 | 0 |
| Trial with V2 fallback or V3-unsuitable decision | 1 | 1 |
| Trials with friction notes | 5 | 1 |
| Trials with advisory false-positive/false-negative notes | 5 | 1 |

## Current Batch Verdict
NOT_READY_FOR_PHASE_2

## Notes
- First Phase 1 trial records that `V3-OP-001` was unsuitable because the request did not name a bounded code-changing objective.
- Batch remains below the 5-trial minimum and still needs at least one trial by a user other than the V3 doc author.
