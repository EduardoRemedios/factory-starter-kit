# Factory BMAD Pilot Defect and UX Backlog

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

Last updated: 2026-08-15

## Purpose

This is the durable working backlog for defects and user-experience findings
discovered while piloting Factory 0.2.1 with BMAD 6.10.0 through Claude Code.
It covers the Odyssey v2 pilot and any reusable findings from earlier companion
verification. It is not an authorization to implement a repair.

The backlog's north star is a reliable, low-friction Factory-BMAD companion for
Factory/BMAD adoption. Odyssey is only the regression vehicle; application
completion is not the objective of this backlog.

Do not silently remove findings. Move an item to `CLOSED` only after its source
repair, generated-package parity, focused regression, and a fresh Claude Code
operator retest all pass.

## Current pilot disposition

- Odyssey v2 is deliberately paused after Stage F. Stages A through F pass;
  Stage G has not started. See `ODYSSEY_V2_PILOT_CHECKPOINT.md`.
- Factory/Factory-BMAD 0.2.3 is `AMENDED_SOURCE_LIVE_QUALIFIED`: all four
  packages are current, focused and full deterministic checks pass, and the
  separately gated isolated Claude Code live lanes passed against the pinned
  amended-source 0.2.3 candidate. First-team rollout remains a separate pilot
  decision.
- Closure evidence:
  `artifacts/verification/conductor_bmad_023_recovery/VM-008.json`,
  `artifacts/verification/conductor_bmad_023_recovery/VM-012.json`,
  `artifacts/verification/conductor_bmad_023_recovery/VM-013.json`, and
  `docs/Conductor/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/RUN_INTEGRITY_REPAIR.md`.
- Odyssey v2 remains paused. Do not resume Stage G by default; use a fresh,
  bounded regression pilot unless the sponsor explicitly chooses Odyssey v2 as
  the next vehicle.
- Publication and organizational rollout remain separate human decisions.

## Status definitions

- `OPEN`: reproduced or source-confirmed; no source repair has been verified.
- `WORKAROUND_VALIDATED`: the pilot can proceed safely without weakening a gate.
- `FIXED_AWAITING_RETEST`: source and automated checks pass; live operator proof
  remains outstanding.
- `CLOSED`: source, packages, regression, and live operator proof all pass.

## Defects

### FB-D001 — Raw-brief checklist triggers its own draft-citation guard

- Priority: P1
- Status: CLOSED
- Observed: Odyssey v2 project preflight returned
  `CONDUCTOR_BMAD_DRAFT_CITATION` because the checklist sentence asserting that no
  draft was cited contained the literal forbidden draft-directory token.
- Source confirmation:
  `plugin-src/conductor-bmad/project-adapter/RAW_BRIEF_TEMPLATE.md` contains the
  token and `conductor_project_preflight` rejects any occurrence of it.
- Safe pilot workaround: use “No mutable BMAD draft is cited” and cite only the
  immutable snapshot ID and aggregate digest.
- Required repair: make the canonical template compatible with the scanner
  without weakening rejection of genuine mutable-draft citations.
- Acceptance: an unedited seeded template passes; a real mutable-draft citation
  fails; generated Claude and Codex project-adapter copies match the source.

### FB-D002 — Snapshot JSON cannot satisfy the Markdown-only recall contract

- Priority: P1
- Status: CLOSED
- Observed: Stage A recall was `WEAK` when
  `SNAPSHOT_MANIFEST.json` was supplied as a required reference even though the
  file existed and project preflight had validated it.
- Cause: the context index deliberately ingests promoted Markdown evidence, not
  snapshot JSON manifests.
- Safe pilot workaround: project preflight validates the manifest, review,
  aggregate digest, and snapshot shape; Stage A recall requires the promoted
  `artifact.md` path.
- Required repair: state this two-part contract consistently in the quick start,
  pilot runbook, intake guidance, raw-brief guidance, and Factory handoff prompt.
