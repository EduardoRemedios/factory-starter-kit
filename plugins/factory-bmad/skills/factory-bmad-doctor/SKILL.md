---
name: factory-bmad-doctor
description: Diagnose the five Factory and BMAD adoption states and return exactly one safe next action without changing the repository.
---

# Factory BMAD Doctor

This is the single adoption front door after the user installs
`factory-bmad`. The compatible Factory plugin is an automatic dependency; do
not ask the user to install a second plugin.

Run the bundled evaluator read-only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" --root . doctor --harness claude
```

For Codex, resolve this plugin root and use `--harness codex`. Return the stable state, reason code, essential evidence, and exactly one next legal action.

## Guardrails

- Do not create, edit, install, delete, or initialize Git.
- Ignore only recognized harness metadata when deciding whether a new target is otherwise empty.
- Treat partial or contradictory state as blocked evidence.
- Keep Factory as the downstream authority.
- In a BMAD-only repository, Factory Brownfield preview/apply is the first
  mutation. The bundled BMAD guard becomes active as soon as Factory and BMAD
  coexist in the Git worktree.
- In an unrelated BMAD-only repository, report the Brownfield route but do not
  claim that Factory enforcement is active yet.
