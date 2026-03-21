# Product Owner Pre-Factory Process

## Version
v1.1

## Change Log
- v1.1 (2026-03-21): Added mandatory PO context-recall report generation before sprint brief drafting and review so prior Red Team rationale, descopes, and accepted trade-offs are auditable.
- v1.0 (2026-03-15): Generic starter-kit version of the pre-Factory Product Owner process. Applicable to any adopting repo that wants a governed phase-planning layer upstream of the Factory.

## 0. Purpose

This document describes the pre-Factory planning process that sits upstream of the Factory pipeline. It governs how a Product Owner (PO) agent translates a human-authored Phase Brief into individual sprint briefs that feed the Factory.

This process produces `raw_brief.md`, the same artifact that enters the Factory at Stage A. The Factory pipeline itself is unchanged. This process governs what happens before the Factory starts.

## 0.1 Relationship to the Factory Pipeline

```
Human sponsor writes Phase Brief
  ↓
Phase Intent Cycle (agent hardens -> Red -> Blue -> Purple, max 2 cycles)
  ↓
Locked Phase Intent
  ↓
PO writes Sprint Brief (within phase intent scope)
  ↓
Brief Review Cycle (Red -> Blue -> Purple, max 1 cycle)
  ↓
Brief PASS -> raw_brief.md enters Factory Pipeline (Stages A -> I2)
  ↓
Pack -> human Go or No-go -> Execution
  ↓
Sprint complete -> state docs updated
  ↓
PO writes next Sprint Brief (if budget remaining)
  ↓
Budget exhausted -> PO halts -> human sponsor writes next Phase Brief
```

## 0.2 Separation of Concerns (HARD)

The PO agent writes briefs. It does not orchestrate the Factory pipeline.

| Responsibility | Owner |
|---------------|-------|
| Phase Brief authorship | Human sponsor |
| Phase Intent hardening | Agent (Intent Contractor role) |
| Phase Intent review (Red/Blue/Purple) | Agents (review roles) |
| Sprint Brief authorship | PO agent |
| Sprint Brief review (Red/Blue/Purple) | Agents (review roles, separate from PO) |
| Factory Pipeline orchestration | Root Planner agent |
| Execution authorization (`EXECUTION_ENABLED`) | Human sponsor |
| Go or No-go on sprint packs | Human sponsor |

The PO must never mark a run as `EXECUTION_ENABLED`. The PO must never orchestrate Factory stages. These boundaries are non-negotiable.

## 1. Phase Intent Lock (done once per phase)

### 1.1 Human sponsor writes the Phase Brief

The human sponsor writes a Phase Brief using `templates/PHASE_BRIEF_TEMPLATE.md`. This is a rough strategic document. It describes the phase goal, approximate scope, hard constraints, and budget. It does not need to be contract-grade.

### 1.2 Agent hardens into Phase Intent