- Acceptance: the documented clean journey selects `artifact.md`, recall is
  `SUFFICIENT`, and tampered or invalid manifest evidence still fails preflight.

### FB-D003 — Normal promote invocation can be rejected as malformed hook input

- Priority: P1
- Status: CLOSED
- Observed: the first `/conductor-bmad:promote` Skill invocation halted with
  `CONDUCTOR_BMAD_HOOK_INPUT_INVALID`; a later direct evaluator journey succeeded.
- Safety note: malformed hook events must continue to fail closed.
- Required repair: reproduce the exact Claude Code Skill event shape, repair the
  parser or invocation boundary rather than relaxing validation, and retain
  malformed/ambiguous-event denial tests.
- Acceptance: a normal namespaced promote invocation reaches preview, malformed
  input remains denied, and no downstream sentinel runs on denial.

### FB-D004 — Claude permission bookkeeping can stale a Greenfield plan

- Priority: P2
- Status: CLOSED
- Observed: Claude Code changed `.claude/settings.local.json` after preview while
  recording permission approvals, invalidating an otherwise current exact plan.
- Boundary: this is a Factory/Claude harness lifecycle issue, not a BMAD policy
  failure. The file correctly remained outside Factory ownership.
- Safe pilot workaround: re-preview after harness metadata settles and approve
  only the new exact plan ID; avoid unnecessary shell probes between preview and
  apply.
- Required repair: design a stable, fail-closed approval journey that accounts
  for expected harness-owned permission churn without allowing unrelated target
  changes or weakening preserved-path guarantees.
- Acceptance: the normal interactive preview/apply journey needs no surprise
  reapproval, while any material non-harness change still makes the plan stale.

### FB-D005 — Promotion manifest cannot carry the review qualifier

- Priority: P2
- Status: CLOSED
- Observed: the promoted manifest recorded `APPROVED` but had no field for the
  sponsor qualifier “unvalidated upstream evidence; not binding product intent.”
  The qualifier survived only inside the promoted artifact and later brief.
- Required repair: add a plan-bound, immutable optional review note or evidence
  classification to the snapshot schema and surface it during promotion review.
- Acceptance: the qualifier survives preview, approval, manifest creation,
  preflight, and raw-brief citation without changing Factory-only authority.

### FB-D006 — Progress advances past a failed Intent Purple Gate

- Priority: P1
- Status: CLOSED
- Observed: Odyssey v2 Stage D correctly recorded `FAIL` and created no locked
  intent or digest, but `/conductor:progress` reported `next_legal_action:
  run_stage_e` because it treated the Stage D handoff as stage completion.
- Risk: an operator is directed into risk and architecture planning against
  unlocked intent, undermining the purpose of the Purple Gate even if a later
  stage independently refuses entry.
- Safe pilot workaround: disregard the reported Stage E action; resolve the
  sponsor blockers, re-run Stage C, and re-adjudicate Stage D before proceeding.
- Required repair: progress must evaluate the Stage D verdict and lock evidence,
  not merely the presence of its handoff. Stage E must also fail closed when no
  valid intent lock exists.
- Acceptance: a Stage D `FAIL` reports a blocked intent-repair action and cannot
  start Stage E; only a contract-valid lock permits the Stage E route. Focused
  progress and run-command regressions cover both states in generated packages.

### FB-D007 — Stage-lint omits hard size caps on stage artifacts

- Priority: P1
- Status: CLOSED
- Observed: Odyssey v2 Stage C and D passed stage-lint even though
  `intent.md`, `intent_synthesis.md`, and `intent_lock_report.md` exceeded their
  hard `DEFINITIONS.md` word caps. The problem surfaced at Stage F because the
  eventual I2 pack-lint would reject it.
- Cause: `conductor_stage_lint.py` enforces the 500-word handoff cap but does not
  enforce the per-artifact caps that `conductor_pack_lint.py` checks later.
- Risk: invalid output crosses multiple stage boundaries, can become locked, and
  then requires the Intent Unlock Protocol for what should have been a local
  compression repair.
