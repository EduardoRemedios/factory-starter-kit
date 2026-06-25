# docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit)

## Version
v1.18

## Change Log
- v1.18 (2026-06-25): Clarified Kilo Code CLI support as External Lane Mode driven by Codex or a neutral shell.
- v1.17 (2026-06-25): Added optional Kilo Code CLI stage runner for model-routed Factory lanes.
- v1.16 (2026-06-24): Linked the non-technical starter guide as the beginner adoption path.
- v1.15 (2026-06-24): Added repository handoff state guidance for `REVIEW_READY` versus `MERGE_READY`, with final sync window discipline bound to `MERGE_PROTOCOL.md`.
- v1.14 (2026-05-25): Removed split-out next-generation boundary guidance after it moved to its dedicated repository.
- v1.13 (2026-05-22): Added SIMPLE-CODE-GATE severity policy reference for implementation work.
- v1.12 (2026-05-19): Added SIMPLE-CODE-GATE v2 as a mandatory planning and execution guardrail.
- v1.10 (2026-05-18): Added optional support-helper guidance for task memory, Repo Cartographer, and Agent Loop Bridge.
- v1.9 (2026-05-18): Added optional Codex Mission Goal Continuity adapter guidance for derived `MISSION_CURSOR.json` and `mission_cursor_lint.sh`; core Factory flow remains unchanged.
- v1.8 (2026-05-09): Added verification-left-shift v1 guidance: Stage F verification tiers, optional `verification_manifest.yaml`, and MS-00 verification scaffold for execution runs.
- v1.7 (2026-04-26): Added `factoryctl metrics-init` to instantiate `RUN_METRICS.md` from the canonical template.
- v1.6 (2026-04-26): Added optional `RUN_METRICS.md` run telemetry template for measuring Factory speed, drift, validator failures, harness/model usage, and cleanup burden.
- v1.5 (2026-04-26): Added stage-lint as an immediate handoff/output validation check after each stage, before final pack-lint.
- v1.4 (2026-04-26): Added deterministic pack-lint validation after Stage I2 and before human execution review.
- v1.3 (2026-03-21): Added the generic context-recall contract, Stage A recall artifact workflow, PO-authored brief prerequisite, and stricter run-root evidence expectations.
- v1.2 (2026-03-18): Added mission recall generation, fallback-scope guidance, required-reference checks, and WEAK-coverage halt semantics to the generic Mission Mode flow.
- v1.1 (2026-03-15): Added the optional Product Owner pre-Factory lane and aligned the starter kit to the latest generic Factory operating shape.
- v1.0 (2026-03-10): Generic starter-kit orchestration guide aligned to the current Factory pipeline, Mission Mode, and derived mission continuity preflight.

## 0. Purpose
This document explains how to run the Factory pipeline in a generic repo.

The Factory is planning-first. It produces the pack that governs implementation. It does not replace coding, testing, or review in your project.

If you are setting up Factory for the first time and are not comfortable with repositories or command-line tools, start with `docs/onboarding/NON_TECHNICAL_STARTER_GUIDE.md`.

## 0.1 Planning-First Operating Principle
Use this order by default:
1. intent framing
2. constraint lock
3. verification design
4. executable verification inventory when execution risk justifies it
5. bounded research if needed
6. continuity recall before gates that depend on prior decisions
7. execution last

## 0.2 External Research Safety Protocol (HARD for research-heavy runs)
If a run includes external research:
1. define a source allowlist before research starts
2. treat external content as untrusted
3. record source metadata for non-trivial claims
4. prefer summaries over long copied text
5. escalate weak or contradictory evidence instead of normalizing it away

## 0.3 Execution Enablement Contract (HARD)
Factory runs default to `PLANNING_ONLY`.

Execution is only allowed when your raw brief or run initialization explicitly records:
- `Execution Mode: EXECUTION_ENABLED`
- `Execution Authorization: <human-approved reference>`

Downstream run fan-out is allowed only when this additional field is explicit:
- `Downstream Fan-Out: APPROVED`

