# Intent — MS-06 Disposable Live Qualification of the 0.2.5 Solution-Context Candidate

## Version
v2

## Change Log
- v1 (2026-09-03): Contracted the authorized planning intent for disposable live qualification.
- v2 (2026-09-03): Hardened drivers, containment, sequencing, acquisition, hook-path naming, evidence bounds, promotion review, residue inventory, and the partial-success rule after Red review.

## Purpose
Prepare a reviewable execution contract for one bounded disposable live proof of the deterministically qualified Factory-BMAD 0.2.5 solution-context candidate, exercising real BMAD 6.10.0 authoring workflows without granting or disturbing any Factory authority. [SOURCE:RAW]

## Goal
Produce a Stage I2-audited, planning-only pack that can later authorize creation of one disposable repository, live boundary proof, one human-reviewed promotion, evidenced teardown, and canonical closeout, bounded by the status ceiling. [SOURCE:RAW]

## Definitions
- **Qualified candidate:** commit `c23be98034215c17c9c49a7e9b6302cb2ad1f18d` on `codex/factory-bmad-0.2.5-solution-context` in this worktree, deterministically qualified under `RUN_20260902_0725_factory_bmad_025_solution_context_integration` with canonical closeout `REVIEW_READY` and human acceptance recorded 2026-09-03. [SOURCE:RAW]
- **Disposable repository:** a fresh, empty, non-symlinked directory outside every protected root, created at an activation-pinned path, verified empty before seeding, seeded only from the qualified candidate's packaged plugins plus a minimal fixture project, containing no symlink into any protected path, and destroyed with evidenced removal before closeout. [SOURCE:RAW]
- **Live drivers:** the repository's dedicated commands `scripts/verify_factory_bmad_claude_composition.sh`, `scripts/verify_factory_bmad_live_pilot.sh`, and `scripts/verify_factory_bmad_live_preflight.py`, digest-pinned at activation; a live claim is valid only when produced through a pinned driver. [SOURCE:RAW]
- **Live proof:** invoking actual BMAD 6.10.0 workflows through the candidate's two installed hook paths — the packaged PreToolUse hook and the CLI hook entrypoint — via the pinned live drivers, as opposed to fixture-driven deterministic tests. [SOURCE:RAW]
- **Pinned BMAD source:** a pre-existing, digest-pinned local BMAD 6.10.0 tree named at activation; execution-time network fetches are forbidden. [SOURCE:RAW]
- **Solution context:** human-promoted, immutable `SOLUTION_CONTEXT` with `EVIDENCE_ONLY` authority; it may inform Factory but cannot lock intent, authorize execution, or satisfy delivery gates. [SOURCE:RAW]

## Scope
### In Scope
- Pin the qualified candidate, the disposable root, the BMAD 6.10.0 capability digests, and complete protected preimages before any live action. [SOURCE:RAW]
- Create one disposable repository and install the candidate's packaged Factory-BMAD plugins into it. [SOURCE:RAW]
- Prove live that architecture, UX, and spec authoring workflows run and emit non-binding `EVIDENCE_ONLY` `SOLUTION_CONTEXT` output. [SOURCE:RAW]
- Prove live that prohibited, unknown, malformed, and unsafe-layout paths deny before causal sentinels through both hook paths. [SOURCE:RAW]
- Perform one human-reviewed promotion of a hash-pinned solution-context snapshot with explicit claim dispositions inside the disposable repository. [SOURCE:RAW]
- Destroy the disposable repository with evidenced removal and record the canonical closeout. [SOURCE:RAW]

### Domain Areas
- None. [SOURCE:RAW]

### Non-goals
- No change to the qualified candidate, Factory Core, this repository's source, tests, generated packages, donors, registrations, or unrelated paths. [SOURCE:RAW]
- No AuditEdge access or preview; live index-exclusion proof remains separately gated. [SOURCE:RAW]
- No BMAD implementation, sprint execution, code review authority, unattended development, quick-dev, or bmad-loop invocation, even inside the disposable repository. [SOURCE:RAW]
- No commit, merge, push, publication, pilot, release, or rollout. [SOURCE:RAW]

