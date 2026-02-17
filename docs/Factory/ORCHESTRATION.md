# docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (v2.6)

## Version
v2.6

## Change Log
- v2.6 (2026-02-14): Added hard execution-enable contract with `PLANNING_ONLY` default, required run-root `EXECUTION_MODE.txt`, and explicit opt-in gating for execution prompt generation and downstream run fan-out.
- v2.5 (2026-02-12): Added external research safety protocol for research-heavy runs, deterministic skill-invocation directive for critical gates (D/J/I2), and made execution prompt generation required post-I2 PASS + human GO via `EXECUTION_PROMPT_TEMPLATE.md`.
- v2.4 (2026-02-11): Added mandatory pre-run knowledge-lint gate (`scripts/knowledge_lint.sh`) and run-root evidence artifact (`KNOWLEDGE_LINT.txt`). Added repo-local `AGENTS.md` as a required pre-run context map.
- v2.3 (2026-02-11): Added a planning-first operating principle trial (`§0.1`) to formalize systems-thinking order of work (intent -> constraints -> verification -> spikes -> execution) for planning-heavy and expansion sprints.
- v2.2 (2026-02-10): Corrected envelope artifact naming references to `<SPRINT_ID>_ENVELOPE.md` and `<SPRINT_ID>_ENVELOPE_REDTEAM.md` to prevent double-prefix generation.
- v2.1 (2026-02-09): Updated cross-run memory protocol. `SCRATCHPAD.md` is now a governed pitfalls index (read `Active Pitfalls` only). Run narratives moved to `runs/<RUN_ID>/RETRO.md`. Added run-structure and pre-run guidance updates.
- v2 (2026-02-08): **Breaking: reordered Stage J before Stage I2** to resolve circular dependency. Added §6.1 (Execution Prompt Generation). Added §11 (Lessons from First Run). Updated stage execution flow to match STAGE_CONTRACTS v4.
- v1 (2026-02-07): Initial orchestration guide for running the Factory pipeline with Claude Code agent teams.

## 0. Purpose
This document tells you **how to run the Factory pipeline end-to-end**. It is the operational companion to the spec documents (`NAMING_CONVENTIONS.md`, `DEFINITIONS.md`, `STAGE_CONTRACTS.md`) and the artifact templates (`docs/Factory/templates/`).

Read this document before starting a Factory run. Also read `docs/Factory/SCRATCHPAD.md` `## Active Pitfalls (Mandatory)` before starting. Historical narratives are optional and live in per-run `RETRO.md` files.

## 0.1 Planning-First Operating Principle (Trial)
When a sprint includes high uncertainty, feature expansion, or architecture-sensitive design, the default mode is planning-first rather than implementation-first.

Required planning order:
1. **Intent framing first**: define target outcomes, non-goals, and acceptance boundaries.
2. **Constraint lock second**: make invariants, policy limits, and fail-closed requirements explicit before design details.
3. **Verification design third**: define checks, fixtures, and traceability before implementation planning.
4. **Research spikes fourth**: time-box unknowns with explicit questions and required outputs.
5. **Execution last**: start coding only after planning artifacts pass Purple + human go/no-go gates.

This trial policy is especially applicable to post-F planning spikes (for example sportsbook depth, UI contract design, and support flow design), where decision quality has higher leverage than raw execution speed.

## 0.2 External Research Safety Protocol (HARD for research-heavy runs)
When a run includes web research, market intelligence, or third-party source synthesis, apply these controls:
1. Define a per-run domain allowlist in `raw_brief.md` or `pack/intent.md` before research starts. Any source outside this allowlist is BLOCKING unless explicitly approved.
2. Treat external content as untrusted. Do not copy executable snippets, credentials, or secrets into prompts or artifacts.
3. Every non-trivial external claim must include evidence metadata (URL, source type, publish date, confidence).
4. Quote minimally. Prefer summaries and explicit inference markers over long copied passages.
5. If evidence is weak or contradictory, record the gap explicitly as BLOCKING/NON-BLOCKING instead of normalizing uncertainty away.

## 0.3 Execution Enablement Contract (HARD)
Factory runs are planning-first and default to **PLANNING_ONLY**.

