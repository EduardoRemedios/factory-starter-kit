---
name: factory-greenfield
description: Prepare a preview-only Factory setup plan for a new repository, preserving human authorization and repository safety gates.
---

# Factory Greenfield

Prepare a Factory setup plan for a new repository.

Use the bundled planner. In Claude Code, run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_plugin.py" greenfield --harness claude`.
In Codex, resolve the package containing this `SKILL.md` and run its
`scripts/factory_plugin.py` by absolute path with `greenfield --harness codex`.
Return the exact per-file plan and halt reason. Only after the user explicitly
approves that plan ID, apply it with the same command plus
`--apply --approve-plan <plan-id>`.

## Workflow

1. Resolve and verify the Git worktree root.
2. Inspect the target before proposing changes; it may be an absent path, an empty
   directory, or an existing Git repository containing only `.git`.
3. Produce one ordered plan for root creation, Git initialization, payload,
   lifecycle metadata, receipt, and validation, limited to approved paths.
4. Classify every planned file as release-owned, generated/pinned, or project-owned.
5. Present the plan for explicit approval.
6. Apply only when the user approves the exact current plan ID, then report the receipt and mutations.

## Guardrails

- Halt on unsafe paths, symlink escapes, conflicts, or an unverified environment.
- Never silently overwrite a user-owned file.
- Do not begin Factory execution or imply human Go.
- Remove transaction-created `.git` during recovery only when its exact unchanged
  post-initialization digest proves Factory ownership.
- Approval must include the exact full current plan ID. Generic approval such as
  “approve”, “apply”, or “approve and apply” is insufficient and must not be
  translated into `--approve-plan`.
