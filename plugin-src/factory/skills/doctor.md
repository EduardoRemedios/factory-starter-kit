# Factory Doctor

Diagnose Factory without changing repository state.

Use the bundled read-only evaluator from the installed plugin root:
`python3 <plugin-root>/scripts/factory_plugin.py doctor --harness <claude-or-codex>`.
Return its evidence-backed result without softening a blocked state.

## Workflow

1. Resolve the Git worktree root from the current directory.
2. Inspect the installed plugin version, supported environment, Factory Core presence, and project compatibility evidence.
3. Apply deterministic evidence precedence: validator failures and contradictory disk evidence outrank optimistic prose.
4. Report the harness, plugin version, project compatibility, blockers, reason codes, and next legal action.
5. Before recommending a setup mode, inspect the worktree root. Recommend Greenfield only when it contains no entry other than `.git`; recommend Brownfield when any other entry exists.
6. If the environment or evidence cannot be verified, halt explicitly instead of guessing.

## Guardrails

- Do not create, edit, or delete repository files.
- Do not bypass Factory stage order, validators, or human Go.
- Keep `AGENTS.md` authoritative.
- Never describe a nonempty repository as suitable for Greenfield.
