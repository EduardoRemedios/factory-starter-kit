# Intent - V3-G011 SIMPLE-CODE-GATE Severity Policy

## Version
v1

## Change Log
- v1 (2026-05-22): Stage A intent for cross-version SIMPLE-CODE-GATE severity policy.

## Purpose
Decide and document when V3-G011 SIMPLE-CODE-GATE findings are advisory versus blocker-class, while keeping the policy portable across ordinary Factory V2 and V3 adopting repos.

## Goal
Create a generic Factory-first severity policy that future operational V3 profile work can cite for checklist C-04.

## Non-goals
- Do not promote Factory v3.
- Do not deprecate Factory v2.
- Do not change eval runner severities or wire advisory checks into required gates.
- Do not make AEGIS a prerequisite for Factory V2 or V3.

## Principles
- Factory V2 remains authoritative until a specific V3 profile is promoted.
- SIMPLE-CODE-GATE applies to ordinary repos by default.
- AEGIS/runtime-kernel handling is an optional additional boundary rule.
- Operational code-changing work must not close with unresolved bloat, brittleness, dependency creep, hidden side effects, silent failures, or speculative abstraction.

## Roles
- Root Planner: coordinate Factory run evidence.
- Policy Author: draft cross-version severity policy.
- Red Team: check for V3-only or AEGIS-centric framing.
- Purple Gate: verify C-04 can be marked done without promoting V3.

## Acceptance Criteria
- A cross-version policy exists at `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`.
- Policy defines `BLOCKER`, `ADVISORY_HIGH`, and `NO_FINDING`.
- Policy states AEGIS/runtime-kernel handling is optional and additive.
- V3 checklist C-04 is marked DONE with evidence paths.
- Project state, roadmap, and changelogs are updated.
- Verification passes.

## Go Or No-Go Rule
GO only if the policy is generic Factory-first, preserves V2 support, keeps V3 research-only, and passes repository checks.

## Open Questions
- NON-BLOCKING: Future operational profile work must decide whether to encode this policy mechanically in profile-specific validators.
