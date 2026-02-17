# intent.md — Sprint A: Adapter Boundary + Toy Sportsbook Adapter

## Version
v2

## Change Log
- v2 (2026-02-08): Blue Team hardening — added C-18 through C-22 resolving RT-01 through RT-07. Added confirm_place_bet registry requirement. Expanded AC-07. No scope expansion.
- v1 (2026-02-08): Initial intent contracted from raw brief by Intent Contractor.

## 0. Purpose
Introduce the **adapter boundary** — the interface between the Harmony policy engine and external systems — and prove it works end-to-end with a **toy sportsbook adapter** that handles `browse_events`/`get_odds` and `place_bet` decision paths, including evidence emission (ToolExecutionRecord) and fail-closed error handling. [SOURCE:RAW]

## 1. Goal
Deliver the minimum viable adapter layer that lets the policy engine call external systems through a well-defined contract, with:
- A minimal `AdapterContract` interface (execute + health + standardized exceptions) [SOURCE:RAW]
- A `ToolExecutor` coordination layer that owns auth gating, adapter selection, timing, TER emission, and fail-closed error handling [SOURCE:RAW]
- A `ToolExecutionRecord` (TER) as the third leg of the evidence triangle (PDR → TER → RR) [SOURCE:RAW]
- `auth_context` and `tenant_context` threading through the request path [SOURCE:RAW]
- A toy `SportsbookAdapter` proving the contract works for `get_events`, `get_odds`, and `place_bet` [SOURCE:RAW]
- A `handle_request()` orchestration entrypoint that sequences engine decision → ToolExecutor call → evidence emission [SOURCE:RAW, clarified per RT-01]

## 2. Non-Goals
- Real API calls to any operator system (toy adapter only) [SOURCE:RAW]
- WalletAdapter, RGAdapter, or CasinoAdapter [SOURCE:RAW]
- Multi-provider routing or adapter registry patterns [SOURCE:RAW]
- Full confirmation lifecycle / UVS binding (Sprint B scope) [SOURCE:RAW]
- Evidence persistence to disk/DB (Sprint D scope) [SOURCE:RAW]
- Retry logic with backoff, circuit breakers, rate limiting [SOURCE:RAW]
- Integration Probe / auto-discovery [SOURCE:RAW]
- Player-auth hooks on the base AdapterContract [SOURCE:RAW]
- Dynamic adapter discovery or registration [SOURCE:RAW]
- Personalized odds / player-specific pricing [SOURCE:RAW]
- Casino adapters or any non-sportsbook domain [SOURCE:RAW]
- Caching layer [SOURCE:RAW]

## 3. Principles
1. **Fail closed.** Any adapter failure, timeout, or unexpected error results in a deny decision. No silent failures. [SOURCE:RAW]
2. **No secrets in evidence.** TERs must not contain API keys, session tokens, or credentials. [SOURCE:RAW]
3. **Backward compatible.** All 43 existing tests pass without modification. New code is additive. [SOURCE:RAW]
4. **Smallest viable interface.** The adapter contract is the minimum needed to make the toy adapter work. No speculative abstractions. [SOURCE:RAW]
5. **Deterministic record IDs.** TER IDs follow the same canonical-JSON + SHA-256 pattern as existing PDR/RR IDs. [SOURCE:RAW]
6. **Tenant-scoped.** Adapters initialized with tenant-specific config. Even the toy adapter demonstrates tenant awareness. [SOURCE:RAW]
7. **PolicyEngine remains pure.** The engine is deterministic and side-effect free — it does not perform I/O, network access, or time calls beyond an injected clock. All side effects are owned by the ToolExecutor. [SOURCE:RAW]

## 4. Scope

### Domain Areas (for fixtures)
- `routing` (adapter selection, action → adapter mapping)
- `policy` (auth gating, fail-closed behavior)
- `verification` (evidence triangle linkage, fingerprints)

