---
name: audit
description: Audit BMAD modules, versions, commands, skills, agents, hooks, configuration, policy coverage, and brownfield evidence. Use when both systems are present, before intake or promotion, or when loop, TEA, unsupported versions, or legacy downstream artifacts could confuse governance.
---

# Factory BMAD Audit

Run read-only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" --root . audit --harness claude
```

Report the supported installation version, every bounded repository-owned BMAD
capability class, coverage digest, missing/unrecognized capabilities, and the
non-destructive brownfield reconciliation summary. The summary includes the
canonical-layout verdict, any fixed legacy-archive inventory, and a zero-write
remediation preview for nested installations. The preview records source and
target paths, hashes, target collisions, and link impacts; it never relocates,
deletes, rewrites, chmods, or symlinks adopter content. `_bmad` at repository
root is the only active installation root. Nested, canonical-plus-nested,
ambiguous, partial, and active-root-symlink layouts fail closed. Preserved
legacy evidence belongs only beneath
`docs/adapters/bmad/legacy-evidence/`, outside the current Factory context-index
patterns; promoted snapshots remain beneath `docs/upstream/bmad/`.

`bmad-loop` blocks
Factory-bound intake. Supported TEA 1.21.1 is classified as optional Stage F
evidence only and its skills remain unavailable through the default upstream
allowlist. Do not uninstall, upgrade, downgrade, or rewrite configuration.

For the same deterministic verdict in CI, run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" --root . policy-lint --harness claude
```

The bundled Claude hooks independently enforce both direct slash-command and
model-initiated `Skill` invocation paths. Audit proves policy coverage; it does
not claim to prevent an intentional user from disabling local plugin controls.
