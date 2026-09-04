# Raw Brief — MS-06 Disposable Live Qualification of the 0.2.5 Solution-Context Candidate

## Brief Review

- Drafted 2026-09-03 by the operator session; the human operator reviewed the draft and approved it the same day ("agree, proceed"). Brief Review: PASS.

## Authorization Boundary

- This brief authorizes planning artifacts only. It does not authorize implementation, disposable-repository creation, BMAD workflow invocation, AuditEdge access, Git commit/merge/push, publication, pilot, release, or rollout. Execution requires a later exact, digest-bound human activation per micro-sprint.

## Context

- `RUN_20260902_0725_factory_bmad_025_solution_context_integration` deterministically qualified the integrated Factory-BMAD 0.2.5 solution-context candidate: canonical execution closeout `REVIEW_READY`, human evidence review accepted 2026-09-03, status `FACTORY_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`.
- The qualified candidate is committed at `c23be98` on `codex/factory-bmad-0.2.5-solution-context` in this repository; deterministic proof used fixtures and the full discovery suite only.
- Deterministic proof does not replace disposable live proof: no actual BMAD 6.10.0 workflow has been invoked against the integrated candidate, so the live authoring boundary, live denial behavior, and live promotion mechanics remain unproven.

## Objective

In a disposable repository created and destroyed inside the run, prove live that the qualified candidate:

1. Permits exactly the BMAD 6.10.0 architecture, UX, and spec authoring workflows, each producing non-binding `EVIDENCE_ONLY` `SOLUTION_CONTEXT` output.
2. Denies prohibited, unknown, malformed, and unsafe-layout workflow paths before causal sentinels through both hook paths, live.
3. Supports one human-reviewed promotion of a hash-pinned solution-context snapshot with explicit claim dispositions.
4. Leaves the disposable repository's Factory authority chain untouched: no implementation, sprint execution, code review authority, unattended development, quick-dev, or bmad-loop occurs.

## Constraints

- The qualified candidate's bytes are consumed, never modified; donors, existing worktrees, registrations, and Factory Core remain no-touch.
- The disposable repository lives outside this repository, is pinned at activation, and is destroyed before closeout; its destruction is evidenced.
- Evidence is bounded and external per the established evidence-root pattern, with bounded in-repo closeout evidence for the canonical closeout.
- A verification manifest is mandatory at Stage F because runnable VM checks exist.
- Completion grants no merge, publication, pilot, release, or rollout authority.

## Acceptance Ceiling

- Maximum claim on full success: `FACTORY_BMAD_025_MS06_DISPOSABLE_LIVE_QUALIFIED`.

## Out of Scope

- AuditEdge access or preview, customer or team rollout, plugin marketplace publication, merge of the candidate branch, and any change to the qualified candidate, Factory Core, or this repository's source and tests.
