# Raw Brief — Factory BMAD Companion Plugin

## Version

v2

## Change Log

- v1 (2026-08-10): Created from the human-approved next phase following the
  Factory 0.2.0 Claude Code Greenfield, Doctor, Progress, and Validate pilot.
- v2 (2026-08-10): Replaced customer and local pilot identifiers with public-safe role descriptions.

## Intake Authority

- Human direction: proceed with the separate BMAD companion phase, keep the
  canonical project documents current, and commit and push bounded work.
- Run ID: `RUN_20260810_1816_factory_bmad_companion`
- Proposed Sprint ID: `SPRINT_20260810_003`
- Execution Mode: `PLANNING_ONLY`
- Execution Authorization: NOT_GRANTED
- Downstream Fan-Out: NOT_APPROVED
- Base: `codex/factory-plugin-0.2.0-public-release` at `9855f7f`

## What To Build

Plan one bounded code-changing sprint for a separate, customer-neutral BMAD
companion plugin. The companion must let a Claude Code team adopt Factory and
BMAD from an empty directory, a Factory-only repository, a BMAD-only
repository, or a brownfield repository without making BMAD a competing SDLC.

The first release is Claude Code-first because the target enterprise pilot uses
Claude Code and Claude Enterprise. It must compose with, and depend on, the
existing Factory plugin rather than copying Factory Core. A portable Codex
package may be prepared only if it reuses the same authored policy and
deterministic runtime without enlarging the live support claim.

## Problem

Factory 0.2.0 now installs safely and exposes the generic upstream index and
project-preflight seams required by a companion. It does not install BMAD,
classify BMAD usage, promote reviewed BMAD evidence, enforce the authority
boundary, or convert that evidence into governed Factory intake. A team could
therefore install both tools but still use BMAD architecture, stories,
implementation loops, or test governance as competing authority.

The pilot also exposed adoption friction: routine commands can produce verbose
raw JSON, Claude permission bookkeeping can mutate the unmanaged local settings
file, and a user needs one clear next action rather than multiple overlapping
workflows.

## What Exists Today

- Factory plugin 0.2.0 with seven namespaced journeys and exact setup receipts.
- Generic indexing of promoted `docs/upstream/**/*.md` evidence.
- Optional schema-locked project preflight after knowledge lint and before
  Stage A recall.
- Claude Greenfield support for the exact harness-created
  `.claude/settings.local.json` shape without managing that file.
- Verified first-maintainer Claude Code journey: Greenfield apply, Doctor,
  Progress, and applicable Validate checks passed without Factory repository
  mutation.
- Official `bmad-method@6.10.0` package and a known enterprise-pilot module
  manifest shape containing Core 6.10.0, BMM 6.10.0, optional external loop,
  and TEA modules.

## Required Companion Journeys

### RB-01 — Diagnose and route

Provide one concise read-only entry journey that classifies:

1. neither Factory nor BMAD installed in a new target;
2. Factory installed, BMAD absent;
3. BMAD installed, Factory absent;
4. both installed;
5. existing brownfield code with neither installed.

The result must name one next legal action, never invent a target, never treat a
non-Git directory as Brownfield, and never mutate the repository.

### RB-02 — Reproducible BMAD bootstrap boundary

- Pin the enterprise pilot to `bmad-method@6.10.0` and Claude Code.
- Default new Factory-bound projects to Core plus BMM only.
- Do not install `bmad-loop` or TEA in the pilot default.
- Preview the exact command, target, module selection, allowed path prefixes,
  current state, and approval token before invoking the upstream installer.
- Audit the post-install manifest and changed paths; halt and retain evidence on
  drift, failure, unexpected modules, unexpected path writes, or partial state.
- Never silently uninstall or alter an existing BMAD module.

### RB-03 — Authority policy and dual-use classification

Ship a one-page project policy with these rules:

- Allowed upstream: brainstorming, idea/forge, PRFAQ, product brief, bounded
  research with Factory source metadata, optional PRD/UX context, and
  brownfield project-context mining as evidence.
- BMAD artifacts remain drafts/evidence and are never binding.
- Banned as Factory authority: BMAD spec, solution architecture,
  epics/stories/sprint planning, Phase 4 implementation/correct-course/code
  review gates, and `bmad-loop`.
- TEA is not Factory authority. When present later, its API/UI automation output
  may be Stage F input evidence under Factory verification governance; it is not
  installed in this pilot.
- BMAD coding use outside a Factory-bound run may exist, but the companion must
  never route Factory-bound work into BMAD solutioning or implementation.
