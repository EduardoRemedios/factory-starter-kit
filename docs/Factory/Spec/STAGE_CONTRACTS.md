# docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.10)

## Version
v4.10

## Change Log
- v4.10 (2026-04-26): Added stage-lint as a deterministic per-stage handoff/output check before advancing to the next stage.
- v4.9 (2026-04-26): Added post-I2 pack-lint validation as a deterministic evidence check before human Go or No-go review.
- v4.8 (2026-03-21): Added mandatory context-recall contracts and run-root `CONTEXT_RECALL_REPORT.md` evidence for Stage A, plus mission-root `MISSION_CONTEXT_RECALL_REPORT.md` continuity evidence for Mission Mode checkpointing.
- v4.7 (2026-03-10): Added Mission Mode pre-run `mission_lint.sh` contract with run-root `MISSION_LINT.txt` evidence, clarified that Mission Mode keeps one authored mission ledger (`MISSION_MANIFEST.md`), and aligned Stage A and Mission wrapper requirements to the mission drift hardening rules.
- v4.6 (2026-02-27): Added additive Mission Mode wrapper contract while preserving the canonical sprint `A -> I2` plus `POST_GATE` flow.
- v4.5 (2026-02-14): Added `EXECUTION_MODE.txt` run contract with `PLANNING_ONLY` default and gated post-gate execution prompt generation and downstream fan-out to `EXECUTION_ENABLED` runs only.
- v4.4 (2026-02-12): Added deterministic skill-invocation contract for critical gates and added required post-I2 PASS plus human GO execution-prompt generation using `EXECUTION_PROMPT_TEMPLATE.md`.
- v4.3 (2026-02-11): Added mandatory pre-run knowledge-lint contract with required run artifact (`KNOWLEDGE_LINT.txt`) and Stage A entry criterion wiring.
- v4.2 (2026-02-10): Aligned Stage H/I/I2 envelope artifact references to `<SPRINT_ID>_ENVELOPE*.md` to avoid `SPRINT_SPRINT_*` naming drift.
- v4.1 (2026-02-09): Added cross-run memory contract: only `SCRATCHPAD.md` `Active Pitfalls` is mandatory pre-run memory; run narratives are run-local in `runs/<RUN_ID>/RETRO.md` and optional.
- v4.0 (2026-02-08): Reordered `STAGE_J` before `STAGE_I2`, resolving the checklist dependency, and added execution prompt generation as the recommended post-pipeline step.

## Global rules (HARD)
- No stage may start unless its entry criteria pass.
- No stage may complete unless its exit criteria pass.
- Pre-run knowledge lint MUST pass (`bash scripts/knowledge_lint.sh`) before `STAGE_A` starts, and output MUST be persisted at `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`.
- If the run is advancing a unit inside an already-authorized mission, pre-run mission lint MUST pass (`bash scripts/mission_lint.sh <MISSION_ID>`) before `STAGE_A` starts, and output MUST be persisted at `docs/Factory/runs/<RUN_ID>/MISSION_LINT.txt`.
- Every stage produces `pack/HANDOFF/HANDOFF_STAGE_<STAGE_CODE>.md` containing:
  - outputs produced
  - changes made
  - assumptions
  - open issues (`BLOCKING` and `NON-BLOCKING`)
  - verification steps recommended
  - exit criteria PASS or FAIL
  - iteration metadata when applicable
- After each stage writes its handoff, run `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE_CODE>`. If stage-lint fails, do not advance to the next stage until the handoff or expected stage output is fixed.
- Handoff size caps and change log format are enforced per `DEFINITIONS.md`.
- For critical gate stages (`STAGE_D`, `STAGE_J`, `STAGE_I2`), stage prompts MUST include deterministic skill invocation when a relevant skill exists:
  - `Use the <skill name> skill.`
  - If no relevant skill exists, prompts MUST declare that explicitly and proceed via the stage contract only.
- Run execution mode defaults to `PLANNING_ONLY` and MUST be persisted in run-root `EXECUTION_MODE.txt`.
- `EXECUTION_PROMPT.md` generation and downstream run fan-out are forbidden unless `EXECUTION_MODE.txt` is `EXECUTION_ENABLED`.
- Mission Mode, if enabled, is additive and MUST NOT alter per-unit stage entry and exit criteria, authorization contracts, or iteration caps.

## Iteration metadata (HARD)
Stages that can run in cycles MUST declare:
- `Iteration: k of max N` (`N = 2` unless explicitly stated otherwise)

Cycle stages:
- `STAGE_B`
- `STAGE_C`
- `STAGE_I`

## Context loading rule (HARD)
Each stage’s inputs must:
- exist on disk
- be loaded into the agent’s working context if marked `LOAD`

Stage inputs are labelled:
- `LOAD`: must be read and summarized before writing outputs
- `DISK`: must exist; may be consulted as needed

