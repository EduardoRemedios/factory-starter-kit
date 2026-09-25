# Factory + BMAD actions (0.3.9 candidate)

People choose the Spec, confirm scope, answer questions, review outputs and approve.
The agent generates identifiers and records, runs the commands and keeps evidence in
files. Terminal output reports status and a path; the durable review material is the
file it names.

Two kinds of action exist, and the difference matters:

- **Commands** are real executables. They behave the same every time and fail with a reason code.
- **Skills** are instructions an agent follows (`/conductor:run`, `/conductor-bmad:reconcile`).
  They call the commands; they are not themselves enforcement.

In the examples below:
- `$FACTORY_PY` is the Factory Python wrapper and `$COMPANION` is `conductor_bmad.py` from the pinned package.
- `./scripts/conductorctl` is the project's installed control script.

## Commands

| Command | Writes | What you get |
|---|---|---|
| `./scripts/conductorctl run-init --slug <name> [--new]` | `docs/Conductor/runs/RUN_YYYYMMDD_HHMM_<name>/` (planning-only skeleton) and `REVIEW_PACKET.md` | `CREATED` with the RUN_ID. If a run for that slug is open and not complete, you get `EXISTING` and nothing is duplicated. A same-minute clash is refused. |
| `./scripts/conductorctl review-packet --run <RUN_ID>` | `REVIEW_PACKET.md` | The gate state, whether the run is ready for G1, then: inputs and snapshots, intent, questions and decisions, the verification plan and results, the Statement of Completion, and the exact digest to sign |
| `./scripts/conductorctl gap open --run <RUN_ID> --requirement <R-ID> --type <type> --question "<text>" --impact active_scope\|future_only\|unknown [--owner "<person or role>"] [--proposal "<text>"]` | `gap_requests/GAP-NNN.json` | One question bound to one requirement and the current intent digest |
| `./scripts/conductorctl gap resolve --run <RUN_ID> --gap GAP-NNN --decided-by "<person>" --decision "<text>" [--new-snapshot-id <ID> --new-snapshot-sha256 <digest>]` | The same gap file | The human decision. An `active_scope` decision that introduces a new snapshot forces a G1 re-lock. |
| `./scripts/conductorctl gap export --run <RUN_ID>` | `UPSTREAM_QUESTIONS.md` | Open questions grouped as blocking or deferred, plus the decisions already made. This is the file you give to `bmad-spec`. |
| `./scripts/conductorctl contract-lint intent\|execution\|completion --run <RUN_ID>` | nothing | The G1, G2 or G3 verdict |
| `./scripts/conductorctl completion-feedback --run <RUN_ID>` | `UPSTREAM_FEEDBACK.md` and `.json` | Refused until G3 is countersigned. Then: the source snapshots, code revision, per-requirement status, evidence, limitations and deferred findings with owners. |
| `"$FACTORY_PY" "$COMPANION" --root . --json promote ... [--git-binding] [--approve-plan <plan id>]` | Without `--approve-plan`, nothing. With it, `docs/upstream/bmad/<ID>/` plus a receipt. | Preview: the full file list, digests and plan ID. Apply: the immutable snapshot. |
| `"$FACTORY_PY" "$COMPANION" --root . --json verify-checkout --snapshot-id <ID> [--run <RUN_ID>]` | nothing | `VERIFIED`, or the exact reason the checkout does not match the approval |
| `"$FACTORY_PY" "$COMPANION" --root . --json automation-capture\|automation-compare --run <RUN_ID>` | `automation/window-001/` | Opens or closes the run's single governed TEA automation window. See `BMAD_GOVERNED_AUTOMATION.md`. |

## Skills

| Skill | Use it to say | What it does |
|---|---|---|
| `/conductor-bmad:reconcile` | "Get spec-042 ready for G1" | Runs the grooming loop below and stops when the packet says it is ready |
| `/conductor:run` | "Continue the run" | Takes the next legal G1/G2/G3 action and stops at every human countersign |
| `/conductor:progress` | "Where is this run?" | Reports the state from disk evidence |
| `/conductor-bmad:promote` | "Snapshot these reviewed inputs" | Previews and, after exact approval, applies a snapshot |

## Snapshot fields

These are the `promote` arguments and manifest fields.

