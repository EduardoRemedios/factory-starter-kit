# docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit)

## Version
v1.0

## Change Log
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
5. execution last

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

If those fields are absent or malformed, the run remains `PLANNING_ONLY`.

## 0.4 Mission Mode (Additive, Optional)
Mission Mode is for ordered multi-sprint chains under one mission checkpoint.

Rules:
1. Mission Mode does not replace the single-sprint A→I2 flow.
2. `MISSION_MANIFEST.md` remains the only authored mission ledger.
3. If you are advancing a unit inside an already-authorized mission, run `bash scripts/mission_lint.sh <MISSION_ID>` before Stage A and persist output as `MISSION_LINT.txt` in the run root.
4. Mission updates must happen in the same closure cycle as the underlying unit evidence.
5. If mission continuity is unclear, halt instead of guessing.

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

## 2. Run Initialization
The Root Planner should:
1. assign a `RUN_ID`
2. create the run root under `docs/Factory/runs/<RUN_ID>/`
3. persist `raw_brief.md`
4. run `bash scripts/knowledge_lint.sh` and persist `KNOWLEDGE_LINT.txt`
5. derive and persist `EXECUTION_MODE.txt`
6. if advancing a unit inside an already-authorized mission:
   - run `bash scripts/mission_lint.sh <MISSION_ID>`
   - persist `MISSION_LINT.txt`
   - halt if mission lint fails

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

`A → B → C → D → E → F → G → H → I → J → I2`

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

For `PLANNING_ONLY` runs, the pack is terminal planning evidence.

For `EXECUTION_ENABLED` runs, execution may begin only after explicit human Go.

## 6. Post-Factory Execution
The Factory does not execute the sprint. It produces the contract for execution.

### 6.1 Execution Prompt Generation (execution-enabled runs only)
If the run is `EXECUTION_ENABLED` and the pack passes:
1. generate `EXECUTION_PROMPT.md`
2. include reading order, micro-sprints, constraints, verification commands, and an exit checklist
3. do not generate it for `PLANNING_ONLY` runs

### 6.2 Mission Execution (Mission Mode only)
If Mission Mode is active:
1. use `MISSION_MANIFEST.md` as the mission ledger
2. run mission lint before advancing an already-authorized unit
3. update the mission manifest when a unit reaches `pack_complete` or `closed_go`
4. update project state docs in the same cycle for GO closures

## 7. Error Handling
Halt when:
- a required lint fails
- a stage fails its exit criteria
- a downstream artifact contradicts locked intent
- execution is attempted without authorization
- mission continuity is broken or ambiguous

## 8. Minimal Output Set
Every run should leave behind:
- run-root metadata
- a complete `pack/`
- handoff files
- lint evidence

Every mission should leave behind:
- `MISSION_MANIFEST.md`
- `MISSION_CHECKPOINT.md`
- `MISSION_COMPLETION_REPORT.md`
