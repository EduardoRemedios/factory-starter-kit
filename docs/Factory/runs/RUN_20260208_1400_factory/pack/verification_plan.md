# verification_plan.md — Sprint A Verification Plan

## Version
v2

## Change Log
- v2 (2026-02-08): Marked VP-03/VP-04 as mandatory inline tests per envelope red team finding ER-01.
- v1 (2026-02-08): Initial verification plan for Sprint A: Adapter Boundary.

## Purpose
Defines the verification strategy for Sprint A. Every Critical/High constraint must have at least one test, fixture, or check.

## Verification Strategy

### Unit Tests (new test file: `tests/test_sprint_A.py`)

| Test ID | Constraint | Description | Fixture |
|---|---|---|---|
| VP-01 | C-01 | All 43 existing tests pass unchanged | N/A (run existing suite) |
| VP-02 | C-02 | Adapter unavailable → deny + TER with AdapterUnavailable | `fixtures/policy/adapter_unavailable/` |
| VP-03 | C-02 | Adapter timeout → deny + TER with AdapterTimeout | Inline test (MANDATORY — must be in test_sprint_A.py, not skippable) |
| VP-04 | C-02 | Adapter auth error → deny + TER with AdapterAuthError | Inline test (MANDATORY — must be in test_sprint_A.py, not skippable) |
| VP-05 | C-03 | TER does not contain secrets (token patterns, API keys) | Inline assertion |
| VP-06 | C-04 | policy_engine.py has no adapter imports | Static analysis test |
| VP-07 | C-05 | require_confirmation → no adapter call, no TER | `fixtures/policy/confirm_no_execute/` |
| VP-08 | C-06, C-07 | Evidence triangle: PDR → TER → RR linkage and ordering | `fixtures/verification/evidence_triangle/` |
| VP-09 | C-08 | Anonymous user → execution denied AUTH_REQUIRED, no adapter | `fixtures/policy/auth_anonymous_deny/` |
| VP-10 | C-10 | Tenant isolation: two adapters with different config return different data | `fixtures/routing/tenant_isolation/` |
| VP-11 | C-11 | Idempotency: duplicate place_bet with same key returns first result | `fixtures/routing/idempotency/` |
| VP-12 | C-12 | action_type consistent across PDR, TER, RR | Part of VP-08 |
| VP-13 | C-13 | tool_call_fingerprint and result_fingerprint are SHA-256 | Part of VP-08 |
| VP-14 | C-14 | No adapter mapped → deny + TER with ADAPTER_NOT_MAPPED | `fixtures/routing/adapter_not_mapped/` |
| VP-15 | AC-01 | AdapterContract has execute + health + exceptions; toy adapter implements it | Structural test |
| VP-16 | AC-02 | ToolExecutor exists with auth gate, adapter selection, timing, TER emission | Integration test |
| VP-17 | AC-07 | ToolExecutor auth gate checks at call time (not decision time) | Inline test |

### Integration Tests

| Test ID | Description |
|---|---|
| VP-18 | Happy path: browse_events → adapter called → TER emitted → evidence complete |
| VP-19 | Happy path: place_bet → require_confirmation (no adapter) → confirm_place_bet → adapter called → TER + final RR |
| VP-20 | Error injection: adapter raises each of 5 exception types → verify TER error_code and RR reason_code mapping |

### Pre-merge Checks (manual or CI)

| Check ID | Description |
|---|---|
| PC-01 | `python3 -m unittest discover -s tests` passes with all tests (43 existing + new) |
| PC-02 | No new imports in `runtime/policy_engine.py` that reference adapter modules |
| PC-03 | Size of new runtime files is reasonable (no over-engineering) |
| PC-04 | Confirmation stub has exactly 3 fields (no UVS, no TTL, no crypto) |

## Coverage Summary

| Severity | Total Constraints | Covered | Uncovered |
|---|---|---|---|
| Critical | 9 (C-01 to C-09) | 9 | 0 |
| High | 5 (C-10 to C-14) | 5 | 0 |
| Medium | 5 (C-15 to C-19) | covered by structural review | 0 |

All Critical and High constraints have at least one verification point.
