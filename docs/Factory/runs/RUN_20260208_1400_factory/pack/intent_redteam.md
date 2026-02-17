# intent_redteam.md — Red Team Report on Intent (Sprint A)

## Version
v1

## Change Log
- v1 (2026-02-08): Initial Red Team findings on intent.md v1.

## Iteration
- Iteration: 1 of max 2

## Inputs Reviewed (LOAD)
- pack/intent.md (v1)

## Executive Summary
The intent is well-structured and draws heavily from a detailed raw brief. The scope is realistic and the non-goals are clearly stated. However, several gaps exist around the engine-to-ToolExecutor handoff mechanism, the `confirm_place_bet` action's integration with the existing action registry, and verification coverage for timing-related behavior. Seven findings identified: 2 Critical, 3 High, 2 Medium.

## Severity-Ranked Findings

| ID | Severity | Category | Finding | Why it matters | Fix recommendation |
|---|---|---|---|---|---|
| RT-01 | Critical | Architecture gap | The intent does not specify HOW the PolicyEngine hands off to the ToolExecutor. The engine's `evaluate_request()` currently returns a dict and exits. There is no call site, no orchestration layer, and no defined entrypoint that sequences "engine decision → ToolExecutor call → TER emission → RR update." Without this, agents will invent incompatible orchestration patterns. | The entire adapter boundary depends on a clear call flow. Without specifying who calls `ToolExecutor.execute()` and where in the stack it sits, implementation will diverge. | Add a constraint or acceptance criterion defining the orchestration entrypoint. Specify whether a new top-level function (e.g., `handle_request()`) wraps `evaluate_request()` + `ToolExecutor`, or if the caller is responsible. |
| RT-02 | Critical | Evidence integrity | The intent says TER is emitted "on every adapter call attempt," including pre-call failures. But it does not specify how the RR is updated to reflect tool execution results. Currently, the engine emits PDR + RR at decision time — BEFORE any adapter call. If the adapter then fails, the RR says "completed" but the actual outcome is "failed." The RR must be updated or a new RR emitted post-execution. | Without this, the evidence triangle is internally contradictory: RR claims success, TER shows failure. Auditors and downstream consumers cannot trust the records. | Specify whether: (a) the initial RR is a "decision-only" stub updated post-execution, (b) a second RR is emitted after TER, or (c) the RR is only emitted after the full flow completes. |
| RT-03 | High | Missing specification | The `confirm_place_bet` action is referenced as the second request in the two-request model, but it does not appear in the existing action registry (`UKGC_BASELINE_POLICY_PACK.yaml`). The engine's closed-world registry will deny it as an unknown action. The intent does not specify whether this action must be added to the registry or handled via a different mechanism. | An unregistered action will be denied by the engine's closed-world enforcement (tested in Sprint 01). The two-request model will fail at step 2. | Specify that `confirm_place_bet` must be added to the action registry with appropriate class (IRREVERSIBLE_REGULATED) and evidence/UVS profiles, OR specify an alternative confirmation mechanism that works within the existing action model. |
| RT-04 | High | Verification gap | The intent defines `duration_ms` in TER but no constraint on timing accuracy or clock source. The engine currently follows "no implicit now" (invariant 2.8), using injected temporal context. If ToolExecutor reads `time.time()` for `duration_ms`, it violates the temporal spine invariant. But if it doesn't read the clock, it can't measure duration. | Either the temporal spine invariant is violated (Critical system invariant breach), or `duration_ms` cannot be populated (incomplete TER). | Explicitly state that `duration_ms` is a ToolExecutor-level operational metric, NOT a policy input, and is therefore exempt from the "no implicit now" invariant. Or specify an injected clock for ToolExecutor. |
| RT-05 | High | Scope ambiguity | The intent says "auth_context and tenant_context in inbound request schema" but doesn't specify whether the existing `evaluate_request()` signature changes. Currently it takes `payload: Any` with `action_id`, `context`, and `temporal`. Adding `auth_context` could mean: (a) a new top-level field in payload, (b) nested inside `context`, (c) a separate parameter. Each has different backward-compatibility implications. | Agents may implement different approaches, breaking the 43 existing tests (violating C-01). | Specify the exact schema change: `auth_context` and `tenant_context` as optional top-level fields in the payload dict, defaulting to anonymous/unknown when absent (preserving backward compatibility). |
| RT-06 | Medium | Verification gap | No fixture or test is specified for the ToolExecutor's auth gate behavior when `auth_context.auth_state` transitions mid-flow (e.g., token expires between engine decision and adapter call). The intent covers static states (anonymous → deny, authenticated → allow) but not transitions. | Mid-flow token expiry is a real production scenario (AUTH_MODEL.md §4.2). If untested, it could result in adapter calls with expired tokens. | Add a fixture/test case for token-expiry-between-decision-and-execution. Even if the ToolExecutor just checks at call time, the scenario should be explicitly covered. |
| RT-07 | Medium | Definition gap | The intent references "standardized exceptions" but does not specify whether these are Python exceptions (raised by the adapter, caught by ToolExecutor) or error codes in the ToolResult. The raw brief implies Python exceptions, but the ToolResult schema has an `error` field. Agents may implement both, creating redundant error paths. | Dual error mechanisms (exceptions + error codes) create ambiguity about which is authoritative and what ToolExecutor should catch. | Clarify: adapters raise Python exceptions for infrastructure failures (unavailable, timeout, auth); `ToolResult.error` is for business-level errors (bet rejected, insufficient funds). ToolExecutor catches exceptions and translates to TER error codes. |

## Agent Failure Modes

- **Mode 1: Orchestration invention.** Without a specified call flow, an agent may embed adapter calls inside `PolicyEngine.evaluate_request()`, violating C-04 and the engine purity principle. Mitigation: explicit architectural constraint on where ToolExecutor sits.
- **Mode 2: RR inconsistency.** An agent may emit the RR before the adapter call completes, then not update it, creating contradictory evidence. Mitigation: specify RR emission timing relative to TER.
- **Mode 3: Clock violation.** An agent may import `time.time()` inside the engine module for `duration_ms`, violating the temporal spine invariant. Mitigation: clarify that timing is ToolExecutor's responsibility, not the engine's.
- **Mode 4: Test breakage from schema change.** An agent adds required `auth_context` field, breaking the 43 existing tests that don't include it. Mitigation: make auth_context optional with safe defaults.

## Verification Holes

- No test specified for evidence ordering (PDR emitted before TER before RR) — only linkage is covered. The raw brief mentions ordering but AC-07 bundles it with linkage.
- No test for `AdapterProtocolError` (upstream response doesn't match expected shape). The brief lists it as an exception but no test scenario covers it.
- No test for `health()` method behavior or return type.
- No negative test for secret leakage in TER (e.g., asserting that TER does not contain specific token patterns).
