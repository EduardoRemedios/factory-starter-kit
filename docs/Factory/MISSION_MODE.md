# docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension)

## Version
v1.4

## Change Log
- v1.4 (2026-05-18): Added optional Codex Mission Goal Continuity adapter with derived `MISSION_CURSOR.json` and `mission_cursor_lint.sh`; preserved `MISSION_MANIFEST.md` as the only authored mission ledger.
- v1.3 (2026-03-21): Added ordered fallback-scope handling, exact required-reference checks, and WEAK-coverage halt semantics for mission recall generation.
- v1.2 (2026-03-15): Added mandatory `MISSION_CONTEXT_RECALL_REPORT.md` generation before mission checkpointing and downstream unit planning.
- v1.1 (2026-03-10): Added mission manifest ledger-of-record rule, normalized mission unit status semantics, same-cycle mission update discipline, and derived mission continuity preflight guidance (`mission_lint.sh`) while preserving additive Mission Mode behavior.
- v1.0 (2026-02-27): Initial Mission Mode contract. Defines mission lifecycle, mission-level checkpointing, HALT semantics, scope controls, and execution sequencing while preserving existing sprint contracts.

## 0. Purpose
Mission Mode is an additive orchestration wrapper for running an ordered sequence of multiple Factory sprint packs after one consolidated human checkpoint.

Mission Mode does not replace or weaken the existing Factory stage contracts (`A -> I2`, plus `POST_GATE` where applicable). Each mission unit remains a standard sprint pack with unchanged guardrails.

## 1. Non-negotiable preservation rules (HARD)
Mission Mode must preserve:
1. fail-closed semantics
2. schema locks and invariants
3. evidence and receipt integrity
4. explicit execution authorization
5. scope boundaries
6. iteration caps

If uncertain, Mission Mode halts.

## 2. Mission object model

### 2.1 Mission
A mission is an ordered set of sprint units:
- `MISSION_ID`
- `MISSION_UNITS[]` (ordered)
- dependency edges between units
- mission scope ledger (locked)
- mission checkpoint state

### 2.2 Mission unit
Each mission unit references a standard Factory sprint run:
- `RUN_ID`
- `SPRINT_ID`
- pack artifacts (`intent.md`, envelope, checklist, audit report, handoffs)
- unit execution status (`planned|running|pack_complete|closed_go|failed|skipped|planning_signal`)

The mission manifest is the authored ledger of record for:
- ordered mission units
- mission unit status
- run references
- pack paths
- mission evidence links

Mission Mode does not introduce a second authored mission-state artifact.

### 2.2.1 Mission unit status semantics
- `planned`: unit is explicitly in the mission sequence and may start when its dependencies and authorization conditions are satisfied
- `running`: the unit's Factory run or bounded execution work is in progress
- `pack_complete`: the unit reached pack closure (`STAGE_I2` PASS or CONDITIONAL PASS) and is terminal for planning-only units, or awaits execution GO on execution-enabled units
- `closed_go`: the unit completed with explicit human GO on an execution-enabled path
- `failed`: the unit halted or failed a mandatory gate
- `skipped`: the unit was not executed because the mission halted or an explicit mission decision withheld it
- `planning_signal`: the unit is intentionally enumerated but is not yet authorized for execution because an upstream lock or prerequisite is missing

### 2.3 Mission scope ledger
The mission scope ledger is an explicit, immutable list of what cross-unit changes are allowed.
Any requirement outside this ledger is `[SCOPE EXPANSION]` plus BLOCKING.

## 3. Mission lifecycle (HARD)
1. `MISSION_PLANNING`
2. `MISSION_READY_FOR_CHECKPOINT`
3. `MISSION_AUTHORIZED`
4. `MISSION_EXECUTING`
5. terminal:
   - `MISSION_HALTED`
   - `MISSION_COMPLETED`

No execution is allowed before `MISSION_AUTHORIZED`.

## 4. Planning vs execution state