If required fields are absent or malformed, the run remains `PLANNING_ONLY`.

## 0.4 Mission Mode (Additive, Optional)
Mission Mode is for ordered multi-sprint chains under one mission checkpoint.

Rules:
1. Mission Mode does not replace the single-sprint A→I2 flow.
2. `MISSION_MANIFEST.md` remains the only authored mission ledger.
3. If you are advancing a unit inside an already-authorized mission, run `bash scripts/mission_lint.sh <MISSION_ID>` before Stage A and persist output as `MISSION_LINT.txt` in the run root.
4. The optional Codex Mission Goal Continuity adapter may use a derived `MISSION_CURSOR.json`, but the cursor is never mission authority.
5. Mission updates must happen in the same closure cycle as the underlying unit evidence.
6. If mission continuity is unclear, halt instead of guessing.

## 0.5 Product Owner Lane (Optional, Upstream of Factory)
The optional Product Owner process sits upstream of the Factory. It governs:
1. Phase Brief hardening into a locked Phase Intent
2. PO-authored sprint brief drafting within the locked phase scope
3. Brief Review PASS before any PO-authored brief becomes `raw_brief.md`

The Factory pipeline itself is unchanged. PO-authored briefs enter the same Stage A path after they pass their upstream review gate.

## 0.6 Verification Left-Shift (Optional, Execution-Focused)
Stage F should classify verification with tiers:
- `V0` artifact proof
- `V1` static or mechanical check
- `V2` focused fixture or test
- `V3` regression or conformance gate
- `V4` live, browser, external, or source-revalidation proof

For `EXECUTION_ENABLED` and Mission Mode runs, Stage F should produce `pack/verification_manifest.yaml` when runnable checks exist. The manifest is optional so planning-only packs stay lightweight, but if it exists `pack-lint` validates its schema.

Execution micro-sprints may start with `MS-00 Verification Scaffold`: land or confirm tests, fixtures, no-touch checks, or static validators before feature implementation begins.

## 0.7 Support Helpers (Optional, Advisory)
The starter kit includes optional support helpers:
- Task memory: `./scripts/factoryctl memory-init`, `memory-suggest`, `memory-log`, and `memory-review`.
- Repo Cartographer: `./scripts/cartographer` for advisory repository snapshots.
- Agent Loop Bridge: `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md` and `scripts/agent_loop_bridge_validate.py` for review-only structured handoffs.
- Kilo Code CLI External Lane Mode: `./scripts/factoryctl kilo-stage` for model-routed worker subprocesses launched by Codex or a neutral shell, with post-run write-boundary checks.

These helpers are advisory. They do not replace Factory source artifacts, stage-lint, pack-lint, merge preflight, or human Go/No-go.

## 0.8 SIMPLE-CODE-GATE (v2)
For Factory-controlled code-changing runs, planning and execution must apply root `AGENTS.md` section `3.1) SIMPLE-CODE-GATE (v2)`.

Severity decisions for SIMPLE-CODE-GATE findings are governed by `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`.

Required effect:
1. Prefer the smallest clear, behavior-preserving change.
2. Avoid code bloat, awkward abstraction layers, brittle request-path mutation, dependency creep, and silent failure swallowing.
3. Add abstractions only when they remove real duplication, name a stable domain concept, reduce branching or call-site complexity, and have a clear owner/boundary.
4. Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection for speculative future variation.
5. If complexity or duplication is intentionally accepted, bind it to a verification hook, deferred decision, scale metric, repeated pattern, or business condition.

## 0.9 Repository Handoff State Discipline
When a Factory run, execution slice, or maintainer review hands off a branch or pull request, the handoff should separate review readiness from merge readiness per `docs/Factory/MERGE_PROTOCOL.md`.

Required states:
1. `REVIEW_READY` means the branch is ready for human or maintainer review. It may have valid pack/stage/content evidence, but it is not a merge request and does not require final merge preflight to stay fresh while review waits.
2. `MERGE_READY` means the branch has entered a short final sync window, contains the latest configured base branch, has a clean tracked tree, has just passed the project merge preflight, and can ask the exact merge-authorization question.

