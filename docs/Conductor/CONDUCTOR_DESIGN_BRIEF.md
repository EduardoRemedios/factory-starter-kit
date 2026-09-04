# Conductor Design Brief

Input for a PLANNING_ONLY design run. Deliverable of that run: `CONDUCTOR_DESIGN_PACK` (sections listed under "Design pack must include"). Nothing in this brief authorizes implementation, Git actions, publication, pilot, or rollout.

Brief version: 1.0 · Date: 2026-09-04 · Author: Eduardo dos Remedios · Internal only until after the pilot. Feature requests are collected from the pilot team afterwards, triaged, and P1s applied.

---

## 0. Decisions already taken (do not reopen)

| Decision | Value |
|---|---|
| Product name | **Conductor** on every user-facing surface. Internal identifiers (`docs/Factory`, `factoryctl`, plugin ids) may keep `factory` until the contract core is rebuilt. |
| Lineage | Factory 0.2.5 candidate `c23be98` (branch `codex/factory-bmad-0.2.5-solution-context`) is merged to `main` and tagged as the **last Factory-lineage release**. Conductor branches from it. MS-06 pilot qualification is **not** run; its evidence is archived as V2-lineage qualification. |
| Pilot | Oleksii's team, AuditEdge repository, sandbox branch `spike-1`. Harnesses: Claude Code CLI (primary), Cursor, Codex desktop app. |
| Party mode | Allowed in the product-context lane under the lane rules in §6. |
| Onboarding | No workshop. Self-serve: one-command install, a short guide, one practical exercise with a checkable result. |
| Rehearsal | Eduardo rehearses on the local AuditEdge clone before handover (fresh adoption, then update from the existing non-compliant 0.2.5 layout). |

---

## 1. Mission

Design Conductor: the successor to Factory V2, built for frontier models (Claude Fable 5.1, GPT-6 Astra) that need less procedural guidance but the same or stronger governance. Preserve the BMAD upstream companion capabilities Oleksii's team depends on. Produce a design pack that a build run can execute step by step.

## 2. Governing principle

**Govern authority, outcomes, and write boundaries. Do not govern steps.**

Conductor constrains three things: who may authorize what, what evidence proves a claim, and where writes may land. Everything that told the model how to think stage by stage is removed. Everything that decides authority, proof, and write boundaries is kept and strengthened.

Corollary: skill and instruction prose is soft (both vendors document that user instructions override skill text). Only deterministic validators, hooks, and CI checks are hard. Anything that must hold goes in the hard layer.

## 3. Why now (source-backed, cross-vendor)

Cite only from this table. Mark any claim with a single source as single-vendor. Do not invent capabilities.

| Claim | Anthropic (Fable 5 / 5.1 guides) | OpenAI (Astra docs / system card) | Status |
|---|---|---|---|
| Prescriptive skills degrade output | "Skills developed for prior models are often too prescriptive … and can degrade output quality. Review and consider removing older instructions if default performance is better." | Astra "stronger at general instruction following" | Verified (A). Conditional advice, not a mandate: requires ablation. |
| Models stop early / ask permission for authorized work; fix is an autonomy instruction | 5.1: "sometimes describes what it would do next instead of doing it … or stops to ask permission for a step the original request already covered." | Guidance: Astra is "more likely to ask the user a question"; fix: "bias towards action … do all the required work first so that user approval is the final step." | Verified both. Convergent. |
| Evidence-audited progress claims | "instruct Claude Fable 5 to audit progress against actual tool results … nearly eliminated fabricated status reports" | System card: misrepresentation in coding 4× lower than GPT-5.6 Sol, but "can strategically sandbag in evaluations" under adversarial elicitation | Verified both. Narration is not a safety net; artifacts are. |
| Reasoning monitorability decreased | — | System card: "substantial decrease in chain-of-thought monitorability compared to previous models" | Verified (O). Single-vendor. |
| Effort is the primary control | "Effort is the primary control for … intelligence, latency, and cost." Names do not map across models. | Astra supports low/medium/high/xhigh/max; `none` returns HTTP 400; effort changeable mid-conversation | Verified both. Record model + effort, never effort alone. |
| Scope / test-coverage creep | 5.1 "Delivering work" block; Fable 5 anti-refactor block | "Do not write tests for reversible, low-impact changes" | Verified both. SIMPLE-CODE-GATE stays verbatim. |
| Instruction files are a governed surface | User instructions override skills | Astra "can be more sensitive to instructions contained in skills and other files, such as AGENTS.md … strongly recommend auditing" | Verified both. New requirement: instruction-file audit. |
| Memory still recommended | "Construct a memory system … one lesson per file"; compaction-preservation instruction | Persisted reasoning, compaction (API-level) | Verified both. Continuity machinery is reclassified, not deleted. |
| Critical cyber capability threshold | — | "first model to reach the Critical level of cybersecurity capability under our Preparedness Framework" | Verified (O). Risk posture only: protected roots, deny-by-default hooks, and receipts stay verbatim. |