- Factory stages E–H own solution decomposition, risk, verification, and
  execution sequencing; Factory execution closeout owns completion evidence.

### RB-04 — Immutable upstream promotion

Implement preview-before-write promotion from selected `_bmad-output` source
artifacts into `docs/upstream/bmad/<SNAPSHOT_ID>/`.

The transaction must include:

- an allowlisted source classification;
- source path, bytes, SHA-256, BMAD version/module/workflow, creation time when
  known, and reviewer decision;
- exact destination paths and output digests;
- a snapshot manifest and stable snapshot digest;
- an exact approval token;
- stale-source rejection;
- path traversal and symlink rejection;
- immutable existing-snapshot rejection;
- rollback/receipt evidence for transaction-created files;
- snapshot reuse across multiple Factory runs without duplication.

No `_bmad-output/` file is directly citable by a Factory brief. Only a human
approved promoted snapshot under `docs/upstream/bmad/` may be cited.

### RB-05 — Factory intake and preflight

- Provide one raw-brief template with an embedded intake checklist rather than
  a separate drifting checklist.
- Require snapshot ID plus digest for each BMAD-derived claim or input.
- Seed the fixed Factory project-preflight declaration and companion-owned
  validator only through an exact reviewed installation plan.
- Preflight must fail closed on missing/invalid policy, direct draft citations,
  missing snapshot, digest mismatch, mutable/symlinked evidence, missing human
  promotion evidence, prohibited authority claims, or malformed output.
- Write its bounded verdict as project-preflight evidence in the normal Stage A
  chain; do not create a new Factory gate.
- Freeze cited BMAD context at Brief Purple PASS. Later BMAD changes require a
  new promoted snapshot and a new brief review, not silent refresh.

### RB-06 — Frictionless Claude Code experience

- Expose a small namespaced journey surface with concise human-first summaries;
  JSON is opt-in evidence, not the default wall of output.
- Declare a same-marketplace version-constrained dependency on Factory 0.2.x
  where supported and fail closed when it is absent, disabled, or incompatible.
- Preserve `.claude/settings.local.json` as unmanaged harness state and avoid
  self-measurement commands that create new permission rules merely to report
  its digest.
- Provide one documented empty-project path and one brownfield path.
- Never claim Claude Desktop support; this release targets Claude Code CLI.

### RB-07 — Packaging, verification, and canonical documentation

- Use one authored companion source and deterministic generated package(s).
- Add customer-neutral manifest, ownership, marketplace, policy, onboarding,
  fixtures, and tests.
- Validate plugin manifest, marketplace, dependency, namespace, package
  determinism, privacy, and no-touch behavior.
- Run an isolated live Claude Code composition journey with Factory 0.2.0 and
  BMAD 6.10.0 without permanently changing the real Claude profile.
- Use the live application-pilot repository only after the companion pack receives I2 PASS and
  separate explicit human execution authorization.
- Update `docs/PROJECT_STATE.md`, `docs/ROADMAP.md`, and `docs/CHANGELOG.md` in
  the implementation closure cycle.

## Explicitly Out Of Scope

- Replacing or modifying Factory Core stage contracts.
- Copying or vendoring BMAD runtime, prompts, or copyrighted workflow content.
- BMAD architecture, epics/stories, sprint planning, implementation, loop, or
  code-review-as-gate for Factory-bound work.
- Installing TEA, selecting an API/UI framework, or delivering a QA automation
  suite in this sprint.
- Claude Desktop, Cursor, Windows, Linux, or organization-wide rollout claims.
- Automatic deletion/uninstallation of any user-owned module or file.
- Publishing, merging, tagging, or installing into the live application pilot
  before separate authorization.

## Hard Constraints

1. Factory remains the SDLC and sole downstream authority.
2. The companion must depend on Factory; it must not duplicate Factory policy,
   gates, runtime, or stage orchestration.
3. Keep all public content customer-neutral and free of private paths, account
   names, tokens, session records, and internal repository details.
4. Apply SIMPLE-CODE-GATE v2; add no dependency unless the approved envelope
   explicitly justifies it.
5. Preview, diagnosis, and planning are zero-write.
6. Every write has a bounded allowlist, exact approval, stale-plan detection,
   post-write validation, receipt, and recoverable rollback where applicable.
7. Never follow symlinks or allow traversal across source, snapshot, receipt,
   preflight, plugin, or target boundaries.
8. Treat external BMAD content as untrusted evidence under Factory section 0.2.
9. A passing companion check is not Factory human Go and grants no execution,
   commit, merge, tag, release, or rollout authority.
