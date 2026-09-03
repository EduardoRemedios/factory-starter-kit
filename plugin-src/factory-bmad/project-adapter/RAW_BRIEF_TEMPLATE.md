# Raw Brief — <initiative>

## Execution

- Execution Mode: `PLANNING_ONLY`
- Downstream Fan-Out: `NOT_APPROVED`

## Problem and outcome

Describe the problem, users, intended outcome, and why it matters.

## Scope and constraints

State in-scope behavior, explicit non-goals, constraints, risks, dependencies, success measures, and unresolved questions.

## BMAD upstream evidence

- BMAD Evidence Type: `SOLUTION_CONTEXT`
- BMAD Snapshot ID: `<SNAPSHOT_ID>`
- BMAD Snapshot SHA-256: `<64-lowercase-hex>`
- BMAD Policy Version: `1.1.0`
- BMAD Promotion Plan ID: `<FULL_PROMOTION_PLAN_ID>`
- BMAD Solution Plan Identity: `<HUMAN_REVIEWED_PLAN_IDENTITY>`
- BMAD Claim Receipt: `PENDING_STAGE_A_D`
- If the snapshot manifest contains a review qualifier, copy it exactly as `BMAD Review Qualifier` in this section.
- BMAD Authority: `EVIDENCE_ONLY`
- BMAD Context Freeze: `Brief Purple PASS`

## Embedded intake checklist

- [ ] Snapshot path is `docs/upstream/bmad/<SNAPSHOT_ID>/`.
- [ ] Snapshot manifest and human review evidence exist.
- [ ] Snapshot aggregate digest matches this brief.
- [ ] Evidence type, policy version, cryptographic promotion plan ID, and human-reviewed solution plan identity exactly match the manifest.
- [ ] Claim receipt is `PENDING_STAGE_A_D` before Factory claim review, then replaced only by a hash-valid run-local receipt recording claim-level `ACCEPTED`, `REJECTED`, `MODIFIED`, `DEFERRED`, or `CONFLICT` outcomes.
- [ ] No mutable BMAD draft is cited; only an immutable snapshot ID and aggregate digest are referenced.
- [ ] BMAD solution context is evidence only; Factory independently hardens intent and scope and owns implementation planning, verification governance, execution authorization, and closeout.
- [ ] `bmad-loop` is absent.
- [ ] TEA, if present, is optional Stage F evidence and not a gate.
- [ ] Evidence is frozen at Brief Purple PASS.
