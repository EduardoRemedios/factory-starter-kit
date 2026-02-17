# AGENTS.md — Repository Context Map

Purpose:
- Give any agent a short, authoritative repo map so work starts with correct context and stable commands.

## 1) Read Order (mandatory)
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/SCRATCHPAD.md` (read only `## Active Pitfalls (Mandatory)`)
5. Current sprint artifacts in `docs/sprints/` and current run pack in `docs/Factory/runs/<RUN_ID>/pack/`

## 2) Canonical Commands
- Knowledge lint preflight: `bash scripts/knowledge_lint.sh`
- Full test suite: `python3 -m pytest tests/` (or your project's test command)

## 3) Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly; new scope must be explicit and approved.
- Keep schema-locked boundaries intact (no undocumented input/output drift).
- Keep deterministic ordering and evidence-chain integrity in reports/artifacts.

## 4) Factory Run Preconditions
- Run `bash scripts/knowledge_lint.sh` before Stage A.
- Persist lint output in run root as `KNOWLEDGE_LINT.txt`.
- If lint fails, halt run initialization and fix context drift first.

## 5) Change Hygiene
- When sprint outcomes are GO, update in the same cycle:
  - `docs/PROJECT_STATE.md`
  - `docs/ROADMAP.md`
  - `docs/CHANGELOG.md`
- Keep `docs/Factory/SCRATCHPAD.md` compact (max 12 active pitfalls).
- Prefer small, auditable changes with explicit evidence paths.

## 6) When Uncertain
- Stop and lock intent/constraints first.
- Add verification hooks before implementation details.
- Escalate ambiguous policy/contract assumptions as BLOCKING instead of guessing.