Execution mode policy:
1. Root Planner MUST persist run execution mode in run root `EXECUTION_MODE.txt`.
2. Default mode is `PLANNING_ONLY` unless raw brief explicitly enables execution.
3. The following raw-brief lines are required to enable execution:
   - `Execution Mode: EXECUTION_ENABLED`
   - `Execution Authorization: <human-approved reference>`
4. Downstream run fan-out requires additional explicit approval:
   - `Downstream Fan-Out: APPROVED`
5. If any required field is missing or malformed, mode remains `PLANNING_ONLY`.
6. In `PLANNING_ONLY`, generating `EXECUTION_PROMPT.md` or initializing downstream runs is forbidden and must halt as a policy violation.

## 1. Prerequisites
Before a run can start, you need:
1. **A raw brief** — a short document (written by Eduardo) describing the high-level goal, scope, and any hard constraints for the upcoming sprint. This is the seed input.
2. **The Harmony product doc spine** — the Factory pipeline references these as source material:
   - `docs/Harmony_V2_Vision_v2.md` (product vision)
   - `docs/HARMONY_V2_SYSTEM_INVARIANTS.md` (non-negotiable invariants)
   - `docs/HARMONY_V2_POLICY_PACK_SPEC.md` (policy pack structure)
   - `docs/HARMONY_V2_EVIDENCE_AND_RECEIPT_SPEC.md` (evidence/receipt spec)
   - `docs/USERLAND_CONTRACT_v0.md` (action registry + decision contract)
   - `docs/CONFORMANCE_TEST_MATRIX.md` (conformance tests)
   - UKGC policy packs (markdown + YAML)
   - Prior sprint artifacts in `docs/sprints/` (for continuity)
3. **The Factory specs** — loaded by the orchestrating agent:
   - `docs/Factory/Spec/NAMING_CONVENTIONS.md`
   - `docs/Factory/Spec/DEFINITIONS.md`
   - `docs/Factory/Spec/STAGE_CONTRACTS.md`
   - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md`
4. **The Factory templates** — used to instantiate each artifact:
   - All files in `docs/Factory/templates/`
5. **The repository context map** — loaded before execution:
   - `AGENTS.md` (root; canonical read order, hard guardrails, and command map)
6. **Knowledge lint preflight script**:
   - `scripts/knowledge_lint.sh` (must pass before Stage A starts)

## 2. Run Initialization
The Root Planner agent performs these steps before any stage begins:

### 2.1 Generate run identifiers
- **RUN_ID**: `RUN_YYYYMMDD_HHMM_factory` (use actual date/time; no placeholders).
- **SPRINT_ID**: assigned later in Stage H (not needed at initialization).

### 2.2 Create run directory structure
```
docs/Factory/runs/<RUN_ID>/
├── raw_brief.md          ← copy of Eduardo's raw brief
├── RETRO.md              ← run-local retrospective (optional at runtime)
├── KNOWLEDGE_LINT.txt    ← pre-run lint output (required)
├── EXECUTION_MODE.txt    ← `PLANNING_ONLY` (default) or `EXECUTION_ENABLED`
├── SPRINT_ID.txt         ← created in Stage H
└── pack/
    ├── intent.md
    ├── intent_redteam.md
    ├── intent_synthesis.md
    ├── intent_lock_report.md
    ├── premortem.md
    ├── risk_register.md
    ├── verification_plan.md
    ├── micro_sprints.md
    ├── traceability_matrix.md
    ├── <SPRINT_ID>_ENVELOPE.md
    ├── <SPRINT_ID>_ENVELOPE_REDTEAM.md
    ├── PACK_AUDIT_REPORT.md
    ├── PACK_MANIFEST.md
    ├── PACK_CHECKLIST.md
    ├── fixtures/
    │   └── <AREA>/<NAME>/
    │       ├── input.json
    │       ├── expected.json
    │       └── notes.md
    └── HANDOFF/
        ├── HANDOFF_STAGE_A.md
        ├── HANDOFF_STAGE_B.md
        ├── ...
        └── HANDOFF_STAGE_J.md
