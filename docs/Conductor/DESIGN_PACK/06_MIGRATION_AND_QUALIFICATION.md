# Conductor Design Pack — 06 Migration, Qualification, Onboarding

## 1. Migration sequence (ordered, independently mergeable)

Each step is one PR that leaves `main` green (344 tests + knowledge lint today). Steps 1–3 are additive and do not change what a valid Factory pack is; the golden-pack test guards every later step.

| # | Step | Touches | Done when |
|---|---|---|---|
| 1 | **Golden packs.** Copy `RUN_20260902_0725_*` and `RUN_20260903_1750_*` packs to `tests/golden_packs/`; test asserts pack-lint PASS on both. **Done 2026-09-04 (`87bbaf3`).** | `tests/` | Test passes; no other change |
| 2 | **Full rename (decision Q1).** `docs/Factory`→`docs/Conductor`, `factoryctl`→`conductorctl`, `scripts/factory_*.py`→`conductor_*.py`, `.agents/skills/factory-*`→`conductor-*`, plugin ids and slash namespace, `FACTORY_*`→`CONDUCTOR_*` reason codes, docs and test strings. Golden packs are **not** rewritten; pack-lint resolves `tests/golden_packs/<RUN_ID>` by direct path and accepts legacy `FACTORY_*` codes inside them. Regenerate plugin packages. | repo-wide, mechanical | 347 tests + golden packs + knowledge lint + both package checks pass under the new names; `git diff --stat` shows renames, not rewrites, for moved files |
| 2b | **Schemas + templates.** Land `docs/Conductor/contracts/*.schema.json` (from this pack), templates, `test_schemas.py` with positive and negative fixtures. | `docs/Conductor/`, `tests/` | Schemas validate templates; nothing consumes them yet |
| 3 | **INVARIANTS + autonomy block.** Create `INVARIANTS.md` with Hard Guardrails and SIMPLE-CODE-GATE byte-copied; add the managed-block composition contract and the autonomy block; AGENTS.md gains the managed block **in addition to** the current content. | `AGENTS.md`, `docs/Conductor/` | Knowledge lint still passes; test asserts verbatim copy |
| 4 | **contract-lint (parallel to pack-lint).** New `conductor_contract_lint.py` with `intent`, `execution`, `completion`; reuses pack-lint and closeout primitives; Statement of Completion at **warning** level. `conductorctl` added beside `factoryctl`. | `scripts/`, `tests/` | Both linters pass on golden packs; contract-lint passes on a new-layout fixture run |
| 5 | **Receipts runner + postimage.** `conductor_receipts.py` writes signed receipts; `conductor_postimage.py` harvested from MS-01 compare; manifest v2 accepted by contract-lint execution. | `scripts/`, `tests/` | Fixture run produces receipts; tampered receipt is rejected |
| 6 | **Project Config.** Schema-locked file; declared BMAD root plumbed into `assess_bmad_layout` (new `declared_root` state); knowledge-lint required-files list read from it. | `plugin-src/factory-bmad/runtime/`, `scripts/` | AC-L3 fixture passes; canonical-root repos unchanged |
| 7 | **Lane policy.** Rewrite `policy_classify` on `lane_policy.json`; invoked-skill rule; unsafe-layout narrowing; new deny message; invert the three tests; PT-09 sentinel. | `plugin-src/factory-bmad/`, `tests/` | AC-L1, AC-L2, AC-L4, AC-L5 fixtures pass |
| 8 | **Gap Request.** Schema in use; `conductor-bmad gap` command; supersession reopen rule in contract-lint intent. | `plugin-src/factory-bmad/`, `scripts/` | AC-L6 fixture passes |
| 9 | **Plugin runtime on the new layout.** `evaluate_progress` reads Intent Pack digest and Statement of Completion; `adopt` composes AGENTS.md managed block; seeds INVARIANTS/GATES/Project Config. | `plugin-src/factory/` | Harness-parity golden updated; setup plan differs only by CLAUDE.md bridge |
| 10 | **CI action.** `.github/workflows/conductor-contract-lint.yml` runs contract-lint completion on PRs touching `docs/Conductor/runs/**`. | `.github/` | Action green on a fixture PR; red on a tampered receipt |
| 11 | **Release surfaces.** README, onboarding titles, marketplace descriptions, versions → 0.3.0. (Identifier rename already done in step 2.) | docs, marketplaces | Docs tests updated; marketplace versions 0.3.0 |
| 12 | **Demote modules.** Move Mission Mode, Kilo, PO lane, task memory, bridge, cartographer under `modules/`; AGENTS.md read order → 2 files; delete stage-lint, handoff/pack templates, STAGE_CONTRACTS, ORCHESTRATION (hard rules relocated to GATES.md first). | broad | Golden packs still lint under compatibility mode; ablation note recorded (§3) |
| 13 | **Statement of Completion → error level.** Manifest required on execution runs. | `scripts/` | Open Question 2 decided |
| 14 | **Onboarding deliverable.** INSTALL, GUIDE, FIRST_EXERCISE, FRICTION_LOG_TEMPLATE. | `docs/Conductor/onboarding/` | Walkthrough executed by Eduardo on spike-1 (§4) |

