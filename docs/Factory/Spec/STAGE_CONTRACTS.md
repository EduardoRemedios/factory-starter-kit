# docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.7)

## Version
v4.7

## Change Log
- v4.7 (2026-03-10): Added Mission Mode pre-run `mission_lint.sh` contract with run-root `MISSION_LINT.txt` evidence, clarified that Mission Mode keeps one authored mission ledger (`MISSION_MANIFEST.md`), and aligned Stage A/MISSION_WRAPPER requirements to the mission drift hardening rules.
- v4.6 (2026-02-27): Added additive Mission Mode wrapper contract (manifest/checkpoint/completion artifacts, mission checkpoint gate, mission halt/restart controls) while preserving the canonical sprint A→I2+POST_GATE flow.
- v4.5 (2026-02-14): Added `EXECUTION_MODE.txt` run contract with `PLANNING_ONLY` default and gated POST_GATE execution prompt generation/downstream fan-out to `EXECUTION_ENABLED` runs only.
- v4.4 (2026-02-12): Added deterministic skill-invocation contract for critical gates (STAGE_D/STAGE_J/STAGE_I2), and added required post-I2 PASS + human GO execution-prompt generation using `EXECUTION_PROMPT_TEMPLATE.md`.
- v4.3 (2026-02-11): Added mandatory pre-run knowledge-lint contract (`bash scripts/knowledge_lint.sh`) with required run artifact (`KNOWLEDGE_LINT.txt`) and Stage A entry criterion wiring.
- v4.2 (2026-02-10): Aligned Stage H/I/I2 envelope artifact references to `<SPRINT_ID>_ENVELOPE*.md` to avoid `SPRINT_SPRINT_*` naming drift.
- v4.1 (2026-02-09): Added cross-run memory contract: only `SCRATCHPAD.md` `Active Pitfalls` is mandatory pre-run memory; run narratives are run-local in `runs/<RUN_ID>/RETRO.md` and optional. Updated run structure accordingly.
- v4 (2026-02-08): **Breaking: reordered STAGE_J before STAGE_I2** to resolve circular dependency (I2 requires PACK_CHECKLIST as input, but J produces it). J now runs immediately after STAGE_I, producing PACK_CHECKLIST + PACK_MANIFEST. I2 then audits the complete pack using the checklist. Added execution prompt generation as recommended post-pipeline step. Added lessons from the first live run.
- v3 (2026-02-06): Canonicalized Stage I½ to STAGE_I2, removed checklist duplication in audit flow (audit references PACK_CHECKLIST as source-of-truth), added iteration metadata requirements, and aligned template file splits.

## Global rules (HARD)
- No stage may start unless its entry criteria pass.
- No stage may complete unless its exit criteria pass.
- Pre-run knowledge lint MUST pass (`bash scripts/knowledge_lint.sh`) before STAGE_A starts, and output MUST be persisted at `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt`.
- If the run is advancing a unit inside an already-authorized mission, pre-run mission lint MUST pass (`bash scripts/mission_lint.sh <MISSION_ID>`) before STAGE_A starts, and output MUST be persisted at `docs/Factory/runs/<RUN_ID>/MISSION_LINT.txt`.
- Every stage produces `pack/HANDOFF/HANDOFF_STAGE_<STAGE_CODE>.md` containing:
  - Outputs produced (paths)
  - Changes made (bullets)
  - Assumptions (bullets)
  - Open issues (BLOCKING/NON-BLOCKING)
  - Verification steps recommended (bullets)
  - Exit criteria PASS/FAIL
  - Iteration metadata (see below)
- Handoff size caps and change log format are enforced per `DEFINITIONS.md`.
- For critical gate stages (STAGE_D, STAGE_J, STAGE_I2), stage prompts MUST include deterministic skill invocation when a relevant skill exists:
  - `Use the <skill name> skill.`
  - If no relevant skill exists, prompts MUST declare that explicitly and proceed via stage contract only.
- Run execution mode defaults to `PLANNING_ONLY` and MUST be persisted in run-root `EXECUTION_MODE.txt`.
- `EXECUTION_PROMPT.md` generation and downstream run fan-out are forbidden unless `EXECUTION_MODE.txt` is `EXECUTION_ENABLED`.
- Mission Mode (if enabled) is additive and MUST NOT alter per-unit stage entry/exit criteria, authorization contracts, or iteration caps.

## Iteration metadata (HARD)
Stages that can run in cycles MUST declare:
- Iteration: `k of max N` (N = 2 unless explicitly stated otherwise)

Cycle stages:
- STAGE_B (Intent Red Team): Iteration required
- STAGE_C (Intent Blue/Synthesis): Iteration required
- STAGE_I (Envelope Red/Blue): Iteration required