### 4.1 Planning state
Planning assembles and validates:
- mission manifest
- unit dependency order
- mission checkpoint inputs
- scope ledger lock

### 4.2 Execution state
Execution is allowed only after:
- mission checkpoint GO
- explicit authorization conditions satisfied

Execution proceeds unit-by-unit using locked mission artifacts.

### 4.3 Same-cycle mission updates (HARD)
When Mission Mode is active, the mission manifest must be updated in the same closure cycle as the underlying unit evidence.

This means:
1. unit status in `MISSION_MANIFEST.md` is updated when the unit reaches `pack_complete` or `closed_go`
2. referenced run paths and evidence links are updated in the same cycle
3. canonical repo-wide state docs are updated in the same cycle when the unit reaches GO
4. relevant `PHASE_STATE.md` entries are updated in the same cycle when the mission unit belongs to a PO-controlled phase chain

If that same-cycle discipline is not maintained, Mission Mode should halt rather than silently allowing mission drift.

## 5. Mission-level checkpoint (single consolidated GO/NO-GO)
Mission checkpoint evaluates:
1. all units are explicitly enumerated and ordered
2. scope ledger is locked and referenced
3. authorization evidence is present
4. no unresolved BLOCKING scope issues remain
5. mission-level halt and restart semantics are explicit
6. `MISSION_CONTEXT_RECALL_REPORT.md` has been refreshed from the artifact recall index and reviewed alongside the mission ledger

Checkpoint result is binary:
- GO
- NO-GO

## 6. HALT semantics (HARD)
Mission Mode halts immediately on:
1. policy violation
2. failed mandatory verification gate in any unit, including any `pack/verification_manifest.yaml` check marked `halt_on_failure: true`
3. contradiction with the locked mission scope ledger
4. missing or inconsistent evidence links across units
5. unauthorized parallel path activation

When halted:
- current unit marked `failed`
- remaining units marked `skipped` until explicit resume decision
- mission completion report must capture halt reason and evidence pointers

## 7. Iteration controls

### 7.1 Per-unit
Existing Factory caps remain unchanged:
- Stage B/C: max 2 cycles
- Stage I: max 2 cycles

### 7.2 Mission-level
Mission checkpoint revisions are capped at max 2 cycles unless human override is recorded explicitly.

## 8. Scope enforcement across sprint chain
Scope lock points:
1. per-unit intent lock (`intent_lock_report.md`)
2. per-unit pack audit (`PACK_AUDIT_REPORT.md`)
3. mission scope ledger lock
4. mission checkpoint

Any cross-unit requirement not represented in these lock points is BLOCKING.

## 9. Interaction with existing stage contracts
Mission Mode does not modify:
- stage order
- stage entry and exit criteria
- handoff requirements
- execution-mode controls

Mission Mode adds mission-level assembly, checkpointing, and completion reporting above existing contracts.

## 10. Execution policy

### 10.1 Default
Sequential execution is default.

### 10.2 Parallel (exceptional)
Parallel worktrees are allowed only when all are true:
1. dependency independence is proven
2. protected artifact overlap is absent
3. a pre-merge verification plan is approved
4. an evidence reconciliation plan is defined

If any condition fails, parallel execution is forbidden and Mission Mode must halt or revert to sequential flow.

## 11. Mission artifacts (minimum)
Required mission artifacts:
- `MISSION_MANIFEST.md`
- `MISSION_CONTEXT_RECALL_REPORT.md`
- `MISSION_CHECKPOINT.md`
- `MISSION_COMPLETION_REPORT.md`

Optional mission execution helper:
- `MISSION_EXECUTION_PROMPT.md`
- `MISSION_CURSOR.json` (Codex Mission Goal Continuity adapter only; derived resume cursor, not authored mission truth)

These artifacts must follow standard Factory rules:
- version and changelog
- no placeholders
- binary gate semantics
- explicit evidence paths

