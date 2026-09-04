---
name: conductor-root-planner
description: Coordinate a Factory run from raw brief through Stage I2. Use when Codex is asked to initialize a Factory run, run Stage A, create or repair run-root evidence, enforce Factory read order, choose PLANNING_ONLY versus EXECUTION_ENABLED posture, coordinate the full stage flow, or prepare a pack for human review without executing implementation.
---

# Factory Root Planner

## Workflow

1. Read `AGENTS.md`, `docs/Conductor/ORCHESTRATION.md`, `docs/Conductor/Spec/STAGE_CONTRACTS.md`, and `docs/Conductor/SCRATCHPAD.md` `## Active Pitfalls (Mandatory)`.
2. Run `bash scripts/knowledge_lint.sh` before Stage A and persist output as `docs/Conductor/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`.
3. Create the run root and required files: `raw_brief.md`, `EXECUTION_MODE.txt`, `CONTEXT_RECALL_REPORT.md`, and later `SPRINT_ID.txt`.
4. If `docs/Conductor/PROJECT_PREFLIGHT.json` exists, run `./scripts/conductorctl project-preflight --run <RUN_ID>` after knowledge lint and before context recall; persist/pass `PROJECT_PREFLIGHT.txt` or halt.
5. Build recall evidence with `./scripts/conductorctl context-index` and `./scripts/conductorctl context-report --profile stage-a`.
6. Keep the run `PLANNING_ONLY` unless the raw brief explicitly authorizes `EXECUTION_ENABLED`.
7. Coordinate stages in order: `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`.
8. After each stage handoff, run `./scripts/conductorctl stage-lint --run <RUN_ID> --stage <STAGE>`.
9. After I2, run `./scripts/conductorctl pack-lint --run <RUN_ID>` before human review.

## Guardrails

- Do not execute sprint implementation during Factory planning.
- Do not expand scope silently; record proposed expansion as BLOCKING unless approved.
- Treat recall artifacts as evidence aids, not authority.
- If `Coverage Verdict: WEAK`, halt and repair recall before drafting intent.
- If any validator fails, fix the artifact or re-run the affected stage before advancing.

## Outputs

Return:
- run id
- execution mode
- evidence paths created
- current stage status
- validator results
- blockers requiring human decision