## Context loading rule (HARD)
Each stage’s inputs must:
- exist on disk (always), and
- be loaded into the agent’s working context if marked **LOAD**.

Stage inputs are labelled:
- **LOAD:** must be read and summarized before writing outputs.
- **DISK:** must exist; may be consulted as needed.

## Cross-run memory rule (HARD)
- Mandatory pre-run cross-run memory is limited to `docs/Factory/SCRATCHPAD.md` `## Active Pitfalls (Mandatory)`.
- Per-run retrospectives live in `docs/Factory/runs/<RUN_ID>/RETRO.md` and are optional context unless explicitly required by a stage brief.

## Run structure (HARD)
A run produces:
- `docs/Factory/runs/<RUN_ID>/raw_brief.md`
- `docs/Factory/runs/<RUN_ID>/RETRO.md` (run-local retrospective)
- `docs/Factory/runs/<RUN_ID>/KNOWLEDGE_LINT.txt` (pre-run lint evidence)
- `docs/Factory/runs/<RUN_ID>/EXECUTION_MODE.txt` (`PLANNING_ONLY` by default; `EXECUTION_ENABLED` only with explicit raw-brief authorization)
- `docs/Factory/runs/<RUN_ID>/SPRINT_ID.txt` (Stage H)
- `docs/Factory/runs/<RUN_ID>/pack/` (all pack artifacts)
- `docs/Factory/runs/<RUN_ID>/EXECUTION_PROMPT.md` (required only when `EXECUTION_MODE.txt = EXECUTION_ENABLED` after STAGE_I2 PASS + human GO)

If Mission Mode is enabled, mission root additionally produces:
- `docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CHECKPOINT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_COMPLETION_REPORT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_EXECUTION_PROMPT.md` (optional helper artifact)

If the run is advancing a unit inside an already-authorized mission, run root additionally produces:
- `docs/Factory/runs/<RUN_ID>/MISSION_LINT.txt`

## Dependency graph (authoritative)
- STAGE_A produces `intent.md` (draft v1)
- STAGE_B consumes `intent.md` → produces `intent_redteam.md`
- STAGE_C consumes `intent.md`, `intent_redteam.md` → updates `intent.md` and produces `intent_synthesis.md`
- STAGE_D consumes intent docs → produces `intent_lock_report.md`
- STAGE_E consumes locked `intent.md` → produces `premortem.md`, `risk_register.md`
- STAGE_F consumes locked `intent.md`, `risk_register.md` → produces `fixtures/`, `verification_plan.md`, `traceability_matrix.md`
- STAGE_G consumes `intent.md`, `risk_register.md`, `verification_plan.md` → produces `micro_sprints.md`
- STAGE_H consumes `intent.md`, `micro_sprints.md`, `verification_plan.md` → produces `<SPRINT_ID>_ENVELOPE.md` and `SPRINT_ID.txt`
- STAGE_I consumes envelope + verification assets → produces envelope red team report and updates artifacts as needed (Red/Blue only)
- **STAGE_J** consumes full pack → produces `PACK_MANIFEST.md`, `PACK_CHECKLIST.md` (mechanical packaging only, **runs before I2**)
- **STAGE_I2** consumes full pack + `PACK_CHECKLIST.md` + `PACK_MANIFEST.md` → produces `PACK_AUDIT_REPORT.md` (Purple only, **runs after J**)
- Mission Mode consumes one or more completed sprint packs and applies a mission-level checkpoint before chained execution.

## Intent Unlock Protocol (HARD)
If any downstream stage discovers the locked intent is flawed:
- Unlock requires Purple + human approval.
- Must create a new `intent.md` version and update its change log.
- Must re-run / re-validate all downstream stages (E–J) against the updated intent.

---

## STAGE_A — Intent Contracting
Inputs:
- LOAD: raw brief (captured into run root)
- DISK: `KNOWLEDGE_LINT.txt` (run root), `EXECUTION_MODE.txt` (run root)
- DISK: `MISSION_LINT.txt` (run root, already-authorized mission unit runs only)

Outputs:
- `raw_brief.md`
- `pack/intent.md` (v1)

Entry criteria:
- raw brief content exists and is non-empty.
- `KNOWLEDGE_LINT.txt` exists in run root and records a successful knowledge-lint preflight.
- If the run is advancing a unit inside an already-authorized mission: `MISSION_LINT.txt` exists in run root and records a successful mission-lint preflight.
- `EXECUTION_MODE.txt` exists in run root and contains exactly one value: `PLANNING_ONLY` or `EXECUTION_ENABLED`.

Exit criteria:
- `intent.md` includes: Purpose, Goal, Non-goals, Principles, Roles, Acceptance Criteria, Go/No-Go rule.
- Open questions labeled BLOCKING/NON-BLOCKING.
- Requirements sourced or `[INFERRED]` per `DEFINITIONS.md`.