Sources: platform.claude.com prompting guides for Fable 5 and Fable 5.1; developers.openai.com model page, reasoning guide, model guidance; deploymentsafety.openai.com GPT-6 Astra system card. The openai.com launch post and Path to Astra post are blocked to automated fetch; do not cite them as verified.

## 4. Target architecture

**Layer 1 — Upstream intent.** Intent Pack (schema-validated) replaces `raw_brief.md` + Brief Review. Sources: human brief, promoted BMAD SOLUTION_CONTEXT snapshot, SPEC per backlog item.

**Layer 2 — Contract core (durable, invest).** Schemas, deterministic validators (`stage-lint`/`pack-lint` → `contract-lint`), evidence receipts, merge authorization, Statement of Completion, Gap Request. SIMPLE-CODE-GATE v2 and Hard Guardrails verbatim.

**Layer 3 — Harness adapters (thin, versioned, expected to churn).** Claude Code plugin, Codex plugin, Cursor via AGENTS.md + CLI, BMAD lane adapter, CI contract-lint action.

### The three gates

| Gate | Entry | Exit | Enforced by |
|---|---|---|---|
| **G1 Intent Lock** (human) | Intent Pack validates; prior-run recall index consulted when non-empty; project config validates (incl. declared BMAD root) | Human locks intent with digest; effort declared per gate with model id | `contract-lint intent`, human countersign file |
| **G2 Governed Execution** (autonomous) | Locked intent; verification manifest present when runnable checks exist; autonomy block loaded | All manifest checks have runner-produced receipts; no writes outside declared boundaries (postimage compare) | `contract-lint execution`, protected-postimage compare, hooks |
| **G3 Adversarial Review + Completion** | Fresh-context verifier subagent report; Statement of Completion drafted | Statement of Completion lint PASS; human countersign; handoff state `REVIEW_READY` → `MERGE_READY` per merge protocol | `contract-lint completion`, CI action, merge preflight |

Stage letters A–I2 survive only as an internal checklist inside G2. Every existing lint check must be mapped to a gate; any check with no home is flagged, not dropped.

## 5. Contracts to specify (schema sketches required)

1. **Intent Pack** — goal, constraints[], scope_in[], scope_out[], budget{effort_per_gate, model}, verification_requirements[], done_definition[] (requirement ids), sources[] (snapshot ids + digests), human_lock{digest, signer, utc}.
2. **Verification Manifest v2** — existing fields plus `result{status, receipt_path, exit_code, utc}` per check; missing manifest on an execution run is an error, not a warning.
3. **Statement of Completion** — rows keyed by Intent Pack requirement id → status ∈ {verified, partial, not_done, out_of_scope}, evidence refs (manifest check ids + receipt paths), limitations, residual gaps. Lint: every `verified` row references an existing, non-empty, PASS receipt; every `out_of_scope` row cites a human decision; derives closeout state (READY / BLOCKED / NEEDS HUMAN DECISION). Countersign file is separate and human-written.
4. **Gap Request** — run id, pack digest, originating snapshot id, requirement id, gap type ∈ {requirement, architecture, ux, product-context}, question, proposed resolution, supersession impact. Generated from `partial`/`not_done` rows; returns to the product-context lane.
5. **Project Config** (single schema-locked file) — declared BMAD root (exactly one, repo-relative, no symlink, not under `docs/`), protected roots, allowed harnesses, default effort, AGENTS.md composition mode.
6. **Lane Policy** — see §6.
7. **Evidence Receipt** — produced by the runner, not by agent prose: command, exit code, stdout digest, utc, run id.
8. **AGENTS.md composition** — managed section markers; project-owned content preserved byte-for-byte; verified in Claude Code, Codex, Cursor.

## 6. BMAD lane adapter (Oleksii's requirements → acceptance criteria)

Policy is expressed by responsibility. Two lanes, default-deny for anything unclassified.

- **Product-context lane (allowed):** any BMAD workflow whose write set stays under the BMAD output directory and that produces no delivery artifact. Includes discovery (brief, PRD, research, validate-prd, document-project), solution-context authoring (architecture, spec, UX), helpers (review-adversarial-general, review-edge-case-hunter, editorial reviews, advanced elicitation, **party mode**), and TEA design-level workflows (test-design, NFR, trace, test-review) as optional evidence.
- **Delivery lane (prohibited for Conductor-bound work):** loop, dev-story, dev-auto, quick-dev, create-story, epics/stories, sprint planning/status, code-review, correct-course, testarch automate/CI/ATDD, generate-project-context.
- **Hook rule:** evaluate the invoked skill's lane, not its parent. Nested skills in the same lane are permitted. This removes the rule that broke PRD finalization.
- **Unsafe layout rule:** nested, ambiguous, or symlinked layouts block intake, promotion, and solution-context authoring only. Discovery continues with a warning. Deny messages carry the real reason code and layout finding; the constant "Doctor was not run" text is removed.
- **Declared root:** via Project Config; digest and inertness checks apply at the declared root exactly as at `_bmad`.
- **Legacy trees:** preserved under `docs/adapters/bmad/legacy-evidence/`; never under `docs/upstream/`.
- **Promotion:** unchanged — human promotes an immutable hash-pinned snapshot; labels such as final/binding have no Conductor authority.
- **Feedback loop:** Gap Request artifact; human promotes revised snapshot; supersession rules decide whether active scope reopens.