- Safe pilot workaround: halt before Stage G; use a sponsor-approved,
  semantics-preserving intent unlock; compress the three artifacts; re-lock;
  and revalidate Stages E and F before continuing.
- Odyssey evidence: the bounded unlock compressed the three artifacts within
  cap, preserved all six semantic inventories plus seven sponsor predicates,
  locked intent v4 at SHA-256
  `01e079d35cd1988273add6b6547613ef9d302d9aadb904bef411ddbc4e91db3f`,
  and re-passed Stages C through F without changing downstream scope or checks.
- Required repair: stage-lint must apply the canonical cap table to every
  artifact produced or updated by the stage being validated.
- Acceptance: over-cap Stage A/C/D/E/F outputs fail at their own handoff; exact-
  cap and under-cap outputs pass; stage-lint and pack-lint share one cap contract
  or have a parity regression that prevents drift in generated packages.

### FB-D008 — Planning commands leave Python bytecode in the adopter repository

- Priority: P2
- Status: CLOSED
- Observed: at the Odyssey v2 pause checkpoint, untracked bytecode existed under
  `scripts/__pycache__/` and `tools/repo_cartographer/__pycache__/` even though
  the run remained planning-only. Timestamps align with the Stage A-to-F pilot.
- Current evidence: twelve `.pyc` files are retained on disk and must not be
  silently deleted or normalized before root cause is classified.
- Likely boundary: the installed 0.2.1 project includes `scripts/conductor-python`
  with `PYTHONDONTWRITEBYTECODE=1`, but `scripts/conductorctl` itself uses a raw
  Python shebang. Ad-hoc Claude probes may also have contributed.
- Implemented repair: the Factory-BMAD runtime activates its own no-bytecode
  control before dynamically importing policy. Authored and packaged fresh-process
  regressions pass without relying on a caller-supplied environment variable;
  pre-existing user state remains untouched.
- Acceptance: a clean A-to-F journey leaves no `.pyc` or `__pycache__` paths, and
  focused tests distinguish canonical-command behavior from unrelated user
  Python without deleting pre-existing user state.

### FB-D009 — Pack-lint crashes before evaluating a completed pack

- Priority: P1
- Status: CLOSED
- Observed: the clean `a00b70d4df48791e9d4338a0fa413b0224596c7e`
  baseline raises `UnboundLocalError` in `lint_pack()` because
  `audited_execution_mode` is supplied to `_check_text_contracts()` before that
  local variable is assigned.
- Source confirmation: working-tree and `HEAD` copies of
  `scripts/conductor_pack_lint.py` share SHA-256
  `75a0aeb12c37080c1d9cd5c927f8056e714503622d28eec9b8f9751ae9d2ef34`;
  the planning run did not modify the validator.
- Risk: no completed pack can obtain deterministic post-I2 validation, so human
  Go cannot be bound safely even when every planning artifact is valid.
- Required repair: pass the already-read current execution mode into the text
  contract, add a focused regression that runs pack-lint on valid and failing
  packs, and retain the existing audited-mode/cross-mode checks.
- Acceptance: a valid planning pack reaches `pack_lint: PASS`; invalid audit,
  cap, mode, and activation evidence return structured FAIL results rather than
  exceptions.
- Implemented repair: pack-lint now evaluates valid and invalid packs without
  the prior unbound-local exception and preserves audited-mode and activation
  fail-closed behavior.

## User-experience improvements

### FB-UX001 — Default interactive output is too JSON-heavy

- Priority: P2
- Status: CLOSED
- Observed: Greenfield and related previews emitted hundreds of raw JSON lines,
  forcing Claude to run extra parsing commands before presenting the plan.
- Required improvement: interactive skills should use concise human output by
  default and request structured JSON only when needed for deterministic
  processing or diagnostics.
- Acceptance: Doctor, Greenfield, Bootstrap, Intake, Promote, and Progress each
  present state, reason, plan ID, changes, risks, and next action without dumping
  the complete payload; explicit JSON remains available.

