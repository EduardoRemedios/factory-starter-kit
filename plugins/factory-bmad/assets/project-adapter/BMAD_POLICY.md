# Factory BMAD Authority Policy

Policy Version: `1.0.0`

## Rule

Factory is the SDLC and sole downstream authority. BMAD artifacts are drafts or evidence and become citable only after human promotion to an immutable snapshot.

## Allowed upstream use

- Brainstorming, idea shaping, PR/FAQ, and product briefs.
- Deep research with source URL, source type, publication date when available, and confidence.
- Optional PRD and UX context for larger initiatives.
- Brownfield project-context mining as input to the Factory context-spine audit.

For BMAD 6.10.0, the exact allowed command/skill names are enforced by
`scripts/factory_bmad_policy.py`. `bmad-document-project` is the brownfield
mining workflow. `bmad-generate-project-context` is solutioning and is therefore
prohibited for Factory-bound work.

## Prohibited authority for Factory-bound work

- BMAD spec as a competing binding artifact.
- BMAD solution architecture, epics/stories, sprint planning, implementation, code-review gates, or correct-course loops.
- `bmad-loop`; its presence blocks Factory intake.
- TEA as governance. If retained later, TEA output is optional Stage F evidence only.

## Promotion and freeze

Drafts remain in `_bmad-output/`. A human promotes selected evidence to `docs/upstream/bmad/<SNAPSHOT_ID>/`. A Factory brief cites the snapshot ID and aggregate SHA-256. Only locked Factory intent binds. Cited BMAD context freezes at Brief Purple PASS.
