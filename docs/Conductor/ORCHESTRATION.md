# docs/Conductor/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit)

## Version
v1.25

## Change Log
- v1.25 (2026-09-03): Made `pack/verification_manifest.yaml` mandatory for execution-enabled runs whose verification plan declares runnable VM checks (pack-lint fails closed), and let a recorded execution closeout stay valid after mode restoration and control archival while recording itself stays strict.
- v1.24 (2026-08-13): Closed missing-mode and symlink fail-open cases, aligned traceability parsing with its canonical verification column, and validated optional execution ordering.
- v1.23 (2026-08-13): Separated pack-lint validation of pinned preimage evidence from lifecycle-timed VM comparison of target bytes.
- v1.22 (2026-08-13): Made the executable verification manifest authoritative, cross-checked VM inventories, and required SHA-pinned no-touch preimage manifests.
- v1.21 (2026-08-13): Separated immutable I2 audited mode from later digest-bound current execution authority.
- v1.20 (2026-08-05): Added deterministic execution-closeout recording and fail-closed progress behavior.
- v1.19 (2026-07-02): Added the direct-source repair path for generated WEAK context recall reports.
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
- v1.7 (2026-04-26): Added `conductorctl metrics-init` to instantiate `RUN_METRICS.md` from the canonical template.
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

### 0.3.1 Post-I2 Cross-Mode Activation

The mode recorded by `PACK_AUDIT_REPORT.md` and `verification_manifest.yaml` describes the pack Purple audited at I2. Those pack artifacts and `PACK_MANIFEST.md` remain unchanged after human review.

When a pack audited as `PLANNING_ONLY` later receives explicit execution authorization:

1. record current mode as `EXECUTION_ENABLED` in `EXECUTION_MODE.txt`
2. create `EXECUTION_AUTHORIZATION.md` from the canonical template
3. record exactly one human-Go marker, prior mode, activated mode, authorized pack-manifest SHA-256, and authorized pack-audit SHA-256
4. run pack-lint before generating `EXECUTION_PROMPT.md` or changing implementation source

Pack-lint recomputes both pinned digests. Missing audited mode, malformed, duplicated, stale, mismatched, or symlinked activation evidence fails closed. It compares verification-manifest mode with the audited pack mode during a valid cross-mode transition. Existing packs whose explicitly audited mode already matches current mode retain legacy behavior.

Activation must not rewrite `PACK_MANIFEST.md`, `PACK_AUDIT_REPORT.md`, the sprint envelope, or `verification_manifest.yaml`; changing those bytes invalidates the human-approved planning evidence.

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

For `EXECUTION_ENABLED` and Mission Mode runs, Stage F must produce `pack/verification_manifest.yaml` whenever `verification_plan.md` declares a runnable `## Checks` VM inventory: the canonical execution closeout cannot be recorded without it, so `pack-lint` fails an execution-enabled run that lacks it and warns a planning-only pack that it cannot legally close after activation. Only packs with no runnable VM inventory may omit the manifest (planning-only packs stay lightweight); if it exists `pack-lint` validates its schema.

When a verification manifest exists, its check IDs are the executable authority. Stage F must use a dedicated `## Checks` inventory in `verification_plan.md`, reference the same IDs in the traceability matrix's named verification coverage column, and keep all three ID sets exactly equal. If `execution_order` is present, it is authoritative and must contain every VM check exactly once; explicitly named non-VM operations may be interposed. Every `no_touch` check must reference a safe run-relative, non-symlink JSON preimage manifest and pin that manifest's SHA-256. Pack-lint validates the evidence file, schema, safe paths, and pin; the declared VM command compares target bytes at the lifecycle point named by the plan. Historical preimages do not become permanent postimplementation postimages.

For Factory self-maintenance, Stage F must also inspect project-owned coupling before locking the envelope: protected digest fixtures, generated payload counterparts, and ownership manifests are explicit planned paths rather than unexpected execution drift.

Execution micro-sprints may start with `MS-00 Verification Scaffold`: land or confirm tests, fixtures, no-touch checks, or static validators before feature implementation begins.

