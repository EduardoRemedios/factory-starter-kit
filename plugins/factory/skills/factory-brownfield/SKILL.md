---
name: factory-brownfield
description: Prepare a preview-only Factory adoption plan for an existing repository, preserving user-owned files and halting on conflicts.
---

# Factory Brownfield

Prepare a conflict-safe Factory adoption plan for an existing repository.

Use the bundled planner. In Claude Code, run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_plugin.py" --root "$PWD" brownfield --harness claude`.
In Codex, resolve the package containing this `SKILL.md` and run its
`scripts/factory_plugin.py` by absolute path with
`--root "$PWD" brownfield --harness codex`.
Return the exact per-file plan from `planned_files` and `change_plan`, plus the
halt reason. In preview, `mutations` is expected to be empty and must not be
used as the proposed change count. Only after the user explicitly
approves that plan ID, apply it with the same command and same `--root` plus
`--apply --approve-plan <plan-id>`.

## Workflow

1. Resolve and verify the Git worktree root.
2. Inventory existing project, Factory, instruction, and skill files without mutation.
3. Classify ownership and produce an exact per-file proposed change plan.
4. Preserve project-owned content and report actionable conflicts.
5. Present the plan for explicit approval.
6. Apply only when the user approves the exact current plan ID, then report the receipt and mutations.

## Guardrails

- Halt before writing when ownership is ambiguous or a conflict remains.
- Reject traversal, unsafe symlinks, and paths outside the worktree root.
- Keep existing repository-scoped skills intact.
- Approval must include the exact full current plan ID. Generic approval such as
  “approve”, “apply”, or “approve and apply” is insufficient and must not be
  translated into `--approve-plan`.
- Keep preview and apply bound to the same quoted target root. Never switch from
  an in-session preview to an implicit or different repository root.