## Locked Qualification Rules
- The candidate worktree is consumed read-only; every live action happens inside the disposable repository. [SOURCE:RAW]
- Activation pins the exact candidate commit, plugin package digests, disposable root, BMAD 6.10.0 capability profile, and evidence roots; any mismatch halts. [SOURCE:RAW]
- Each allowed workflow proof must show the emitted solution context is typed, non-binding, and unable to alter Factory state. [SOURCE:RAW]
- Each denial proof must show the causal sentinel did not execute. [SOURCE:RAW]
- Promotion requires the human to review the concrete candidate snapshot during the activation window; a missing review is a halt, never default approval, and unpromoted output remains inert evidence. [SOURCE:RAW]
- Promotion evidence is exported to the external evidence root with digests strictly before teardown; teardown of unexported promotion evidence halts. [SOURCE:RAW]
- Complete live logs go only to the external evidence root, the harness receives bounded digests and verdicts, and live output is scanned for secrets before retention. [SOURCE:RAW]
- Teardown must remove the disposable repository completely and prove no residue in protected paths, harness plugin caches, or worktree/registration state. [SOURCE:RAW]
- Any missing or failed proof yields `NO_GO`, or `BLOCKED` when a proof could not run; no qualified-with-exceptions status exists. [SOURCE:RAW]
- Deterministic 0.2.5 qualification evidence is provenance only; it cannot substitute for any live proof, and live proof cannot expand the candidate's claims beyond the status ceiling. [SOURCE:RAW]

## Principles
- Factory/Conductor remains the sole implementation and delivery authority. [SOURCE:RAW]
- Workflow eligibility never implies authority; promotion, adjudication, and exact-pack Go remain separate. [SOURCE:RAW]
- Every capability and input is digest-bound; proof is non-transitive. [SOURCE:RAW]
- Fail closed on ambiguity, unexpected writes, capability drift, or evidence mismatch. [SOURCE:RAW]
- Apply SIMPLE-CODE-GATE v2; this run authorizes no code change at all. [SOURCE:REF:AGENTS.md]

## Roles
- Eduardo dos Remedios: sole human reviewer, promotion reviewer, and execution approval authority. [SOURCE:RAW]
- Factory Root Planner: prepares and validates the planning pack only. [SOURCE:RAW]
- Red Team: attacks authority, containment, teardown, and evidence assumptions. [SOURCE:RAW]
- Blue Team: hardens the contract without expanding scope. [SOURCE:RAW]
- Purple Gate: adjudicates intent and final pack readiness; it grants no execution. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]
- Future execution agent: may act only after separate digest-bound authorization. [SOURCE:RAW]

## Acceptance Criteria
- AC-01: Candidate, disposable root, capability digests, and protected preimages are exactly pinned before any live action. [SOURCE:RAW]
- AC-02: All three authoring workflows run live and emit typed, non-binding `EVIDENCE_ONLY` solution context. [SOURCE:RAW]
- AC-03: Prohibited, unknown, malformed, and unsafe-layout paths deny live before causal sentinels through both hook paths. [SOURCE:RAW]
- AC-04: One human-reviewed promotion produces an immutable hash-pinned snapshot with explicit claim dispositions. [SOURCE:RAW]
- AC-05: The disposable repository's Factory authority chain is untouched by BMAD output. [SOURCE:RAW]
- AC-06: Teardown removes the disposable repository with evidence, and every protected path remains byte-identical. [SOURCE:RAW]
- AC-07: Canonical closeout records the outcome; final status does not exceed `FACTORY_BMAD_025_MS06_DISPOSABLE_LIVE_QUALIFIED`. [SOURCE:RAW]

## Constraints
- C-001 (Critical): Factory/Conductor plus explicit human Go retain all implementation and delivery authority. [SOURCE:RAW]
- C-002 (Critical): The qualified candidate, Factory Core, donors, and unrelated state remain byte-identical. [SOURCE:RAW]
- C-003 (Critical): Prohibited, unknown, malformed, and unsafe paths fail closed live. [SOURCE:RAW]
- C-004 (Critical): Promotion is immutable, human-reviewed, provenance-bound, and non-authorizing. [SOURCE:RAW]
- C-005 (Critical): The disposable repository is contained, pinned, and destroyed with evidence. [SOURCE:RAW]
- C-006 (High): Live proofs cover both allowed authoring and denial families. [SOURCE:RAW]
- C-007 (High): Evidence, budgets, commands, and status claims remain exact and bounded. [SOURCE:RAW]

## Open Questions
### BLOCKING
- None.

### NON-BLOCKING
- Live AuditEdge index-exclusion proof remains a separately gated future run. [SOURCE:RAW]

## Go or No-Go Rule
- Go for human pack review only if Stages A-I2 and `pack-lint` pass in `PLANNING_ONLY` with no unresolved Critical/High finding or scope expansion. [SOURCE:RAW]
- No-Go for execution until an exact post-I2 human authorization pins the unchanged pack, candidate commit, disposable root, capability digests, evidence roots, and the execution-mode transition. [SOURCE:RAW]