## 0.7 Support Helpers (Optional, Advisory)
The starter kit includes optional support helpers:
- Task memory: `./scripts/conductorctl memory-init`, `memory-suggest`, `memory-log`, and `memory-review`.
- Repo Cartographer: `./scripts/cartographer` for advisory repository snapshots.
- Agent Loop Bridge: `docs/Conductor/Harnesses/AGENT_LOOP_BRIDGE.md` and `scripts/agent_loop_bridge_validate.py` for review-only structured handoffs.
- Kilo Code CLI External Lane Mode: `./scripts/conductorctl kilo-stage` for model-routed worker subprocesses launched by Codex or a neutral shell, with post-run write-boundary checks.

These helpers are advisory. They do not replace Factory source artifacts, stage-lint, pack-lint, merge preflight, or human Go/No-go.

## 0.8 SIMPLE-CODE-GATE (v2)
For Factory-controlled code-changing runs, planning and execution must apply root `AGENTS.md` section `3.1) SIMPLE-CODE-GATE (v2)`.

Severity decisions for SIMPLE-CODE-GATE findings are governed by `docs/Conductor/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`.

Required effect:
1. Prefer the smallest clear, behavior-preserving change.
2. Avoid code bloat, awkward abstraction layers, brittle request-path mutation, dependency creep, and silent failure swallowing.
3. Add abstractions only when they remove real duplication, name a stable domain concept, reduce branching or call-site complexity, and have a clear owner/boundary.
4. Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection for speculative future variation.
5. If complexity or duplication is intentionally accepted, bind it to a verification hook, deferred decision, scale metric, repeated pattern, or business condition.

## 0.9 Repository Handoff State Discipline
When a Factory run, execution slice, or maintainer review hands off a branch or pull request, the handoff should separate review readiness from merge readiness per `docs/Conductor/MERGE_PROTOCOL.md`.

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
   - `docs/Conductor/ARCHITECTURE.md`
   - `docs/Conductor/ORCHESTRATION.md`
   - `docs/Conductor/MISSION_MODE.md`
   - `docs/Conductor/SCRATCHPAD.md`
   - `docs/Conductor/Spec/`
   - `docs/Conductor/templates/`
4. `AGENTS.md`
5. `bash scripts/knowledge_lint.sh`
6. continuity tooling:
   - `./scripts/conductorctl context-index`
   - `./scripts/conductorctl context-report --profile stage-a`
   - `./scripts/conductorctl stage-lint --run <RUN_ID> --stage <STAGE>`
   - `./scripts/conductorctl pack-lint --run <RUN_ID>`
7. optional run telemetry template:
   - `docs/Conductor/templates/RUN_METRICS_TEMPLATE.md`
   - `./scripts/conductorctl metrics-init --run <RUN_ID>`
8. optional Codex Mission Goal Continuity adapter:
   - `scripts/mission_cursor_lint.sh`
   - `docs/Conductor/templates/MISSION_CURSOR_TEMPLATE.json`
9. optional support helpers:
   - `scripts/cartographer`
   - `scripts/agent_loop_bridge_validate.py`
   - `docs/Conductor/Harnesses/AGENT_LOOP_BRIDGE.md`
10. if using the optional PO lane:
   - `docs/Conductor/ProductOwner/PO_PROCESS.md`
   - `docs/Conductor/ProductOwner/PO_ROLE_DEFINITION.md`
   - `docs/Conductor/ProductOwner/templates/`