## Context recall rule (HARD)
- `STAGE_A` may not start until `docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md` exists and was generated from the artifact recall index via `./scripts/factoryctl context-report --profile stage-a`.
- Mission checkpointing and downstream mission-unit planning may not proceed until `docs/Factory/missions/<MISSION_ID>/MISSION_CONTEXT_RECALL_REPORT.md` exists and was generated via `./scripts/factoryctl context-report --profile mission-checkpoint`.
- PO sprint brief drafting and review must follow the PO process recall contract in `docs/Factory/ProductOwner/PO_PROCESS.md`; Factory stage execution assumes that upstream brief-cycle recall evidence already exists when the raw brief originated from the PO lane.
- Context recall artifacts are evidence aids, not authority. Source artifacts remain canonical.

## Cross-run memory rule (HARD)
- Mandatory pre-run cross-run memory is limited to `docs/Factory/SCRATCHPAD.md` `## Active Pitfalls (Mandatory)`.
- Per-run retrospectives live in `docs/Factory/runs/<RUN_ID>/RETRO.md` and are optional context unless explicitly required by a stage brief.

## Run structure (HARD)
A run produces:
- `docs/Factory/runs/<RUN_ID>/raw_brief.md`
- `docs/Factory/runs/<RUN_ID>/RETRO.md`
- `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`
- `docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
- `docs/Factory/runs/<RUN_ID>/EXECUTION_MODE.txt`
- `docs/Factory/runs/<RUN_ID>/SPRINT_ID.txt`
- `docs/Factory/runs/<RUN_ID>/pack/`
- `docs/Factory/runs/<RUN_ID>/EXECUTION_PROMPT.md` (required only when `EXECUTION_MODE.txt = EXECUTION_ENABLED` after `STAGE_I2` PASS plus human GO)

If Mission Mode is enabled, mission root additionally produces:
- `docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CONTEXT_RECALL_REPORT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CHECKPOINT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_COMPLETION_REPORT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_EXECUTION_PROMPT.md` (optional)

If the run is advancing a unit inside an already-authorized mission, run root additionally produces:
- `docs/Factory/runs/<RUN_ID>/MISSION_LINT.txt`

## Dependency graph (authoritative)
- `STAGE_A` produces `intent.md`
- `STAGE_B` consumes `intent.md` and produces `intent_redteam.md`
- `STAGE_C` consumes `intent.md` and `intent_redteam.md`, updates `intent.md`, and produces `intent_synthesis.md`
- `STAGE_D` consumes intent docs and produces `intent_lock_report.md`
- `STAGE_E` consumes locked `intent.md` and produces `premortem.md` and `risk_register.md`
- `STAGE_F` consumes locked `intent.md` and `risk_register.md` and produces `fixtures/`, `verification_plan.md`, and `traceability_matrix.md`
- `STAGE_G` consumes `intent.md`, `risk_register.md`, and `verification_plan.md` and produces `micro_sprints.md`
- `STAGE_H` consumes `intent.md`, `micro_sprints.md`, and `verification_plan.md` and produces `<SPRINT_ID>_ENVELOPE.md` and `SPRINT_ID.txt`
- `STAGE_I` consumes the envelope and verification assets and produces the envelope red-team report plus any hardened revisions
- `STAGE_J` consumes the full pack and produces `PACK_MANIFEST.md` and `PACK_CHECKLIST.md`
- `STAGE_I2` consumes the full pack plus `PACK_CHECKLIST.md` and `PACK_MANIFEST.md` and produces `PACK_AUDIT_REPORT.md`
- Mission Mode consumes one or more completed sprint packs and applies a mission-level checkpoint before chained execution

## STAGE_VALIDATION — Stage Lint
Purpose:
- deterministically validate one stage handoff and its expected outputs immediately after that stage completes
- catch malformed handoffs, unresolved placeholders, missing iteration metadata, missing stage outputs, and handoff word-cap drift before later stages build on them

Command:
- `./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE_CODE>`

Exit criteria:
- `stage_lint: PASS`
- if stage-lint returns FAIL, fix the stage handoff or expected output before advancing

Authority:
- stage-lint is a deterministic evidence check; it does not replace Red, Blue, Purple, or human judgment

## Intent Unlock Protocol (HARD)
If any downstream stage discovers the locked intent is flawed:
- unlock requires Purple plus human approval
- a new `intent.md` version must be created with an updated change log
- downstream stages `E` through `J` must be re-run or re-validated against the updated intent

## STAGE_A — Intent Contracting
Inputs:
- `LOAD`: `raw_brief.md`, `CONTEXT_RECALL_REPORT.md`
- `DISK`: `KNOWLEDGE_LINT.txt`, `EXECUTION_MODE.txt`
- `DISK`: `MISSION_LINT.txt` (already-authorized mission-unit runs only)

Outputs:
- `raw_brief.md`
- `pack/intent.md`

Entry criteria:
- raw brief content exists and is non-empty
- `KNOWLEDGE_LINT.txt` exists and records a successful knowledge-lint preflight
- `CONTEXT_RECALL_REPORT.md` exists and records a Stage A recall pass generated from the artifact recall index for this run
- if the run is advancing a unit inside an already-authorized mission, `MISSION_LINT.txt` exists and records a successful mission-lint preflight
- `EXECUTION_MODE.txt` exists and contains exactly one value: `PLANNING_ONLY` or `EXECUTION_ENABLED`

Exit criteria:
- `intent.md` includes Purpose, Goal, Non-goals, Principles, Roles, Acceptance Criteria, and Go or No-Go rule
- open questions are labeled `BLOCKING` or `NON-BLOCKING`
- requirements are sourced or tagged `[INFERRED]` per `DEFINITIONS.md`

## STAGE_B — Red Team (Intent)
Inputs:
- `LOAD`: `pack/intent.md`

Outputs:
- `pack/intent_redteam.md`

Exit criteria:
- findings include severity, why it matters, and fix recommendation
- findings include agent failure modes and verification holes

Iteration:
- required: `Iteration: k of max 2`

## STAGE_C — Blue Team + Synthesis (Intent)
Inputs:
- `LOAD`: `pack/intent.md`, `pack/intent_redteam.md`

Outputs:
- updated `pack/intent.md`
- `pack/intent_synthesis.md`

Exit criteria:
- no unresolved critical findings remain, or they are explicitly marked blocking for Purple
- any net-new requirement is tagged `[SCOPE EXPANSION]` and marked blocking

Iteration:
- required: `Iteration: k of max 2`

## STAGE_D — Purple Gate (Intent Lock)
Inputs:
- `LOAD`: `pack/intent.md`, `pack/intent_redteam.md`, `pack/intent_synthesis.md`

Outputs:
- `pack/intent_lock_report.md`

Prompt rule (HARD):
- if a relevant skill exists, the prompt MUST include `Use the <skill name> skill.`

Exit criteria:
- `intent_lock_report.md` records verdict, reasons, and any bounded deferrals with micro-sprint hooks
- no PASS or CONDITIONAL PASS is allowed if any `[SCOPE EXPANSION]` remains unapproved

## STAGE_E — Pre-mortem + Risk Register
Inputs:
- `LOAD`: locked `pack/intent.md`
- `DISK`: `pack/intent_lock_report.md`

Outputs:
- `pack/premortem.md`
- `pack/risk_register.md`

Exit criteria:
- premortem lists top failure scenarios and mitigations
- risk register lists severity, mitigation, and suggested verification hook

## STAGE_F — Verification Assets
Inputs:
- `LOAD`: locked `pack/intent.md`, `pack/risk_register.md`
- `DISK`: `pack/intent_lock_report.md`

Outputs:
- `pack/fixtures/…`
- `pack/verification_plan.md`
- `pack/traceability_matrix.md`

Exit criteria:
- every Critical or High constraint has at least one fixture, test, or check
- traceability matrix is complete for Critical and High items
- fixtures follow naming conventions

## STAGE_G — Micro-sprint Sequencing
Inputs:
- `LOAD`: `pack/intent.md`, `pack/risk_register.md`, `pack/verification_plan.md`
- `DISK`: `pack/traceability_matrix.md`, `pack/intent_synthesis.md`

Outputs:
- `pack/micro_sprints.md`

Exit criteria:
- each micro-sprint includes objective, inputs, outputs, entry criteria, exit criteria, and stop or go gate
- micro-sprints reference bounded deferral hooks where applicable

## STAGE_H — Sprint Envelope
Inputs:
- `LOAD`: `pack/intent.md`, `pack/micro_sprints.md`, `pack/verification_plan.md`
- `DISK`: `pack/traceability_matrix.md`

Outputs:
- `SPRINT_ID.txt`
- `pack/<SPRINT_ID>_ENVELOPE.md`

Exit criteria:
- envelope includes file-touch budget fields per micro-sprint and in total
- envelope includes verification steps required before merge and references `verification_plan.md` and `traceability_matrix.md`
- sprint ID conforms to naming conventions and is written to `SPRINT_ID.txt`

## STAGE_I — Red/Blue on Envelope + Verification
Inputs:
- `LOAD`: `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/verification_plan.md`, `pack/traceability_matrix.md`, `pack/micro_sprints.md`
- `DISK`: `pack/fixtures/`, `pack/risk_register.md`, `pack/intent_lock_report.md`

Outputs:
- `pack/<SPRINT_ID>_ENVELOPE_REDTEAM.md`
- updated `pack/<SPRINT_ID>_ENVELOPE.md`
- updated verification assets if needed

Exit criteria:
- max 2 Red/Blue cycles completed
- no unresolved critical findings remain, or they are explicitly marked blocking for Purple adjudication
- any `[SCOPE EXPANSION]` introduced is blocking and must be carried to Purple

Iteration:
- required: `Iteration: k of max 2`

## STAGE_J — Pack Consolidation (runs BEFORE I2)
Inputs:
- `DISK`: all pack artifacts except `PACK_AUDIT_REPORT.md`

Outputs:
- `pack/PACK_MANIFEST.md`
- `pack/PACK_CHECKLIST.md`

Prompt rule (HARD):
- if a relevant skill exists, the prompt MUST include `Use the <skill name> skill.`

Exit criteria:
- manifest lists all required files and confirms non-empty status, with `PACK_AUDIT_REPORT.md` marked pending
- checklist items match the spec and are fully yes/no answerable with evidence fields
- checklist answers are populated from available artifacts

## STAGE_I2 — Purple Audit (Pack Gate, runs AFTER J)
Inputs:
- `LOAD`: `pack/intent.md`, `pack/intent_lock_report.md`, `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/traceability_matrix.md`, `pack/verification_plan.md`, `pack/micro_sprints.md`, `pack/PACK_CHECKLIST.md`, `pack/PACK_MANIFEST.md`
- `DISK`: everything else in `pack/`

Outputs:
- `pack/PACK_AUDIT_REPORT.md`
- updated `pack/PACK_MANIFEST.md`

Prompt rule (HARD):
- if a relevant skill exists, the prompt MUST include `Use the <skill name> skill.`

Exit criteria:
- Purple Gate Checklist evaluated via the run-specific `PACK_CHECKLIST.md`
- verdict recorded: PASS, CONDITIONAL PASS, or FAIL
- no PASS or CONDITIONAL PASS allowed if any `[SCOPE EXPANSION]` remains unapproved
- `PACK_MANIFEST.md` updated to mark `PACK_AUDIT_REPORT.md` as present and non-empty

## POST_I2_VALIDATION — Pack Lint
Purpose:
- run deterministic validation over the completed planning pack before human Go or No-go review

Command:
- `./scripts/factoryctl pack-lint --run <RUN_ID>`

Checks include:
- required run-root and pack files exist and are non-empty
- expected handoffs exist
- no unresolved placeholders remain
- word caps are satisfied
- checklist critical items are `YES`
- audit verdict is not `FAIL`
- execution-mode evidence is internally consistent

Exit criteria:
- `pack-lint` returns PASS before the pack is presented for human execution review
- if `pack-lint` returns FAIL, defects are fixed in the pack and affected stage handoffs are updated

## POST_GATE — Execution Prompt Generation (execution-enabled runs only)
Skip rule:
- if `EXECUTION_MODE.txt = PLANNING_ONLY`, this stage is skipped and the run terminates at planning-pack completion

Entry criteria:
- `STAGE_I2` verdict is PASS
- human review decision is explicit Go
- `EXECUTION_MODE.txt` equals `EXECUTION_ENABLED`

Inputs:
- `LOAD`: `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/micro_sprints.md`, `pack/verification_plan.md`, `pack/traceability_matrix.md`
- `DISK`: `pack/intent.md`, `pack/risk_register.md`, `pack/PACK_AUDIT_REPORT.md`, `docs/Factory/SCRATCHPAD.md`

Outputs:
- `EXECUTION_PROMPT.md`

Exit criteria:
- prompt is instantiated from `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md`
- prompt has no unresolved placeholders
- prompt includes deterministic skill routing instructions and stage-aligned guardrails

## MISSION_WRAPPER (additive, optional — not a replacement stage chain)
Purpose:
- wrap multiple completed sprint packs into one mission execution sequence under one consolidated checkpoint

Mission inputs:
- `DISK`: referenced sprint run roots and packs
- `DISK`: `docs/Factory/MISSION_MODE.md`
- `LOAD`: mission manifest, mission context recall report, checkpoint, and completion artifacts

Mission outputs:
- `docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CONTEXT_RECALL_REPORT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CHECKPOINT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_COMPLETION_REPORT.md`

Mission hard rules:
1. Mission does not bypass per-unit `A -> I2` contracts
2. per-unit iteration caps remain unchanged
3. mission checkpoint must record one explicit GO or NO-GO decision
4. any policy, scope, or verification breach in a unit halts the mission
5. remaining units after halt are marked skipped until restart authorization
6. `MISSION_MANIFEST.md` remains the authored ledger of record
7. if a unit run is advancing an already-authorized mission, pre-run mission lint must pass before `STAGE_A` begins

Mission restart rule:
- resume from a failed unit only if mission scope ledger, prior evidence integrity, and mission checkpoint authorization remain valid