10. Preserve unrelated worktrees and all existing private run evidence.

## Expected Proof Shape

- V1: manifest/schema checks, source metadata, path allowlists, deterministic
  build, policy lint, privacy scans, canonical-doc consistency.
- V2: state-routing matrix, install-plan fixtures, module-policy fixtures,
  promotion success/failure matrix, preflight failure matrix, concise-output
  snapshots, stale/symlink/traversal/rollback tests.
- V3: full Factory regression, package-current check, cross-package semantics,
  no-touch and protected-state verification.
- V4: isolated Claude Code plugin dependency/composition and BMAD 6.10.0
  installation/promotion/intake pilot.

## Acceptance Criteria

1. AC-01: All five starting states return one stable, correct next action with
   no mutation.
2. AC-02: New-project BMAD planning pins installer 6.10.0, Core+BMM, Claude
   Code, and excludes loop/TEA by default.
3. AC-03: Existing BMAD installs are audited without silent module changes;
   loop blocks Factory-bound intake and TEA is classified only as optional
   evidence.
4. AC-04: Only allowed upstream workflow outputs can enter an immutable,
   reusable `docs/upstream/bmad/<SNAPSHOT_ID>/` snapshot.
5. AC-05: Promotion is exact-approval, stale-safe, symlink-safe, traversal-safe,
   receipt-backed, rollback-tested, and deterministic.
6. AC-06: The raw-brief template embeds its checklist and binds every cited
   snapshot ID and digest.
7. AC-07: Project preflight fails closed on every authority, citation, digest,
   mutability, path, and promotion-evidence violation without adding a new gate.
8. AC-08: Factory 0.2.x dependency and namespaced Claude Code composition pass
   positive and negative isolated tests.
9. AC-09: Default output is concise and actionable; full JSON remains available
   as explicit evidence.
10. AC-10: No Factory Core duplication, BMAD vendoring, TEA implementation,
    customer data, hidden mutation, dependency creep, or unsupported platform
    claim is introduced.
11. AC-11: Canonical state, roadmap, changelog, onboarding, policy, and package
    documentation agree with the actual delivered boundary.
12. AC-12: The sprint closes at technical `REVIEW_READY`; live application
    installation and organization rollout remain separate decisions.

## External Source Metadata

### BMAD installer

- Source: `https://docs.bmad-method.org/how-to/install-bmad/`
- Authority: official BMAD documentation.
- Retrieved: 2026-08-10.
- Material facts: the supported installer is `npx bmad-method install`; Core and
  BMM versions follow the installer package; modules and Claude Code tooling can
  be selected non-interactively.
- Revalidation trigger: installer CLI, module codes, output paths, or version
  model changes.

### BMAD package pin

- Source: official npm registry metadata for `bmad-method@6.10.0`.
- Retrieved: 2026-08-10.
- Version: `6.10.0`.
- Published: `2026-07-03T23:57:11.757Z`.
- Tarball: `https://registry.npmjs.org/bmad-method/-/bmad-method-6.10.0.tgz`.
- Integrity:
  `sha512-Z14VEk9R7JE0d016BLPiJPNcsS/ZIu97rC/76Ahe1IN7Wkqz3pK6Frljf5/FH8NZGOBawDY5SLyCybFcPJ/eMw==`.
- Revalidation trigger: registry integrity mismatch or package withdrawal.

### Claude Code plugin dependencies

- Source: `https://code.claude.com/docs/en/plugin-dependencies`.
- Authority: official Anthropic documentation.
- Retrieved: 2026-08-10.
- Material facts: dependencies can be declared in `plugin.json` or marketplace
  entries; same-marketplace dependencies support semver constraints; missing,
  disabled, or unsatisfied dependencies surface as plugin errors.
- Revalidation trigger: dependency schema, tag-resolution, or marketplace trust
  behavior changes.

## Open Issues

### BLOCKING

- None for Factory planning. Implementation must halt if current Claude strict
  validation or live dependency behavior contradicts the documented contract.

### NON-BLOCKING

- Final public product name and exact companion version may be selected within
  the envelope if they remain customer-neutral and namespace-safe.
- A later sprint may add Codex live support after its portable plugin release
  contract is current; this may not weaken the Claude-first boundary.

## Go / No-Go

Go for implementation only if Stage I2 passes, pack-lint passes, all code and
write boundaries are explicit, and the human sponsor grants a new exact
execution authorization bound to the pack digest. Otherwise No-Go.