## 2. Run Initialization
The Root Planner should:
1. assign a `RUN_ID`
2. create the run root under `docs/Conductor/runs/<RUN_ID>/`
3. persist `raw_brief.md`
4. run `bash scripts/knowledge_lint.sh` and persist `KNOWLEDGE_LINT.txt`
5. if `docs/Conductor/PROJECT_PREFLIGHT.json` exists, run `./scripts/conductorctl project-preflight --run <RUN_ID>` and halt unless `PROJECT_PREFLIGHT.txt` records PASS
6. refresh the continuity index with `./scripts/conductorctl context-index`
7. generate `docs/Conductor/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md` with:
   - `./scripts/conductorctl context-report --profile stage-a --scope <RUN_ID> --output docs/Conductor/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
8. add `--focus`, `--trace-id`, and `--required-ref` for binding upstream identifiers when the brief names them explicitly
9. if explicit fallback scopes are not provided, rely on the default Stage A order:
   - requested run scope
   - `docs/Conductor/runs`
   - `docs/Conductor/ProductOwner/phases`
   - `docs`
10. if the written report still records `Coverage Verdict: WEAK`, use the Stage A direct-source repair path in section 2.1 or halt
11. derive and persist `EXECUTION_MODE.txt`
12. if advancing a unit inside an already-authorized mission:
   - run `bash scripts/mission_lint.sh <MISSION_ID>`
   - persist `MISSION_LINT.txt`
   - halt if mission lint fails
13. if the optional Codex Mission Goal Continuity adapter is enabled:
   - confirm `docs/Conductor/missions/<MISSION_ID>/MISSION_CURSOR.json` exists before using it
   - run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before continuing from the cursor or any external goal/bookmark
   - halt if mission cursor lint fails; repair source artifacts or regenerate the cursor from valid artifacts
14. if the raw brief came from the optional PO lane:
   - confirm the brief already passed the Brief Review gate
   - treat missing upstream recall or review evidence as blocking
15. if collecting process telemetry, run `./scripts/conductorctl metrics-init --run <RUN_ID>` to create `RUN_METRICS.md`

### 2.0.1 Optional Project Preflight

An adopting project may declare one additional fail-closed check without changing Factory Core authority. Create `docs/Conductor/PROJECT_PREFLIGHT.json` with schema version 1 and an optional integer `timeout_seconds` from 1 through 300. Factory always executes the fixed repository command `scripts/conductor_project_preflight --run <RUN_ID> --json` directly; the declaration cannot supply shell text or another command.

The project command must return one JSON object with exactly `schema_version`, `status`, `reason_code`, and `evidence_paths`. Status is `PASS` or `FAIL`; reason codes use uppercase letters, digits, and underscores; evidence paths are existing repository-relative files. Each output stream is capped at 64 KiB. Invalid declarations, missing/non-executable commands, timeout, non-zero exit, oversized or malformed/ambiguous output, explicit failure, and unsafe evidence paths halt before Stage A with stable Core reason codes. When no declaration exists, current Factory behavior is unchanged and `PROJECT_PREFLIGHT.txt` is not required.

### 2.1 Stage A Direct-Source Repair For WEAK Recall
Direct-source repair is a narrow fallback after generated recall remains `WEAK`. It strengthens the recall gate by replacing unresolved index references with explicit local source review evidence; it does not allow Stage A to proceed on raw weak recall.

Allowed only when all are true:
1. `./scripts/conductorctl context-index` was refreshed for the current repo state.
2. `context-report` was regenerated after fallback scopes were attempted.
3. Each unresolved generated ref being repaired is a concrete local file path, code path, or exact artifact path.
4. The agent reads each source directly from disk and records a concise source summary in `CONTEXT_RECALL_REPORT.md`.
5. No remaining unresolved ref is material to Stage A intent, constraints, approvals, or scope.

Not allowed when any are true:
1. The required source does not exist, is unreadable, or is empty.
2. The missing context is a human decision, approval, external source, or ambiguous artifact that cannot be verified locally.
3. Any unresolved generated ref remains material to Stage A intent.
4. The repair section omits exact files read, source summaries, remaining unresolved refs, or final repaired verdict.

Repair format:
- Preserve the generated report content, including `Coverage Verdict: WEAK`.
- Add `## Direct-Source Repair`, `## Direct Sources Read`, and `## Source Summaries` sections.
- Record `Original Generated Verdict: WEAK`, `Direct-Source Repair Status: APPLIED`, and `Final Repaired Verdict: REPAIRED_DIRECT_SOURCE_CHECK`.
- Record `Unresolved Generated Refs`, `Context Index Refreshed: YES`, `Fallback Scopes Attempted: YES`, `Remaining Unresolved Generated Refs`, `Remaining Material Unresolved Refs: None`, and `Materiality Check: PASS`.
- Treat the report as passable only when `stage-lint` and `pack-lint` recognize the repaired verdict and direct-source evidence. Otherwise halt before Stage A.

