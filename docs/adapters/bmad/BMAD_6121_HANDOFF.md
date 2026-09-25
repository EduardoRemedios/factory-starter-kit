# From a BMAD Spec to a Factory delivery

This describes the local **0.3.6 candidate**, supporting exact BMAD **6.12.1-next.0** alongside **6.10.0**. Publication, installation and live harness qualification are separate. The existing bootstrap command still installs 6.10.0; it does not upgrade a team's BMAD installation.

Use a small example: a failed logout currently leaves the user without a useful message. The intended slice is to show a clear retry message while keeping the existing session. This is an illustrative product decision, not an approved customer requirement.

## 1. Select and check the input

The PM chooses the slice. The BA records expected behaviour and open questions; the architect identifies constraints. They use BMAD's Spec workflow to generate `SPEC.md` and its companions. In 6.12.1, the append-only `.memlog.md` records decisions; BMAD derives the Spec from it. Do not patch the derived Spec directly.

The developer opens the Factory-enabled repository. First check the actual installed candidate identity. Set `COMPANION` to the **reviewed installed package's** `scripts/conductor_bmad.py`, not an arbitrary downloaded script. Run from the repository root:

```bash
./scripts/conductor-python "$COMPANION" --root . --json doctor --harness claude
./scripts/conductor-python "$COMPANION" --root . --json audit --harness claude
```

For Codex, use `--harness codex --route guarded-mcp` on audit. Every BMAD workflow load must then use the exposed `load_workflow` MCP tool, including nested helpers. An audit cannot prove the desktop loaded that tool.

For a nested BMAD install, `PROJECT_CONFIG.json` declares `adapters.bmad.declared_root`, for example `bmad/_bmad`, with the adapter schema present. Its output root is then `bmad/_bmad-output`, and skill root `bmad/.claude/skills`. A root `.claude/skills` symlink is accepted only if it points to that exact internal skill tree. No relocation is required.

The audit checks complete public-source dependencies, including references and support scripts. Missing reference files, altered scripts, unknown versions and unreviewed effective overrides block the applicable route. A generic `references/` Git ignore can leave a clone incomplete even when every skill entry file is present. Restore missing dependencies from the pinned upstream release under normal project approval; do not suppress the check.

For initial adapter intake, preview `intake --harness claude` and `seed-contracts`; review each exact plan before repeating with `--approve-plan FULL_PLAN_ID`. Conflicts need a reviewed project update, never overwriting team files.

## 2. Review and freeze the selected package

The PM/BA review the selected Spec and companions. The architect reviews relevant architecture constraints. Ask the agent to show the complete file list and hashes before approval:

```bash
./scripts/conductor-python "$COMPANION" --root . --json promote \
  --source bmad/_bmad-output/specs/session-error/SPEC.md \
  --snapshot-id session-error-v1 --workflow spec \
  --evidence-type SOLUTION_CONTEXT --authority EVIDENCE_ONLY \
  --plan-identity session-error-review-1 --reviewer "Reviewer name" \
  --review-ref "review record"
```

Repeat the identical command with `--approve-plan FULL_PLAN_ID` only after the human approves that exact current plan. No approval is implied by a preview.

For this version, selecting `SPEC.md` or its containing directory packages the Spec, its decision log when present, and the recursive declared companion closure. It does not copy the entire output corpus. Companion paths may be Spec-relative or BMAD-project-relative, but must resolve unambiguously to regular files beneath the declared output root. Both block lists and plain/quoted flow lists are accepted; unsupported declarations fail explicitly. Missing, ambiguous or unsafe links block promotion. The snapshot preserves output-relative paths under `content/`, with each original path, mode and digest in its manifest.

The working BMAD files remain editable upstream context. The promoted snapshot is immutable evidence. Neither grants implementation authority.

## 3. Harden, ask questions and reconcile

Ask Factory to draft the delivery intent from that snapshot: selected requirements, constraints, exclusions, verification checks and unresolved questions. Record how each relevant claim was accepted, modified, deferred or rejected. The adapter's claim-disposition record and raw-brief template provide the executable handoff; the project preflight checks their snapshot identities and integrity.

For example, Factory may ask whether a failed logout should keep the menu open or close it and show a message. The BA takes the question to the product owner; the architect checks whether the answer changes a technical constraint. The answer goes back through BMAD: append the decision to the memlog, then ask `bmad-spec` to regenerate and validate the Spec and companions. Do not silently change locked Factory requirements.

Preview and approve a **new** snapshot, using `--supersedes-snapshot-id session-error-v1 --supersedes-sha256 PRIOR_AGGREGATE_SHA256`. The original remains intact. Revise the Factory intent to cite the new manifest's **file SHA-256**; this differs from the snapshot's aggregate digest used by promotion and supersession.

Before approval, run:

```bash
./scripts/conductorctl project-preflight --run RUN_ID
./scripts/conductorctl contract-lint intent --run RUN_ID
```

A question found after execution begins becomes a Gap Request through `conductorctl gap open`. A resolution that changes active scope requires renewed G1/G2 approval against the changed intent; an old approval does not carry forward. Retain the old gap, snapshot and approval history.

## 4. Approve and implement

The human reviews Factory's intent and checks, then approves **G1 Intent Lock and G2 Execution Go against the exact intent digest**. Those approvals are recorded in the run countersigns. The developer then implements within that approved scope through Factory.

Freeze check definitions separately from the runner-owned verification manifest: the runner adds results to the manifest. Do not hash-pin that mutable results file as an immutable input.

```bash
./scripts/conductorctl postimage capture --run RUN_ID
./scripts/conductorctl receipts run --run RUN_ID
./scripts/conductorctl postimage compare --run RUN_ID
./scripts/conductorctl contract-lint execution --run RUN_ID --require-complete
```

Capture comes before implementation; checks and comparison follow it. The project's own build/tests belong in the reviewed manifest. Starter Kit unit tests cannot verify a customer's product.

## 5. Review and complete

A fresh reviewer checks the delivered change, runner receipts and preserved boundaries. Factory drafts the completion statement and runs:

```bash
./scripts/conductorctl contract-lint completion --run RUN_ID
```

The human approves G3 against the completion statement's exact digest. Revalidation may produce `REVIEW_READY`; merge/release authority remains separate. A BMAD review can contribute advisory findings, but cannot replace this independent Factory review or countersign.

## What the controls do

The project rule is that Factory owns delivery. The hooks and guarded loader help an agent obey that rule when a permitted BMAD workflow recommends a delivery workflow. They block BMAD build, unattended build, sprint execution, legacy code-review delivery, governance-file rewriting and ship/approve walkthroughs. The consolidated `bmad-review` is a checked advisory helper; unchanged document-review defaults may nest within architecture/UX. Effect-changing customization requires qualification. Other IDEs and unrelated skills are not blanket-blocked, and these controls are not protection against intentional raw-filesystem bypass.

## Repeatable evidence

`tests/test_conductor_bmad_6121_intake.py` exercises exact-byte packaging, supersession, stale approval, missing/ambiguous dependencies and tampering. Its synthetic lifecycle runs actual CLI preflight, intent, receipt, postimage and completion validators. It simulates decisions, Spec regeneration and countersigns using explicitly synthetic data; it proves protocol wiring, not model authorship or real approval. The qualification driver retains the CLI transcript plus separate guarded MCP, live Claude and private read-only packaging evidence. Any blocked lane stays blocked.
