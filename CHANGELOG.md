# Changelog

The detailed, dated changelog lives in `docs/CHANGELOG.md`. This file keeps release-level entries.

## 0.3.3 - 2026-09-05

- Documentation housekeeping for the 0.3 line: legacy banners on 0.2-era process documents, GitHub-marketplace install text, 0.3 wording in the BMAD and lifecycle skills. No runtime behaviour change.

## 0.3.2 - 2026-09-04

- `update` migrates 0.2-era installs to the 0.3 layout with exact rollback (finding F-7).
- README rewritten for the 0.3 line. The product name is Factory; Conductor is the working name kept as plugin id and command namespace.

## 0.3.1 - 2026-09-04

- Brownfield adoption migrates a project `CLAUDE.md` into `AGENTS.md` and writes the bridge as one previewed action (F-1).
- BMAD companion `seed-contracts` seeds the inert adapter contracts independently of intake (F-6).

## 0.3.0 - 2026-09-04

- Three gates (Intent Lock, Governed Execution, Adversarial Review and Completion) replace the eleven-stage process; contract schemas, `conductorctl contract-lint`, signed evidence receipts, protected-postimage compare, Gap Requests, human countersign files.
- BMAD adapter expressed by lane; declared non-root BMAD installation; one-line denials.
- Self-serve onboarding under `docs/Conductor/onboarding/`. The 0.2 line closed at tag `factory-lineage-v0.2.5`.

## Unreleased (0.2 line, historical)

- Add a non-technical starter guide for local Factory setup with Cursor, Claude, or Codex.
- Restore this repository to Factory V2 and earlier starter-kit scope.
- Add review-ready versus merge-ready handoff discipline for async branch/PR review.

## v0.2.0 - 2026-03-21

- Refresh the starter-kit docs and specs to the latest generic Factory, Mission Mode, and optional Product Owner process shape.
- Add the continuity-recall contract across Stage A, mission checkpointing, and PO brief review.
- Replace the dead `AgentArchitecture` handoff reference with a generic execution-profile field.

## v0.1.0 - 2026-03-10

- Add Apache-2.0 licensing at the repo root.
- Clarify pre-1.0 maturity, starter-kit adaptation expectations, and first-step adoption guidance in the root README.