| Field | Meaning | Who sets it |
|---|---|---|
| `snapshot-id` | Stable name of this frozen input package, e.g. `spec-042-v1`. It is never reused. A changed package gets a new ID that supersedes the old one. | Agent proposes, human reviews |
| `workflow` | The BMAD workflow that produced the source (`spec`). Only product-context and evidence-only workflows can be promoted. | Agent, from the source |
| `evidence-type` | `SOLUTION_CONTEXT`: architecture, UX or Spec authoring evidence | Fixed for a Spec package |
| `authority` | `EVIDENCE_ONLY`. A snapshot never authorises implementation. Only G1 plus an `EXECUTION_GO` countersign does. | Fixed |
| `plan-identity` | A short label that ties the snapshot to the review record, e.g. `spec-042-grooming-2026-09-25`. The raw brief or intent repeats it. | Agent proposes |
| `reviewer` | The person who reviewed the exact package | Human |
| `review-ref` | Where that review is recorded, e.g. a PR, ticket or meeting note | Human |
| plan ID | The SHA-256 of the whole plan. Approval is exactly this value. | Command |

### Why snapshot `ENGINEERING_STANDARDS.md`

`AGENTS.md` makes the file discoverable, but discovery always reads its current
bytes. Snapshotting fixes the exact version that was reviewed with the Spec. Later
edits then show up as a changed input, not as a silent change to the rules the work
is judged by. This matters whenever `main` changes the standards between grooming and
implementation.

## Main to feature branch

1. **Groom on the main checkout, then commit.** Commit the reviewed Spec, memlog and companions. Preview with
   `--repo-companion docs/ENGINEERING_STANDARDS.md --git-binding`. The plan records:
   - the approval commit;
   - each input's Git blob;
   - repository-relative paths, with no absolute folder.
2. **Approve and commit the snapshot.** A human approves the plan ID. Apply it, then commit the snapshot with the grooming work.
3. **Verify the feature checkout.** Create the feature branch from that commit or any later one. In the feature checkout,
   `verify-checkout --snapshot-id <ID> --run <RUN_ID>` needs no new approval.

   It returns `VERIFIED` only when all of these hold:
   - the snapshot is intact;
   - the approval commit is an ancestor of HEAD;
   - every input is byte-identical;
   - the locked intent cites the snapshot.

   Otherwise it names the problem:
   - `CHECKOUT_INPUTS_CHANGED`: review a superseding snapshot.
   - `CHECKOUT_BASE_INCOMPATIBLE` or `CHECKOUT_BASE_UNKNOWN`: rebase or fetch. Do not re-approve.
   - `CHECKOUT_INTENT_STALE`: the execution boundary changed, so G1 must be re-locked.

Existing root-bound snapshots and receipts are left as they are. They verify only in
their original checkout and report `SNAPSHOT_ROOT_BOUND_ELSEWHERE` in any other.

## The grooming loop and its exit

1. **Inspect the inputs.** Run the `promote` preview.
2. **Draft scope and questions.** Use `run-init`, then `gap open` with an owner.
3. **Reconcile in BMAD.**
   1. `gap export` writes `UPSTREAM_QUESTIONS.md`.
   2. The person runs `bmad-spec` to update the existing Spec, with that file as its input.
   3. BMAD appends decisions to `.memlog.md` and re-derives `SPEC.md`.
   4. PRD, architecture and UX change only through `bmad-prd`, `bmad-architecture` and `bmad-ux`.
4. **Review the changed inputs.** The `promote` preview shows the changed files. The person approves a superseding snapshot. The old one stays.
5. **Refresh the draft.** Cite the new snapshot, record each decision with `gap resolve`, then run `review-packet`.

**Exit to G1.** The packet reports *Ready for G1 review: yes* only when:
- no `active_scope` or `unknown` gap is open;
- every `future_only` finding names an owner;
- every snapshot introduced by a decision is cited.

A future-only finding with an owner never blocks a ready slice.

## Completion feedback

After G3 is countersigned, `completion-feedback` writes the handoff for BMAD. PM/BA
own the backlog decisions, with SA and QA contributing. The handoff:
- says it is not merge, deployment, release or backlog approval;
- lists deferred findings with their owners;
- never marks a capability delivered in BMAD.

An approved requirement cannot be closed through a `future_only` gap: contract-lint
rejects that with `CONDUCTOR_CONTRACT_SCOPE_RELABEL`. Dropping approved scope needs an
explicit `active_scope` decision, which stays visible as `NEEDS_HUMAN_DECISION`.
Otherwise the intent is re-locked without that requirement.
