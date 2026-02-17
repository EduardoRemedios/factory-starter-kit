# Sprint Envelope — Sprint A: Adapter Boundary

## Version
v1

## Change Log
- v1 (2026-02-08): Initial sprint envelope created for RUN_20260208_1400_factory.

## Sprint Metadata
- RUN_ID: RUN_20260208_1400_factory
- Sprint ID: SPRINT_20260208_001
- Owner: Eduardo
- Created: 2026-02-08 15:45 (local)

## Iteration (for envelope review cycles)
- Iteration: 1 of max 2

## Inputs (LOAD)
- intent.md (v2, locked)
- micro_sprints.md (v1)
- verification_plan.md (v1)
- traceability_matrix.md (v1)

## Inputs (DISK)
- risk_register.md (v1)
- premortem.md (v1)
- intent_lock_report.md (v1)

## Purpose
Sprint A introduces the adapter boundary between the Harmony policy engine and external systems. It delivers a minimal AdapterContract interface, a ToolExecutor coordination layer, a ToolExecutionRecord (TER) evidence type, auth context threading, and a toy sportsbook adapter that proves the contract works end-to-end. The engine remains pure and side-effect free; all external interaction is owned by the ToolExecutor.

## Scope
### In Scope
- AdapterContract interface (execute + health + 5 standardized exceptions)
- ToolExecutor (auth gate, adapter selection, timing, TER emission, fail-closed)
- handle_request() orchestration entrypoint
- ToolExecutionRecord with deterministic IDs, fingerprints, linkage
- ToolCall and ToolResult normalized schemas
- auth_context and tenant_context as optional payload fields
- Toy SportsbookAdapter (get_events, get_odds, place_bet)
- confirm_place_bet action in registry with stub confirmation payload
- TER-to-RR reason code mapping
- RR emission timing (decision-only stub → final RR post-execution)

### Out of Scope
- Real API calls (toy adapter only)
- WalletAdapter, RGAdapter, CasinoAdapter
- Multi-provider routing, adapter registry, dynamic discovery
- Full confirmation lifecycle / UVS binding (Sprint B)
- Evidence persistence (Sprint D)
- Retry, circuit breakers, rate limiting
- Personalized odds, caching

### Domain Areas (for fixtures)
- routing
- policy
- verification

## Acceptance Criteria (binary)
- AC-01: AdapterContract exists with execute + health + exceptions. Toy adapter implements it.
- AC-02: ToolExecutor exists. Engine does NOT call adapters. ToolExecutor owns auth gate, selection, timing, TER, fail-closed.
- AC-03: TER emitted on every adapter call attempt. Deterministic record_id. Fingerprints. pdr_record_id + request_id linkage. No secrets.
- AC-04: auth_context + tenant_context optional in payload. Anonymous → AUTH_REQUIRED deny. Backward compatible.
- AC-05: require_confirmation → no adapter call. Execution only on allow_execute.
- AC-06: Adapter failures → deny + TER with error_code. No hangs, no partial success.
- AC-07: Evidence triangle: PDR → TER → RR linked and ordered. Dedicated test. Auth gate timing test.
- AC-08: All 43 existing tests pass + new tests for all scenarios.
- AC-09: PolicyEngine remains pure — no I/O, no network, no side effects.

## Constraints (must/must-not)
Every Critical/High constraint appears in traceability_matrix.md.
- C-01 (Critical): All 43 existing tests pass unchanged
- C-02 (Critical): Adapter failures → deny + TER with error_code
- C-03 (Critical): No secrets in TER
- C-04 (Critical): Engine does NOT call adapters directly
- C-05 (Critical): require_confirmation → no adapter call, no TER
- C-06 (Critical): Evidence triangle: PDR → TER → RR linkage
- C-07 (Critical): TER record_id is deterministic SHA-256
- C-08 (Critical): Anonymous → AUTH_REQUIRED deny, no adapter
- C-09 (Critical): System invariants not violated
- C-10 (High): Tenant isolation via ServiceConfig
- C-11 (High): Idempotency for place_bet
- C-12 (High): action_type consistent across all records
- C-13 (High): Fingerprints are SHA-256
- C-14 (High): No adapter mapped → deny + TER ADAPTER_NOT_MAPPED

## File-Touch Budgets (HARD)
### Per Micro-sprint Budgets
| Micro-sprint ID | Modified (max) | Created (max) | Deleted (max) | Justification if outside guidance |
|---|---:|---:|---:|---|
| MS-01 | 5 | 3 | 0 | |
| MS-02 | 3 | 3 | 0 | |
| MS-03 | 2 | 2 | 0 | |
| MS-04 | 2 | 1 | 0 | |

Guidance reference: DEFINITIONS.md §7.

### Sprint Total Budget
| Modified (max) | Created (max) | Deleted (max) | Justification if outside guidance |
|---:|---:|---:|---|
| 12 | 9 | 0 | |

## Execution Plan (micro-sprint sequencing)
Reference micro_sprints.md; stop/go points:
- Gate 1 (after MS-01): All 43 existing tests pass. Schema changes are backward compatible.
- Gate 2 (after MS-02): Engine purity verified (no adapter imports). ToolExecutor functional.
- Gate 3 (after MS-03): Tenant isolation and idempotency verified. Adapter contract compliance.
- Gate 4 (after MS-04, final): Full test suite green. All VP checks pass. CI green.

## Verification Plan (must run before merge)
References:
- verification_plan.md
- traceability_matrix.md

Required checks:
- VP-01: All 43 existing tests pass unchanged
- VP-02 through VP-04: Adapter error handling (unavailable, timeout, auth)
- VP-05: No secrets in TER
- VP-06: No adapter imports in policy_engine.py
- VP-07: require_confirmation → no adapter call
- VP-08: Evidence triangle linkage + ordering + fingerprints
- VP-09: Anonymous deny with AUTH_REQUIRED
- VP-10: Tenant isolation
- VP-11: Idempotency
- VP-14: Adapter not mapped → ADAPTER_NOT_MAPPED
- VP-15 through VP-20: Contract compliance, integration flows

Fixture coverage confirmation:
- "All Critical/High constraints have at least one fixture/test/check." (YES at pack time — see traceability_matrix.md)

## Rollback / Abort Criteria
Abort if:
- Any existing test breaks and cannot be fixed without modifying its assertions (C-01 violation)
- Adapter logic appears inside policy_engine.py (C-04 / C-09 violation)
- Evidence triangle has contradictory records that cannot be resolved (SR-03 materialized)
Rollback approach:
- Revert all Sprint A changes. Phase 0 state is preserved in git. No Sprint A code merges until all gates pass.

## Risks to Watch
Top risks from risk_register.md:
- SR-01 (Critical): Engine purity violation — mitigated by Gate 2 and VP-06
- SR-02 (Critical): Backward compatibility break — mitigated by Gate 1 and VP-01
- SR-03 (Critical): Evidence triangle inconsistency — mitigated by C-19 and VP-08
- SR-08 (Critical): Secret leakage in TER — mitigated by VP-05

## Open Issues
### BLOCKING
- None

### NON-BLOCKING
- None

## Scope Expansion Log
- None
