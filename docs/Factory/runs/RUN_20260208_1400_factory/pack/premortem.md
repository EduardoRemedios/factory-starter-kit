# premortem.md — Sprint A Pre-mortem

## Version
v1

## Change Log
- v1 (2026-02-08): Initial pre-mortem for Sprint A: Adapter Boundary.

## Purpose
Enumerate the top failure scenarios for Sprint A execution and identify mitigations that must be in place before or during the sprint.

## Top Failure Scenarios

### F-01: Adapter calls leak into PolicyEngine
- **What goes wrong:** An agent implementing the adapter boundary places tool execution logic inside `policy_engine.py` instead of a separate ToolExecutor, violating C-04 and the engine purity principle.
- **Why it's likely:** The engine already has the decision result and the action context. The path of least resistance is to add adapter calls inline.
- **Impact:** Violates system invariant 2.5 (authority separation). Makes the engine non-deterministic and side-effect-bearing. Breaks architectural boundary permanently.
- **Mitigation:** The intent explicitly requires handle_request() as a separate orchestration function. Sprint tests must assert that `policy_engine.py` has no imports of adapter modules. Code review gate.

### F-02: Existing tests break from auth_context schema change
- **What goes wrong:** Adding `auth_context` as a required field breaks the 43 existing tests that don't provide it.
- **Why it's likely:** Schema validation in `validate_userland_request()` currently rejects unknown fields. If auth_context is added to the schema, old tests need updating.
- **Impact:** Violates C-01 (43 tests unchanged). Cascading failures across the test suite.
- **Mitigation:** C-21 specifies auth_context as optional with backward-compatible defaults. Tests should be run before and after schema changes. If the schema validator uses strict unknown-field rejection, auth_context must be added to the allowed-fields list without making it required.

### F-03: Evidence triangle is internally contradictory
- **What goes wrong:** The engine emits a "completed" RR before the adapter call, then the adapter fails. The RR says success but the TER says failure. Downstream consumers (audit, compliance) see contradictory records.
- **Why it's likely:** The engine currently emits both PDR and RR atomically in `_boundary_finalize()`. Adding a post-execution RR requires restructuring the emission flow.
- **Impact:** Evidence integrity violation. Regulatory audit failure. Trust in the evidence chain collapses.
- **Mitigation:** C-19 specifies decision-only RR stub from engine, final RR post-execution. The existing `decision_only: True` field in the RR output supports this pattern. Test must verify RR final_outcome matches TER success status.

### F-04: Toy adapter is too realistic or too abstract
- **What goes wrong:** The toy adapter either (a) tries to simulate too many real sportsbook behaviors (pricing logic, market states, settlement) and becomes a maintenance burden, or (b) is so trivial (returns hardcoded JSON) that it doesn't exercise the contract meaningfully.
- **Why it's likely:** The brief asks for "realistic enough to test the full flow" but also "not a production adapter." The boundary is ambiguous.
- **Impact:** (a) Scope creep into Sprint A. (b) False confidence — contract bugs only discovered in Sprint C when real adapters are attempted.
- **Mitigation:** The toy adapter should support configurable responses (happy path, error injection, auth failure, stale data) via constructor parameters or config dict. It should NOT implement business logic beyond echoing configured responses.

### F-05: Idempotency implementation is under-specified
- **What goes wrong:** The idempotency_key for place_bet is required by C-11 but the storage mechanism is unspecified. An in-memory dict works for the toy adapter but doesn't carry across restarts. Agents may over-engineer with persistence.
- **Why it's likely:** Idempotency typically requires state storage, which is explicitly out of scope for Sprint A.
- **Impact:** Either the idempotency test is fragile (in-memory only, lost on restart) or the agent adds persistence (scope creep).
- **Mitigation:** Toy adapter uses in-memory dict for idempotency. This is sufficient for test-level verification. Persistent idempotency is a Phase 2+ concern. Document this boundary explicitly.

### F-06: confirm_place_bet action registry integration fails
- **What goes wrong:** Adding `confirm_place_bet` to the action registry YAML requires careful alignment with the schema validator. The new action may fail schema validation or conflict with existing action classification logic.
- **Why it's likely:** The action registry schema in schemas.py is strict. A new action must match the exact shape of existing entries.
- **Impact:** confirm_place_bet is denied by the engine's closed-world enforcement, breaking the two-request model.
- **Mitigation:** Add the action to the YAML pack with the same field shape as existing IRR actions. Run the pack loader and schema validation as a first test.
