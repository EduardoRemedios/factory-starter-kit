---
name: promote
description: Promote selected reviewed BMAD draft output into an immutable product-level Factory evidence snapshot. Use after human review and before drafting a Factory raw brief.
---

# Factory BMAD Promote

Preview a selected source under `_bmad-output/`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" --root . promote --source _bmad-output/path/file.md --snapshot-id SNAPSHOT_ID --workflow product-brief --reviewer "Name" --review-ref "record"
```

When human review includes a material qualifier, add
`--review-qualifier "exact qualifier"`. The qualifier is plan-bound, stored in
the immutable snapshot manifest, and must be copied exactly into the Factory
raw brief.

Apply only after exact approval with `--approve-plan <FULL_PLAN_ID>`. Cite the resulting snapshot ID and aggregate digest in the raw brief, never the draft path. Use `rollback --receipt <path>` only when every created snapshot byte still matches the receipt.

Reject traversal, symlinks, stale inputs, downstream workflows, and existing different snapshots. Never edit a promoted snapshot.

For BMAD 6.10.0, promotion accepts only reviewed upstream workflow identifiers
represented by the shared allowlist. In particular, brownfield mining is
`document-project`; `generate-project-context`, architecture, stories, sprint,
implementation, QA automation, and review workflows remain non-binding and are
not promotable through this command.