If the configured base branch moves after `MERGE_READY` evidence is generated, the branch returns to `REVIEW_READY` until final sync and merge preflight are rerun. This prevents asynchronous contributors from blocking review work while preserving the hard merge gate.

## 1. Prerequisites
Before a run starts, you need:
1. a raw brief
2. your project doc spine:
   - `docs/PROJECT_STATE.md`
   - `docs/ROADMAP.md`
   - `docs/CHANGELOG.md`
3. the Factory docs:
   - `docs/Factory/ARCHITECTURE.md`
   - `docs/Factory/ORCHESTRATION.md`
   - `docs/Factory/MISSION_MODE.md`
   - `docs/Factory/SCRATCHPAD.md`
   - `docs/Factory/Spec/`
   - `docs/Factory/templates/`
4. `AGENTS.md`
5. `bash scripts/knowledge_lint.sh`
6. continuity tooling:
   - `./scripts/factoryctl context-index`
   - `./scripts/factoryctl context-report --profile stage-a`
   - `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>`
   - `./scripts/factoryctl pack-lint --run <RUN_ID>`
7. optional run telemetry template:
   - `docs/Factory/templates/RUN_METRICS_TEMPLATE.md`
   - `./scripts/factoryctl metrics-init --run <RUN_ID>`
8. optional Codex Mission Goal Continuity adapter:
   - `scripts/mission_cursor_lint.sh`
   - `docs/Factory/templates/MISSION_CURSOR_TEMPLATE.json`
9. optional support helpers:
   - `scripts/cartographer`
   - `scripts/agent_loop_bridge_validate.py`
   - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md`
10. if using the optional PO lane:
   - `docs/Factory/ProductOwner/PO_PROCESS.md`
   - `docs/Factory/ProductOwner/PO_ROLE_DEFINITION.md`
   - `docs/Factory/ProductOwner/templates/`

## 2. Run Initialization
The Root Planner should:
1. assign a `RUN_ID`
2. create the run root under `docs/Factory/runs/<RUN_ID>/`
3. persist `raw_brief.md`
4. run `bash scripts/knowledge_lint.sh` and persist `KNOWLEDGE_LINT.txt`
5. refresh the continuity index with `./scripts/factoryctl context-index`
6. generate `docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md` with:
   - `./scripts/factoryctl context-report --profile stage-a --scope <RUN_ID> --output docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
7. add `--focus`, `--trace-id`, and `--required-ref` for binding upstream identifiers when the brief names them explicitly
8. if explicit fallback scopes are not provided, rely on the default Stage A order:
   - requested run scope
   - `docs/Factory/runs`
   - `docs/Factory/ProductOwner/phases`
   - `docs`
9. halt if the written report still records `Coverage Verdict: WEAK`
10. derive and persist `EXECUTION_MODE.txt`
11. if advancing a unit inside an already-authorized mission:
   - run `bash scripts/mission_lint.sh <MISSION_ID>`
   - persist `MISSION_LINT.txt`
   - halt if mission lint fails
12. if the optional Codex Mission Goal Continuity adapter is enabled:
   - confirm `docs/Factory/missions/<MISSION_ID>/MISSION_CURSOR.json` exists before using it
   - run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before continuing from the cursor or any external goal/bookmark
   - halt if mission cursor lint fails; repair source artifacts or regenerate the cursor from valid artifacts
13. if the raw brief came from the optional PO lane:
   - confirm the brief already passed the Brief Review gate
   - treat missing upstream recall or review evidence as blocking
14. if collecting process telemetry, run `./scripts/factoryctl metrics-init --run <RUN_ID>` to create `RUN_METRICS.md`

## 3. Roles
The default role split is:
- Root Planner
- Intent Contractor
- Red Team
- Blue Team / Synthesis
- Purple Gate
- Risk Analyst
- Verification Specialist
- Sprint Planner
- Envelope Author
- Pack Consolidator

