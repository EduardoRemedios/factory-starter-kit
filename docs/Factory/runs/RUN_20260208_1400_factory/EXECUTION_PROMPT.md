# Sprint A Execution — Adapter Boundary + Toy Sportsbook Adapter

You are executing **Sprint A** for the Harmony project. This sprint introduces the adapter boundary between the policy engine and external systems. A complete sprint pack has been produced by the Doc Factory pipeline and approved. Your job is to implement the code changes described in the pack.

---

## Step 0: Read these files FIRST (in this order)

Read every file listed below before writing any code. Do not skip any.

### Execution contract (your instructions)
1. `docs/Factory/runs/RUN_20260208_1400_factory/pack/SPRINT_SPRINT_20260208_001_ENVELOPE.md` — the sprint envelope. This is your execution contract: scope, constraints, acceptance criteria, file-touch budgets, stop/go gates.
2. `docs/Factory/runs/RUN_20260208_1400_factory/pack/micro_sprints.md` — the step-by-step execution sequence. You MUST follow MS-01 → MS-02 → MS-03 → MS-04 **in order**, stopping at each gate.
3. `docs/Factory/runs/RUN_20260208_1400_factory/pack/intent.md` — the locked intent (v2). This is the authoritative reference for what is in scope, what is NOT in scope, and all constraints.
4. `docs/Factory/runs/RUN_20260208_1400_factory/pack/verification_plan.md` — tells you exactly what tests to write and what each must check.
5. `docs/Factory/runs/RUN_20260208_1400_factory/pack/traceability_matrix.md` — maps every constraint to its verification point.
6. `docs/Factory/runs/RUN_20260208_1400_factory/pack/risk_register.md` — sprint-level risks to watch for.

### Product context (what exists today)
7. `docs/HARMONY_STATE.md` — current state of the build. What exists, what doesn't.
8. `docs/AUTH_MODEL.md` — two-layer auth model, auth context object shape (§3), ServiceConfig shape (§9).
9. `docs/HARMONY_V2_SYSTEM_INVARIANTS.md` — non-negotiable system invariants. Do not violate these.
10. `runtime/policy_engine.py` — the existing policy engine. **DO NOT MODIFY THIS FILE** except to add auth_context support as an optional field (C-21). Do NOT add adapter imports or I/O to this file.
11. `runtime/schemas.py` — existing schema validators. You will extend these.
12. `runtime/errors.py` — existing error classes.
13. `runtime/pack_loader.py` — YAML pack loader.
14. `packs/UKGC_BASELINE_POLICY_PACK.yaml` — the action registry. You will add `confirm_place_bet` here.
15. `tests/test_sprint_00.py`, `tests/test_sprint_01.py`, `tests/test_sprint_02.py`, `tests/test_sprint_03.py` — the 43 existing tests. **DO NOT MODIFY THESE FILES.** All must continue to pass.

### Detailed specifications (from the raw brief)
16. `docs/Factory/briefs/BRIEF_SPRINT_A_ADAPTER_BOUNDARY.md` — the original raw brief with detailed implementation specs: ToolCall/ToolResult schemas, TER field list, reason code mapping table, confirmation stub contract, adapter exception types, call flow diagram. **This is your implementation reference for data shapes.**

### Golden test fixtures
17. `docs/Factory/runs/RUN_20260208_1400_factory/pack/fixtures/` — 8 fixture sets with input.json, expected.json, and notes.md. Use these as your golden test vectors.

---

## Step 1: Verify entry criteria

Before writing any code:
```bash
python3 -m unittest discover -s tests
```
All 43 tests must pass. If they don't, STOP and report.

---

## Step 2: Execute micro-sprints in order

### MS-01: Foundation — Schema Extension + AdapterContract + Exceptions

**What to build:**
- `runtime/adapter_contract.py` containing:
  - `AdapterContract` (abstract base class or Protocol) with: `adapter_id: str`, `__init__(self, service_config: ServiceConfig)`, `execute(self, tool_call: ToolCall, ctx: RequestContext) -> ToolResult`, `health(self) -> HealthStatus`
  - `ServiceConfig` dataclass/dict: `tenant_id`, `base_url`, `auth_mechanism`, `credentials_ref`
  - `ToolCall` schema: `tool_id: str`, `params: dict`, `idempotency_key: str | None`, `requested_at: str`
  - `ToolResult` schema: `tool_id: str`, `success: bool`, `data: dict | None`, `error: str | None`
  - 5 exception classes: `AdapterUnavailable`, `AdapterTimeout`, `AdapterAuthError`, `AdapterUpstreamError`, `AdapterProtocolError`
- Update `runtime/schemas.py`: add `auth_context` and `tenant_context` as **optional** top-level fields in the userland request schema. When absent, default to `auth_state: "anonymous"`, `tenant_id: "unknown"`. **This MUST NOT break the 43 existing tests.**
- Update `packs/UKGC_BASELINE_POLICY_PACK.yaml`: add `confirm_place_bet` to the action registry as `IRREVERSIBLE_REGULATED` with `confirmation_required: false`.
- Document the `action_id` vs `action_type` distinction (D-002) in a brief comment or docstring.

