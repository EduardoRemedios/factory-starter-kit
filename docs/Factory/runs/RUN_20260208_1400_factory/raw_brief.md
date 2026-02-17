# Raw Brief — Sprint A: Adapter Boundary + Toy Sportsbook Adapter

> **Author:** Eduardo dos Remedios
> **Date:** 2026-02-08
> **Status:** APPROVED — ready for Factory pipeline
> **Approved:** 2026-02-08
> **Factory run:** Not yet assigned (Root Planner will generate RUN_ID)

---

## What I want to build

Right now the Harmony policy engine makes decisions but can't do anything with them. It evaluates a request, emits a PolicyDecisionRecord and a ReceiptRecord, and that's it. There's no way for the engine to call an external system, no adapter layer, no tool execution. The "truth sources" in our test vectors are just hardcoded context blobs.

This sprint introduces the **adapter boundary** — the interface between the policy engine and the outside world — and proves it works with a **toy sportsbook adapter** that can handle the `browse_events`/`get_odds` and `place_bet` decision paths.

---

## The problem

1. **No adapter contract exists.** The engine has no defined way to call external systems. There's no interface, no contract, no error handling pattern.
2. **No ToolExecutionRecord (TER).** When an adapter is called, there's no evidence trail. We need a TER to sit alongside the existing PDR and RR.
3. **No fail-closed behavior for adapter failures.** If the sportsbook API is down, the engine should deny — not hang, not return garbage, not swallow the error.
4. **No auth context in the request path.** The engine currently ignores authentication. Sprint A needs to thread `auth_context` and `tenant_context` through the request so adapters know who they're acting for.

---

## What exists today (read HARMONY_STATE.md for full detail)

- `runtime/policy_engine.py` — deterministic policy engine with `evaluate_request()` entrypoint
- `runtime/schemas.py` — inbound request validation + outbound `PolicyDecision` schema validation
- `runtime/pack_loader.py` — YAML policy pack loader
- `runtime/errors.py` — `ValidationError`, `DecisionError`
- 43 passing tests across 4 sprint test files
- 12 golden fixture vectors
- 3 policy packs (baseline, betting, casino) — all UKGC-scoped
- CI pipeline on GitHub Actions
- Evidence emission: PDR + RR for every decision, deterministic record IDs

What does NOT exist: adapter boundary, tool execution, TER emission, auth context threading, any external calls whatsoever.

---

## Scope: what Sprint A must deliver

### 1. AdapterContract interface

A Python abstract base class (or protocol) that defines the **minimum viable contract** every adapter must implement. The guiding principle is: what is the smallest surface area that lets the toy adapter work?

**The contract:**

```python
class AdapterContract:
    adapter_id: str

    def __init__(self, service_config: ServiceConfig): ...
    def execute(self, tool_call: ToolCall, ctx: RequestContext) -> ToolResult: ...
    def health(self) -> HealthStatus: ...
```

That's it. Four things: an identity, initialization, execution, and health.

**Standardized exceptions** (all adapters raise these, ToolExecutor catches them):

- `AdapterUnavailable` — adapter or upstream is down
- `AdapterTimeout` — call exceeded deadline
- `AdapterAuthError` — service-level or player-level auth failure
- `AdapterUpstreamError` — upstream returned an error response
- `AdapterProtocolError` — upstream response doesn't match expected shape

**Where auth gating lives:** NOT on the adapter contract. The ToolExecutor performs the auth gate (token presence, expiry, tenant binding) *before* calling `adapter.execute()`. Player-auth methods (`authenticate_player`, `is_player_token_valid`, `on_player_auth_failure`) are NOT part of the base contract — if needed later, they go on a separate mixin/interface (e.g., `PlayerAuthCapableAdapter`). This avoids forcing every adapter (including future non-player ones like content/stats) to carry player-auth semantics.