```

### 2.3 Validate prerequisites
- Confirm raw brief is non-empty.
- Confirm all Factory specs and templates are readable.
- Confirm the Harmony product doc spine is accessible.
- Confirm root `AGENTS.md` exists and is non-empty.
- Confirm `docs/Factory/SCRATCHPAD.md` has a non-empty `Active Pitfalls` section (governed cross-run memory).
- Run `bash scripts/knowledge_lint.sh` and write output to `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`.
- Derive execution mode from `raw_brief.md` per §0.3 and persist it as `docs/Factory/runs/<RUN_ID>/EXECUTION_MODE.txt`.
- If mode is `PLANNING_ONLY`, do not initialize downstream runs and do not generate `EXECUTION_PROMPT.md`.
- If any prerequisite fails: HALT and report to Eduardo.

## 3. Role-to-Agent Mapping
The Factory pipeline uses specialist roles. Each role is played by a separate agent (or sub-agent) to enforce separation of concerns.

| Role | Responsibility | Stages Active |
|------|---------------|---------------|
| **Root Planner** | Orchestrates the pipeline. Enforces stage contracts, validates entry/exit criteria, manages handoffs, ensures completeness. Does NOT generate artifact content. | All stages |
| **Intent Contractor** | Converts raw brief into contract-grade `intent.md`. Sources requirements, tags inferred items, defines scope/non-goals/acceptance criteria. | A |
| **Red Team** | Attacks artifacts for gaps, contradictions, ambiguity, agent failure modes, verification holes. Findings only — no solutions. | B, I |
| **Blue Team / Synthesis** | Hardens artifacts based on Red Team findings. No scope expansion (any new requirement tagged `[SCOPE EXPANSION]` + BLOCKING). Produces synthesis summaries. | C, I |
| **Purple Team** | Adjudicates Red/Blue disputes. Evaluates the Purple Gate Checklist. Issues PASS/CONDITIONAL PASS/FAIL. Checklist-based gating only — no vibes. | D, I2 |
| **Risk Analyst** | Produces premortem and risk register from locked intent. | E |
| **Verification Specialist** | Creates fixtures, verification plan, and traceability matrix. Ensures every Critical/High constraint has coverage. | F |
| **Sprint Planner** | Sequences micro-sprints with entry/exit criteria, stop/go gates, and bounded deferral hooks. | G |
| **Envelope Author** | Produces the sprint envelope (execution contract) with file-touch budgets, verification steps, and rollback criteria. | H |
| **Pack Consolidator** | Mechanical packaging: manifest + checklist + non-empty validation. No adjudication. | J |

### 3.1 Agent instructions
Each agent MUST be provided with:
- This orchestration guide (for pipeline context).
- The relevant stage contract from `STAGE_CONTRACTS.md` (entry criteria, inputs, outputs, exit criteria).
- The relevant template(s) from `docs/Factory/templates/`.
- The `DEFINITIONS.md` file (size caps, impact rubric, bounded deferral rules, placeholder rules).
- The specific input artifacts for their stage (as defined in `STAGE_CONTRACTS.md`, marked LOAD or DISK).

Determinism directive for critical gates:
- For STAGE_D, STAGE_J, and STAGE_I2, the stage prompt MUST include explicit skill invocation when a relevant skill exists:
  - `Use the <skill name> skill.`
- If no relevant skill exists, the prompt MUST say so explicitly:
  - `No dedicated skill applies; execute via stage contract only.`

### 3.2 Context loading
- **LOAD** inputs: the agent MUST read and summarize these before writing outputs.
- **DISK** inputs: these must exist on disk; the agent may consult them as needed.

## 4. Stage-by-Stage Execution Flow

### Stage A — Intent Contracting
- **Actor**: Intent Contractor
- **Input**: `raw_brief.md` (LOAD)
- **Output**: `pack/intent.md` (v1)
- **Key rules**: Source every requirement (`[SOURCE:RAW]` or `[INFERRED]`). Tag open questions BLOCKING/NON-BLOCKING. Include Version + Change Log headers.
- **Exit**: intent.md has Purpose, Goal, Non-goals, Principles, Roles, Acceptance Criteria, Go/No-Go rule.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_A.md`