### Key Deliverables
1. **AdapterContract interface** — Python abstract base class / protocol: `adapter_id`, `__init__(service_config)`, `execute(tool_call, ctx)`, `health()`. Standardized exceptions: `AdapterUnavailable`, `AdapterTimeout`, `AdapterAuthError`, `AdapterUpstreamError`, `AdapterProtocolError`. [SOURCE:RAW]
2. **ToolExecutionRecord (TER)** — New evidence record emitted on every tool execution attempt. Fields: `record_type`, `record_id` (deterministic SHA-256), `pdr_record_id`, `request_id`, `action_type`, `adapter_id`, `tool_call`, `tool_call_fingerprint`, `tool_result`, `result_fingerprint`, `duration_ms`, `success`, `error_code`, timestamps, `tenant_id`, `user_id`. No secrets. [SOURCE:RAW]
3. **ToolCall and ToolResult schemas** — Normalized shapes for `get_events`, `get_odds`, `place_bet`. `idempotency_key` required for `place_bet`. [SOURCE:RAW]
4. **Toy SportsbookAdapter** — Stub/mock implementing AdapterContract for sportsbook operations. Supports `get_events`, `get_odds`, `place_bet`. Simulates errors, auth failures, stale data. [SOURCE:RAW]
5. **ToolExecutor** — Thin coordination layer: auth gate → adapter selection (dict mapping) → `adapter.execute()` → timing (monotonic clock) → TER emission → fail-closed error handling. [SOURCE:RAW]
6. **handle_request() orchestration entrypoint** — Top-level function that wraps `evaluate_request()` + conditional `ToolExecutor.execute()`. Does NOT modify the PolicyEngine. Callers use this for execution-class actions. [SOURCE:RAW, clarified per RT-01]
7. **Auth context threading** — `auth_context` and `tenant_context` as optional top-level fields in the payload dict. When absent: `auth_state: "anonymous"`, `tenant_id: "unknown"`. Anonymous user → execution denied fail-closed with `AUTH_REQUIRED`. [SOURCE:RAW, clarified per RT-05]
8. **`confirm_place_bet` action** — Added to action registry as IRREVERSIBLE_REGULATED. Engine evaluates stub confirmation payload, decides `allow_execute` if valid. [SOURCE:RAW, clarified per RT-03]
9. **`require_confirmation` does NOT trigger adapter calls** — Execution only on `allow_execute` (confirmed path). Sprint A stubs confirmation payload shape without implementing full lifecycle. [SOURCE:RAW]
10. **Confirmation stub contract** — Minimal: `{nonce, issued_at, pdr_record_id}`. No cryptographic validation, no TTL enforcement, no odds-drift detection. [SOURCE:RAW]
11. **TER-to-RR reason code mapping** — Stable, machine-readable mapping from TER `error_code` to RR `reason_code`. [SOURCE:RAW]
12. **RR emission timing** — Initial engine call emits decision-only RR stub. After tool execution, final RR is emitted reflecting actual outcome. TER sits between PDR and final RR. [SOURCE:RAW, clarified per RT-02]

## 5. Constraints

### Critical
- C-01: All 43 existing tests pass unchanged. [SOURCE:RAW]
- C-02: Adapter failures produce deny + TER with error_code. No hangs, no partial success, no swallowed errors. [SOURCE:RAW]
- C-03: TERs must not contain API keys, session tokens, or credentials. [SOURCE:RAW]
- C-04: PolicyEngine does NOT call adapters directly. ToolExecutor is the intermediary. [SOURCE:RAW]
- C-05: `require_confirmation` does NOT trigger adapter calls or TER emission. [SOURCE:RAW]
- C-06: Evidence triangle wired correctly: PDR → TER → RR linked via `pdr_record_id`, `request_id`, and `action_type`. [SOURCE:RAW]
- C-07: TER `record_id` is deterministic (canonical-JSON + SHA-256). [SOURCE:RAW]
- C-08: Anonymous user → execution denied fail-closed with `AUTH_REQUIRED` reason code; no adapter call. [SOURCE:RAW]
- C-09: System invariants (HARMONY_V2_SYSTEM_INVARIANTS.md) are not violated. [SOURCE:REF:docs/HARMONY_V2_SYSTEM_INVARIANTS.md]

### High
- C-10: Adapters initialized with tenant-specific ServiceConfig. Two toy adapter instances with different ServiceConfig return different data. [SOURCE:RAW]
- C-11: `idempotency_key` required for `place_bet`. Duplicate calls return first result. [SOURCE:RAW]
- C-12: `action_type` used consistently across PDR, TER, RR. [SOURCE:RAW]
- C-13: `tool_call_fingerprint` and `result_fingerprint` are SHA-256 hashes of canonical serialized data. [SOURCE:RAW]
- C-14: No adapter mapped for action → fail closed → deny + TER with `ADAPTER_NOT_MAPPED`, `adapter_id: "none"`. [SOURCE:RAW]

