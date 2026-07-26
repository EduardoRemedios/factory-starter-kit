---
name: factory-greenfield
description: Prepare a preview-only Factory setup plan for a new repository, preserving human authorization and repository safety gates.
---

# Factory Greenfield

Prepare a Factory setup plan for a new repository.

Use the bundled planner from the installed plugin root:
`python3 <plugin-root>/scripts/factory_plugin.py greenfield --harness <claude-or-codex>`.
Return the exact per-file plan and halt reason. Only after the user explicitly
approves that plan ID, apply it with the same command plus
`--apply --approve-plan <plan-id>`.

## Workflow

1. Resolve and verify the Git worktree root.
2. Inspect the repository before proposing changes.
3. Produce a per-file plan limited to approved Factory and project-adapter paths.
4. Classify every planned file as release-owned, generated/pinned, or project-owned.
5. Present the plan for explicit approval.
6. Apply only when the user approves the exact current plan ID, then report the receipt and mutations.

## Guardrails

- Halt on unsafe paths, symlink escapes, conflicts, or an unverified environment.
- Never silently overwrite a user-owned file.
- Do not begin Factory execution or imply human Go.
- Approval must include the exact full current plan ID. Generic approval such as
  “approve”, “apply”, or “approve and apply” is insufficient and must not be
  translated into `--approve-plan`.
