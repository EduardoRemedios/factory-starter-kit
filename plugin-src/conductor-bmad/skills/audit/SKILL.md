---
name: audit
description: Audit BMAD modules, versions, commands, skills, agents, hooks, configuration, policy coverage, and brownfield evidence. Use when both systems are present, before intake or promotion, or when loop, TEA, unsupported versions, or legacy downstream artifacts could confuse governance.
---

# Factory BMAD Audit

Run read-only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . audit --harness claude
```

Report the supported installation version, every bounded repository-owned BMAD
capability class, coverage digest, missing/unrecognized capabilities, and the
non-destructive brownfield reconciliation summary. The summary includes the
canonical-layout verdict, any fixed legacy-archive inventory, and a zero-write
remediation preview for nested installations. The preview records source and
target paths, hashes, target collisions, and link impacts; it never relocates,
deletes, rewrites, chmods, or symlinks adopter content. Exactly one active installation root: `_bmad` at the repository root, or the
directory declared in `docs/Conductor/PROJECT_CONFIG.json` under
`adapters.bmad.declared_root`. Nested, canonical-plus-nested, ambiguous,
partial, and active-root-symlink layouts block intake, promotion, and
solution-context authoring; discovery and helpers continue with a layout warning. Preserved
legacy evidence belongs only beneath
`docs/adapters/bmad/legacy-evidence/`, outside the current Factory context-index
patterns; promoted snapshots remain beneath `docs/upstream/bmad/`.

`bmad-loop` blocks
Factory-bound intake. Supported TEA 1.21.1 design-level workflows (test design, NFR, trace, test
review) are evidence-only and allowed; TEA automation, CI, ATDD, and framework
workflows are delivery lane and denied. Do not uninstall, upgrade, downgrade, or rewrite configuration.

For the same deterministic verdict in CI, run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . policy-lint --harness claude
```

The bundled Claude hooks independently enforce both direct slash-command and
model-initiated `Skill` invocation paths. Audit proves policy coverage; it does
not claim to prevent an intentional user from disabling local plugin controls.