### FB-UX002 — Bootstrap does not make the Claude restart/reload step obvious

- Priority: P2
- Status: CLOSED
- Observed: after BMAD installation, the newly installed skills were not
  discoverable predictably in the existing Claude Code session.
- Required improvement: the apply result must state whether a fresh Claude Code
  session or plugin reload is required and must make that the next operator step
  before attempting BMAD workflows.
- Acceptance: a first-time user can install, restart/reload once, and discover an
  allowed BMAD skill without troubleshooting.

### FB-UX003 — Allowed BMAD workflows advertise prohibited follow-on workflows

- Priority: P1
- Status: CLOSED
- Observed: the allowed brainstorming workflow recommended party mode, advanced
  elicitation, and later architecture, all of which the Factory-BMAD policy
  correctly prohibits for Factory-bound work.
- Required improvement: inject a durable Factory-bound session constraint or
  companion guidance that prevents allowed workflows from recommending denied
  helpers or downstream BMAD solutioning.
- Acceptance: an allowed brainstorming/product workflow remains useful but does
  not recommend a prohibited skill; explicit prohibited invocation is still
  denied by the hook.

### FB-UX004 — Command discovery can make a blocked workflow look misrouted

- Priority: P2
- Status: CLOSED
- Observed: typing `/bmad-architecture` displayed an unrelated `/doctor`
  autocomplete entry, creating the impression that the requested command had
  invoked Doctor. The hook later correctly blocked the explicit command.
- Required improvement: onboarding must explain namespaced command discovery,
  post-install reload, and the difference between a suggested next action and an
  automatically executed action. Denials should explicitly say that Doctor was
  not run.
- Acceptance: a first-time operator can distinguish autocomplete, hook denial,
  and the optional `/conductor-bmad:doctor` recovery action.

### FB-UX005 — The fastest safe BMAD-to-Factory handover is not visible

- Priority: P2
- Status: CLOSED
- Observed: a five-technique brainstorming session could have consumed much of
  the pilot before the user asked how to converge and hand over to Factory.
- Required improvement: document a time-boxed discovery path: run one useful
  technique, converge to the product-brief synthesis shape, human-review,
  promote, cite the immutable snapshot, then start Factory.
- Acceptance: the quick start offers both “full discovery” and “pilot/fast
  handover” routes and states that completeness is not required if limitations
  are recorded honestly.

### FB-UX006 — Preflight and recall responsibilities are not explained together

- Priority: P2
- Status: CLOSED
- Observed: the operator reasonably treated the JSON manifest as the strongest
  recall reference, causing a halt that looked like missing evidence.
- Required improvement: show one compact handover map:
  manifest integrity is checked by project preflight; promoted Markdown content
  is resolved by Stage A recall; Factory intent becomes authoritative only after
  its own Purple Gate.
- Acceptance: the runbook and generated intake guidance use the same map and no
  longer suggest the JSON manifest as a recall reference.

## Deferred capability, not a current defect

### FB-E001 — Optional TEA automation evidence mapping

- Priority: P3
- Status: OPEN
- Context: TEA was installed in an early adopter project as a future QA automation option, but
  no suite, framework, or final selection exists yet.
- Boundary: Factory already owns verification strategy and governance. TEA may
  later generate API/UI automation assets as optional Stage F evidence; it must
  not become a competing quality gate.
- Trigger: revisit when a pilot project has a concrete test framework and a real
  automation suite or when an adopting organization selects its preferred API/UI tooling.

## Closure state after live qualification

1. Separately authorized isolated live qualification passed against pinned
   candidate `3d583029efced8313911092e6e15d488de34bbe5`.
2. P1/P2 backlog items are closed by the combined evidence set above.
3. The recommended next regression vehicle is Odyssey v3, a deliberately small
   fresh BMAD-to-Factory pilot, rather than resuming Odyssey v2 by default.
4. Consider FB-E001 only when concrete TEA evidence exists.
