# AGENTS.md — Repository Context Map

Purpose:
- Give any agent a short, authoritative repo map so work starts with correct context and stable commands.

## 1) Read Order (mandatory)
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/MISSION_MODE.md` (if using Mission Mode)
5. `docs/Factory/SCRATCHPAD.md` (read only `## Active Pitfalls (Mandatory)`)
6. current sprint artifacts in `docs/sprints/` and current run pack in `docs/Factory/runs/<RUN_ID>/pack/`

## 2) Canonical Commands
- Knowledge lint preflight: `bash scripts/knowledge_lint.sh`
- Mission continuity preflight: `bash scripts/mission_lint.sh <MISSION_ID>` (only when advancing a unit inside an already-authorized mission)
- Full test suite: replace with your project’s canonical test command

## 3) Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly; new scope must be explicit and approved.
- Keep schema-locked boundaries intact.
- Keep deterministic ordering and evidence-chain integrity in reports and artifacts.
- Do not create a second authored source of truth for mission state when Mission Mode is active.

## 4) Factory Run Preconditions
- Run `bash scripts/knowledge_lint.sh` before Stage A.
- Persist lint output in run root as `KNOWLEDGE_LINT.txt`.
- If the run is advancing a unit inside an already-authorized mission, run `bash scripts/mission_lint.sh <MISSION_ID>` before Stage A and persist output as `MISSION_LINT.txt`.
- If either lint fails, halt run initialization and fix context drift first.

## 5) Change Hygiene
- When sprint outcomes are GO, update in the same cycle:
  - `docs/PROJECT_STATE.md`
  - `docs/ROADMAP.md`
  - `docs/CHANGELOG.md`
- If Mission Mode is active, update `MISSION_MANIFEST.md` in the same closure cycle as unit evidence.
- Keep `docs/Factory/SCRATCHPAD.md` compact (max 12 active pitfalls).
- Prefer small, auditable changes with explicit evidence paths.

## 6) When Uncertain
- Stop and lock intent and constraints first.
- Add verification hooks before implementation details.
- Escalate ambiguous policy or contract assumptions as BLOCKING instead of guessing.
