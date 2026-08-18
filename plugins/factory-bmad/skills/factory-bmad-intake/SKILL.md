---
name: factory-bmad-intake
description: Preview or seed the Factory BMAD policy, embedded-checklist brief template, and fail-closed project preflight adapter.
---

# Factory BMAD Intake

Preview only:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" --root . intake --harness claude
```

Show every destination, action, digest, and plan ID. Apply only after exact
`--approve-plan` approval. Existing different policy, preflight, command,
template, or evidence files are conflicts requiring human reconciliation. The
seed includes the byte-identical shared policy module plus a point-in-time
capability audit and immutable brownfield reconciliation record. Project
preflight re-runs policy lint and fails on policy, coverage, citation, or
authority drift. This uses the existing Stage A preflight seam; it does not add
a Factory gate or grant execution.

Explain the handover contract when presenting the intake result: project
preflight validates `SNAPSHOT_MANIFEST.json` integrity and human review; Stage A
recall resolves the promoted `artifact.md`; only Factory intent after Purple
Gate PASS becomes authoritative. Never recommend the JSON manifest as a recall
required reference.
