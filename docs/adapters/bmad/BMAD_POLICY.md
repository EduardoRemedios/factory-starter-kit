# Conductor BMAD Authority Policy

Policy Version: `2.0.0`

## Rule

Factory is the SDLC and sole downstream authority; Conductor is its current name. BMAD artifacts are mutable authoring drafts or non-binding evidence and become citable only after human promotion to an immutable snapshot. Conductor independently locks intent (G1), governs execution against receipts (G2), and requires a countersigned Statement of Completion (G3). No BMAD label (`canonical`, `binding`, `final`, `implementation-ready`, `release approved`) carries authority.

## Lanes, not per-workflow permissions

Policy is expressed by responsibility. The machine-readable contract is `docs/adapters/bmad/lane_policy.json` (schema `docs/adapters/bmad/contracts/lane_policy.schema.json`); `conductor_bmad_policy.py` mirrors it and tests assert equality.

**Product-context lane (allowed for Conductor-bound work).** Any BMAD workflow whose write set stays beneath `_bmad-output/` and that produces no delivery artifact:

- Discovery: brainstorming, forge-idea, product-brief, PR/FAQ, market/domain/technical research, PRD create/edit/validate, document-project (brownfield mining), help.
- Solution-context authoring: `bmad-architecture`, `bmad-spec`, `bmad-ux`, permitted only when the exact installed skill and customization digests match the pinned BMAD 6.10.0 profile, overrides are inert, and the layout is canonical.
- Persona agents: analyst, PM, UX designer, architect, tech writer, while the active workflow is product-context.
- Helpers, which may nest freely inside any product-context workflow: adversarial and edge-case review, editorial reviews, advanced elicitation, party mode, sharding, indexing. PRD finalization's mandatory review step therefore works under the hook.
- Evidence-only TEA design work: test design, NFR, trace, test review, teach-me-testing. Promotable as `EVIDENCE_ONLY`; TEA output is optional Stage F evidence only and never a gate.

**Delivery lane (prohibited for Conductor-bound work).** Epics and stories, dev-story, dev-auto, quick-dev, sprint planning and status, code review, correct-course, implementation-readiness checks, retrospective, e2e generation, TEA automate/CI/ATDD/framework, generate-project-context, the deprecated `bmad-create-architecture` shim, the dev agent, the TEA agent, and `bmad-loop` (its presence blocks intake).

**Unknown `bmad-*` names are denied by default.** Neutral tooling (customize, project settings, manifest, checkpoint preview) passes without injected context; customization changes are caught by profile digests.

## The hook evaluates the invoked skill, never its parent

Each `PreToolUse(Skill)` and `UserPromptExpansion` event is classified by the lane of the skill being invoked. Same-lane nesting is permitted by construction; party mode cannot reach `bmad-dev-story` because that invocation is classified delivery and denied. The hook is an invocation gate plus explicit context, not a filesystem sandbox: write containment is proven separately by Conductor's protected-postimage compare.

Denials name the real cause: reason code, lane, layout state and reason, what is allowed in the current state, and the next concrete command.

## Layout: declared root, unsafe layouts, legacy evidence

- Exactly one active BMAD root. Default `_bmad` at the repository root; a project may declare another location in `docs/Conductor/PROJECT_CONFIG.json` → `adapters.bmad.declared_root` (repo-relative, no symlinks, not under `docs/`, directory named `_bmad`). Every digest, version, and override check applies unchanged at the declared root. A canonical `_bmad` plus a differing declared root is an unsafe multiple-roots layout.
- Nested, canonical-plus-nested, ambiguous, partial, and symlinked layouts block **authority actions only**: intake, promotion, and solution-context authoring. Discovery and helpers continue with a layout warning in their context.
- Historical installations are preserved only beneath the fixed inactive namespace `docs/adapters/bmad/legacy-evidence/`. An unpromoted legacy tree must not remain beneath `docs/upstream/`, which the context index scans. Audit produces a zero-write remediation preview; the move itself needs exact-plan approval.

## Promotion, freeze, feedback

Drafts remain in `_bmad-output/`. A human promotes selected evidence to `docs/upstream/bmad/<SNAPSHOT_ID>/` with an aggregate SHA-256. An Intent Pack cites the snapshot as an `upstream_snapshot` source; G1 locks the digest. Later BMAD changes never alter locked scope silently. Questions raised during a Conductor run return to the product-context lane as Gap Requests (`conductorctl gap open`); a resolution that supersedes active scope with a new snapshot reopens G1.