**Gate 1:** Run `python3 -m unittest discover -s tests`. All 43 tests must pass. If ANY fail, the schema change broke backward compatibility — fix before proceeding.

---

### MS-02: ToolExecutor + Auth Gate + TER Emission

**What to build:**
- `runtime/tool_executor.py` containing:
  - `ToolExecutor` class with:
    - Auth gate: checks `auth_context.auth_state` before calling adapter. If anonymous + execution action → deny + no adapter call.
    - Adapter selection: simple dict mapping `action_id → adapter`. Example: `{"place_bet": sportsbook_adapter, "get_events": sportsbook_adapter, ...}`.
    - Calls `adapter.execute(tool_call, ctx)`
    - Measures `duration_ms` via **monotonic clock** (`time.monotonic()`, NOT `time.time()` — this is a ToolExecutor-level metric, not a policy input)
    - Emits TER with ALL required fields (see raw brief §2 for full list)
    - Catches all 5 adapter exception types → fail closed → deny + TER with `error_code`
    - When no adapter is mapped → deny + TER with `error_code: "ADAPTER_NOT_MAPPED"`, `adapter_id: "none"`
  - TER `record_id` generation: canonical-JSON + SHA-256, same pattern as existing PDR/RR
  - `tool_call_fingerprint`: SHA-256 of canonical serialized tool_call (secret-stripped)
  - `result_fingerprint`: SHA-256 of canonical serialized tool_result
- `runtime/orchestrator.py` (or combine with tool_executor.py) containing:
  - `handle_request(payload, packs, tool_executor)` function that:
    1. Calls `PolicyEngine.evaluate_request(payload)`
    2. If decision is `allow_execute` (or `allow` for read actions that need tool execution) AND action requires adapter call → calls `ToolExecutor.execute()`
    3. If decision is `require_confirmation` → does NOT call ToolExecutor. Returns PDR + decision-only RR. No TER.
    4. After tool execution → emits final RR reflecting actual outcome (replaces the decision-only RR stub from the engine)
    5. Returns complete evidence chain: PDR + TER + final RR (or PDR + RR if no execution)

**CRITICAL CONSTRAINT:** Do NOT add any imports, adapter logic, or I/O to `runtime/policy_engine.py`. The engine must remain pure. The ToolExecutor and orchestrator live in separate files.

**TER-to-RR reason code mapping** (from raw brief):
| TER error_code | RR reason code |
|---|---|
| `AdapterUnavailable` | `UPSTREAM_UNAVAILABLE` |
| `AdapterTimeout` | `UPSTREAM_TIMEOUT` |
| `AdapterAuthError` | `AUTH_REQUIRED` |
| `AdapterUpstreamError` | `UPSTREAM_ERROR` |
| `AdapterProtocolError` | `ADAPTER_PROTOCOL_ERROR` |
| `ADAPTER_NOT_MAPPED` | `EXECUTION_UNAVAILABLE` |
| `AUTH_GATE_FAILED` | `AUTH_REQUIRED` |

**Gate 2:** Run `python3 -m unittest discover -s tests`. All 43 tests pass. Also verify: `runtime/policy_engine.py` has NO new imports referencing adapter modules. If engine purity is violated, STOP and refactor.

---

### MS-03: Toy SportsbookAdapter + Tenant Isolation + Idempotency

**What to build:**
- `runtime/adapters/sportsbook_toy.py` containing:
  - `SportsbookAdapter` implementing `AdapterContract`
  - `adapter_id` includes tenant scoping (e.g., `f"sportsbook_toy_{service_config.tenant_id}"`)
  - Supports `tool_id` values: `get_events`, `get_odds`, `place_bet`
  - **Configurable responses** via constructor — the adapter is a stub that returns configured data, NOT a real API client. Support:
    - Happy path responses (configurable per tool_id)
    - Error injection (configure adapter to raise any of the 5 exception types)
    - Auth failure simulation
  - **Tenant isolation**: two instances with different `ServiceConfig` must return different data
  - **Idempotency**: in-memory dict keyed by `idempotency_key`. If same key sent twice for `place_bet`, return first result without re-executing
  - `health()` returns a meaningful status

**Do NOT:**
- Implement real business logic (pricing, market state, settlement)
- Add persistence beyond in-memory dict
- Add retry logic, caching, or circuit breakers

Wire the adapter into ToolExecutor's mapping: `{get_events, get_odds, place_bet, confirm_place_bet} → sportsbook_toy`

**Gate 3:** Write and run tests for tenant isolation (VP-10), idempotency (VP-11), and contract compliance (VP-15). All must pass. If tenant isolation fails, STOP.

---

### MS-04: Integration Tests + Evidence Triangle Verification