A fresh agent session receives the Phase Brief plus project context:
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/Factory/SCRATCHPAD.md` Active Pitfalls

The agent produces a Phase Intent document using `templates/PHASE_INTENT_TEMPLATE.md`.

### 1.3 Phase Intent Review Cycle

The Phase Intent goes through an adversarial review:

| Step | Role | What happens |
|------|------|-------------|
| Red Team | Attacks the Phase Intent for scope overreach, missing constraints, ambiguous boundaries, unrealistic budget, compliance gaps, and PO authority gaps |
| Blue Team | Hardens based on Red Team findings. No scope expansion beyond the Phase Brief |
| Purple Gate | Evaluates against `PHASE_INTENT_REVIEW_CHECKLIST.md`. PASS or FAIL |

- Max 2 Red/Blue cycles.
- If FAIL after 2 cycles: escalate to the human sponsor with specific findings.
- If PASS: the Phase Intent is locked.

### 1.4 Phase State Initialization

After the Phase Intent is locked, create a Phase State file using `templates/PHASE_STATE_TEMPLATE.md`.

Store at:
- `docs/Factory/ProductOwner/phases/<PHASE_ID>/PHASE_STATE.md`
- `docs/Factory/ProductOwner/phases/<PHASE_ID>/PHASE_INTENT.md`

## 2. Sprint Brief Cycle (repeats per sprint, within budget)

### 2.1 Budget check (HARD)

Before the PO writes a brief, check `PHASE_STATE.md`:
- if `sprints_consumed >= sprint_budget`: HALT and escalate
- if budget remains: proceed

### 2.2 PO writes Sprint Brief

Before the PO writes a sprint brief, generate a scoped recall artifact:
- Path: `docs/Factory/ProductOwner/phases/<PHASE_ID>/BRIEF_SPRINT_<N>_CONTEXT_RECALL_REPORT.md`
- Command:
  - `./scripts/factoryctl context-report --profile po-brief --scope <PHASE_ID> --output docs/Factory/ProductOwner/phases/<PHASE_ID>/BRIEF_SPRINT_<N>_CONTEXT_RECALL_REPORT.md`

Required focus terms and trace IDs should include:
- the target sprint ID if already assigned
- prior sprint IDs and prior run IDs the new brief explicitly builds on
- preserved candidate IDs, constraint IDs, risk IDs, or human-checkpoint IDs named in the phase ledger or prior outcomes

Add `--required-ref` for any exact upstream artifact path or exact identifier that must be recovered for the brief review to remain valid.

If explicit fallback scopes are not provided, `context-report` applies the PO default order automatically:
1. requested phase scope
2. `docs/Factory/ProductOwner/phases`
3. `docs/Factory/runs`
4. `docs`

If the written report still records `Coverage Verdict: WEAK`, halt the brief cycle and repair recall coverage before drafting or review.

The PO agent receives:
- the locked Phase Intent
- `docs/PROJECT_STATE.md`
- `docs/ROADMAP.md`
- `docs/Factory/SCRATCHPAD.md` Active Pitfalls
- `BRIEF_SPRINT_<N>_CONTEXT_RECALL_REPORT.md`
- previous sprint completion reports if any

The PO writes a sprint brief. The brief must:
- stay within the Phase Intent's scope boundaries
- reference the Phase Intent explicitly
- include: what to build, the problem, what exists today, scope, out of scope, hard constraints, acceptance criteria
- tag any requirement not traceable to the Phase Intent as `[PO_INFERRED]`
- tag any requirement outside the Phase Intent scope as `[SCOPE EXPANSION]` plus BLOCKING

### 2.3 Brief Review Cycle

The sprint brief goes through a lightweight adversarial review:

| Step | Role | What happens |
|------|------|-------------|
| Red Team | Attacks the brief for scope exceeding the Phase Intent, missing domain context, ambiguous requirements, vague acceptance criteria, stale assumptions, dropped rationale from earlier decisions, and compliance gaps |
| Blue Team | Hardens based on Red Team findings. No scope expansion beyond the Phase Intent |
| Purple Gate | Evaluates against `BRIEF_REVIEW_CHECKLIST.md`. PASS or FAIL |

- Max 1 Red/Blue cycle.
- If FAIL after 1 cycle: PO revises and resubmits once.
- If FAIL after retry: escalate to the human sponsor.
- If PASS: the brief becomes `raw_brief.md` and enters the Factory pipeline.

Purple must treat missing or stale recall evidence as a gate issue. If the brief materially relies on prior decisions but the brief-cycle recall report still records `Coverage Verdict: WEAK` or leaves required refs unresolved, Purple must halt adjudication until the recall artifact is repaired.

### 2.4 Handoff to Factory

When the brief passes the Brief Purple Gate:
1. the brief is saved as `raw_brief.md` in the Factory run directory
2. the Root Planner initializes and orchestrates the Factory run
3. the Factory pipeline proceeds as normal (`A -> I2`)
4. the human sponsor reviews the pack and decides Go or No-go

### 2.5 Sprint Completion

After a sprint completes with GO:
1. project state docs are updated per the existing change hygiene rules
2. `PHASE_STATE.md` is updated: increment `sprints_consumed`, add entry to the sprint log
3. if budget remains: the PO may write the next sprint brief
4. if budget is exhausted: HALT and escalate

## 3. Error Handling

### 3.1 Phase Intent FAIL
If the Phase Intent fails Purple after 2 cycles: HALT. The human sponsor reviews the findings and either revises the Phase Brief or adjusts the Phase Intent directly.

### 3.2 Sprint Brief FAIL
If a sprint brief fails Purple after 1 cycle plus 1 retry: HALT. The human sponsor reviews. Options:
- provide feedback to the PO for another attempt
- write the brief directly
- adjust the Phase Intent if the failure reveals a strategic gap

### 3.3 Budget exhaustion
When `sprints_consumed >= sprint_budget`, the PO halts and reports:
- what was accomplished
- what remains unresolved in the phase scope
- whether a new Phase Brief is required

### 3.4 PO authority violation
If the PO attempts to orchestrate the Factory, mark a run as `EXECUTION_ENABLED`, modify Factory specs/templates/SCRATCHPAD, or exceed the sprint budget:
- HALT immediately
- record the violation
- escalate to the human sponsor

## 4. Known Limitations

1. The PO is an AI agent. Its domain knowledge comes from context and training data, not years of operator experience.
2. The brief review cycle adds overhead. Whether that overhead is worth it depends on the quality of the briefs.
3. The budget should start conservatively until the process proves it adds value.
4. The PO and Red Team may share blind spots. Human review gates still matter.

## 5. File Locations

| Item | Path |
|------|------|
| This process guide | `docs/Factory/ProductOwner/PO_PROCESS.md` |
| PO role definition | `docs/Factory/ProductOwner/PO_ROLE_DEFINITION.md` |
| Phase Brief template | `docs/Factory/ProductOwner/templates/PHASE_BRIEF_TEMPLATE.md` |
| Phase Intent template | `docs/Factory/ProductOwner/templates/PHASE_INTENT_TEMPLATE.md` |
| Phase Intent Review Checklist | `docs/Factory/ProductOwner/PHASE_INTENT_REVIEW_CHECKLIST.md` |
| Brief Review Checklist | `docs/Factory/ProductOwner/BRIEF_REVIEW_CHECKLIST.md` |
| Phase State template | `docs/Factory/ProductOwner/templates/PHASE_STATE_TEMPLATE.md` |
| Phase artifacts | `docs/Factory/ProductOwner/phases/<PHASE_ID>/` |
| Context recall report template | `docs/Factory/templates/CONTEXT_RECALL_REPORT_TEMPLATE.md` |
