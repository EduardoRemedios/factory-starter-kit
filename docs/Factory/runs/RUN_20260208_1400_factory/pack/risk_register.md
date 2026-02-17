# risk_register.md — Sprint A Risk Register

## Version
v1

## Change Log
- v1 (2026-02-08): Initial sprint-level risk register for Sprint A: Adapter Boundary.

## Purpose
Sprint-specific execution risks for Sprint A. Distinct from the project-level risk register at `docs/RISK_REGISTER.md`.

## Risks

### SR-01: Engine purity violation
| Field | Value |
|---|---|
| Severity | Critical |
| Likelihood | Possible |
| Description | Agent places adapter/I/O logic inside PolicyEngine instead of ToolExecutor, breaking the determinism boundary. |
| Mitigation | Intent C-04 and C-09 explicitly prohibit this. Test: assert policy_engine.py has no adapter imports. Code review gate after MS-02. |
| Verification Hook | Test: `test_engine_has_no_adapter_imports` |

### SR-02: Backward compatibility break (43 tests)
| Field | Value |
|---|---|
| Severity | Critical |
| Likelihood | Possible |
| Description | Schema changes for auth_context break existing tests that don't provide it. |
| Mitigation | C-21 mandates auth_context is optional. Run full test suite after every file change in MS-01. |
| Verification Hook | Test: all 43 existing tests pass unchanged (CI gate) |

### SR-03: Evidence triangle inconsistency
| Field | Value |
|---|---|
| Severity | Critical |
| Likelihood | Possible |
| Description | RR emitted before adapter call shows "completed" while TER shows failure, creating contradictory audit trail. |
| Mitigation | C-19 specifies decision-only RR stub, final RR post-execution. Test: assert RR.final_outcome matches TER.success. |
| Verification Hook | Test: `test_evidence_triangle_consistency` |

### SR-04: Adapter contract over-engineering (project R-001)
| Field | Value |
|---|---|
| Severity | High |
| Likelihood | Possible |
| Description | Agent adds speculative methods to AdapterContract (retry, caching, multi-provider) beyond the 3 required (execute, health, adapter_id). |
| Mitigation | Intent §3.4 (smallest viable interface). Code review: contract has exactly the specified surface area. |
| Verification Hook | Test: `test_adapter_contract_surface_area` |

### SR-05: Toy adapter scope creep
| Field | Value |
|---|---|
| Severity | Medium |
| Likelihood | Possible |
| Description | Toy adapter implements real business logic (pricing, settlement, market state management) instead of configurable stub responses. |
| Mitigation | Toy adapter uses constructor-configurable response dict. No business logic beyond echoing configured responses and error injection. |
| Verification Hook | Code review: adapter has no domain logic beyond response configuration |

### SR-06: Confirmation stub over-implementation
| Field | Value |
|---|---|
| Severity | Medium |
| Likelihood | Possible |
| Description | Agent implements UVS generation, TTL enforcement, or odds-drift detection in Sprint A instead of the minimal stub. |
| Mitigation | Intent §2 (Non-Goals) and C-16 explicitly exclude full confirmation lifecycle. Stub has exactly 3 fields: nonce, issued_at, pdr_record_id. |
| Verification Hook | Code review: confirmation handling has no crypto, no TTL, no drift detection |

### SR-07: Service auth confusion with player auth
| Field | Value |
|---|---|
| Severity | High |
| Likelihood | Possible |
| Description | Agent conflates service-level auth (Harmony → operator API) with player-level auth (user → operator), violating the two-layer model. |
| Mitigation | AUTH_MODEL.md §0 defines the two layers. ServiceConfig holds service credentials; auth_context holds player state. ToolExecutor checks player auth; adapter init checks service auth. |
| Verification Hook | Test: `test_tenant_isolation` verifies different ServiceConfig produces different results |

### SR-08: Secret leakage in TER
| Field | Value |
|---|---|
| Severity | Critical |
| Likelihood | Unlikely |
| Description | TER inadvertently includes API keys, session tokens, or raw credentials in tool_call or tool_result fields. |
| Mitigation | C-03 prohibits secrets in evidence. TER fields are secret-stripped before serialization. Fingerprints are computed on scrubbed data. |
| Verification Hook | Test: `test_no_secrets_in_ter` asserts TER does not contain token patterns |
