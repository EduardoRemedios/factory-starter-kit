# Intent - V3 Operational Profile And V2 Guarantee Matrix

## Version
v1

## Change Log
- v1 (2026-05-22): Stage A intent.

## Purpose
Define the first bounded optional V3 operational profile candidate and map Factory v2 guarantees to preserved V3 controls for that profile.

## Goal
Produce decision-prep evidence for C-05, C-06, and C-07 without promoting Factory v3 operationally.

## Non-goals
- Do not approve operational Factory v3 use.
- Do not deprecate Factory v2.
- Do not wire V3 evals into gates.
- Do not change validators, matchers, or scripts.
- Do not claim runtime-kernel authority.

## Principles
- Factory v2 remains authoritative until a release decision explicitly promotes a V3 profile.
- The first profile must be narrow enough to reason about.
- V2 fallback must be explicit and easy to trigger.
- The matrix must preserve guarantees, not merely rename V2 artifacts.

## Roles
- Root Planner: coordinate run evidence.
- Profile Author: draft `V3-OP-001`.
- Matrix Author: map V2 guarantees to profile controls.
- Red Team: check for over-broad scope and hidden promotion.
- Purple Gate: confirm checklist updates are evidence-backed.

## Acceptance Criteria
- A named profile exists under `docs/Factory/v3/`.
- The profile defines eligible work, excluded work, authority limits, verification expectations, evidence requirements, and V2 fallback triggers.
- A V2 guarantee preservation matrix exists for the named profile.
- C-05, C-06, and C-07 are updated only if evidence supports them.
- C-08, C-09, and C-10 remain open.
- Verification passes.

## Go Or No-Go Rule
GO only if the profile is bounded, V2 fallback remains explicit, V3 remains unpromoted, and the matrix has no unresolved critical profile-definition gaps.

## Open Questions
- NON-BLOCKING: Future operational-readiness decision work must decide whether `V3-OP-001` is actually promoted.
