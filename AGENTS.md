# AGENTS.md — Repository Context Map

Purpose:
- Give any agent a short, authoritative repo map so work starts with correct context and stable commands.

## 1) Read Order (mandatory)
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/MISSION_MODE.md` (if using Mission Mode)
5. `docs/Factory/ProductOwner/PO_PROCESS.md` (if working on PO-authored briefs or phase planning)
6. `docs/Factory/SCRATCHPAD.md` (read only `## Active Pitfalls (Mandatory)`)
7. current sprint artifacts in `docs/sprints/` and current run pack in `docs/Factory/runs/<RUN_ID>/pack/`

## 2) Canonical Commands
- Knowledge lint preflight: `bash scripts/knowledge_lint.sh`
- Context index refresh: `./scripts/factoryctl context-index`
- Stage A recall report: `./scripts/factoryctl context-report --profile stage-a --scope <RUN_ID> --output docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
- Stage validation after each handoff: `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>`
- Pack validation after I2: `./scripts/factoryctl pack-lint --run <RUN_ID>`
- Run metrics initialization: `./scripts/factoryctl metrics-init --run <RUN_ID>`
- Mission continuity preflight: `bash scripts/mission_lint.sh <MISSION_ID>` (only when advancing a unit inside an already-authorized mission)
- Full test suite: replace with your project’s canonical test command

## 3) Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly; new scope must be explicit and approved.
- Keep schema-locked boundaries intact.
- Keep deterministic ordering and evidence-chain integrity in reports and artifacts.
- Do not create a second authored source of truth for mission state when Mission Mode is active.
- Keep continuity artifacts as evidence aids, not as replacement authority for the underlying source documents.

## 4) Factory Run Preconditions
- Run `bash scripts/knowledge_lint.sh` before Stage A.
- Persist lint output in run root as `KNOWLEDGE_LINT.txt`.
- Refresh the recall index and generate `CONTEXT_RECALL_REPORT.md` before Stage A.
- After each stage handoff, run `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>` before advancing.
- After Stage I2, run `./scripts/factoryctl pack-lint --run <RUN_ID>` before presenting the pack for human Go or No-go review.
- For process improvement runs, instantiate `docs/Factory/templates/RUN_METRICS_TEMPLATE.md` as `docs/Factory/runs/<RUN_ID>/RUN_METRICS.md`.
- Prefer `./scripts/factoryctl metrics-init --run <RUN_ID>` to create `RUN_METRICS.md` from the canonical template.
- If the run is advancing a unit inside an already-authorized mission, run `bash scripts/mission_lint.sh <MISSION_ID>` before Stage A and persist output as `MISSION_LINT.txt`.
- If the raw brief originates from the PO process, confirm it has a Brief Review PASS before entering the Factory.
- If any required lint or recall artifact is missing or weak, halt run initialization and fix context drift first.

## 4.1) Product Owner Process
- PO process docs: `docs/Factory/ProductOwner/PO_PROCESS.md`, `docs/Factory/ProductOwner/PO_ROLE_DEFINITION.md`
- Phase artifacts: `docs/Factory/ProductOwner/phases/<PHASE_ID>/`
- The PO writes sprint briefs within a locked Phase Intent. The Factory pipeline is unchanged: PO briefs enter as `raw_brief.md` only after passing a Brief Review Cycle.

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
