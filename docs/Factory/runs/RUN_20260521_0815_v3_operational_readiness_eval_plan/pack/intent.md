# Intent - V3 Operational Readiness Eval Suite Plan

## Version
v1.1

## Change Log
- v1 (2026-05-21): Stage A initial intent contract.
- v1.1 (2026-05-21): Stage C hardened intent after red-team review.

## Purpose
Plan a Factory v2-governed sprint that defines the eval suite, golden fixtures, and pilot evidence needed before Factory v3 can be considered for optional operational use.

## Goal
Produce a reviewable planning pack for designing V3 operational-readiness evals. The pack must start from the V3 pre-mortem, preserve Factory v2 as supported fallback, and avoid promoting V3 during this run.

## Non-goals
- Do not implement eval code.
- Do not wire V3 checks into `factoryctl`, `knowledge_lint.sh`, `stage-lint`, `pack-lint`, mission lint, merge preflight, or CI.
- Do not promote V3 out of research mode.
- Do not deprecate Factory v2.
- Do not introduce AEGIS dependency or runtime-kernel behavior.

## Principles
- Use Factory v2 as the governing process for all V3 promotion work.
- Convert pre-mortem failures into eval families, fixtures, and pilot evidence requirements.
- Preserve each V2 safety guarantee before allowing any V3 ceremony collapse.
- Treat V3 as optional and bounded until explicit future human approval.
- Prefer deterministic fixtures and reviewable reports over narrative confidence.

## Roles
- Root Planner: coordinates this Factory v2 run.
- Red Team: attacks intent, envelope, and eval sufficiency.
- Blue Team: hardens scope and resolves findings.
- Purple Gate: decides pass, conditional pass, or fail on evidence.
- Verification Specialist: defines eval families, fixture inventory, and traceability.

## Acceptance Criteria
- AC-01: The pack defines a pre-mortem-first eval-suite design path for V3 operational readiness.
- AC-02: The pack includes golden fixture candidates with expected pass or fail outcomes.
- AC-03: The pack maps Critical and High constraints to verification tiers and evidence paths.
- AC-04: The pack includes explicit red-team, blue-team, and purple-team review steps.
- AC-05: The pack states V3 remains research-only and V2 remains supported until a later promotion decision.

## Scope
### In Scope
- Planning artifacts for a future V3 operational-readiness eval suite.
- Pre-mortem failure modes and eval families.
- Golden fixture inventory and expected result shape.
- Pilot evidence templates and decision report requirements.
- Red/Blue/Purple review gates for the eval-suite design.

### Out of Scope
- Eval implementation.
- New required validators.
- V3 operational promotion.
- Runtime governance or AEGIS kernel integration.
- Changes to Factory v2 operating contracts.

### Domain Areas
- Factory v3 operational-readiness eval planning
- Factory v2 governance preservation
- Mission-envelope evaluation
- V2 fallback and non-deprecation
- AEGIS boundary review

## Constraints
- C-01 (Critical): V3 must remain research-only in this run.
- C-02 (Critical): V2 must remain supported and explicitly available as fallback.
- C-03 (Critical): Every proposed V3 ceremony collapse must preserve the equivalent V2 guarantee.
- C-04 (High): Eval design must start from the pre-mortem and map failure modes to fixtures or pilots.
- C-05 (High): Golden fixtures must include negative cases, not only clean-pass examples.
- C-06 (High): AEGIS and runtime-kernel boundaries must remain intact.
- C-07 (High): SIMPLE-CODE-GATE v2 must be represented in eval planning for code-changing V3 work.

## Go or No-Go Rule
Go for human review only if the final pack passes `stage-lint` for all stages and `pack-lint`, and the Purple audit records PASS or CONDITIONAL PASS with no unapproved scope expansion.

## Open Questions
### BLOCKING
- None

### NON-BLOCKING
- The exact future implementation language for the eval runner is deferred to a later execution-enabled run.