### 11.1 Derived mission continuity checks
Mission continuity must be verified from:
- `MISSION_MANIFEST.md`
- `MISSION_CONTEXT_RECALL_REPORT.md`
- `MISSION_CHECKPOINT.md`
- referenced run-root and pack artifacts
- relevant `PHASE_STATE.md` when the mission chain is bound to a PO phase ledger

This continuity check is derived. Mission Mode does not maintain a second authored mission-state file.

### 11.2 Mission recall generation contract
Before mission checkpointing or authorizing the next downstream unit:
1. refresh the artifact recall index with `./scripts/factoryctl context-index`
2. generate `docs/Factory/missions/<MISSION_ID>/MISSION_CONTEXT_RECALL_REPORT.md` with `./scripts/factoryctl context-report --profile mission-checkpoint --scope <MISSION_ID> --output docs/Factory/missions/<MISSION_ID>/MISSION_CONTEXT_RECALL_REPORT.md`
3. include focus terms and trace IDs for completed unit run IDs, relevant sprint IDs, unresolved blocker IDs, and any human checkpoint references that remain binding on the next unit
4. add `--required-ref` for any exact run artifact path or exact identifier that must still be recoverable before the next unit is authorized
5. if explicit fallback scopes are not provided, `context-report` applies the mission default order automatically:
   - requested mission scope
   - `docs/Factory/missions`
   - `docs/Factory/runs`
   - `docs`
6. if the written report still records `Coverage Verdict: WEAK` after attempted scopes, halt checkpoint adjudication until recall coverage is repaired

### 11.3 Codex Mission Goal Continuity adapter (experimental)
Some repositories may use Codex goal or bookmark features as a compact Mission Mode resume aid for long-running, multi-session work.

This adapter is optional and does not change the core Factory A-to-I2 process.

Adapter artifacts:
- `docs/Factory/missions/<MISSION_ID>/MISSION_CURSOR.json`
- `scripts/mission_cursor_lint.sh`
- `docs/Factory/templates/MISSION_CURSOR_TEMPLATE.json`

`MISSION_CURSOR.json` is a derived mission resume cursor. It records the current mission, current unit, current unit status, next legal action, execution mode, latest non-cursor validator evidence, and source artifact fingerprints. It exists so an agent session can re-ground before continuing.

Hard rules:
1. `MISSION_MANIFEST.md` remains the only authored mission ledger.
2. `MISSION_CURSOR.json` is not authority, not evidence, and not execution authorization.
3. `MISSION_CURSOR.json` may be deleted and regenerated from mission/run artifacts.
4. Any external goal, task bookmark, or chat summary is only a compact bookmark mirrored from `MISSION_CURSOR.json`.
5. The valid direction is repository artifacts -> `MISSION_CURSOR.json` -> external bookmark.
6. The reverse direction is forbidden; an external bookmark must never update repository truth.
7. Before any continuation uses this adapter, run `bash scripts/mission_cursor_lint.sh <MISSION_ID>`.
8. If mission cursor lint fails, halt continuation and repair the underlying artifact mismatch or regenerate the cursor from valid artifacts.
9. If `halt_required` is true, the only legal next action is `halt`.

Closed `next_legal_action` set:
- `read_mission_artifacts`
- `read_current_unit_pack`
- `initialize_unit_factory_run`
- `run_mission_lint`
- `run_unit_validator`
- `execute_unit_micro_sprint`
- `update_unit_handoff`
- `update_manifest_from_unit_evidence`
- `advance_to_next_unit`
- `await_human_checkpoint`
- `halt`

The adapter must not be used first on auth, wallet, KYC, regulated execution paths, schema boundary changes, or irreversible actions.

## 12. Restart policy
Resume from a failed unit only when:
1. the mission scope ledger is unchanged
2. completed unit evidence remains valid
3. the authorization checkpoint is still valid
4. derived mission continuity preflight passes

If any of these conditions are invalidated:
- require a fresh mission checkpoint decision before resuming
