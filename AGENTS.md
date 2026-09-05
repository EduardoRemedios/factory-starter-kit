# AGENTS.md — Repository Context Map

<!-- conductor:managed:start v=0.3.0-dev sha256=068bdb48464b4fa9c42c9c80098f71a4421c1a509dac8e68de2068978a951a7a -->
## Conductor (managed block)
Read order (mandatory): `docs/PROJECT_STATE.md`, then `docs/Conductor/INVARIANTS.md`. Everything else on demand.

Conductor governs authority, outcomes, and write boundaries; it does not govern steps. Three gates: G1 Intent Lock (human countersign), G2 Governed Execution (autonomous, receipt-audited), G3 Adversarial Review and Completion (fresh-context verifier, Statement of Completion, human countersign). Merge authorization follows `docs/Conductor/MERGE_PROTOCOL.md`.

Autonomy contract (applies inside any G2 run):
You are operating under Conductor governance. The Intent Pack sets the scope and the scope is the deliverable: do not narrow, widen, or swap it. For reversible actions inside the locked intent, proceed without asking. Stop only for a destructive action, a genuine scope change, or input only a human can provide; record such a stop as a Gap Request, not as a question in chat. Before reporting progress, audit each claim against a receipt from this run; report only what a receipt proves, and say explicitly what is not yet verified. Before ending your turn, check your last paragraph: if it is a plan, a question, or a promise, do that work now. Implement the smallest clear change (SIMPLE-CODE-GATE v2 applies). Do not write tests for reversible, low-impact changes beyond what the verification manifest requires.

Everything below this block is project-owned and preserved byte for byte by Conductor adoption and update.
<!-- conductor:managed:end -->

> The sections below are the 0.2-era operating instructions, kept for archived runs and the golden-pack tests. For new work the managed block above is authoritative: read `docs/PROJECT_STATE.md` and `docs/Conductor/INVARIANTS.md`, then follow the three gates in `docs/Conductor/onboarding/GUIDE.md`.

Purpose:
- Give any agent a short, authoritative repo map so work starts with correct context and stable commands.

## 1) Read Order (mandatory)
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Conductor/ARCHITECTURE.md`
4. `docs/Conductor/ORCHESTRATION.md`
5. `docs/Conductor/MISSION_MODE.md` (if using Mission Mode)
6. `docs/Conductor/ProductOwner/PO_PROCESS.md` (if working on PO-authored briefs or phase planning)
7. `docs/Conductor/SCRATCHPAD.md` (read only `## Active Pitfalls (Mandatory)`)
8. current sprint artifacts in `docs/sprints/` and current run pack in `docs/Conductor/runs/<RUN_ID>/pack/`

