# Factory BMAD Authority Policy

Policy Version: `1.1.0`

## Rule

Factory is the SDLC and sole downstream authority. BMAD artifacts are mutable authoring drafts or non-binding evidence and become citable only after human promotion to an immutable snapshot. Factory independently hardens intent and scope, creates the implementation and verification pack, and requires exact-pack human Go before execution.

## Allowed upstream use

- Brainstorming, idea shaping, PR/FAQ, and product briefs.
- Deep research with source URL, source type, publication date when available, and confidence.
- Optional PRD context for larger initiatives.
- Brownfield project-context mining as input to the Factory context-spine audit.

## Allowed solution-context authoring

- BMAD 6.10.0 UX, architecture, and spec may author candidate product solution context only when the exact installed skill/customization profile passes the Factory-BMAD invocation gate.
- These workflows write mutable drafts beneath `_bmad-output/`; their `canonical`, `binding`, `final`, `build substrate`, or `implementation-ready` labels have no Factory authority.
- Architecture and spec are promotable only through schema-v2 `SOLUTION_CONTEXT` / `EVIDENCE_ONLY` snapshots. Promotion does not accept their claims, lock Factory intent, or authorize delivery.
- A parent workflow cannot authorize a nested skill. External/design handoffs, callbacks, and downstream recommendations remain outside the Factory-bound authoring lane.

For BMAD 6.10.0, the exact allowed command/skill names are enforced by
`scripts/factory_bmad_policy.py`. Solution-context invocation additionally
requires exact BMAD version, installed skill/customization digests,
files-manifest declaration, and inert project/user overrides.
`bmad-document-project` is the brownfield
mining workflow. `bmad-generate-project-context` is solutioning and is therefore
prohibited for Factory-bound work.

## Prohibited authority for Factory-bound work

- BMAD architecture or spec as binding, final, implementation-ready, or execution-authorizing artifacts.
- The deprecated `bmad-create-architecture` forwarding shim.
- BMAD epics/stories, sprint planning/status, implementation, unattended/quick development, code-review gates, or correct-course loops.
- `bmad-loop`; its presence blocks Factory intake.
- TEA as governance. If retained later, TEA output is optional Stage F evidence only.

## Promotion and freeze

Drafts remain in `_bmad-output/`. A human promotes selected evidence to `docs/upstream/bmad/<SNAPSHOT_ID>/`. A Factory brief cites the snapshot ID and aggregate SHA-256. Stage D produces `INTENT_LOCKED`; only later human Go against the exact E-I2 pack produces `EXECUTION_AUTHORIZED`. Cited BMAD context freezes at Brief Purple PASS.

The runtime hook is an invocation gate plus explicit context, not a filesystem sandbox. Complete write-set qualification occurs separately in disposable repositories before rollout.

## Canonical layout and legacy evidence

- `_bmad` at repository root is the only active BMAD installation root. Configurable or nested active roots are unsupported.
- Nested, canonical-plus-nested, ambiguous, partial, and active-root-symlink layouts fail closed before intake or solution-context authoring.
- Historical installations may be preserved only beneath the fixed inactive namespace `docs/adapters/bmad/legacy-evidence/`. Content there is evidence only and must not be loaded as BMAD capability or cited as promoted Factory context.
- The current Factory context index includes Markdown beneath `docs/upstream/**` and does not provide a per-subtree exclusion. Therefore an unpromoted legacy tree must not remain beneath `docs/upstream/`.
- Audit produces a zero-write remediation preview for a nested installation. It records the proposed namespaced target, source path/hash inventory, target collision, and repository link impacts; it does not move, copy, delete, rewrite, chmod, or symlink anything.
- Only human-reviewed immutable snapshots beneath `docs/upstream/bmad/` are intended to enter Factory recall. A future relocation or link repair requires separate approval and fresh before/after evidence.