**What to build:**
- `tests/test_sprint_A.py` — all new tests. Must cover every VP from the verification plan:

| Must test | VP | What to assert |
|---|---|---|
| Existing suite still green | VP-01 | All 43 original tests pass |
| Adapter unavailable → deny + TER | VP-02 | TER has `error_code: "AdapterUnavailable"`, RR has `UPSTREAM_UNAVAILABLE` |
| Adapter timeout → deny + TER | VP-03 | TER has `error_code: "AdapterTimeout"` (MANDATORY) |
| Adapter auth error → deny + TER | VP-04 | TER has `error_code: "AdapterAuthError"` (MANDATORY) |
| No secrets in TER | VP-05 | Assert TER serialization contains no token/key patterns |
| Engine purity | VP-06 | Assert `policy_engine.py` has no adapter-related imports |
| require_confirmation → no adapter | VP-07 | `place_bet` → `require_confirmation` → no TER, no adapter call |
| Evidence triangle linkage | VP-08 | PDR → TER → RR: `pdr_record_id` matches, `request_id` matches, `action_type` matches, ordering correct, fingerprints present |
| Anonymous deny | VP-09 | Anonymous + execution action → `AUTH_REQUIRED`, no adapter call, no TER |
| Tenant isolation | VP-10 | Two adapter instances, different config → different data |
| Idempotency | VP-11 | Duplicate `place_bet` with same `idempotency_key` → first result returned |
| action_type consistency | VP-12 | Same `action_type` across PDR, TER, RR |
| Fingerprints | VP-13 | `tool_call_fingerprint` and `result_fingerprint` are valid SHA-256 hex strings |
| Adapter not mapped | VP-14 | Unknown action → deny + TER with `ADAPTER_NOT_MAPPED`, `adapter_id: "none"` |
| Contract compliance | VP-15 | AdapterContract has `execute`, `health`; toy adapter passes `isinstance` check |
| ToolExecutor integration | VP-16 | Full ToolExecutor flow works end-to-end |
| Auth gate timing | VP-17 | ToolExecutor checks auth at call time, not at engine decision time |
| Happy browse E2E | VP-18 | `get_events` → adapter called → TER + evidence chain |
| Full place_bet E2E | VP-19 | `place_bet` → `require_confirmation` → `confirm_place_bet` → `allow_execute` → adapter → TER + final RR |
| Error injection for all 5 types | VP-20 | Each exception type → correct TER error_code + correct RR reason_code |

**Gate 4 (Final):** Run `python3 -m unittest discover -s tests`. ALL tests (43 existing + new) must pass. This is the final gate.

---

## Hard rules (do not violate)

1. **DO NOT modify existing test files.** All 43 tests must pass as-is. (C-01)
2. **DO NOT put adapter logic in `policy_engine.py`.** Engine remains pure and side-effect free. (C-04, C-09)
3. **DO NOT implement full confirmation lifecycle.** The confirmation stub has exactly 3 fields: `nonce`, `issued_at`, `pdr_record_id`. No crypto validation, no TTL enforcement, no odds-drift detection. That's Sprint B. (C-16)
4. **DO NOT add retry logic, caching, or circuit breakers.** Fail closed and report. (Non-goals)
5. **No secrets in evidence records.** TERs must not contain API keys, tokens, or credentials. (C-03)
6. **File-touch budget:** max 12 modified, 9 created, 0 deleted across the entire sprint. (Envelope §File-Touch Budgets)
7. **`require_confirmation` does NOT trigger adapter calls or TER emission.** (C-05)
8. **auth_context must be OPTIONAL** with backward-compatible defaults. (C-21)

---

## File-touch budget summary

| Micro-sprint | Modified (max) | Created (max) | Deleted (max) |
|---|---:|---:|---:|
| MS-01 | 5 | 3 | 0 |
| MS-02 | 3 | 3 | 0 |
| MS-03 | 2 | 2 | 0 |
| MS-04 | 2 | 1 | 0 |
| **Total** | **12** | **9** | **0** |

---

## When you're done

After Gate 4 passes:
1. Run `python3 -m unittest discover -s tests` one final time and confirm all tests pass.
2. List all files you created and modified.
3. Confirm each acceptance criterion (AC-01 through AC-09) is met with a one-line evidence pointer.
4. Note any issues, surprises, or recommendations for the next sprint.

---

## If you get stuck

- If an existing test breaks: the schema change is not backward-compatible. Make auth_context/tenant_context truly optional with safe defaults.
- If you're unsure about a data shape: the raw brief (`docs/Factory/briefs/BRIEF_SPRINT_A_ADAPTER_BOUNDARY.md`) has the detailed schemas for ToolCall, ToolResult, TER, and the confirmation stub.
- If you're tempted to add something not in scope: check intent.md §2 (Non-Goals). If it's listed there, don't build it.
- If you find a contradiction with a locked artifact: STOP and report it. Do not silently work around it.