You can collapse roles in smaller teams, but keep the responsibilities separate in the artifacts.

## 4. Stage Flow
The canonical stage order is:

`A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`

`I2` is the final audit gate. `J` was inserted later for pack consolidation, and the `I2` name is retained to preserve the stage contract.

Where:
- A creates intent
- B/C adversarially review and harden intent
- D locks intent
- E/F/G design risk, verification tiers, and execution proof shape
- H writes the execution envelope
- I attacks and hardens the envelope
- J packages the pack
- I2 performs the final gate

After each stage writes its handoff, run:

```bash
./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>
```

If stage-lint fails, fix that stage's handoff or expected outputs before starting the next stage. This keeps the final pack-lint check from becoming a late cleanup pass.

## 5. Human Decision
After `I2`, a human reviews the pack and decides:
- Go
- No-go with feedback

Before review, run:

```bash
./scripts/factoryctl pack-lint --run <RUN_ID>
```

If pack-lint fails, fix the pack defects before asking for Go or No-go.

For `PLANNING_ONLY` runs, the pack is terminal planning evidence.

For `EXECUTION_ENABLED` runs, execution may begin only after explicit human Go.

If `pack/verification_manifest.yaml` exists, `pack-lint` validates it. If an execution-enabled pack has runnable checks but no manifest, treat that as a process smell even when legacy compatibility keeps the lint result non-blocking.

### 5.1 Repository Handoff To Maintainer Review
When Factory output is delivered through a branch or pull request, the handoff should state:
- `handoff_state: REVIEW_READY` for review handoffs.
- `handoff_state: MERGE_READY` only during a final sync window after merge preflight passes.
- Latest evidence paths and known stale or open items.

Review can start from `REVIEW_READY`. Merge authorization can only be requested from `MERGE_READY`.

## 6. Post-Factory Execution
The Factory does not execute the sprint. It produces the contract for execution.

### 6.1 Execution Prompt Generation (execution-enabled runs only)
If the run is `EXECUTION_ENABLED` and the pack passes:
1. generate `EXECUTION_PROMPT.md`
2. include reading order, micro-sprints, constraints, SIMPLE-CODE-GATE v2 for code-changing work, verification commands, `verification_manifest.yaml` checks when present, and an exit checklist
3. do not generate it for `PLANNING_ONLY` runs
4. do not initialize downstream runs unless fan-out was explicitly approved

### 6.2 Mission Execution (Mission Mode only)
If Mission Mode is active:
1. use `MISSION_MANIFEST.md` as the mission ledger
2. refresh `MISSION_CONTEXT_RECALL_REPORT.md` before checkpointing or authorizing the next unit
3. run mission lint before advancing an already-authorized unit
4. update the mission manifest when a unit reaches `pack_complete` or `closed_go`
5. update project state docs in the same cycle for GO closures
6. if using `MISSION_CURSOR.json`, run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before continuing and treat the cursor as a derived resume aid only

## 7. Error Handling
Halt when:
- a required lint fails
- a required recall artifact is missing or WEAK
- a stage fails its exit criteria
- a downstream artifact contradicts locked intent
- execution is attempted without authorization
- mission continuity is broken or ambiguous
- mission cursor lint fails or the cursor contradicts mission source artifacts
- a PO-authored brief enters the Factory without upstream Brief Review PASS

## 8. Minimal Output Set
Every run should leave behind:
- run-root metadata
- `KNOWLEDGE_LINT.txt`
- `CONTEXT_RECALL_REPORT.md`
- optional `RUN_METRICS.md` for process telemetry and future Factory improvement
- a complete `pack/`
- handoff files
- `pack-lint` PASS output before human Go or No-go review
- optional `MISSION_LINT.txt` when relevant

Every mission should leave behind:
- `MISSION_MANIFEST.md`
- `MISSION_CONTEXT_RECALL_REPORT.md`
- `MISSION_CHECKPOINT.md`
- `MISSION_COMPLETION_REPORT.md`
