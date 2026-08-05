---
name: progress
description: Report Factory run state, completed validators, blockers, and the next legal action from deterministic disk evidence.
---

# Factory Progress

Report the current Factory state from repository evidence.

Use the bundled read-only evaluator. In Claude Code, run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_plugin.py" progress`. In Codex,
resolve the package containing this `SKILL.md` and run its
`scripts/factory_plugin.py` by absolute path with `progress`.
Return its evidence-backed result without softening a blocked state.

## Workflow

1. Resolve the Git worktree root and identify the active Factory run, if any.
2. Read execution mode, stage handoffs, deterministic validator results, recall evidence, pack state, and human authorization evidence.
3. After those checks, validate any run-root `EXECUTION_CLOSEOUT.json` through
   the canonical Core validator on every read.
4. Treat artifact absence as legacy behavior and any present-invalid artifact as
   a blocked contradiction; never fall back from invalid closeout evidence.
5. Report the stable state, completed gates, blockers, reason codes, and next legal action.
6. If no run exists, report readiness to initialize rather than inventing progress.

## Guardrails

- Do not create, edit, or delete repository files.
- A failed validator outranks a prose claim of success.
- Never infer human Go from planning completion.
- A valid closeout is derived evidence and grants no new authority.
