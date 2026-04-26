# docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit)

## Version
v1.4

## Change Log
- v1.4 (2026-04-26): Added deterministic pack-lint validation after Stage I2 and before human execution review.
- v1.3 (2026-03-21): Added the generic context-recall contract, Stage A recall artifact workflow, PO-authored brief prerequisite, and stricter run-root evidence expectations.
- v1.2 (2026-03-18): Added mission recall generation, fallback-scope guidance, required-reference checks, and WEAK-coverage halt semantics to the generic Mission Mode flow.
- v1.1 (2026-03-15): Added the optional Product Owner pre-Factory lane and aligned the starter kit to the latest generic Factory operating shape.
- v1.0 (2026-03-10): Generic starter-kit orchestration guide aligned to the current Factory pipeline, Mission Mode, and derived mission continuity preflight.

## 0. Purpose
This document explains how to run the Factory pipeline in a generic repo.

The Factory is planning-first. It produces the pack that governs implementation. It does not replace coding, testing, or review in your project.

## 0.1 Planning-First Operating Principle
Use this order by default:
1. intent framing
2. constraint lock
3. verification design
4. bounded research if needed
5. continuity recall before gates that depend on prior decisions
6. execution last

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
4. Mission updates must happen in the same closure cycle as the underlying unit evidence.
5. If mission continuity is unclear, halt instead of guessing.

## 0.5 Product Owner Lane (Optional, Upstream of Factory)
The optional Product Owner process sits upstream of the Factory. It governs:
1. Phase Brief hardening into a locked Phase Intent
2. PO-authored sprint brief drafting within the locked phase scope
3. Brief Review PASS before any PO-authored brief becomes `raw_brief.md`

The Factory pipeline itself is unchanged. PO-authored briefs enter the same Stage A path after they pass their upstream review gate.

## 1. Prerequisites
Before a run starts, you need:
1. a raw brief
2. your project doc spine:
   - `docs/PROJECT_STATE.md`
   - `docs/ROADMAP.md`
   - `docs/CHANGELOG.md`
3. the Factory docs:
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
   - `./scripts/factoryctl pack-lint --run <RUN_ID>`
7. if using the optional PO lane:
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
12. if the raw brief came from the optional PO lane:
   - confirm the brief already passed the Brief Review gate
   - treat missing upstream recall or review evidence as blocking

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
- E/F/G design risk and verification
- H writes the execution envelope
- I attacks and hardens the envelope
- J packages the pack
- I2 performs the final gate

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

## 6. Post-Factory Execution
The Factory does not execute the sprint. It produces the contract for execution.

### 6.1 Execution Prompt Generation (execution-enabled runs only)
If the run is `EXECUTION_ENABLED` and the pack passes:
1. generate `EXECUTION_PROMPT.md`
2. include reading order, micro-sprints, constraints, verification commands, and an exit checklist
3. do not generate it for `PLANNING_ONLY` runs
4. do not initialize downstream runs unless fan-out was explicitly approved

### 6.2 Mission Execution (Mission Mode only)
If Mission Mode is active:
1. use `MISSION_MANIFEST.md` as the mission ledger
2. refresh `MISSION_CONTEXT_RECALL_REPORT.md` before checkpointing or authorizing the next unit
3. run mission lint before advancing an already-authorized unit
4. update the mission manifest when a unit reaches `pack_complete` or `closed_go`
5. update project state docs in the same cycle for GO closures

## 7. Error Handling
Halt when:
- a required lint fails
- a required recall artifact is missing or WEAK
- a stage fails its exit criteria
- a downstream artifact contradicts locked intent
- execution is attempted without authorization
- mission continuity is broken or ambiguous
- a PO-authored brief enters the Factory without upstream Brief Review PASS

## 8. Minimal Output Set
Every run should leave behind:
- run-root metadata
- `KNOWLEDGE_LINT.txt`
- `CONTEXT_RECALL_REPORT.md`
- a complete `pack/`
- handoff files
- `pack-lint` PASS output before human Go or No-go review
- optional `MISSION_LINT.txt` when relevant

Every mission should leave behind:
- `MISSION_MANIFEST.md`
- `MISSION_CONTEXT_RECALL_REPORT.md`
- `MISSION_CHECKPOINT.md`
- `MISSION_COMPLETION_REPORT.md`
