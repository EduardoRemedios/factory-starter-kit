# Conductor BMAD Authority Policy

Policy Version: `2.0.0`

## Rule

Factory is the SDLC and sole downstream authority; Conductor is the working name of the 0.3 line and its command namespace. BMAD artifacts are mutable authoring drafts or non-binding evidence and become citable only after human promotion to an immutable snapshot. Conductor independently locks intent (G1), governs execution against receipts (G2), and requires a countersigned Statement of Completion (G3). No BMAD label (`canonical`, `binding`, `final`, `implementation-ready`, `release approved`) carries authority.

## Lanes, not per-workflow permissions

Policy is expressed by responsibility. The machine-readable contract is `docs/adapters/bmad/lane_policy.json` (schema `docs/adapters/bmad/contracts/lane_policy.schema.json`); `conductor_bmad_policy.py` mirrors it and tests assert equality.

**Product-context lane (allowed for Conductor-bound work).** Any BMAD workflow whose write set stays beneath `_bmad-output/` and that produces no delivery artifact:

- Discovery: brainstorming, forge-idea, product-brief, PR/FAQ, market/domain/technical research, PRD create/edit/validate, document-project (brownfield mining), help.
- Solution-context authoring: `bmad-architecture`, `bmad-spec`, `bmad-ux`, permitted only when the exact installed skill and customization digests match the reviewed version profile (6.10.0 or candidate 6.12.1-next.0), effective overrides are qualified, and the declared layout is safe. The new profile checks supporting scripts/references and TOML/YAML layers; plain user/language preferences are allowed, effect-changing overrides are blocked.
- Persona agents: analyst, PM, UX designer, architect, tech writer, while the active workflow is product-context.
- Helpers, which may nest freely inside any product-context workflow: adversarial and edge-case review, editorial reviews, advanced elicitation, party mode, sharding, indexing. The new consolidated `bmad-review` reports advisory findings only; it never grants delivery approval or substitutes for Factory G3. PRD finalization's mandatory review step therefore works under the hook.
- Evidence-only TEA design work: test design, NFR, trace, test review, teach-me-testing. Promotable as `EVIDENCE_ONLY`; TEA output is optional Stage F evidence only and never a gate.

**Delivery lane (prohibited for Conductor-bound work).** New `bmad-build`, `bmad-build-auto`, `bmad-project-context` (rewrites governance files) and `bmad-walkthrough` (can patch/approve a PR), plus Epics and stories, dev-story, dev-auto, quick-dev, sprint planning and status, legacy `bmad-code-review`, correct-course, implementation-readiness checks, retrospective, e2e generation, TEA automate/CI/ATDD/framework, generate-project-context, the deprecated `bmad-create-architecture` shim, the dev agent, the TEA agent, and `bmad-loop` (its presence blocks intake).

**One run-scoped exception: governed `bmad-testarch-automate`.** It stays classified as delivery (audits, coverage digests and snapshot citations are unchanged, so the policy version is unchanged). The hook admits it only for exact 6.12.1-next.0 TEA bytes with inert overrides, when exactly one execution-enabled run holds a G1-pinned `bmad_automation_authority.json` naming the workflow, its inputs and write roots, with current `INTENT_LOCK` and `EXECUTION_GO`, no completion, a pinned `automation-compare` check and the run's single window opened by `automation-capture`. The compare recomputes the window every time and fails on any watched change since capture outside the frozen write roots, including dependency manifests, local settings, git configuration and hooks, and the run's own records. Ignored and out-of-repository paths remain unobserved, and the check detects accidental out-of-root writes rather than deliberate tampering with Factory's own evidence files. TEA coverage, gate and approval statements stay advisory; generated tests count only through the run's pinned checks. ATDD, framework, CI and the TEA agent remain prohibited. See `docs/adapters/bmad/BMAD_GOVERNED_AUTOMATION.md`.

**Unknown `bmad-*` names are denied by default.** Neutral tooling (customize, project settings, manifest, checkpoint preview) passes without injected context; customization changes are caught by profile digests.

## The hook evaluates the invoked skill, never its parent

Each `PreToolUse(Skill)` and `UserPromptExpansion` event is classified by the lane of the skill being invoked. Same-lane nesting is permitted by construction; party mode cannot reach `bmad-dev-story` because that invocation is classified delivery and denied. The hook is an invocation gate plus explicit context, not a filesystem sandbox: write containment is proven separately by Conductor's protected-postimage compare.

Denials name the real cause: reason code, lane, layout state and reason, what is allowed in the current state, and the next concrete command.

## Layout: declared root, unsafe layouts, legacy evidence

- Exactly one active BMAD root. Default `_bmad` at the repository root; a project may declare another location in `docs/Conductor/PROJECT_CONFIG.json` → `adapters.bmad.declared_root` (repo-relative, no symlinks, not under `docs/`, directory named `_bmad`). Every digest, version, and override check applies unchanged at the declared root. A canonical `_bmad` plus a differing declared root is an unsafe multiple-roots layout.
- Nested, canonical-plus-nested, ambiguous, partial, and symlinked layouts block **authority actions only**: intake, promotion, and solution-context authoring. Legacy 6.10.0 discovery/helpers retain their layout-warning behaviour. New 6.12.1 workflows require the qualified layout and complete dependencies before loading.
- Historical installations are preserved only beneath the fixed inactive namespace `docs/adapters/bmad/legacy-evidence/`. An unpromoted legacy tree must not remain beneath `docs/upstream/`, which the context index scans. Audit produces a zero-write remediation preview; the move itself needs exact-plan approval.

## Promotion, freeze, feedback

Drafts remain in the declared BMAD output root (`_bmad-output/` or the corresponding nested path). A human promotes selected evidence to `docs/upstream/bmad/<SNAPSHOT_ID>/` with an aggregate SHA-256. A Spec with repository companions can be approved as committed content plus its Git commit (`--git-binding`) so a descendant implementation checkout verifies it locally (`verify-checkout`) without a second content approval; root-bound snapshots keep their original contract. An Intent Pack cites the snapshot as an `upstream_snapshot` source; G1 locks the digest. Later BMAD changes never alter locked scope silently. Questions raised during a Conductor run return to the product-context lane as Gap Requests (`conductorctl gap open`); a resolution that supersedes active scope with a new snapshot reopens G1.