---

## STAGE_B — Red Team (Intent)
Inputs:
- LOAD: `pack/intent.md`

Outputs:
- `pack/intent_redteam.md`

Exit criteria:
- Findings include severity, why it matters, fix recommendation.
- Includes agent failure modes and verification holes.

Iteration:
- Required: `Iteration: k of max 2`

---

## STAGE_C — Blue Team + Synthesis (Intent)
Inputs:
- LOAD: `pack/intent.md`, `pack/intent_redteam.md`

Outputs:
- Updated `pack/intent.md` (v2+)
- `pack/intent_synthesis.md`

Exit criteria:
- No unresolved Critical findings remain OR they are explicitly marked BLOCKING for Purple.
- Any net-new requirement tagged `[SCOPE EXPANSION]` and marked BLOCKING.

Iteration:
- Required: `Iteration: k of max 2`

---

## STAGE_D — Purple Gate (Intent Lock)
Inputs:
- LOAD: `pack/intent.md`, `pack/intent_redteam.md`, `pack/intent_synthesis.md`

Outputs (REQUIRED):
- `pack/intent_lock_report.md`

Prompt rule (HARD):
- If a relevant skill exists, prompt MUST include: `Use the <skill name> skill.`

Exit criteria:
- `intent_lock_report.md` records verdict (PASS/CONDITIONAL PASS/FAIL), reasons, and any bounded deferrals with micro-sprint hooks.
- No PASS/CONDITIONAL PASS allowed if any `[SCOPE EXPANSION]` remains unapproved.

---

## STAGE_E — Pre-mortem + Risk Register
Inputs:
- LOAD: locked `pack/intent.md`
- DISK: `pack/intent_lock_report.md`

Outputs:
- `pack/premortem.md`
- `pack/risk_register.md`

Exit criteria:
- Premortem lists top failure scenarios and mitigations.
- Risk register lists severity, mitigation, and suggested verification hook.

---

## STAGE_F — Verification Assets
Inputs:
- LOAD: locked `pack/intent.md`, `pack/risk_register.md`
- DISK: `pack/intent_lock_report.md`

Outputs:
- `pack/fixtures/…`
- `pack/verification_plan.md`
- `pack/traceability_matrix.md`

Exit criteria:
- Every Critical/High constraint has at least one fixture/test/check.
- Traceability matrix is complete for Critical/High.
- Fixtures follow naming conventions; domain areas only if listed in intent scope.

---

## STAGE_G — Micro-sprint Sequencing
Inputs:
- LOAD: `pack/intent.md`, `pack/risk_register.md`, `pack/verification_plan.md`
- DISK: `pack/traceability_matrix.md`, `pack/intent_synthesis.md`

Outputs:
- `pack/micro_sprints.md`

Exit criteria:
- Each micro-sprint includes: objective, inputs, outputs, entry criteria, exit criteria, stop/go gate.
- Micro-sprints reference bounded deferral hooks where applicable.

---

## STAGE_H — Sprint Envelope
Inputs:
- LOAD: `pack/intent.md`, `pack/micro_sprints.md`, `pack/verification_plan.md`
- DISK: `pack/traceability_matrix.md`

Outputs:
- `SPRINT_ID.txt` (run root)
- `pack/<SPRINT_ID>_ENVELOPE.md`

Note (HARD):
- File-touch budgets are instantiated into the envelope in this stage using DEFINITIONS.md guidance ranges.

Exit criteria:
- Envelope includes file-touch budget fields per micro-sprint and total.
- Envelope includes verification steps required before merge and references verification_plan.md and traceability_matrix.md.
- Sprint ID conforms to naming conventions and is written to `SPRINT_ID.txt`.

---

## STAGE_I — Red/Blue on Envelope + Verification
Purpose:
- Red Team attacks envelope + verification assets.
- Blue Team hardens envelope + assets.
- No Purple adjudication here.

Inputs:
- LOAD: `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/verification_plan.md`, `pack/traceability_matrix.md`, `pack/micro_sprints.md`
- DISK: `pack/fixtures/`, `pack/risk_register.md`, `pack/intent_lock_report.md`

Outputs:
- `pack/<SPRINT_ID>_ENVELOPE_REDTEAM.md`
- Updated `pack/<SPRINT_ID>_ENVELOPE.md` (v2+ if changed)
- Updated verification assets if needed (fixtures/plan/matrix), versioned + changelog

Exit criteria:
- Max 2 Red/Blue cycles completed.
- No unresolved Critical findings remain OR they are explicitly marked BLOCKING for Purple adjudication.
- Any `[SCOPE EXPANSION]` introduced is BLOCKING and must be carried to Purple.