### Stage B — Red Team (Intent)
- **Actor**: Red Team
- **Input**: `pack/intent.md` (LOAD)
- **Output**: `pack/intent_redteam.md`
- **Key rules**: Findings only — no solutions. Include severity, why it matters, fix recommendation. Include agent failure modes and verification holes.
- **Iteration**: `Iteration: 1 of max 2` (may cycle with Stage C up to 2 times).
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_B.md`

### Stage C — Blue Team + Synthesis (Intent)
- **Actor**: Blue Team / Synthesis
- **Input**: `pack/intent.md` (LOAD), `pack/intent_redteam.md` (LOAD)
- **Output**: Updated `pack/intent.md` (v2+), `pack/intent_synthesis.md`
- **Key rules**: No scope expansion. Any net-new requirement tagged `[SCOPE EXPANSION]` + BLOCKING. No unresolved Critical findings remain, or they are marked BLOCKING for Purple.
- **Iteration**: `Iteration: 1 of max 2` (cycles with Stage B).
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_C.md`

### Red/Blue Cycling (B + C)
- Max **2** Red/Blue cycles.
- After the cap, proceed to Stage D with the current state. Purple adjudicates.
- Root Planner tracks iteration count and enforces the cap.

### Stage D — Purple Gate (Intent Lock)
- **Actor**: Purple Team
- **Input**: `pack/intent.md` (LOAD), `pack/intent_redteam.md` (LOAD), `pack/intent_synthesis.md` (LOAD)
- **Output**: `pack/intent_lock_report.md`
- **Template**: `INTENT_LOCK_REPORT_TEMPLATE.md`
- **Key rules**: Evaluate against `PURPLE_GATE_CHECKLIST.md` (Critical items). Record PASS/CONDITIONAL PASS/FAIL with reasons. Any bounded deferral must have a micro-sprint hook.
- **Gate**: If FAIL → HALT pipeline. Report to Eduardo with reasons and required changes.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_D.md`

### Stage E — Pre-mortem + Risk Register
- **Actor**: Risk Analyst
- **Input**: locked `pack/intent.md` (LOAD), `pack/intent_lock_report.md` (DISK)
- **Output**: `pack/premortem.md`, `pack/risk_register.md`
- **Key rules**: List top failure scenarios and mitigations. Risk register includes severity, mitigation, and verification hook.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_E.md`

### Stage F — Verification Assets
- **Actor**: Verification Specialist
- **Input**: locked `pack/intent.md` (LOAD), `pack/risk_register.md` (LOAD), `pack/intent_lock_report.md` (DISK)
- **Output**: `pack/fixtures/...`, `pack/verification_plan.md`, `pack/traceability_matrix.md`
- **Template**: `docs/Factory/templates/TRACEABILITY_MATRIX_TEMPLATE.md`
- **Key rules**: Every Critical/High constraint must have at least one fixture/test/check. Fixtures follow naming conventions (§7). Domain areas only if listed in intent scope.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_F.md`

### Stage G — Micro-sprint Sequencing
- **Actor**: Sprint Planner
- **Input**: `pack/intent.md` (LOAD), `pack/risk_register.md` (LOAD), `pack/verification_plan.md` (LOAD), `pack/traceability_matrix.md` (DISK), `pack/intent_synthesis.md` (DISK)
- **Output**: `pack/micro_sprints.md`
- **Key rules**: Each micro-sprint has objective, inputs, outputs, entry criteria, exit criteria, stop/go gate. Reference bounded deferral hooks where applicable.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_G.md`