**Do NOT include in the base contract:**
- Domain-specific logic (belongs in concrete adapters)
- Multi-provider routing (Phase 2+)
- Caching layer (not Sprint A scope)
- Retry logic beyond "fail and report" (keep it fail-closed)
- Player auth hooks (auth gating is ToolExecutor's job)

### 2. ToolExecutionRecord (TER)

A new evidence record type emitted every time the ToolExecutor **attempts** tool execution. This is the missing third leg of the evidence triangle (PDR → TER → RR).

TERs are emitted for all execution attempts, including pre-call failures (e.g., no adapter mapped, auth gate failure). If the system *intended to execute* but couldn't, that's still a tool-execution failure event. This makes audits and debugging unambiguous: PDR says "allow_execute", TER says what happened (or what went wrong), RR says the final outcome.

Must include:
- `record_type: "ToolExecutionRecord"`
- `record_id` (deterministic, same canonical-JSON + SHA-256 pattern as PDR/RR)
- `pdr_record_id` — explicit linkage to the PDR that authorized this execution
- `request_id` — correlation ID for the request instance (ties PDR + TER + RR together)
- `action_type` — what kind of action (e.g., `place_bet`), consistent with PDR's `action_type`
- `adapter_id` — which adapter was called (or `"none"` if execution failed before an adapter was selected, e.g., `ADAPTER_NOT_MAPPED`)
- `tool_call` — what was requested (serializable, secret-stripped, **normalized** — see ToolCall schema below)
- `tool_call_fingerprint` — SHA-256 hash of canonical serialized `tool_call` after secret-stripping. Stable linkage for offline verifiers; proves "this exact request was executed"
- `tool_result` — what came back (serializable, **normalized** — not raw upstream response, no PII beyond what's necessary)
- `result_fingerprint` — SHA-256 hash of canonical serialized `tool_result` (scrubbed). Same purpose
- `duration_ms` — how long the adapter call took
- `success: bool`
- `error_code` (if failed, null otherwise)
- Timestamp, tenant_id, user_id (same fields as PDR — but NOT session tokens)

**Naming discipline (applies to all records — PDR, TER, RR):**
- `action_type` = what kind of action (e.g., `place_bet`, `get_events`). Use `action_type` consistently in all evidence records. The existing PDR already uses `action_type`; TER and RR must match.
- `record_id` = unique to this record instance (deterministic, canonical-JSON + SHA-256)
- `pdr_record_id` = which PDR authorized this execution (TER-specific)
- `request_id` = correlates all records (PDR + TER + RR) for one request instance. This is the forensic thread.

**Note:** the codebase and packs currently use `action_id` in some places and `action_type` in others. For evidence records, prefer `action_type` (consistent with the existing PDR). The policy engine's internal routing can continue to use `action_id` as its lookup key — the distinction is: `action_id` is an internal routing identifier, `action_type` is the stable label in evidence records.

Must NOT include: raw credentials, raw upstream API responses, session tokens, service credentials.

### 2.1 ToolCall schema (normalized shape)

To ensure fingerprints are deterministic and tests are fixture-driven, define a minimal ToolCall schema:

```python
ToolCall = {
    "tool_id": str,             # One of: "get_events" | "get_odds" | "place_bet"
    "params": dict,             # Strict keys per tool_id (see below)
    "idempotency_key": str | None,  # REQUIRED for place_bet; optional for reads
    "requested_at": str,        # ISO 8601 timestamp
}
```

**Per-tool param shapes for Sprint A:**

| tool_id | Required params | Notes |
|---------|----------------|-------|
| `get_events` | `{ sport?, competition?, date_range? }` | All optional filters |
| `get_odds` | `{ event_id, market_type? }` | `event_id` required |
| `place_bet` | `{ event_id, market_id, selection_id, stake, odds, currency }` | All required |

**`idempotency_key` rule:** Required for `place_bet` (and any future write operations). Even the toy adapter must respect it — if the same `idempotency_key` is sent twice, the second call returns the result of the first, not a duplicate execution. This is not scope creep; it's the difference between a "toy" and a "dangerous toy" that could mask double-execution bugs.

**ToolResult schema:**

```python
ToolResult = {
    "tool_id": str,             # Echoes the tool_id from ToolCall
    "success": bool,
    "data": dict | None,        # Normalized response (not raw upstream)
    "error": str | None,        # Machine-readable error code if success=false
}
```

### 3. Toy SportsbookAdapter

A concrete adapter that implements the `AdapterContract` for sportsbook operations. This is a **stub/mock** — it returns hardcoded or configurable responses, not real API calls.

Must support:
- `get_events` — returns a list of events (markets, odds)
- `get_odds` — returns odds for a specific event
- `place_bet` — accepts a bet and returns a bet confirmation (or rejection)

Must behave realistically enough to:
- Test the full decision→execute→record flow
- Simulate errors (API down, timeout, invalid response)
- Simulate auth failures (expired token, invalid player)
- Simulate stale data scenarios

This is NOT a production adapter. It's a test harness adapter that proves the contract works.

### 4. Auth context threading

The engine's `evaluate_request` currently accepts `payload` with `action_id`, `context`, and `temporal`. Sprint A must add support for `auth_context` and `tenant_context` in the request, gated as follows:

- Anonymous user → browse actions allowed, execution actions denied **fail-closed** with reason code `AUTH_REQUIRED`
- Authenticated user → browse + execution actions allowed (subject to existing policy gates)
- The policy engine must check `auth_context.auth_state` before allowing execution-class actions
- This is the "auth gate" described in `AUTH_MODEL.md` §6

**Important:** when an anonymous user is denied an execution action, the engine emits a deny decision with reason code `AUTH_REQUIRED`. The user-facing "please log in" message is rendered via the **RR template** (e.g., a `user_visible_summary` field referencing the reason code), NOT hardcoded in engine logic. The engine does not generate UI copy — it emits structured decisions and reason codes.

### 5. Engine-to-adapter call flow

The policy engine must NOT call adapters directly. The flow is:

```
Request → PolicyEngine.evaluate_request() → PolicyDecision
                                                ↓
                                        (if decision = allow_execute
                                         AND action requires tool execution)
                                                ↓
                                        ToolExecutor.execute(adapter, tool_call) → TER
                                                ↓
                                        Adapter.execute(tool_call, ctx) → ToolResult
```

**Critical: do NOT execute on `require_confirmation`.** If the policy decision is `require_confirmation`, Sprint A emits the PDR + RR and **stops**. No adapter call. No TER. The caller must come back with a confirmed request. This avoids dragging Sprint B's confirmation lifecycle (UVS binding, fingerprint verification, TTL enforcement) into Sprint A.

For `place_bet`, the two-request model is:

1. **Request 1:** `place_bet` → engine decides `require_confirmation` → PDR + RR emitted → response includes confirmation payload shape (stubbed)
2. **Request 2:** `confirm_place_bet` (with confirmation token/payload) → engine decides `allow_execute` → ToolExecutor calls adapter → TER emitted

Sprint A stubs the confirmation payload shape without implementing the full confirmation lifecycle. Sprint B will replace this stub with proper UVS binding. The stub contract is intentionally minimal to prevent anyone from accidentally building a mini-UVS system.

**Confirmation stub contract for Sprint A:**

```python
confirmation_stub = {
    "nonce": str,           # Opaque string, present but NOT cryptographically validated
    "issued_at": str,       # ISO 8601 timestamp
    "pdr_record_id": str    # Must reference the PDR from request 1
}
```

**Engine validation rules for `confirm_place_bet` (Sprint A only):**
- `pdr_record_id` must be present and must reference an existing PDR from the same session/request flow
- `nonce` must be present and non-empty (no cryptographic validation — that's Sprint B)
- `issued_at` must be present and parseable (no TTL enforcement — that's Sprint B)
- If any field is missing or `pdr_record_id` doesn't match: deny, fail closed

**What the stub explicitly does NOT do:**
- No cryptographic nonce validation
- No TTL / expiry enforcement on the confirmation
- No odds-drift detection or reconfirmation
- No UVS generation or fingerprint binding

**The `ToolExecutor` is a thin coordination layer that:**

- **Auth gate:** Checks `auth_context` (token presence, expiry, tenant binding) *before* calling the adapter. If auth fails, deny + TER with `error_code: "AUTH_GATE_FAILED"` and `adapter_id: "none"`.
- **Adapter selection:** Maps `action_id` → adapter via a simple **dict mapping in code**. No registry pattern, no dynamic discovery. Example: `{"place_bet": sportsbook_adapter, "get_events": sportsbook_adapter, "get_odds": sportsbook_adapter}`. This dict will evolve into pack-defined mapping + adapter registry in Phase 2+, but for Sprint A a hardcoded dict is honest and sufficient.
- Calls `adapter.execute(tool_call, ctx)`
- Captures timing (`duration_ms`)
- Emits the TER (including fingerprints)
- Handles adapter failure: any exception from the standardized set → fail closed → deny + TER with `error_code`

**RR reason codes for execution failures:** When the ToolExecutor produces a TER with `success=false`, the corresponding RR must include a **stable, machine-readable reason code** mapped from the TER error. No freeform error strings in the RR beyond a safe, template-controlled summary.

| TER error_code | RR reason code |
|----------------|---------------|
| `AdapterUnavailable` | `UPSTREAM_UNAVAILABLE` |
| `AdapterTimeout` | `UPSTREAM_TIMEOUT` |
| `AdapterAuthError` | `AUTH_REQUIRED` |
| `AdapterUpstreamError` | `UPSTREAM_ERROR` |
| `AdapterProtocolError` | `ADAPTER_PROTOCOL_ERROR` |
| `ADAPTER_NOT_MAPPED` | `EXECUTION_UNAVAILABLE` |
| `AUTH_GATE_FAILED` | `AUTH_REQUIRED` |

This keeps the RR deterministic and safe for user-facing rendering via templates.

### 6. Integration with existing tests

- All 43 existing tests MUST continue to pass unchanged
- New tests must cover:
  - Adapter contract enforcement (missing methods → error at instantiation, not at call time)
  - Happy path: browse → adapter call → TER emitted
  - Happy path: `place_bet` → `require_confirmation` (no adapter call, no TER) → `confirm_place_bet` → `allow_execute` → adapter call → TER emitted
  - Failure path: adapter down → fail closed → deny + TER with `AdapterUnavailable` error
  - Failure path: adapter timeout → fail closed → deny + TER with `AdapterTimeout` error
  - Failure path: adapter auth failure → deny + TER with `AdapterAuthError` error
  - Anonymous user → execution denied with `AUTH_REQUIRED` reason code (no adapter call)
  - Authenticated user → execution allowed
  - No adapter mapped for action → fail closed → deny + TER with `error_code: "ADAPTER_NOT_MAPPED"`, `adapter_id: "none"`, `tool_call` present (what was attempted)
  - **Tenant isolation:** two toy adapter instances initialized with different `ServiceConfig` (Tenant A, Tenant B) return different data for the same `get_events` call. This forces `ServiceConfig` to actually be used and proves tenant-scoping is not decorative.
  - **Idempotency:** calling `place_bet` twice with the same `idempotency_key` returns the first result, not a duplicate execution
  - **Evidence ordering and linkage:** for a tool-execution action, verify:
    - PDR emitted first
    - TER emitted with `pdr_record_id` matching the PDR's `record_id`
    - RR emitted with same `request_id` as PDR and TER
    - All three records share the same `action_type` and `request_id`
    - The triangle is complete and unambiguous

---

## Explicitly out of scope

- Real API calls to any operator system (toy adapter only)
- WalletAdapter or RGAdapter (Sprint A is sportsbook only)
- Multi-provider routing or adapter registry patterns
- **Full confirmation lifecycle / UVS binding (that's Sprint B)** — Sprint A stubs the confirmation payload shape but does NOT implement UVS generation, fingerprint binding, TTL enforcement, or odds-drift reconfirmation
- Evidence persistence to disk/DB (that's Sprint D)
- Casino adapters
- Personalization (odds or otherwise)
- Rate limiting
- Circuit breakers
- Retry with backoff
- Integration Probe / auto-discovery
- Player-auth hooks on the base AdapterContract (auth gating is ToolExecutor's job)
- Dynamic adapter discovery or registration

---

## Hard constraints

1. **Fail closed.** Any adapter failure, timeout, or unexpected error results in a deny decision. No silent failures.
2. **No secrets in evidence.** TERs must not contain API keys, session tokens, or credentials. Ever.
3. **Backward compatible.** All existing tests pass without modification. The new code must be additive.
4. **Smallest viable interface.** The adapter contract must be the minimum needed to make the toy adapter work. No speculative abstractions. (See risk R-001.)
5. **Deterministic record IDs.** TER IDs must follow the same canonical-JSON + SHA-256 pattern as existing PDR/RR IDs.
6. **Tenant-scoped.** Adapters must be initialized with tenant-specific config. Even the toy adapter must demonstrate tenant awareness.

---

## Known risks (from RISK_REGISTER.md)

- **R-001: Adapter Interface Over-Engineering** — The biggest risk. Mitigate by building the minimum interface that makes the toy adapter work, then iterate.
- **R-004: Operator API Diversity** — Not a Sprint A risk (toy adapter), but the contract shape should not make this harder later.
- **R-012: Service-Level Auth Missing** — Sprint A must include the service auth pattern in the adapter contract, even if the toy adapter's "service auth" is a no-op.

---

## Key context documents

| Document | Why it matters |
|----------|---------------|
| `docs/HARMONY_STATE.md` | Current state of the build — what exists, what's missing |
| `docs/ROADMAP.md` | Sprint A definition, dependencies, acceptance criteria |
| `docs/INTEGRATION_LANDSCAPE.md` | Integration domains, adapter grouping (§4), adapter contract preview (§4), truth source mapping |
| `docs/AUTH_MODEL.md` | Two-layer auth (§0), auth context object (§3), adapter auth contract (§9), Sprint A implications (§10) |
| `docs/RISK_REGISTER.md` | R-001, R-004, R-012 |
| `docs/REDTEAM_AUTH_INTEGRATION_v1.md` | Red team findings that shaped the auth and integration design |
| `docs/PHASE_0_CLOSURE_REPORT.md` | What Phase 0 proved |
| `docs/Harmony_V2_Vision_v2.md` | High-level product vision |
| `docs/HARMONY_V2_SYSTEM_INVARIANTS.md` | System invariants the adapter must not violate |
| `runtime/policy_engine.py` | The engine code the adapter plugs into |
| `runtime/schemas.py` | Schemas that may need extension for auth_context |
| `packs/UKGC_BASELINE_POLICY_PACK.yaml` | Action registry, reason codes, truth sources |
| `packs/UKGC_BETTING_PACK.yaml` | Sportsbook-specific policy rules |

---

## Acceptance criteria (tight, unambiguous)

1. **AdapterContract exists** with minimal surface area (`execute` + `health` + standardized exceptions). Toy sportsbook adapter implements it.
2. **ToolExecutor exists.** PolicyEngine does NOT directly call adapters. ToolExecutor owns auth gating, adapter selection (dict mapping), timing, TER emission, and fail-closed error handling.
3. **TER exists.** Emitted on every adapter call. Deterministic `record_id`. Includes `tool_call_fingerprint` and `result_fingerprint`. Contains `pdr_record_id` and `request_id` for explicit linkage. No secrets.
4. **`auth_context` + `tenant_context` supported** in inbound request schema. Anonymous users denied execution actions fail-closed with `AUTH_REQUIRED` reason code. Auth prompt rendered via RR template, not hardcoded.
5. **`require_confirmation` does NOT trigger adapter calls.** Execution only happens on `allow_execute` (confirmed path). Sprint A stubs confirmation payload shape without implementing full lifecycle.
6. **Adapter failures produce deny + TER with error_code.** No hangs, no partial success, no swallowed errors.
7. **Evidence triangle is wired correctly.** PDR → TER → RR linked via `pdr_record_id`, `request_id`, and `action_type`. A dedicated test verifies ordering and linkage.
8. **All 43 existing tests pass unchanged** + new tests cover happy/failure/auth/no-adapter/tenant-isolation/idempotency/evidence-linkage cases.
9. **PolicyEngine remains pure.** The engine is deterministic and side-effect free: it does not perform I/O, network access, or time calls (beyond an injected clock). All side effects (adapter calls, timing, TER emission) are owned by the ToolExecutor. This boundary is architectural and non-negotiable.

## Success looks like

After Sprint A, I should be able to:

1. Send a `place_bet` request → get `require_confirmation` → no adapter call, no TER, just PDR + RR
2. Send a `confirm_place_bet` with stubbed confirmation payload → get `allow_execute` → toy adapter called → TER emitted alongside PDR and RR
3. Inspect the TER and confirm: `pdr_record_id` links to the PDR, fingerprints are present, no secrets
4. Simulate the adapter being down → fail closed → deny + TER with `AdapterUnavailable`
5. Send an execution request as anonymous user → denied with `AUTH_REQUIRED`, no adapter call
6. Run all 43 existing tests and see them pass unchanged
7. Inspect the evidence triangle (PDR + TER + RR) and trace a single request through all three records via `request_id`

---

## Dual purpose of this sprint

This is also the first live test of the **Doc Factory v2 pipeline**. The Factory should take this brief and produce a sprint-ready execution pack (locked intent, constraints, risks, test fixtures, micro-sprint plan, sprint envelope). I will evaluate both:

1. **Sprint A quality** — Is the execution pack clear enough to build from?
2. **Factory quality** — Did the pipeline produce consistent, complete, reviewable output? Where did it struggle?

Feedback on the Factory process will be captured separately and used to iterate the pipeline.
