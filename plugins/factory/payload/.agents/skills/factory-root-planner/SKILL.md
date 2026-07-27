---
name: factory-root-planner
description: Coordinate a Factory run from raw brief through Stage I2. Use when Codex is asked to initialize a Factory run, run Stage A, create or repair run-root evidence, enforce Factory read order, choose PLANNING_ONLY versus EXECUTION_ENABLED posture, coordinate the full stage flow, or prepare a pack for human review without executing implementation.
---

# Factory Root Planner

## Workflow

1. Read `AGENTS.md`, `docs/Factory/ORCHESTRATION.md`, `docs/Factory/Spec/STAGE_CONTRACTS.md`, and `docs/Factory/SCRATCHPAD.md` `## Active Pitfalls (Mandatory)`.
2. Run `bash scripts/knowledge_lint.sh` before Stage A and persist output as `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`.
3. Create the run root and required files: `raw_brief.md`, `EXECUTION_MODE.txt`, `CONTEXT_RECALL_REPORT.md`, and later `SPRINT_ID.txt`.
4. Build recall evidence with `./scripts/factoryctl context-index` and `./scripts/factoryctl context-report --profile stage-a`.
5. Keep the run `PLANNING_ONLY` unless the raw brief explicitly authorizes `EXECUTION_ENABLED`.
6. Coordinate stages in order: `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`.
7. After each stage handoff, run `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>`.
8. After I2, run `./scripts/factoryctl pack-lint --run <RUN_ID>` before human review.

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
