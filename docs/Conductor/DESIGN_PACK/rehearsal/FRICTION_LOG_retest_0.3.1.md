# Friction log — Conductor 0.3.1 re-test (spike-1, 2026-09-04, evening)

Plugins installed and updated from the GitHub marketplace (0.3.0 -> 0.3.1). Every command below ran from the installed plugin cache, the bytes a pilot user receives.

| # | Step | What I expected | What happened | Time lost | Severity |
|---|---|---|---|---|---|
| 1 | Brownfield preview on clean spike-1 with the real `CLAUDE.md` | PLAN_READY | PLAN_READY: `AGENTS.md` compose, `CLAUDE.md` migrate_bridge, 109 creates, no conflicts. No manual conversion (F-1 fixed). | 0 | none |
| 2 | Apply by plan ID | APPLIED | APPLIED with receipt; `AGENTS.md` = project guide + managed block; `CLAUDE.md` = `@AGENTS.md`; only `CLAUDE.md` modified among tracked files. | 0 | none |
| 3 | Doctor / progress | COMPATIBLE / READY_TO_INITIALIZE | as expected | 0 | none |
| 4 | Declare `bmad/_bmad`, BMAD doctor | BOTH_PRESENT | BOTH_PRESENT, next: audit | 0 | none |
| 5 | `seed-contracts` preview, apply, re-preview | 4 creates, APPLIED, CURRENT | as expected; receipt written (F-6 fixed) | 0 | none |
| 6 | G1 lint with declared adapter | PASS INTENT_DRAFT | PASS INTENT_DRAFT, no hand-copied files | 0 | none |
| 7 | Hook decisions (installed companion) | lanes as designed | product-brief, party-mode, testarch-test-design allowed with context; dev-story and testarch-automate denied naming lane and layout | 0 | none |

Remaining known items from pass one: F-3 (declared-root IDE skills location, pilot-team decision), F-7 (update from Factory installs), F-9 (constraint source validation). Audit still blocks intake on `bmad-loop` in the legacy tree, correctly.