## 2) Canonical Commands
- Knowledge lint preflight: `bash scripts/knowledge_lint.sh`
- Optional declared project preflight: `./scripts/conductorctl project-preflight --run <RUN_ID>`
- Context index refresh: `./scripts/conductorctl context-index`
- Stage A recall report: `./scripts/conductorctl context-report --profile stage-a --scope <RUN_ID> --output docs/Conductor/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
- Stage validation after each handoff: `./scripts/conductorctl stage-lint --run <RUN_ID> --stage <STAGE>`
- Kilo external model lane (optional): `./scripts/conductorctl kilo-stage --run <RUN_ID> --stage <STAGE> --model <KILO_MODEL_ID> --variant high --auto --timeout-seconds 900`
- Pack validation after I2: `./scripts/conductorctl pack-lint --run <RUN_ID>`
- Execution closeout recording: `./scripts/conductorctl execution-closeout --run <RUN_ID> --input <AUTHORED_DRAFT.json> --json`
- Run metrics initialization: `./scripts/conductorctl metrics-init --run <RUN_ID>`
- Task memory initialization (optional): `./scripts/conductorctl memory-init`
- Repo cartographer scan (optional): `./scripts/cartographer`
- Agent Loop Bridge fixture validation (optional): `./scripts/conductor-python scripts/agent_loop_bridge_validate.py tests/fixtures/agent_loop_bridge/valid_handoff.json --json`
- Install script dependencies: `./scripts/conductor-python -m pip install -r requirements.txt`
- Mission continuity preflight: `bash scripts/mission_lint.sh <MISSION_ID>` (only when advancing a unit inside an already-authorized mission)
- Mission cursor lint (optional Codex Mission Goal Continuity adapter): `bash scripts/mission_cursor_lint.sh <MISSION_ID>`
- Merge preflight: define/adapt `bash scripts/merge_preflight.sh` in adopting repos; see `docs/Conductor/MERGE_PROTOCOL.md`
- Full test suite: replace with your project’s canonical test command

## 3) Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly; new scope must be explicit and approved.
- Keep schema-locked boundaries intact.
- Keep deterministic ordering and evidence-chain integrity in reports and artifacts.
- Run Factory-controlled Python verification through `./scripts/conductor-python`; do not bypass its bytecode guard with a raw interpreter command.
- Keep complete high-volume evidence in an explicitly authorized file and emit only bounded summaries through the harness. Never make conversational output the evidence store.
- Do not create a second authored source of truth for mission state when Mission Mode is active.
- Keep continuity artifacts as evidence aids, not as replacement authority for the underlying source documents.
- If an adopting repo has a separate autonomy governance kernel, do not duplicate kernel authority, policy, evidence, lease, or runtime-action behavior inside Factory.

## 3.1) SIMPLE-CODE-GATE (v2)
Availability:
- Mandatory implementation guardrail for Factory-controlled code-changing work.
- Applies to planning, execution, and review wherever Factory controls implementation scope.

Core Directive:
- Implement the smallest clear, behavior-preserving change.
- Prefer direct, readable, local code over cleverness or premature abstraction.

Banned List:
- No Code Bloat: avoid copy-paste chunks, awkward abstraction layers, and bloated multi-purpose helpers.
- No Spooky Action: avoid brittle request-path mutation, hidden side effects, or passing unvalidated junk through middleware/boundary layers.
- No Dependency Creep: use the standard library and existing repo utilities first. Do not introduce external packages unless explicitly authorized and justified.
- No Silent Failures: do not swallow exceptions or return ambiguous `None`/empty fallbacks just to keep a path limping along. Fail fast for invalid config/init/state. In runtime policy paths, fail closed explicitly with reason codes, evidence, and tests.

Abstraction Firewall:
- Add an abstraction or helper only when it passes all four checks:
  1. Removes real, existing duplication.
  2. Names a stable domain concept.
  3. Reduces branching or call-site complexity.
  4. Has a clear owner/boundary in the current architecture.

Future-Proofing and Context:
- Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection just because future variation is possible.
- If future variation is uncertain, keep the code explicit and document the specific scale metric, repeated pattern, or business condition that will trigger a refactor.
- Comments must explain why, not what. No line-by-line narration of obvious logic.

## 4) Factory Run Preconditions
- Run `bash scripts/knowledge_lint.sh` before Stage A.
- Persist lint output in run root as `KNOWLEDGE_LINT.txt`.
- If `docs/Conductor/PROJECT_PREFLIGHT.json` exists, run `./scripts/conductorctl project-preflight --run <RUN_ID>` after Core knowledge lint and before context recall; persist/pass `PROJECT_PREFLIGHT.txt` or halt.
- Refresh the recall index and generate `CONTEXT_RECALL_REPORT.md` before Stage A.
- After each stage handoff, run `./scripts/conductorctl stage-lint --run <RUN_ID> --stage <STAGE>` before advancing.
- After Stage I2, run `./scripts/conductorctl pack-lint --run <RUN_ID>` before presenting the pack for human Go or No-go review.
- After authorized execution, record `EXECUTION_CLOSEOUT.json` only through the canonical validator; present-invalid closeout evidence blocks and never falls back to legacy progress.
- For execution-enabled or Mission Mode runs, `pack/verification_manifest.yaml` is mandatory whenever `verification_plan.md` declares runnable VM checks: the canonical execution closeout cannot be recorded without it, `pack-lint` fails an execution-enabled run that lacks it, and a planning-only pack gets a warning that it cannot legally close after activation. When present, `pack-lint` validates it.
- For process improvement runs, instantiate `docs/Conductor/templates/RUN_METRICS_TEMPLATE.md` as `docs/Conductor/runs/<RUN_ID>/RUN_METRICS.md`.
- Prefer `./scripts/conductorctl metrics-init --run <RUN_ID>` to create `RUN_METRICS.md` from the canonical template.
- Optional task memory and cartographer outputs are advisory artifacts only; they do not replace Factory source artifacts, pack-lint, stage-lint, or human Go/No-go.
- If the run is advancing a unit inside an already-authorized mission, run `bash scripts/mission_lint.sh <MISSION_ID>` before Stage A and persist output as `MISSION_LINT.txt`.
- If using the optional Codex Mission Goal Continuity adapter, run `bash scripts/mission_cursor_lint.sh <MISSION_ID>` before continuing from `MISSION_CURSOR.json` or an external goal/bookmark; `MISSION_CURSOR.json` is a derived resume cursor, not mission truth.
- If the raw brief originates from the PO process, confirm it has a Brief Review PASS before entering the Factory.
- If any required lint or recall artifact is missing or weak, halt run initialization and fix context drift first.

## 4.1) Product Owner Process
- PO process docs: `docs/Conductor/ProductOwner/PO_PROCESS.md`, `docs/Conductor/ProductOwner/PO_ROLE_DEFINITION.md`
- Phase artifacts: `docs/Conductor/ProductOwner/phases/<PHASE_ID>/`
- The PO writes sprint briefs within a locked Phase Intent. The Factory pipeline is unchanged: PO briefs enter as `raw_brief.md` only after passing a Brief Review Cycle.

## 5) Change Hygiene
- When sprint outcomes are GO, update in the same cycle:
  - `docs/PROJECT_STATE.md`
  - `docs/ROADMAP.md`
  - `docs/CHANGELOG.md`
- If Mission Mode is active, update `MISSION_MANIFEST.md` in the same closure cycle as unit evidence.
- Keep `docs/Conductor/SCRATCHPAD.md` compact (max 12 active pitfalls).
- Prefer small, auditable changes with explicit evidence paths.

## 6) When Uncertain
- Stop and lock intent and constraints first.
- Add verification hooks before implementation details.
- Escalate ambiguous policy or contract assumptions as BLOCKING instead of guessing.
