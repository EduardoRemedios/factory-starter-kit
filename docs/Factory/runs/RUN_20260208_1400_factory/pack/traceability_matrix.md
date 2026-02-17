# traceability_matrix.md — Sprint A Traceability Matrix

## Version
v1

## Change Log
- v1 (2026-02-08): Initial traceability matrix for Sprint A.

| Constraint ID | Severity | Statement (short) | Source | Scope Tag | Verification (fixture/test/check) | Artifact Path |
|---|---|---|---|---|---|---|
| C-01 | Critical | All 43 existing tests pass unchanged | [SOURCE:RAW] | OK | VP-01: run existing test suite | tests/test_sprint_0*.py |
| C-02 | Critical | Adapter failures → deny + TER with error_code | [SOURCE:RAW] | OK | VP-02, VP-03, VP-04: adapter error fixtures + inline tests | fixtures/policy/adapter_unavailable/ |
| C-03 | Critical | No secrets in TER | [SOURCE:RAW] | OK | VP-05: assert no token patterns in TER | tests/test_sprint_A.py |
| C-04 | Critical | Engine does NOT call adapters directly | [SOURCE:RAW] | OK | VP-06: static analysis of policy_engine.py imports | runtime/policy_engine.py |
| C-05 | Critical | require_confirmation → no adapter call, no TER | [SOURCE:RAW] | OK | VP-07: confirm_no_execute fixture | fixtures/policy/confirm_no_execute/ |
| C-06 | Critical | Evidence triangle wired: PDR → TER → RR linkage | [SOURCE:RAW] | OK | VP-08: evidence_triangle fixture | fixtures/verification/evidence_triangle/ |
| C-07 | Critical | TER record_id is deterministic SHA-256 | [SOURCE:RAW] | OK | VP-08: verify record_id format | fixtures/verification/evidence_triangle/ |
| C-08 | Critical | Anonymous → execution denied AUTH_REQUIRED | [SOURCE:RAW] | OK | VP-09: auth_anonymous_deny fixture | fixtures/policy/auth_anonymous_deny/ |
| C-09 | Critical | System invariants not violated | [SOURCE:REF:docs/HARMONY_V2_SYSTEM_INVARIANTS.md] | OK | VP-06: engine purity check; structural review | runtime/policy_engine.py |
| C-10 | High | Tenant isolation: different config → different data | [SOURCE:RAW] | OK | VP-10: tenant_isolation fixture | fixtures/routing/tenant_isolation/ |
| C-11 | High | Idempotency: duplicate key → first result | [SOURCE:RAW] | OK | VP-11: idempotency fixture | fixtures/routing/idempotency/ |
| C-12 | High | action_type consistent across PDR, TER, RR | [SOURCE:RAW] | OK | VP-12 (part of VP-08) | fixtures/verification/evidence_triangle/ |
| C-13 | High | Fingerprints are SHA-256 of canonical data | [SOURCE:RAW] | OK | VP-13 (part of VP-08) | fixtures/verification/evidence_triangle/ |
| C-14 | High | No adapter mapped → deny + TER ADAPTER_NOT_MAPPED | [SOURCE:RAW] | OK | VP-14: adapter_not_mapped fixture | fixtures/routing/adapter_not_mapped/ |
| C-15 | Medium | Auth context follows AUTH_MODEL.md §3 shape | [SOURCE:REF:docs/AUTH_MODEL.md] | OK | Structural review | runtime/ |
| C-16 | Medium | Confirmation stub is minimal (3 fields) | [SOURCE:RAW] | OK | PC-04: manual check | runtime/ |
| C-17 | Medium | RR reason codes mapped from TER error_code | [SOURCE:RAW] | OK | VP-20: error injection integration test | tests/test_sprint_A.py |
| C-18 | Medium | handle_request() wraps engine + ToolExecutor | [SOURCE:RAW] | OK | VP-16, VP-18: integration tests | runtime/ |
| C-19 | Medium | RR: decision-only stub → final RR post-execution | [SOURCE:RAW] | OK | VP-08, VP-19: evidence checks | fixtures/verification/evidence_triangle/ |
| C-20 | Medium | duration_ms via monotonic clock, not policy input | [SOURCE:RAW] | OK | VP-08: verify duration_ms present | tests/test_sprint_A.py |
| C-21 | Medium | auth_context optional, defaults to anonymous | [SOURCE:RAW] | OK | VP-01: existing tests still pass without auth_context | tests/test_sprint_0*.py |
| C-22 | Medium | Exceptions for infra, ToolResult.error for business | [SOURCE:RAW] | OK | VP-02, VP-20: exception handling tests | tests/test_sprint_A.py |
