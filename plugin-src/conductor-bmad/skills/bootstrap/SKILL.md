---
name: bootstrap
description: Preview or execute the pinned BMAD 6.10.0 Core+BMM Claude Code installer. Use only after Factory is present and Doctor routes to BMAD bootstrap.
---

# Factory BMAD Bootstrap

Preview first:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . bootstrap --harness claude
```

Show the exact target, command, module set, allowed write prefixes, and full plan ID. Apply only after the human quotes that exact plan ID using `--approve-plan <FULL_PLAN_ID>`.

## Guardrails

- Pin `bmad-method@6.10.0`, `bmm`, and `claude-code`; never add loop or TEA.
- Re-evaluate immediately before execution; stale plans halt.
- Audit post-state and retain a receipt. Never clean unexpected state automatically.
- A supported install contains the exact 46 Core+BMM Claude Code skills. Missing,
  unknown, or version-drifted capabilities quarantine intake instead of being
  silently repaired.

After a successful apply, tell the operator to close and open a fresh Claude
Code session before attempting an installed BMAD skill. The next action is to
run `/conductor-bmad:doctor` in that fresh session; do not imply that the current
session has reloaded plugin-installed skills.
