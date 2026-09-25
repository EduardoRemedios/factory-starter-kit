# Explicit repository companions — local 0.3.7 candidate

This candidate extends the exact BMAD 6.12.1-next.0 Spec handoff. It is not a
published release, an installed-plugin update, BMAD 7 support, or project rollout.
Existing 6.10.0 and 6.12.1 output-only snapshots keep their formats and semantics.

A Spec sometimes declares an engineering standards file outside BMAD output.
Use a repeatable `--repo-companion` argument to permit that exact regular Markdown
file. The declared `companions:` closure must actually reach it; unused entries,
directories, globs, hidden paths, symlinks, escapes and ambiguous references fail.
Only the explicit companion graph is followed, never a scan of repository docs.

For example, a Spec at `bmad/_bmad-output/specs/header/SPEC.md` can declare
`../../../../docs/engineering-standards.md`. With the nested root already declared,
preview from the project root using the reviewed companion package script:

```bash
"$FACTORY_PY" "$COMPANION" --root . --json promote \
  --source bmad/_bmad-output/specs/header/SPEC.md \
  --repo-companion docs/engineering-standards.md \
  --snapshot-id header-input-v1 --workflow spec \
  --evidence-type SOLUTION_CONTEXT --authority EVIDENCE_ONLY \
  --plan-identity header-review-v1 \
  --reviewer "Actual reviewer" --review-ref "Actual review record"
```

Resolve `FACTORY_PY` to the guarded Python wrapper and `COMPANION` to the reviewed
package's `scripts/conductor_bmad.py`. This command previews; it does not approve.
After reviewing every path, digest and mode, a human approves the full current
plan ID. Repeat the same command with `--approve-plan FULL_APPROVED_PLAN_ID`.

The new opt-in representation stores `source_root: "."` and a strict
`repository_companions` provenance object: `target_root`, `output_root`,
`selected_source` and sorted exact `paths`. All source paths are then repository
relative and copied under `content/`. The preview binds the resolved repository
root, permissions, selected paths, bytes and modes. Any change requires a new
preview. Project preflight rejects malformed permission/provenance combinations,
undeclared external artifacts and snapshot tampering. This root-bound form must
be re-promoted/reviewed if moved to another checkout; do not edit its manifest.
Frozen snapshots do not follow subsequent edits to working source documents.

The lifecycle remains:

1. PM/BA reviews the BMAD Spec and companions; SA checks technical constraints.
2. A human approves promotion of the complete package. It remains evidence only.
3. Factory drafts the delivery intent, verification definitions and questions.
4. Product decisions return to BMAD's decision log and regenerated outputs. If
   inputs change, approve a new snapshot with the previous ID/digest in the
   supersession arguments; retain the old snapshot.
5. A human locks G1 and authorizes G2 against the resulting intent digest.
6. Execution produces runner receipts; fresh-context review and human G3 accept
   completion. Project PR review and merge authority remain separate.

An author's assertion in a Spec is not delivery approval. Neither a third-party
workflow nor a promoted snapshot can alter the locked intent or declare Factory
completion. Workflow classifications and hook/MCP permissions are unchanged by
this intake extension. Route qualification here uses actual MCP protocol and
hook subprocesses on synthetic inputs; it is not live model or desktop activation.