Steps 1–5 can proceed in parallel branches after step 1 lands. Steps 6–8 are the BMAD track and depend on 2. Step 12 waits for 4–9.

## 2. Pilot scope guard

**0.3.0 (pilot):** steps 1–11 and 14. **0.3.x after pilot feedback:** 12–13, plus triaged P1 feature requests. Anything under `modules/` is not tested in the pilot.

## 3. Ablation note (brief §9)

Removed instructions are re-tested, not assumed. Record for each orphaned family (02 §4) before deletion in step 12:

| Removed control | Hypothesis | Evidence source during pilot |
|---|---|---|
| Red/Blue iteration caps and handoffs | Fresh-context verifier at G3 finds at least what two self-critique rounds found | Compare verifier findings on spike-1 pass one against the archived I2 audit reports' finding categories |
| 8-document read order | Two-file read order does not increase scope or constraint violations | Postimage compare and Statement rows on pass one and two; friction log entries mentioning "missing context" |
| Word caps | Output length is not a governance property | None needed; drop |
| Micro-sprint sequencing artifact | Agent-internal sequencing is sufficient under the autonomy block | Receipt timestamps show monotonic progress; no G2 run stalls |
| Mandatory recall report | Risk-triggered recall catches every prior BLOCKING/GO decision that mattered | Recall receipt on pass two (index non-empty) lists the archived run's decisions |

If a hypothesis fails in the pilot, the control returns in 0.3.x as a Project Config option, not as a global mandate.

## 4. Qualification (evidence-first; replaces MS-06)

| Step | Harness | Proves | Artifacts |
|---|---|---|---|
| Q1 Golden packs | CI | Lint compatibility with V2 evidence | test result |
| Q2 Disposable brownfield + BMAD 6.10 (canonical root) | Claude Code | AC-L1, AC-L2, AC-L5; adopt/doctor/validate/progress; postimage clean | receipts, hook decision log, postimage compare |
| Q3 Disposable brownfield, BMAD at declared root `tools/bmad/_bmad` | Codex desktop app | AC-L3; Codex marketplace load; AGENTS.md composition read by Codex | same |
| Q4 Disposable repo opened in Cursor (**optional smoke, decision Q4**) | Cursor | AGENTS.md managed block applied; CLI-only operation viable | screenshot + CLI receipts, if run |
| Q5 **Spike-1 pass one**: reset to `a4c1ebb`, fresh adopt, one PLANNING_ONLY run on the ingestion-throughput spike, one Gap Request | Claude Code (+ Codex, Cursor smoke) | Real-repo adoption; AC-L6; real brief through G1→G3 | full run layout, countersigned Statement |
| Q6 **Spike-1 pass two**: check out archive branch (non-compliant 0.2.5 layout), run update to 0.3.0 | Claude Code | AC-L4; update path; legacy-tree remediation preview | update receipt, postimage, Statement |
| Q7 Fresh-context verifier | subagent | Every `verified` row in Q5/Q6 Statements audited | verifier reports |
| Q8 Countersign | Eduardo | Handover authorization | `countersign/COMPLETION.json` × 2 |

Each Q step is a single autonomous session with the autonomy block loaded. No micro-stage activations, no digest-bound execution prompts. Human involvement is exactly G1 and G3 per run.

## 5. Onboarding deliverable (replaces the workshop)

**INSTALL.md** — one command per harness:

```
claude plugin marketplace add EduardoRemedios/factory-starter-kit
claude plugin install conductor-bmad@factory-starter-kit
```
Project settings in spike-1 pre-register the marketplace and enable both plugins, so teammates run only the install line. Codex: repo-scoped marketplace appears in the Plugins Directory. Cursor: nothing to install; AGENTS.md is read on open.

**GUIDE.md** — one page: what Conductor governs (authority, proof, write boundaries), the three gates, the two lanes, the five commands (`doctor`, `adopt`, `run`, `validate`, `progress`), where receipts live, what a countersign is.

**FIRST_EXERCISE.md** — on spike-1, 45 minutes, self-checked:
1. `/conductor:doctor` → expected state and reason code shown.
2. Run `bmad-product-brief` for a small feature; observe the injected non-authority context.
3. Promote the brief as a snapshot → expected `SNAPSHOT_MANIFEST.json` fields listed.
4. `/conductor:run` → G1: draft Intent Pack from the snapshot; countersign with your name.
5. G2 in PLANNING_ONLY → expected receipts directory contents listed.
6. G3 → read the derived state in the Statement of Completion; identify the one row the exercise leaves `partial` and the Gap Request it produced.
7. Open the PR → CI contract-lint result visible.
Expected outputs are printed so the tester knows if they are on track without asking.

**FRICTION_LOG_TEMPLATE.md** — one line per "what now?" moment: step, what was expected, what happened, time lost. This log is the ablation evidence in §3 and the feature-request intake for post-pilot triage.