Acceptance criteria for the adapter design: AC-L1 PRD flow with review + elicitation completes under the hook; AC-L2 party mode cannot reach a delivery-lane skill (negative proof); AC-L3 declared non-root BMAD root passes doctor and intake; AC-L4 nested legacy tree blocks only authority actions; AC-L5 TEA design output promotable as evidence, testarch-automate blocked; AC-L6 gap request round-trips to a new snapshot with supersession decision recorded.

## 7. Harness adapters and CI

- Claude Code and Codex: plugins served from the GitHub marketplace (`EduardoRemedios/factory-starter-kit`), registered in the AuditEdge repo's project settings; versions pinned in the marketplace manifest.
- Cursor: no plugin; consumes the installed AGENTS.md and CLI. Verify Cursor Team Rules do not override the Conductor section.
- **CI contract-lint action:** runs `contract-lint completion` on pull requests; requires receipts and a valid Statement of Completion for merge. Harness-neutral enforcement at the merge boundary; this is the primary answer to "we cannot block every tool".
- Instruction-file audit: contract-lint inventories every instruction-bearing file (AGENTS.md, CLAUDE.md, skills, hooks) with digests, mirroring what the BMAD adapter already does for BMAD skills.

## 8. Onboarding deliverable (replaces the workshop)

1. **Install:** one marketplace command; project settings pre-registered in spike-1.
2. **Guide:** one page. What Conductor governs, the three gates, the two lanes, the five commands.
3. **Practical exercise:** on spike-1, run a discovery workflow in BMAD, promote a snapshot, lock intent from it, run one PLANNING_ONLY G2, produce a Statement of Completion, and read the CI result. Expected outputs are listed so the tester can check themselves.
4. **Friction log** template: every point where the tester asked "what now".

## 9. Required analyses in the design pack

- **Per-boundary classification** of every existing stage boundary and preflight: "model-weakness pause" (remove) vs "human-authority gate" (keep). Only the first kind is obsoleted by frontier models.
- **Per-file disposition table:** keep / rewrite / demote-to-optional / delete, one-line reason.
- **Lint check mapping** to G1/G2/G3; orphans flagged.
- **Continuity machinery:** classify context recall (→ G1 input, risk-triggered), Mission Cursor (→ Layer 3 optional), task memory (unchanged, optional). Note only recall is mandatory today.
- **Compatibility intersection** with the 0.2.5 candidate: files both touch.
- **Working-tree drift:** the project-preflight feature exists in plugin payloads and PROJECT_STATE prose but not in the working tree; disposition it explicitly.
- **Migration sequence:** ordered, independently mergeable steps; golden-pack fixtures first.
- **Ablation note:** which removed instructions will be re-tested against the pilot friction log before the release after the pilot (three-gate collapse of stage handoffs is staged, not assumed).

## 10. Pilot scope guard

**In:** three gates, contract core schemas above, BMAD lane adapter, Project Config, Claude Code + Codex plugins, Cursor via AGENTS.md, CI action, onboarding deliverable.
**Deferred to optional modules:** Mission Mode, Kilo external lane, Product Owner lane, task memory, Agent Loop Bridge, Repo Cartographer.

## 11. Qualification (evidence-first)

1. Golden pack fixtures: archived 0.2.5 and MS-06 packs must still lint.
2. Disposable brownfield-with-BMAD adoption per harness, each a single autonomous session audited by a fresh-context verifier; protected-postimage compare after every apply.
3. Spike-1 rehearsal pass one (fresh adoption + one PLANNING_ONLY run on the ingestion-throughput spike) and pass two (update from the archived non-compliant 0.2.5 layout).
4. Countersigned Statement of Completion per pass. This replaces MS-06 as the handover authorization.

## 12. Constraints

- Planning only. No file changes, branches, commits, or installs during the design run.
- Honor the kit's own rules: smallest clear change, no silent failures, no scope beyond this brief.
- Do not import anything from the private Factory_V3 repository. If a V3 concept seems required, list it as an open question by name.
- Cite model behavior only from §3.

## 13. Open questions for human decision

1. Rename internal identifiers (`docs/Factory`, `factoryctl`, plugin ids) in 0.3.0 or in the release after.
2. Does adopting the Statement of Completion make the verification manifest mandatory on all execution runs (proposed: yes)?
3. Public GitHub marketplace vs private for the pilot.
4. Cursor: accept CLI-only operation, or add a Cursor skill wrapping doctor/progress.
5. Which TEA design-level workflows are in the product-context lane on day one.
6. Whether Gap Requests may be authored by the agent or must be human-authored.

## 14. Acceptance criteria for the design pack itself

- Every §5 contract has a field-level schema sketch.
- Every existing lint check appears in the G1/G2/G3 mapping or in the orphan list.
- Every §6 acceptance criterion maps to a qualification step in §11.
- The migration sequence's first step is the golden-pack fixture.
- Open questions are listed, not resolved by assumption.
