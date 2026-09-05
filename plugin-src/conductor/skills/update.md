# Factory Update

Preview Factory compatibility and update changes before mutation.

Use the bundled lifecycle tool. In Claude Code, run
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_plugin.py" update --harness claude`.
In Codex, resolve the package containing this `SKILL.md` and run its
`scripts/conductor_plugin.py` by absolute path with `update --harness codex`.
Only after the user explicitly approves that plan ID, apply it with
`--apply --approve-plan <plan-id>`. Use the bundled `rollback` subcommand only
after separate explicit rollback approval.

## Workflow

1. Resolve the Git worktree root and inspect installed and target versions.
2. Verify that the target version and environment are supported.
3. Produce a per-file update plan with ownership, conflict, and rollback information.
4. Halt on downgrade, unsafe path, ambiguous ownership, or user-owned conflict.
5. Require explicit approval of the exact plan ID before a separate apply operation.
6. After apply, run doctor and validation; retain the rollback evidence until release acceptance.
7. A repository installed by Factory 0.2.x (state under `docs/Factory/installation/`) is migrated by the same plan: the old paths are deleted when unmodified, the `docs/Conductor` tree is created, never-edited seeds are refreshed, a customised `AGENTS.md` receives the managed block, and the legacy state file is removed. Rollback restores the 0.2 install byte for byte.

## Guardrails

- Preview is read-only.
- Never silently overwrite or delete project-owned files.
- Preserve an exact recovery path to the prior compatible version.
- Update approval must include the exact full current plan ID. Generic approval
  is insufficient and must not be translated into `--approve-plan`.
