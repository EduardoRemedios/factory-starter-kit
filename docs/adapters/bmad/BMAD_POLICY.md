# Factory BMAD Authority Policy

Policy Version: `1.0.0`

Factory is the sole downstream SDLC authority. BMAD artifacts are drafts or
evidence, never binding instructions for Factory-bound work.

## Allowed upstream only

- Brainstorming, idea shaping, PR/FAQ, product briefs, and deep research.
- Optional PRD/UX context for larger initiatives.
- Brownfield project-context mining as context-spine input.
- Research only with source URL, type, date when available, and confidence.

The exact BMAD 6.10.0 allowlist is:

- `bmad-brainstorming`, `bmad-forge-idea`, `bmad-prfaq`, and
  `bmad-product-brief`;
- `bmad-domain-research`, `bmad-market-research`, and
  `bmad-technical-research`;
- `bmad-prd`, `bmad-create-prd`, `bmad-edit-prd`, `bmad-validate-prd`, and
  `bmad-ux`;
- `bmad-document-project` for brownfield project mining; and
- `bmad-help` for discovery under this authority policy.

Every other or unknown `bmad-*` command or skill is denied by default in an
enforcement-active repository. `bmad-generate-project-context` is solutioning,
not the approved brownfield-mining workflow, and is prohibited.

## Not authority for Factory-bound work

- BMAD spec, solution architecture, epics/stories, sprint planning,
  implementation, code-review gates, or correct-course loops.
- `bmad-loop`; its presence blocks intake.
- TEA governance. Retained TEA output may be optional Stage F evidence only.

Supported TEA `v1.21.1` may remain installed and is inventoried, but its skills
are not in the upstream invocation allowlist. Factory Stage F may accept
human-reviewed TEA output as optional evidence; TEA never becomes an execution
or quality gate.

Factory-BMAD supports the canonical root BMAD layout. A nested install such as
`bmad/_bmad`, `bmad/_bmad-output`, or `bmad/.claude/skills` is not silently
treated as absent. It blocks as `CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT` until a
human reviews whether to migrate, isolate, or authorize a separate configured
path flow.

Drafts stay in `_bmad-output/`. Human-approved snapshots live immutably at
`docs/upstream/bmad/<SNAPSHOT_ID>/`. Briefs cite snapshot ID and digest. Only
Factory locked intent binds, and cited BMAD context freezes at Brief Purple PASS.

The local Claude hooks cover direct slash-command expansion and model-initiated
`Skill` calls, including unknown future names. They protect normal and accidental
use even in bypass-permissions mode. Intentional disabling of plugins or hooks
requires protected CI/branch policy or optional enterprise managed settings;
this local companion does not claim to defeat a malicious administrator.