Iteration:
- Required: `Iteration: k of max 2`

---

## STAGE_J — Pack Consolidation (runs BEFORE I2)
Purpose:
- Mechanical packaging only: manifest + checklist + non-empty validation.
- No adjudication.
- **Must run before STAGE_I2** so that PACK_CHECKLIST.md exists for the Purple audit.

Inputs:
- DISK: all pack artifacts (excluding PACK_AUDIT_REPORT.md, which does not yet exist)

Outputs:
- `pack/PACK_MANIFEST.md`
- `pack/PACK_CHECKLIST.md`

Prompt rule (HARD):
- If a relevant skill exists, prompt MUST include: `Use the <skill name> skill.`

Exit criteria:
- Manifest lists all required files and confirms non-empty (PACK_AUDIT_REPORT.md listed as "pending — produced by STAGE_I2").
- Checklist items match the spec 1:1 and are fully yes/no answerable with evidence fields.
- Checklist answers are populated based on available artifacts. PACK_AUDIT_REPORT.md references are marked "pending I2."

Note (HARD):
- PACK_MANIFEST.md will be updated in STAGE_I2 to confirm PACK_AUDIT_REPORT.md exists and is non-empty.

---

## STAGE_I2 — Purple Audit (Pack Gate, runs AFTER J)
Inputs:
- LOAD: `pack/intent.md`, `pack/intent_lock_report.md`, `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/traceability_matrix.md`, `pack/verification_plan.md`, `pack/micro_sprints.md`, `pack/PACK_CHECKLIST.md`, `pack/PACK_MANIFEST.md`
- DISK: everything else in `pack/`

Outputs:
- `pack/PACK_AUDIT_REPORT.md`
- Updated `pack/PACK_MANIFEST.md` (confirms PACK_AUDIT_REPORT.md exists and is non-empty)

Prompt rule (HARD):
- If a relevant skill exists, prompt MUST include: `Use the <skill name> skill.`

Exit criteria:
- Purple Gate Checklist evaluated via the run-specific PACK_CHECKLIST (instantiation of spec checklist).
- Verdict recorded: PASS / CONDITIONAL PASS / FAIL.
- No PASS/CONDITIONAL PASS allowed if any `[SCOPE EXPANSION]` remains unapproved.
- PACK_MANIFEST.md updated to mark PACK_AUDIT_REPORT.md as present and non-empty.

---

## POST_GATE — Execution Prompt Generation (execution-enabled runs only)
Skip rule:
- If `EXECUTION_MODE.txt = PLANNING_ONLY`, this stage is skipped and the run terminates at planning-pack completion.

Entry criteria:
- STAGE_I2 verdict is PASS.
- Human review decision is explicit **Go**.
- `EXECUTION_MODE.txt` (run root) equals `EXECUTION_ENABLED`.

Inputs:
- LOAD: `pack/<SPRINT_ID>_ENVELOPE.md`, `pack/micro_sprints.md`, `pack/verification_plan.md`, `pack/traceability_matrix.md`
- DISK: `pack/intent.md`, `pack/risk_register.md`, `pack/PACK_AUDIT_REPORT.md`, `docs/Factory/SCRATCHPAD.md`

Outputs:
- `EXECUTION_PROMPT.md` (run root)

Exit criteria:
- Prompt is instantiated from `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md`.
- Prompt has no unresolved placeholders.
- Prompt includes deterministic skill routing instructions and stage-aligned guardrails.

---

## MISSION_WRAPPER (additive, optional — not a replacement stage chain)
Purpose:
- Wrap multiple completed sprint packs into one mission execution sequence under one consolidated checkpoint.

Mission inputs:
- DISK: referenced sprint run roots and packs (`docs/Factory/runs/<RUN_ID>/...`)
- DISK: `docs/Factory/MISSION_MODE.md`
- LOAD: mission manifest/checkpoint/completion artifacts

Mission outputs:
- `docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_CHECKPOINT.md`
- `docs/Factory/missions/<MISSION_ID>/MISSION_COMPLETION_REPORT.md`

Mission hard rules:
1. Mission does not bypass per-unit A→I2 contracts.
2. Per-unit iteration caps remain unchanged.
3. Mission checkpoint must record one explicit GO/NO-GO decision.
4. Any policy/scope/verification breach in a unit halts mission.
5. Remaining units after halt are marked skipped/not executed until restart authorization.
6. `MISSION_MANIFEST.md` remains the authored ledger of record for ordered units, mission unit status, run references, pack paths, and mission evidence links.
7. If a unit run is advancing an already-authorized mission, pre-run mission lint must pass before STAGE_A begins.

Mission restart rule:
- Resume from failed unit only if mission scope ledger, prior evidence integrity, and mission checkpoint authorization remain valid.