### 2.2 Downstream Migration Note
Downstream repositories should import this starter-kit update by copying the changed Factory Core docs, `docs/Conductor/templates/CONTEXT_RECALL_REPORT_TEMPLATE.md`, `scripts/conductor_pack_lint.py`, `scripts/conductor_stage_lint.py`, and `scripts/knowledge_lint.sh`, then running:

```bash
bash scripts/knowledge_lint.sh
./scripts/conductorctl context-index
./scripts/conductorctl pack-lint --run <RUN_ID>
```

Existing runs do not need to be rewritten unless they still contain an unrepaired `Coverage Verdict: WEAK`. For those runs, append the direct-source repair sections only when the missing refs are locally verifiable and no material unresolved refs remain.

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
./scripts/conductorctl stage-lint --run <RUN_ID> --stage <STAGE>
```

If stage-lint fails, fix that stage's handoff or expected outputs before starting the next stage. This keeps the final pack-lint check from becoming a late cleanup pass.

## 5. Human Decision
After `I2`, a human reviews the pack and decides:
- Go
- No-go with feedback

Before review, run:

```bash
./scripts/conductorctl pack-lint --run <RUN_ID>
```

If pack-lint fails, fix the pack defects before asking for Go or No-go.

For `PLANNING_ONLY` runs, the pack is terminal planning evidence.

For `EXECUTION_ENABLED` runs, execution may begin only after explicit human Go.

If `pack/verification_manifest.yaml` exists, `pack-lint` validates it. If an execution-enabled pack declares runnable VM checks in `verification_plan.md` but has no manifest, `pack-lint` fails closed: such a run is structurally unable to record its canonical execution closeout. Legacy compatibility remains only for packs whose plan declares no VM inventory, where the absence stays a warning.

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

### 6.2 Execution Closeout

When an execution-enabled run finishes its approved micro-sprints:
1. retain evidence for every enabled verification-manifest check
2. author exactly one `REVIEW_READY`, `NO_GO`, or `BLOCKED` outcome using
   `docs/Conductor/templates/EXECUTION_CLOSEOUT_TEMPLATE.json`
3. record it only through `./scripts/conductorctl execution-closeout --run <RUN_ID> --input <DRAFT> --json`
4. run plugin progress for the explicit run and for default selection
5. treat any present-invalid closeout as blocking; absence alone preserves legacy behavior
6. record the closeout while `EXECUTION_MODE.txt` is still `EXECUTION_ENABLED` and `EXECUTION_AUTHORIZATION.md` is still live; recording refuses a restored or archived state
7. after recording, the run may be restored to `PLANNING_ONLY` and its controls archived (e.g. `MS05_EXECUTION_AUTHORIZATION.md`): the recorded closeout stays valid as long as a byte-identical archived authorization remains at the run root

Closeout is derived evidence, not authority. `REVIEW_READY` permits maintainer
review only and does not permit commit, merge, tag, push, publication, adapter
continuation, phase closure, or mission completion.

### 6.3 Mission Execution (Mission Mode only)
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

### 7.1 Execution Evidence Boundaries

- Factory-controlled Python verification uses `./scripts/conductor-python`, which disables bytecode writes before invoking Python.
- Complete high-volume evidence is written only to an exact path authorized by the active envelope. Harness output contains bounded summaries, not inventory bodies or secret-bearing records.
- Every `Outputs Produced (paths)` entry is one backtick-quoted exact relative path. Globs, expressions, absolute paths, traversal, symlink escape, malformed bullets, and missing or empty targets fail closed in both stage-lint and Progress.
- An execution prompt records human authorization with `- Human Go: RECORDED`; the label alone or any other value is not authorization.

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
