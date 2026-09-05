# PROJECT_STATE.md - Canonical Build State

> **Purpose:** Single source of truth for the current starter-kit state.
>
> **Last updated:** 2026-09-04

## What Exists

- **Factory 0.3.3 (pilot candidate, `main`, tag `conductor-v0.3.3-pilot`;
  working name Conductor).** The 0.2 line closed at tag
  `factory-lineage-v0.2.5` (`7d0d20e`). Factory 0.3 governs authority, outcomes, and write boundaries through three
  gates (G1 Intent Lock, G2 Governed Execution, G3 Adversarial Review and
  Completion) enforced by `conductorctl contract-lint`, signed evidence
  receipts (`conductorctl receipts`), protected-postimage compare, Gap Requests,
  and human countersign files. Contracts are JSON Schemas under
  `docs/Conductor/contracts/`; the BMAD adapter's lane policy (2.0.0) and
  adapter config live under `docs/adapters/bmad/contracts/`. The plugin
  runtime reports Conductor-layout runs by gate and composes an existing
  `AGENTS.md` with the managed block on adoption. CI runs contract-lint on
  pull requests. Self-serve onboarding is under `docs/Conductor/onboarding/`.
  Migration steps 1-11 and 14 of the design pack are done; steps 12-13
  (module demotion, read-order trim, manifest mandatory) are post-pilot.
  0.3.0 is merged to `main` (tag `conductor-v0.3.0-pilot`). Rehearsal pass one
  on the pilot sandbox branch reached `REVIEW_READY` through all three gates.
  0.3.1 fixed CLAUDE.md migration on adoption and added `seed-contracts`;
  0.3.2 made `update` migrate 0.2-era installs (legacy state path, deletes,
  seed refresh, AGENTS.md composition, exact rollback). 0.3.3 is the documentation
  housekeeping release (legacy banners, GitHub-marketplace install text, 0.3
  wording in the BMAD skills). Handover to the pilot team is done. Remaining from `08_REHEARSAL_RESULTS.md`: F-3 (pilot-team
  decision), F-9 (constraint source validation).
- The 0.2-era stage process (stage-lint, pack-lint, handoffs, Purple Gate, Mission Mode, mission lints, context recall as a hard preflight, task memory, Repo Cartographer, Agent Loop Bridge) remains in the tree, bannered as legacy, for the archived runs and golden-pack tests; it is scheduled for retirement after the pilot (design pack steps 12-13).
- SIMPLE-CODE-GATE v2 remains the implementation guardrail for Factory-controlled code-changing work.
- Merge handoff discipline now separates `REVIEW_READY` from `MERGE_READY` repository handoffs, with final sync window guidance in `docs/Conductor/MERGE_PROTOCOL.md`.
- Product Owner process docs and templates remain available under `docs/Conductor/ProductOwner/`.
- Non-technical onboarding now exists at `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md` for first-time local setup with Cursor, Claude, or Codex.
- Kilo Code CLI stage routing now exists as an optional harness adapter with `./scripts/conductorctl kilo-stage`.
- Stage A context recall now has a formal direct-source repair path for generated `WEAK` reports when unresolved refs are concrete local sources that can be read and summarized directly.
- Factory plugin technical RC `0.2.0` has one authored source that generates Codex and Claude Code packages with Doctor, Greenfield, Brownfield, Progress, Run, Validate, and Update entry points.
- Factory and Factory-BMAD now have coherent authored `0.2.5` maintenance
  identities. Runtime-owned no-bytecode protection, current Claude permission
  preflight, evidence-preserving live verification, complete protected-root
  comparison, same-version Claude cache comparison, and first-team CLI approval
  labels are integrated; all four generated packages are current. The original
  `0.2.3` closeout passed deterministic and isolated live qualification; the
  `0.2.4` cache-integrity bump repaired the F10 stale Claude plugin cache retest
  blocker and was tester-smoked before the `0.2.5` operator-label polish.
  Publication and rollout remain separate decisions.
- Greenfield setup now supports an absent or empty target through an exact root/Git/payload/metadata/validation transaction with fail-closed Git ownership recovery.
- Greenfield CLI root selection now defaults only Greenfield to the invocation
  current directory; Doctor and every established-project command retain Git-root
  discovery, and explicit absent or spaced targets remain preview-only.