### Stage H — Sprint Envelope
- **Actor**: Envelope Author
- **Input**: `pack/intent.md` (LOAD), `pack/micro_sprints.md` (LOAD), `pack/verification_plan.md` (LOAD), `pack/traceability_matrix.md` (DISK)
- **Output**: `SPRINT_ID.txt` (run root), `pack/<SPRINT_ID>_ENVELOPE.md`
- **Template**: `SPRINT_ENVELOPE_TEMPLATE.md`
- **Key rules**: Assign SPRINT_ID (`SPRINT_YYYYMMDD_NNN`). Include file-touch budgets per micro-sprint and total. Include verification steps before merge. Include explicit stop/go gates.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_H.md`

### Stage I — Red/Blue on Envelope + Verification
- **Actor**: Red Team (attack), then Blue Team (harden)
- **Input**: `pack/<SPRINT_ID>_ENVELOPE.md` (LOAD), `pack/verification_plan.md` (LOAD), `pack/traceability_matrix.md` (LOAD), `pack/micro_sprints.md` (LOAD), `pack/fixtures/` (DISK), `pack/risk_register.md` (DISK), `pack/intent_lock_report.md` (DISK)
- **Output**: `pack/<SPRINT_ID>_ENVELOPE_REDTEAM.md`, updated envelope (v2+ if changed), updated verification assets if needed
- **Template**: `SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md`
- **Iteration**: Max 2 Red/Blue cycles. After cap, proceed to Stage I2.
- **Key rules**: No Purple adjudication here. Any `[SCOPE EXPANSION]` is BLOCKING and carried to Purple.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_I.md`

### Stage J — Pack Consolidation (runs BEFORE I2)
- **Actor**: Pack Consolidator
- **Input**: all pack artifacts except PACK_AUDIT_REPORT.md (DISK)
- **Output**: `pack/PACK_MANIFEST.md`, `pack/PACK_CHECKLIST.md`
- **Templates**: `PACK_MANIFEST_TEMPLATE.md`, `PACK_CHECKLIST_TEMPLATE.md`
- **Key rules**: Mechanical packaging only. List all required files and confirm non-empty. Checklist items match spec 1:1. PACK_AUDIT_REPORT.md is listed in the manifest as "pending — produced by STAGE_I2."
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_J.md`
- **Why J runs before I2**: STAGE_I2 (Purple Audit) requires PACK_CHECKLIST.md as a LOAD input. The checklist must exist before the audit can evaluate it. This was a circular dependency in v1 that was discovered and worked around during the first live run (RUN_20260208_1400_factory).

### Stage I2 — Purple Audit (Pack Gate, runs AFTER J)
- **Actor**: Purple Team
- **Input**: Full pack (LOAD: intent, lock report, envelope, traceability, verification plan, micro-sprints, PACK_CHECKLIST, PACK_MANIFEST; DISK: everything else)
- **Output**: `pack/PACK_AUDIT_REPORT.md`, updated `pack/PACK_MANIFEST.md` (confirms audit report exists)
- **Template**: `PACK_AUDIT_REPORT_TEMPLATE.md`
- **Key rules**: Evaluate via PACK_CHECKLIST (instantiation of PURPLE_GATE_CHECKLIST). Record PASS/CONDITIONAL PASS/FAIL. No PASS if any `[SCOPE EXPANSION]` remains unapproved. After producing the audit report, update PACK_MANIFEST.md to mark PACK_AUDIT_REPORT.md as present and non-empty.
- **Gate**: If FAIL → HALT pipeline. Report to Eduardo with reasons.
- **Handoff**: `pack/HANDOFF/HANDOFF_STAGE_I2.md`

## 5. Human Review Gate
After Stage I2 completes, the full pack is ready for Eduardo's review.

### 5.1 What Eduardo receives
- The complete pack directory at `docs/Factory/runs/<RUN_ID>/pack/`
- Key documents to review first:
  1. `PACK_CHECKLIST.md` — binary go/no-go items with evidence pointers
  2. `PACK_AUDIT_REPORT.md` — Purple's verdict and rationale
  3. `intent.md` — the locked intent (scope, constraints, acceptance criteria)
  4. `<SPRINT_ID>_ENVELOPE.md` — the execution contract
  5. `micro_sprints.md` — the execution sequence

### 5.2 Eduardo's decision
- **"Go" (planning-only run)**: pack is approved as planning evidence only; no downstream run fan-out and no execution prompt generation.
- **"Go" (execution-enabled run)**: sprint executes against the pack; envelope and micro-sprints become the execution contract.
- **"No-go" with feedback**: Eduardo provides specific feedback. The Root Planner re-runs affected stages (respecting the intent unlock protocol if the locked intent must change).

## 6. Sprint Execution (Post-Factory)
Execution starts only when Eduardo says "go" **and** run mode is `EXECUTION_ENABLED`:
- The **envelope** defines scope, constraints, file-touch budgets, and acceptance criteria.
- The **micro-sprints** define the execution sequence with stop/go gates.
- The **verification plan** and **traceability matrix** define what must be tested.
- The **fixtures** provide golden test inputs/outputs.
- Agents reference the Harmony product doc spine (invariants, policy pack spec, evidence spec) as source-of-truth for implementation decisions.

The Factory pipeline does NOT execute the sprint. It only produces the pack that governs execution.
If run mode is `PLANNING_ONLY`, Factory output is terminal planning evidence for that run.

### 6.1 Execution Prompt Generation (execution-enabled runs only)
After Stage I2 PASS, Eduardo's explicit "Go", and `EXECUTION_MODE.txt = EXECUTION_ENABLED`, the Root Planner MUST generate a self-contained **execution prompt** that can be pasted into a fresh agent session.

Generation contract:
- Use `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md`.
- Instantiate into `docs/Factory/runs/<RUN_ID>/EXECUTION_PROMPT.md`.
- No placeholders may remain.
- If `EXECUTION_MODE.txt = PLANNING_ONLY`, this step is skipped by contract.

This prompt must include:

1. **File reading order** — all pack artifacts and product context docs the execution agent must read before writing code.
2. **Micro-sprint sequence** — the step-by-step execution plan with gate checks between each step.
3. **Detailed data shapes** — inline the critical schemas (ToolCall, ToolResult, TER fields, reason code mappings) so the agent doesn't have to hunt for them across multiple docs.
4. **Hard guardrails** — explicit "do not violate" rules derived from Critical constraints and known agent failure modes.
5. **Troubleshooting guidance** — what to do when stuck (e.g., "if tests break, the schema change is not backward-compatible").
6. **Exit checklist** — what to report after the final gate passes.
7. **Skill routing contract** — which skill(s) are mandatory for execution subtasks and the explicit deterministic directive format (`Use the <skill name> skill.`).
8. **External research safety constraints** (if the sprint includes research) — run allowlist, evidence metadata requirements, and untrusted-content handling rules.

When referencing cross-run memory in execution prompts, point to `docs/Factory/SCRATCHPAD.md` and explicitly instruct reading only `## Active Pitfalls (Mandatory)`.

