# micro_sprints.md — Sprint A Micro-sprint Sequence

## Version
v1

## Change Log
- v1 (2026-02-08): Initial micro-sprint sequencing for Sprint A: Adapter Boundary.

## Purpose
Breaks Sprint A into gated micro-sprints with entry/exit criteria and stop/go gates.

---

## MS-01: Foundation — Schema Extension + AdapterContract + Exceptions

### Objective
Establish the foundational types and interfaces: extend the request schema for auth_context/tenant_context, define AdapterContract, ToolCall/ToolResult schemas, standardized exceptions, and ServiceConfig. Add `confirm_place_bet` to the action registry. Resolve deferred items D-001 and D-002.

### Inputs
- runtime/schemas.py (existing)
- runtime/errors.py (existing)
- packs/UKGC_BASELINE_POLICY_PACK.yaml (existing)
- docs/AUTH_MODEL.md §3, §9 (reference)
- pack/intent.md §4 (locked)

### Outputs
- runtime/adapter_contract.py (AdapterContract ABC, ServiceConfig, ToolCall, ToolResult, 5 exception classes)
- runtime/schemas.py (updated: auth_context + tenant_context as optional fields)
- runtime/errors.py (updated: adapter exception classes, or new file)
- packs/UKGC_BASELINE_POLICY_PACK.yaml (updated: confirm_place_bet action added)

### Entry Criteria
- All 43 existing tests pass (CI green)
- intent.md v2 locked

### Exit Criteria
- AdapterContract defined with execute, health, adapter_id
- 5 standardized exception classes defined
- ToolCall and ToolResult schemas defined
- auth_context and tenant_context accepted as optional payload fields
- confirm_place_bet in action registry
- All 43 existing tests still pass (C-01)
- D-001 and D-002 documentation completed

### Stop/Go Gate
- **Gate 1:** Run `python3 -m unittest discover -s tests`. All 43 tests must pass. If any fail, STOP — schema change broke backward compatibility. Fix before proceeding.

---

## MS-02: ToolExecutor + Auth Gate + TER Emission

### Objective
Build the ToolExecutor coordination layer with auth gating, adapter selection (dict mapping), timing, TER emission, and fail-closed error handling. Build the handle_request() orchestration entrypoint.

### Inputs
- runtime/adapter_contract.py (from MS-01)
- runtime/policy_engine.py (existing, read-only)
- pack/intent.md §4.5, §4.6, §4.12 (locked)

### Outputs
- runtime/tool_executor.py (ToolExecutor class)
- runtime/orchestrator.py (handle_request() entrypoint) — or combined with tool_executor.py
- TER emission logic with deterministic record_id, fingerprints, linkage fields

### Entry Criteria
- MS-01 exit criteria met (Gate 1 passed)
- AdapterContract and exceptions exist

### Exit Criteria
- ToolExecutor performs auth gate check before adapter call
- ToolExecutor maps action_id to adapter via dict
- ToolExecutor measures duration_ms via monotonic clock
- TER emitted with all required fields (record_id, pdr_record_id, request_id, action_type, adapter_id, tool_call, tool_call_fingerprint, tool_result, result_fingerprint, duration_ms, success, error_code)
- TER record_id is deterministic (canonical-JSON + SHA-256)
- handle_request() sequences: engine decision → conditional ToolExecutor call → evidence chain
- No adapter imports in policy_engine.py (C-04)
- RR emission timing correct: decision-only stub from engine, final RR post-execution (C-19)
- Fail-closed on all 5 exception types

### Stop/Go Gate
- **Gate 2:** Run `python3 -m unittest discover -s tests`. All 43 tests pass + VP-06 (no adapter imports in engine) passes. If engine purity is violated, STOP — architectural boundary breach. Refactor before proceeding.

---

## MS-03: Toy SportsbookAdapter + Tenant Isolation + Idempotency

### Objective
Implement the toy SportsbookAdapter with configurable responses, tenant-scoped behavior, and idempotency support. Wire it into the ToolExecutor's adapter mapping.

### Inputs
- runtime/adapter_contract.py (from MS-01)
- runtime/tool_executor.py (from MS-02)
- pack/intent.md §4.4 (locked)
- pack/fixtures/ (from Stage F)

### Outputs
- runtime/adapters/sportsbook_toy.py (SportsbookAdapter)
- ToolExecutor adapter mapping updated: {get_events, get_odds, place_bet, confirm_place_bet} → sportsbook_toy

### Entry Criteria
- MS-02 exit criteria met (Gate 2 passed)
- ToolExecutor exists with auth gate and TER emission

### Exit Criteria
- SportsbookAdapter implements AdapterContract (execute + health)
- Supports get_events, get_odds, place_bet tool_ids
- Configurable responses via constructor (happy path, errors, auth failures)
- Tenant isolation: different ServiceConfig → different adapter_id and response data (C-10)
- Idempotency: duplicate place_bet with same key returns first result (C-11)
- Health check returns meaningful status
- No business logic beyond response configuration

### Stop/Go Gate
- **Gate 3:** VP-10 (tenant isolation), VP-11 (idempotency), VP-15 (contract compliance) all pass. If tenant isolation fails, STOP — multi-tenancy assumption violated.

---

## MS-04: Integration Tests + Evidence Triangle Verification

### Objective
Write all new tests covering happy paths, failure paths, auth scenarios, evidence linkage, and secret leakage checks. Verify the complete evidence triangle. Run the full suite.

### Inputs
- All runtime code from MS-01 through MS-03
- pack/verification_plan.md (VP-01 through VP-20)
- pack/fixtures/ (from Stage F)

### Outputs
- tests/test_sprint_A.py (all new tests)
- CI configuration updated if needed

### Entry Criteria
- MS-03 exit criteria met (Gate 3 passed)
- Toy adapter wired and functional

### Exit Criteria
- All VP-01 through VP-20 tests written and passing
- All 43 existing tests pass unchanged (C-01)
- Evidence triangle test verifies ordering + linkage + fingerprints (AC-07)
- Secret leakage test confirms no tokens in TER (C-03)
- require_confirmation → no adapter call test passes (C-05)
- Anonymous deny test passes (C-08)
- Error injection tests for all 5 exception types pass
- Integration test: place_bet → require_confirmation → confirm_place_bet → execute → evidence chain
- Full suite green: `python3 -m unittest discover -s tests`

### Stop/Go Gate
- **Gate 4 (Final):** All tests pass. CI green. Sprint A is complete and ready for review.

---

## Bounded Deferral Hooks

| Deferral ID | Description | Hooked to |
|---|---|---|
| D-001 | Legacy decide() path documentation | MS-01 |
| D-002 | action_id vs action_type naming documentation | MS-01 |
