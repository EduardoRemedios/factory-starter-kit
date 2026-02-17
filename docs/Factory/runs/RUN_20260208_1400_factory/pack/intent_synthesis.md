# intent_synthesis.md — Blue Team Synthesis Report (Sprint A)

## Version
v1

## Change Log
- v1 (2026-02-08): Initial synthesis responding to intent_redteam.md v1.

## Iteration
- Iteration: 1 of max 2

## Inputs Reviewed (LOAD)
- pack/intent.md (v1)
- pack/intent_redteam.md (v1)

## Synthesis Summary
All 7 Red Team findings addressed. Both Critical findings resolved by adding explicit specification to intent.md v2. No scope expansion introduced. No new requirements added — all resolutions are clarifications of existing requirements from the raw brief.

## Finding Resolutions

| RT ID | Severity | Resolution | Scope Expansion? | Status |
|---|---|---|---|---|
| RT-01 | Critical | Added constraint C-18 defining the orchestration pattern: a new top-level `handle_request()` function wraps `evaluate_request()` + conditional `ToolExecutor.execute()`. The PolicyEngine is not modified. The caller invokes `handle_request()` instead of `evaluate_request()` directly for execution-class actions. This is consistent with the raw brief's call flow diagram (§5). | No | RESOLVED |
| RT-02 | Critical | Added constraint C-19 specifying RR emission timing: the initial engine call emits a "decision-only" RR stub. After tool execution completes, a final RR is emitted (or the stub is replaced) reflecting the actual outcome. The TER sits between the PDR and the final RR. This aligns with the existing `decision_only: True` and `downstream_stub` fields already present in the engine's RR output. | No | RESOLVED |
| RT-03 | High | Added to Scope §4: `confirm_place_bet` must be added to the action registry as an IRREVERSIBLE_REGULATED action with `confirmation_required: false` (it IS the confirmation). The engine evaluates it, checks the stub confirmation payload, and if valid, decides `allow_execute`. This is implicit in the raw brief's two-request model but was not explicitly stated as a registry addition. | No | RESOLVED |
| RT-04 | High | Added constraint C-20: `duration_ms` is a ToolExecutor-level operational metric measured by the ToolExecutor using a monotonic clock. It is NOT a policy input and does NOT flow through the engine. The "no implicit now" invariant (§2.8) applies to policy decisions, not to operational metrics in the execution layer. ToolExecutor is explicitly outside the engine's determinism boundary. | No | RESOLVED |
| RT-05 | High | Added constraint C-21: `auth_context` and `tenant_context` are optional top-level fields in the payload dict passed to `evaluate_request()`. When absent, defaults are `auth_state: "anonymous"` and `tenant_id: "unknown"`. This preserves backward compatibility — existing tests that omit these fields continue to work because the engine treats missing auth_context as anonymous (browse actions still allowed, execution denied). | No | RESOLVED |
| RT-06 | Medium | Added to verification expectations (AC-07 expanded): include a test case for token state checked at ToolExecutor call time, not at engine decision time. The ToolExecutor's auth gate is the last check before adapter call. | No | RESOLVED |
| RT-07 | Medium | Added constraint C-22: Adapters raise Python exceptions for infrastructure failures (the 5 standardized exception types). `ToolResult.error` is for business-level errors returned by the upstream (bet rejected, insufficient funds, invalid selection). ToolExecutor catches infrastructure exceptions and maps them to TER `error_code`. Business errors flow through `ToolResult` and are recorded in TER as `success: false` with the business error code. | No | RESOLVED |

## Scope Expansion Check
- No `[SCOPE EXPANSION]` items introduced.
- All resolutions are clarifications of existing raw brief requirements.

## Unresolved Items
- None. All Critical and High findings resolved.

## Recommendations for Purple
- RT-01 resolution (orchestration entrypoint) is architecturally significant. Purple should confirm this does not conflict with any system invariant.
- RT-02 resolution (RR emission timing) leverages existing `decision_only` fields. Purple should verify this is consistent with the Evidence and Receipt Spec.