Store the prompt at `docs/Factory/runs/<RUN_ID>/EXECUTION_PROMPT.md` for traceability.

The execution prompt bridges the Factory's planning output and the execution agent's implementation session. Without it, the execution agent must navigate 15+ documents independently, increasing the risk of missed constraints or misinterpreted scope.

## 7. Error Handling

### 7.1 Stage failure
If a stage fails its exit criteria:
- Retry within the iteration cap (max 2 for cycle stages B, C, I).
- If retry fails: HALT and report to Eduardo with the failure reason and the stage handoff.

### 7.2 Dependency conflict or contradiction
If a downstream stage discovers a conflict with a locked artifact:
- HALT and surface to Eduardo.
- Do NOT silently patch or work around contradictions.

### 7.3 Intent unlock
If downstream work reveals the locked intent is flawed:
- Intent unlock requires Purple + Eduardo approval.
- A new `intent.md` version is created with a change log entry.
- All downstream stages (E through J) must re-run against the updated intent.

### 7.4 Snapshot / rollback
Each stage must snapshot its inputs and outputs before writing. If validation fails, revert to the prior snapshot before retrying.

### 7.5 Unauthorized execution/fan-out attempt
If any agent attempts execution prompt generation or downstream run initialization while `EXECUTION_MODE.txt = PLANNING_ONLY`:
- HALT immediately.
- Record the violation in the current stage handoff as BLOCKING.
- Require explicit human authorization update before continuing.

## 8. Handoff Protocol
Every stage produces a handoff file at `pack/HANDOFF/HANDOFF_STAGE_<CODE>.md` using the `HANDOFF_STAGE_TEMPLATE.md`.

