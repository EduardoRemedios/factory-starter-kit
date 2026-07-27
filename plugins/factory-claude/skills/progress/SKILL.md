---
name: progress
description: Report Factory run state, completed validators, blockers, and the next legal action from deterministic disk evidence.
---

# Factory Progress

Report the current Factory state from repository evidence.

Use the bundled read-only evaluator from the installed plugin root:
`python3 <plugin-root>/scripts/factory_plugin.py progress`.
Return its evidence-backed result without softening a blocked state.

## Workflow

1. Resolve the Git worktree root and identify the active Factory run, if any.
2. Read execution mode, stage handoffs, deterministic validator results, recall evidence, pack state, and human authorization evidence.
3. Apply documented evidence precedence and detect contradictions.
4. Report the stable state, completed gates, blockers, reason codes, and next legal action.
5. If no run exists, report readiness to initialize rather than inventing progress.

## Guardrails

- Do not create, edit, or delete repository files.
- A failed validator outranks a prose claim of success.
- Never infer human Go from planning completion.
