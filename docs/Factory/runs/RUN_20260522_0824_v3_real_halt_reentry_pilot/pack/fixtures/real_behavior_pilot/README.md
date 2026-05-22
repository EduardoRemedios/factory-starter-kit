# Real Behavior Pilot Fixture

## Version
v1

## Change Log
- v1 (2026-05-22): Stage F fixture inventory for real halt and reentry behavior.

## Fixture Inventory
| ID | Type | Expected Result |
|---|---|---|
| halt_failed_command | command execution | nonzero command records `halted: true` and no continuation marker |
| reentry_valid | state comparison | matching source/cursor records `resume_allowed: true` |
| reentry_stale_cursor | state comparison | conflicting cursor records `halted: true` |

## Notes
- Concrete inputs and outputs are written under `execution_evidence/` during execution.