The handoff MUST include:
- Outputs produced (paths)
- Changes made (bullets)
- Assumptions (bullets)
- Open issues (BLOCKING / NON-BLOCKING)
- Verification steps recommended (bullets)
- Exit criteria PASS/FAIL
- Iteration metadata (for cycle stages)

The Root Planner reads each handoff before starting the next stage. If exit criteria = FAIL, the Root Planner handles retry or halt per §7.

## 9. Size Caps and Placeholder Rules
- All artifact size caps are defined in `DEFINITIONS.md` §2. If exceeded, the stage fails and must compress.
- No placeholders may remain in final artifacts (`DEFINITIONS.md` §12). All `YYYY-MM-DD`, `<RUN_ID>`, `<SPRINT_ID>` values must be replaced with actuals.
- Every artifact must include `## Version` and `## Change Log` headers (`DEFINITIONS.md` §10–11).

## 10. Quick Reference: File Locations

| Category | Path |
|----------|------|
| Factory specs | `docs/Factory/Spec/` |
| Factory templates | `docs/Factory/templates/` |
| Factory runs | `docs/Factory/runs/<RUN_ID>/` |
| This guide | `docs/Factory/ORCHESTRATION.md` |
| Harmony product docs | `docs/` (top-level markdown files) |
| YAML policy packs | `docs/policy_packs/ukgc/` |
| Runtime code | `runtime/` |
| Tests | `tests/` |
| Phase 0 sprint artifacts | `docs/sprints/` |

## 11. Lessons from First Live Run (RUN_20260208_1400_factory)

The first live Factory v2 pipeline run produced the Sprint A: Adapter Boundary pack. These observations informed the v2 spec updates.

### 11.1 Stage ordering bug (fixed in v2)
**Problem**: STAGE_I2 (Purple Audit) required `PACK_CHECKLIST.md` as a LOAD input, but STAGE_J (Pack Consolidation) was the stage that produced it. I2 ran before J, creating a circular dependency.

**What happened**: The pipeline detected the issue, reasoned about it, and worked around it safely — producing the checklist in I2 as a prerequisite, then validating it in J. This was a process-spec flaw, not a hallucination.

**Fix**: Reordered stages so J runs before I2. J produces the checklist and manifest (mechanical), then I2 audits using the checklist (adjudication). This is the natural dependency order.

### 11.2 Single-agent execution is viable
The entire pipeline (all 13 stages, all roles) was executed by a single agent in one session. Role separation was enforced by context and instruction, not by separate agent processes. This works for sprints of Sprint A's complexity. For larger sprints, separate agent sessions per role may be needed for context window reasons.

### 11.3 Execution prompt is essential
Pasting the raw envelope into an execution agent is insufficient. The agent needs: the envelope, the micro-sprints, the intent, the verification plan, the detailed data shapes from the raw brief, and the product doc spine. The execution prompt (§6.1) consolidates these into a single self-contained instruction set.

### 11.4 Schema strictness creates friction
The existing `validate_userland_request()` in `schemas.py` rejects unknown top-level fields. When Sprint A added `tool_call`, `confirmation_stub`, `auth_context`, and `tenant_context` as new payload fields, the validator rejected them. The execution agent hit 14 test failures before diagnosing and fixing this. **Recommendation**: Future briefs should flag schema extension requirements explicitly, and the verification plan should include a "schema backward-compatibility" test that runs immediately after any schema change.

### 11.5 Path references in docs must be canonical
Several documents referenced YAML policy packs at `packs/` but the actual path is `docs/policy_packs/ukgc/`. The execution agent had to discover the correct path at runtime. All doc references should use canonical paths. See R-016 in RISK_REGISTER.md.

### 11.6 Reason code naming must be locked before execution
The execution agent used `ADAPTER_PR_ERROR` instead of `ADAPTER_PROTOCOL_ERROR` for the AdapterProtocolError RR reason code. This happened because the code name was not locked in a single authoritative location. **Recommendation**: All reason codes should be defined in one canonical table (e.g., in the baseline policy pack or a dedicated reason-code registry) and referenced by all other documents. See R-015 in RISK_REGISTER.md.