- Claude Greenfield now tolerates only the exact harness-created
  `.claude/settings.local.json` shape in an otherwise new target. Its path,
  bytes, modes, types, and directory entries are plan-bound read-only evidence,
  excluded from Factory writes and management, and preserved through lifecycle recovery.
- Promoted upstream Markdown is indexed as generic evidence, while project-specific Stage A preflight is optional, schema-locked, bounded, and ordered after Core knowledge lint and before context recall.
- Codex app loading, Brownfield adoption, Greenfield setup, validation, update, and exact rollback restoration have passed pre-pilot verification.
- Project-specific Factory installation state is excluded from distributable plugin payloads and covered by a regression test.
- Execution-enabled runs now close through the schema-locked, non-authorizing
  `conductor.execution-closeout.v1` record; progress revalidates its identities,
  pins, complete verification coverage, retained evidence, and digests on every read.
- Execution-closeout and project-preflight evidence paths now reject symlinks in
  every run-root ancestor before external reads or writes; focused regression
  covers `docs`, `docs/Conductor`, and `docs/Conductor/runs` with no-damage assertions.
- The maintainer Claude Code Greenfield slice has now passed in a harness-initialized
  new directory: exact setup approval applied Factory 0.2.0, Doctor reported
  compatible/current, Progress reported no active run, and all applicable
  validation checks passed without a Factory repository mutation.
- A separate customer-neutral upstream-evidence companion 0.2.0 candidate is generated from
  one authored source into Claude Code and mechanically portable Codex packages.
  It preserves one explicit companion install with automatic protected Factory
  dependency resolution and one Doctor front door.
- Repository-scoped Claude guards now cover direct `UserPromptExpansion` and
  model-initiated `PreToolUse`/`Skill` paths. The exact supported upstream
  allowlist is default-deny for every other or unknown workflow capability.
- Capability audit now covers exact supported core and optional test-extension versions, modules,
  commands, skills, agents, hooks/configuration, coverage, and non-destructive
  brownfield reconciliation. Runtime, project preflight, and CI lint use the
  same authored policy implementation.
- Focused enforcement/preflight/package/privacy tests, isolated one-install
  dependency composition, and real pinned-installer greenfield/neither,
  brownfield/neither, and brownfield/upstream-system-only journeys pass. The authenticated
  model-choice attempt is advisory rather than a hard gate: the generated Claude
  package's exact `PreToolUse`/`Skill` declaration, production command, event
  schema, activation/classifier, structured denial, and causal sentinel boundary
  now pass deterministic package-level verification. The release driver is
  source-safe, explicitly fail-closed in direct and conditional caller contexts,
  token-locks its evidence root, and publishes verified unique attempt snapshots.
  The fixed-order gate passes 200 tests with package-current, privacy, knowledge-
  lint, and protected-state evidence.
- The coordinated 0.2.3 source passed deterministic repository qualification,
  focused runtime/verifier recovery, package-current, privacy, policy,
  knowledge-lint, pack-lint, local source/generated-boundary checks, and the
  separately authorized authenticated Claude Code live lanes before the Odyssey
  v3 pilot exposed the adapter bytecode leak. The repaired adapter source now
  passes deterministic requalification, Odyssey v3 no-new-bytecode retest, and
  amended-source isolated live requalification.
- First-team Claude Code CLI rollout now has a read-only prerequisite preflight,
  guided operator playbook, bootstrap recovery guide, compatibility policy, and
  same-version Claude plugin cache comparison.
  Claude Desktop remains unsupported until a separate Desktop validation lane
  passes.
- A first-tester BMAD-to-Factory handoff checklist now uses the bounded Odyssey
  v3 seed in a greenfield path to validate bootstrap, allowed BMAD discovery,
  human-reviewed promotion, Factory brief drafting, and planning-only Factory
  handoff. The two brownfield team states remain required follow-up rehearsal
  before rollout.

## Current Tracking Snapshot

