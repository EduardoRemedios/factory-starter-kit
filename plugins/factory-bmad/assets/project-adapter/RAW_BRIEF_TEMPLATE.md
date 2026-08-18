# Raw Brief — <initiative>

## Execution

- Execution Mode: `PLANNING_ONLY`
- Downstream Fan-Out: `NOT_APPROVED`

## Problem and outcome

Describe the problem, users, intended outcome, and why it matters.

## Scope and constraints

State in-scope behavior, explicit non-goals, constraints, risks, dependencies, success measures, and unresolved questions.

## BMAD upstream evidence

- BMAD Snapshot ID: `<SNAPSHOT_ID>`
- BMAD Snapshot SHA-256: `<64-lowercase-hex>`
- If the snapshot manifest contains a review qualifier, copy it exactly as `BMAD Review Qualifier` in this section.
- BMAD Authority: `EVIDENCE_ONLY`
- BMAD Context Freeze: `Brief Purple PASS`

## Embedded intake checklist

- [ ] Snapshot path is `docs/upstream/bmad/<SNAPSHOT_ID>/`.
- [ ] Snapshot manifest and human review evidence exist.
- [ ] Snapshot aggregate digest matches this brief.
- [ ] No mutable BMAD draft is cited; only an immutable snapshot ID and aggregate digest are referenced.
- [ ] BMAD is evidence only; Factory owns architecture, decomposition, planning, verification governance, execution control, and closeout.
- [ ] `bmad-loop` is absent.
- [ ] TEA, if present, is optional Stage F evidence and not a gate.
- [ ] Evidence is frozen at Brief Purple PASS.
