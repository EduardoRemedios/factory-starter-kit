# Conductor Design Pack — 08 Rehearsal Results (2026-09-04)

Rehearsal on Eduardo's local clone of the pilot repository, sandbox branch `spike-1`, using the published 0.3.0 plugins installed from the GitHub marketplace. Evidence copies: `rehearsal/`. Origin was unreachable from the machine (credentials), so the rehearsal ran against the 27 August snapshot and nothing was pushed to the pilot repository.

## Qualification table outcome

| Step | Result | Notes |
|---|---|---|
| Q1 Golden packs | PASS | In CI and the test suite since step 1 |
| Q2 Disposable brownfield + BMAD (canonical root) | **Superseded by Q5** | The real repository exercised the same paths with a real nested BMAD tree |
| Q3 Declared root, Codex app | **Partial** | Declared root proven on the real tree (Q5); Codex desktop app not driven (no GUI automation available); Codex marketplace file ships and the plugin installed via the Claude marketplace path |
| Q4 Cursor smoke | Not run | Deferred by decision Q4 |
| Q5 Spike-1 pass one | **PASS** | Fresh adoption via marketplace plugin, G1→G2→G3 to `REVIEW_READY`, human countersigns at G1 and G3, human attestation for the manual check, fresh-context verifier, one Gap Request. Run committed on spike-1 (`83caecd`). |
| Q6 Spike-1 pass two (update from non-compliant 0.2.5) | **BLOCKED (fail-closed), as it should be for now** | `CONDUCTOR_INSTALLATION_STATE_MISSING`: 0.3.0 does not discover the Factory-era state path. Nothing was touched. Fix in 0.3.1 (F-7). Pilot impact none: the pilot repository has no prior Factory install. |
| Q7 Fresh-context verifier | PASS | Recomputed every receipt digest, re-checked each fact independently, found one defect the lint misses (F-9) |
| Q8 Countersign | PASS | Eduardo authorized INTENT_LOCK, the VM-003 attestation, and COMPLETION in chat; files record that provenance |

Acceptance criteria: AC-L1 (PRD helpers allowed), AC-L2 (party mode allowed, dev-story denied from the same session), AC-L5 (TEA design allowed, automate denied) proven by live hook decisions on the real tree; AC-L3 (declared non-root installation canonical) proven via `PROJECT_CONFIG.json`; AC-L4 (nested layout blocks authority actions only) proven before the declaration; AC-L6 (Gap Request round trip) opened but not resolved, resolution left for the product-context owner.

## Findings that become 0.3.1 work

| # | Finding | Fix |
|---|---|---|
| F-1 | An existing project `CLAUDE.md` conflicts with the pinned bridge; manual conversion to `@AGENTS.md` plus moving the guide into `AGENTS.md` was required | Treat `CLAUDE.md` like `AGENTS.md`: migrate its content into the project-owned `AGENTS.md` body and write the bridge, as one previewed action |
| F-3 | With a declared non-root BMAD installation, the pinned-profile check looks for IDE skills at the repo-root `.claude/skills`, which the split installation does not have; harnesses only load root skills anyway | Document the limitation: a declared root supports discovery and helpers; solution-context authoring needs root-level skills (copy or symlink, then digests apply). Decide with the pilot team |
| F-6 | Declaring `adapters.bmad` makes G1 lint demand the adapter schema, which only `intake` seeds, and intake can be blocked (bmad-loop) | Companion seeds its inert contract files (schemas, lane policy, policy doc) on `doctor`, independent of intake |
| F-7 | Update from a Factory 0.2.5 install is BLOCKED: legacy state path and managed paths are not discovered | Rename-aware update: discover `docs/Factory/installation/INSTALLATION_STATE.json`, plan the `docs/Factory` → `docs/Conductor` managed-set migration |
| F-9 | Constraint `source` paths are not validated; the verifier caught a dangling reference | contract-lint intent: repo-relative constraint sources must resolve |

Findings 2, 4, 5, 8 are correct behaviour or environment facts, not defects. The full log is `rehearsal/FRICTION_LOG_pass_one.md`.

## What the rehearsal did not prove

- Live hook behaviour inside an interactive Claude Code session on this repository (the packaged sentinel matrix covers the hook; the decisions here were produced by invoking the packaged hook script directly).
- Codex desktop app and Cursor surfaces.
- Anything about the spike harness's code, build, or deployment; the run was PLANNING_ONLY and scoped to three documentation requirements by design.

## Handover readiness

Ready to hand to the pilot team after the F-1 and F-6 fixes land, because both hit any real repository on day one. F-3 needs a decision from the pilot team about where their BMAD IDE skills live. F-7 and F-9 can follow in 0.3.1 without blocking the handover.
