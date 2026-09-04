---
name: doctor
description: Diagnose a repository's combined Factory and BMAD adoption state. Use before setup, migration, or intake when the safe next action depends on whether Factory, BMAD, both, or neither are present.
---

# Factory BMAD Doctor

This is the single adoption front door after the user installs
`conductor-bmad`. The compatible Factory plugin is an automatic dependency; do
not ask the user to install a second plugin.

Run the bundled evaluator read-only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . doctor --harness claude
```

For Codex, resolve this plugin root and use `--harness codex`. Return the stable state, reason code, essential evidence, and exactly one next legal action.

## Guardrails

- Do not create, edit, install, delete, or initialize Git.
- Ignore only recognized harness metadata when deciding whether a new target is otherwise empty.
- Treat partial or contradictory state as blocked evidence.
- Keep Factory as the downstream authority.
- In a repository whose starting state is BMAD present and Factory absent,
  Factory Brownfield preview/apply is the first mutation. This is an adoption
  source state only, not an approved BMAD-without-Factory operating mode.
- The bundled BMAD guard becomes active as soon as Factory and BMAD coexist in
  the Git worktree. Until then, report the Brownfield route but do not claim
  that Factory enforcement is active yet.
