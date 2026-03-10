# docs/Factory/templates/MISSION_MANIFEST_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md
- Must enumerate mission units in deterministic order.
- Must include unit references: RUN_ID + SPRINT_ID + pack path.
- Must include dependency edges and scope ledger reference.
- Must include evidence-link fields for each unit.
- No placeholders may remain in final artifacts.
-->

## Version
v2

## Change Log
- v2 (2026-03-10): Normalized mission unit status vocabulary to distinguish planning-only pack closure from execution GO and to explicitly allow `planning_signal` units.
- v1 (YYYY-MM-DD): Initial mission manifest.

## Mission Metadata
- Mission ID: MISSION_YYYYMMDD_NNN
- Owner: Project owner
- Created: YYYY-MM-DD HH:MM (local)
- Execution posture: SEQUENTIAL_DEFAULT

## Purpose
One paragraph describing the mission objective and boundaries.

## Mission Scope Ledger (locked)
- Scope Ledger ID:
- Scope Ledger Path:
- Lock Timestamp:

## Ordered Mission Units
| Order | RUN_ID | SPRINT_ID | Pack Path | Depends On | Status (planned/running/pack_complete/closed_go/failed/skipped/planning_signal) |
|---:|---|---|---|---|---|
| 1 | RUN_... | SPRINT_... | docs/Factory/runs/<RUN_ID>/pack | none | planned |
| 2 | RUN_... | SPRINT_... | docs/Factory/runs/<RUN_ID>/pack | 1 | planned |

Status semantics:
- `pack_complete` is the terminal state for planning-only units after pack closure.
- `closed_go` is the terminal state for execution-enabled units after explicit human GO and execution completion.
- `planning_signal` is allowed only when a unit is intentionally enumerated but not yet authorized for execution.

## Dependency Graph
- Unit 1 -> Unit 2
- Unit 2 -> Unit 3

## Authorization Preconditions
- Execution mode requirement:
- Human checkpoint requirement:
- Downstream fan-out policy:

## Unit Evidence Links
| Unit | intent_lock_report | PACK_CHECKLIST | PACK_AUDIT_REPORT | HANDOFF_STAGE_I2 | Notes |
|---|---|---|---|---|---|
| 1 | <path> | <path> | <path> | <path> |  |
| 2 | <path> | <path> | <path> | <path> |  |

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None
