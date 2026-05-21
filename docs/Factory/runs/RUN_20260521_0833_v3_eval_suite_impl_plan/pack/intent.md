# Intent - V3 Eval Suite Implementation Plan

## Version
v1

## Change Log
- v1 (2026-05-21): Stage A intent for standalone V3 operational-readiness eval-suite implementation plan.

## Purpose
Plan an execution-enabled implementation sprint for the first standalone advisory V3 operational-readiness eval suite.

## Goal
Implement a small, local, non-blocking eval runner and golden fixtures that test whether V3 operational-readiness artifacts preserve V2 guarantees before any optional V3 operational promotion.

## Non-goals
- Do not promote V3 operationally.
- Do not deprecate V2.
- Do not wire the eval runner into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, merge preflight, or CI.
- Do not introduce external dependencies.
- Do not implement runtime-kernel authority, AEGIS proof, or production action mediation.

## Principles
- Use the standard library and existing repo patterns.
- Keep the runner standalone and advisory.
- Prefer explicit fixture checks over generic framework abstractions.
- Preserve V2 fallback and non-deprecation checks.
- Apply SIMPLE-CODE-GATE v2 to all code-changing work.

## Roles
- Planner: prepares implementation contract.
- Implementer: adds the runner and fixtures in a later execution step.
- Red Team: attacks scope, authority, verification, and bloat risk.
- Purple Gate: audits readiness before execution.

## Acceptance Criteria
- AC-01: Plan names exact target files for the first implementation.
- AC-02: Plan defines fixture coverage for V3-G001 through V3-G014.
- AC-03: Plan defines expected JSON output and report template behavior.
- AC-04: Plan defines verification commands for runner fixtures and existing Factory checks.
- AC-05: Plan keeps runner advisory and outside required gates.

## Scope
### In Scope
- `scripts/factory_v3_operational_readiness_eval.py`
- `tests/fixtures/factory_v3_operational_readiness_eval/`
- `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_TEMPLATE.md`
- documentation links from V3 research docs if needed

### Out of Scope
- Required-gate integration.
- CI integration.
- Operational V3 release.
- AEGIS dependency.

### Domain Areas
- V3 operational-readiness eval runner
- Golden fixture contracts
- Advisory report shape
- V2 fallback preservation

## Constraints
- C-01 (Critical): Runner remains standalone and advisory.
- C-02 (Critical): V3 remains research-only after implementation.
- C-03 (Critical): V2 remains supported and non-deprecated.
- C-04 (High): Implementation uses no new dependencies.
- C-05 (High): Fixtures cover all V3-G001 through V3-G014 cases.
- C-06 (High): Output includes false-positive and false-negative review fields.
- C-07 (High): SIMPLE-CODE-GATE v2 blocks speculative abstraction and dependency creep.

## Go or No-Go Rule
Go for execution only after this pack passes Stage I2, `pack-lint`, and a separate human GO for this implementation pack.

## Open Questions
### BLOCKING
- None

### NON-BLOCKING
- Future promotion thresholds remain deferred until real pilot evidence exists.