- Current repository scope: Factory V2, starter-kit content, and the dual-platform Factory plugin release candidate.
- Latest verified milestone: the coordinated Factory/Factory-BMAD 0.2.5 source
  preserves the passed first-tester matrix, retains the 0.2.4 cache-integrity
  guard, and adds explicit approval-plan labels before first-team CLI rollout.
- Current release state: Factory 0.2.5 maintenance is `REVIEW_READY`; the
  independent first-time-user pilot, merge/tag/publication decisions, and
  Product Owner sign-off remain pending.
- Current companion state: the 0.2.5 maintenance candidate is `REVIEW_READY`
  with additional CLI rollout hardening for the first two adopter teams.
  A post-closeout audit found that `SPRINT_20260811_003`
  retained at least 63 created evidence paths against an approved maximum of
  36, so that sprint's historical budget conformance is `FAIL` even though its
  technical verification passed. `SPRINT_20260811_004` prospectively accepts
  the retained current state without retroactively authorizing that overrun or
  changing predecessor evidence.
  `LIVE_DIRECT_EXPANSION` is retained evidence,
  `DETERMINISTIC_PACKAGED_PRETOOLUSE` is the hard enforcement proof, and
  `ADVISORY_MODEL_CHOICE_SMOKE` is not required for the release verdict. Merge,
  application pilot, publication, and rollout remain separate human decisions.
- Solution-context integration state: the 0.2.5 candidate is integrating the
  BMAD solution-context authoring boundary under
  `RUN_20260902_0725_factory_bmad_025_solution_context_integration`. BMAD
  PRD/UX/architecture/spec authoring may produce non-binding
  `SOLUTION_CONTEXT` evidence; human promotion freezes hash-pinned snapshots
  and claim dispositions; Factory/Conductor retains all implementation
  planning, verification, execution authorization, and closeout authority.
  BMAD implementation, sprint execution, code review authority, unattended
  development, quick-dev, and bmad-loop remain prohibited. The integrated
  candidate is deterministically qualified: MS-01 through MS-05 closed under
  archived digest-bound activations, the complete 339-test discovery suite,
  governance lints, and no-touch verification passed, and the canonical
  `EXECUTION_CLOSEOUT.json` records `REVIEW_READY` with human evidence review
  accepted on 2026-09-03. Achieved status is
  `CONDUCTOR_BMAD_025_INTEGRATION_DETERMINISTICALLY_QUALIFIED`; MS-06,
  AuditEdge, and any rollout decision remain separately gated and unclaimed.
- Publication-boundary source verification now protects every Git ref by
  default while allowing only disclosed rotation under the exact
  `refs/codex/turn-diffs/` prefix. Focused disposable-repository tests cover
  volatile add/remove/object changes and fail closed for HEAD, branches, tags,
  remote-tracking refs, other Codex/unknown refs, remotes, and staged index.
  Exact candidate and clean-clone revalidation remain pending in the active
  execution gate; no publication authority has been granted.
- The final companion integrity repair now reserves `receipts` and
  `install-receipts` case-insensitively, treats each promoted snapshot as an
  exact two-file mode-bound evidence object, compares complete protected
  file/symlink inventories in both Python and shell consumers, and requires an
  exact candidate commit plus an empty final clone status. Focused snapshot,
  preflight, protected-inventory, and clone-boundary checks pass. One frozen
  candidate/clone transaction and schema closeout remain the final technical
  gate; publication and the fresh-project pilot remain separately unauthorized.

## What Does NOT Exist Here

- Product-specific run history for adopters.
- Project-specific test commands beyond starter-kit validation helpers.
- A released companion plugin; the technical `REVIEW_READY` candidate is
  not merged, tagged, published, or approved for organization rollout.
- Enterprise
  managed-settings enforcement, project-scope installation compatibility,
  optional test-extension delivery, or intentional-bypass protection without CI/branch policy.

## How To Verify

```bash
bash scripts/knowledge_lint.sh
./scripts/conductorctl context-index
./scripts/conductorctl kilo-stage --help
python3 -m unittest tests.test_context_recall_repair
python3 -m unittest discover -s tests -v
python3 scripts/build_conductor_plugins.py --check
python3 scripts/agent_loop_bridge_validate.py tests/fixtures/agent_loop_bridge/valid_handoff.json --json
```
