---
name: progress
description: Report Factory run state, completed validators, blockers, and the next legal action from deterministic disk evidence.
---

# Conductor Progress

Report the current Conductor state from repository evidence.

Use the bundled read-only evaluator. In Claude Code, run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_plugin.py" progress`. In Codex,
resolve the package containing this `SKILL.md` and run its
`scripts/conductor_plugin.py` by absolute path with `progress`.
Return its evidence-backed result without softening a blocked state.

## Workflow

1. Resolve the Git worktree root and identify the active run, if any.
2. For a Conductor-layout run (`intent_pack.json` present) the evaluator calls the
   repository's `conductorctl contract-lint` for G1, G2, and G3 and reports the
   gate state: `WAITING_HUMAN_LOCK`, `WAITING_HUMAN_GO`, `EXECUTION_IN_PROGRESS`,
   `EXECUTION_COMPLETE_WAITING_STATEMENT`, `WAITING_HUMAN_COUNTERSIGN`,
   `REVIEW_READY`, `MERGE_READY`, or `BLOCKED` with the lint errors attached.
3. For a Factory-lineage run (no `intent_pack.json`) it reads stage handoffs,
   validator results, recall evidence, pack state, and human authorization
   evidence exactly as before, and validates any `EXECUTION_CLOSEOUT.json`
   through the canonical validator on every read.
4. Treat artifact absence as legacy behavior and any present-invalid artifact as
   a blocked contradiction; never fall back from invalid evidence.
5. Report the stable state, gate details, blockers, reason codes, and next legal action.
6. If no run exists, report readiness to initialize rather than inventing progress.

## Guardrails

- Do not create, edit, or delete repository files.
- A failed validator outranks a prose claim of success.
- Never infer a human countersign or Go from planning completion.
- A tampered or agent-authored receipt is a blocker, not a warning.
