---
name: conductor-bmad-promote
description: Preview, create, reuse, or safely roll back an immutable reviewed BMAD evidence snapshot for Factory intake.
---

# Factory BMAD Promote

For a legacy discovery artifact, preview a selected file under `_bmad-output/`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . promote --source _bmad-output/path/file.md --snapshot-id SNAPSHOT_ID --workflow product-brief --reviewer "Name" --review-ref "record"
```

For an opt-in reviewed solution-context package, select one directory and bind
its evidence-only authority, policy contract, and human-reviewed plan identity:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py" --root . promote --source _bmad-output/path/package --snapshot-id SNAPSHOT_ID --workflow ux --evidence-type SOLUTION_CONTEXT --authority EVIDENCE_ONLY --plan-identity "review-record-plan-identity" --reviewer "Name" --review-ref "record"
```

Every regular file is copied into `content/` with its exact relative source
path, mode, and SHA-256 in schema v2. Empty directories, symlinks, traversal,
mutable aliases such as `latest`, and unknown or currently prohibited workflows
fail closed. The workflow allowlist is unchanged by this package type.

For exact-profile BMAD 6.10.0, `ux`, `architecture`, and `spec` are the only
solution-context workflow identifiers. Architecture and spec require this
schema-v2 package form; they cannot use legacy single-file discovery promotion.
The deprecated `create-architecture` shim remains prohibited.

When human review includes a material qualifier, add
`--review-qualifier "exact qualifier"`. The qualifier is plan-bound, stored in
the immutable snapshot manifest, and must be carried exactly into the Intent
Pack that cites the snapshot.

Apply only after exact approval with `--approve-plan <FULL_PLAN_ID>`. Cite the resulting snapshot ID and aggregate digest as an `upstream_snapshot` source in the Intent Pack, never the draft path. Use `rollback --receipt <path>` only when every created snapshot byte still matches the receipt.

When a new snapshot intentionally supersedes an older one, supply both
`--supersedes-snapshot-id <ID>` and `--supersedes-sha256 <DIGEST>`. The prior
snapshot remains immutable and independently citable; there is no floating
"current" snapshot.

`SOLUTION_CONTEXT` is authoring evidence, never implementation authority. Its
claims remain unaccepted until a human locks intent at G1, and even accepted
claims do not authorize execution. G1 locks intent; only a human `EXECUTION_GO`
countersign against that exact Intent Pack authorizes implementation.

Reject traversal, symlinks, stale inputs, downstream workflows, and existing different snapshots. Never edit a promoted snapshot.

For BMAD 6.10.0, promotion accepts only reviewed discovery or solution-context
workflow identifiers represented by the shared exact-name policy. In
particular, brownfield mining is `document-project`; `generate-project-context`,
the deprecated architecture shim, stories, sprint, implementation, QA
automation, review, TEA gates, and unknown workflows remain prohibited.