### Medium
- C-15: Auth context object follows shape from AUTH_MODEL.md §3. [SOURCE:REF:docs/AUTH_MODEL.md]
- C-16: Confirmation stub is minimal. [SOURCE:RAW]
- C-17: RR reason codes mapped from TER error_code per defined table. [SOURCE:RAW]
- C-18: Orchestration entrypoint `handle_request()` wraps engine + ToolExecutor. PolicyEngine not modified. [SOURCE:RAW, clarified per RT-01]
- C-19: RR emission timing: decision-only stub from engine, final RR post-execution reflecting actual outcome. [SOURCE:RAW, clarified per RT-02]
- C-20: `duration_ms` is ToolExecutor-level operational metric via monotonic clock. Not a policy input. Exempt from "no implicit now" invariant. [SOURCE:RAW, clarified per RT-04]
- C-21: `auth_context` and `tenant_context` are optional payload fields. Absent → anonymous/unknown defaults. Backward compatible. [SOURCE:RAW, clarified per RT-05]
- C-22: Adapters raise Python exceptions for infrastructure failures. `ToolResult.error` for business errors. ToolExecutor catches exceptions and maps to TER error codes. [SOURCE:RAW, clarified per RT-07]

## 6. Roles
- **PolicyEngine**: Evaluates requests, emits PDR + decision-only RR stub. Does NOT call adapters. Pure, deterministic, side-effect free.
- **ToolExecutor**: Coordinates adapter calls. Owns auth gate, adapter selection, timing, TER emission, and fail-closed handling. Emits final RR post-execution.
- **handle_request()**: Top-level orchestration function. Calls engine, conditionally calls ToolExecutor, returns complete evidence chain.
- **AdapterContract**: Interface that concrete adapters implement. Defines execute, health, and standardized exceptions.
- **SportsbookAdapter**: Concrete toy adapter implementing AdapterContract for sportsbook operations.

## 7. Acceptance Criteria (binary, testable)
- AC-01: `AdapterContract` exists with `execute` + `health` + standardized exceptions. Toy sportsbook adapter implements it. [SOURCE:RAW]
- AC-02: `ToolExecutor` exists. PolicyEngine does NOT directly call adapters. ToolExecutor owns auth gating, adapter selection, timing, TER emission, fail-closed handling. [SOURCE:RAW]
- AC-03: TER emitted on every adapter call attempt. Deterministic `record_id`. Includes `tool_call_fingerprint` and `result_fingerprint`. Contains `pdr_record_id` and `request_id`. No secrets. [SOURCE:RAW]
- AC-04: `auth_context` + `tenant_context` supported as optional payload fields. Anonymous users denied execution fail-closed with `AUTH_REQUIRED`. [SOURCE:RAW]
- AC-05: `require_confirmation` does NOT trigger adapter calls. Execution only on `allow_execute`. Confirmation stub present. [SOURCE:RAW]
- AC-06: Adapter failures produce deny + TER with `error_code`. No hangs, no partial success, no swallowed errors. [SOURCE:RAW]
- AC-07: Evidence triangle wired: PDR → TER → RR linked via `pdr_record_id`, `request_id`, `action_type`. Dedicated test verifies ordering, linkage, and ToolExecutor auth gate timing. [SOURCE:RAW]
- AC-08: All 43 existing tests pass unchanged + new tests cover happy/failure/auth/no-adapter/tenant-isolation/idempotency/evidence-linkage/protocol-error/secret-leakage. [SOURCE:RAW]
- AC-09: PolicyEngine remains pure — no I/O, no network, no side effects. [SOURCE:RAW]

## 8. Open Questions

### BLOCKING
- None.

### NON-BLOCKING
- OQ-01: Should the `decide()` legacy path be unified with `evaluate_request()` as part of Sprint A? Risk R-004 suggests early resolution. [INFERRED]
- OQ-02: `action_id` vs `action_type` naming in codebase — document distinction, no rename. [SOURCE:RAW]

## 9. Go/No-Go Rule
PASS requires:
- All Critical items in PURPLE_GATE_CHECKLIST are YES
- No unbounded deferrals
- Traceability complete for all Critical/High constraints
- No unapproved scope expansions
- Final authority: Eduardo
