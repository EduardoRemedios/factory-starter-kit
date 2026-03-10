# docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.4)

## Version
v3.4

## Change Log
- v3.4 (2026-02-27): Added Mission Mode artifact caps and hard mission wrapper constraints (additive-only, checkpoint gate, and halt/restart integrity controls).
- v3.3 (2026-02-14): Added execution-mode gating contract so `EXECUTION_PROMPT.md` is required only for `EXECUTION_ENABLED` runs, with `PLANNING_ONLY` as default.
- v3.2 (2026-02-12): Upgraded execution-prompt generation from recommended to required post-I2 PASS + human GO, and added mandatory template usage (`EXECUTION_PROMPT_TEMPLATE.md`).
- v3.1 (2026-02-08): Added §14 (execution prompt) and §15 (schema extension guidance). Compatible with STAGE_CONTRACTS v4.
- v3 (2026-02-06): Added explicit date placeholder rule, added iteration metadata rules reference, and tightened change log placeholder guidance.

## 1. Deterministic (STRUCTURAL)
Deterministic means fixed:
- directory structure
- filenames
- required section headings per artifact template
- stage ordering

Content may vary.

## 2. Size caps (HARD)
Caps are per artifact, excluding code blocks.

- `intent.md`: ≤ 1,200 words
- `intent_redteam.md`: ≤ 1,500 words
- `intent_synthesis.md`: ≤ 800 words
- `intent_lock_report.md`: ≤ 600 words
- `premortem.md`: ≤ 900 words
- `risk_register.md`: ≤ 900 words
- `verification_plan.md`: ≤ 1,000 words
- `micro_sprints.md`: ≤ 1,200 words
- `SPRINT_*_ENVELOPE.md`: ≤ 1,800 words
- `SPRINT_*_ENVELOPE_REDTEAM.md`: ≤ 1,200 words
- `PACK_AUDIT_REPORT.md`: ≤ 900 words
- `PACK_MANIFEST.md`: ≤ 600 words
- `PACK_CHECKLIST.md`: ≤ 800 words
- `MISSION_MANIFEST.md`: ≤ 700 words
- `MISSION_CHECKPOINT.md`: ≤ 700 words
- `MISSION_EXECUTION_PROMPT.md`: ≤ 1,600 words
- `MISSION_COMPLETION_REPORT.md`: ≤ 900 words

Handoffs:
- `HANDOFF_STAGE_*.md`: ≤ 500 words, bullets only
- `HANDOFF_SUMMARY.md`: ≤ 700 words, bullets only

Checklist item rule:
- each checklist line must be one sentence, yes/no answerable

If a cap is exceeded, the stage fails and must compress.

## 3. Fail-closed on ambiguity
If any requirement, definition, or constraint can be interpreted in multiple ways by an agent, it must become one of:
- an explicit definition in this file, or
- an explicit Open Issue marked BLOCKING, or
- an explicit bounded deferral with a future hook

No guessing to fill blanks.

## 4. Impact rubric (verification obligations)
Classify each constraint as:

- **Critical**: could violate an invariant, cause unsafe/irreversible behavior, break compliance posture, or invalidate evidence/receipts. Blocks execution if unverified.
- **High**: affects multiple micro-sprints or would cause major rework if wrong.
- **Medium**: limited to a single micro-sprint or a non-critical pathway.
- **Low**: readability, formatting, minor ergonomics.

Verification REQUIRED for Critical + High.

## 5. Bounded deferral (HARD)
A deferral is bounded only if it has all of:
1) a specific future micro-sprint hook ID (e.g., `MS-03`)
2) a named owner/role responsible for resolving it
3) explicit scope boundary (“what is deferred / what is not”)
4) it does not impact any Critical Purple gate item

Otherwise it is unbounded and blocks PASS.

## 6. Conditional Pass
Conditional Pass is allowed only if:
- all Critical checklist items are YES
- all deferrals are bounded
- each bounded deferral is hooked into `micro_sprints.md`

## 7. File-touch budget
The sprint envelope must include file-touch budget fields:
- max files modified
- max files created
- max files deleted
Per micro-sprint and for sprint total.

If missing, the envelope fails validation.

Guidance ranges (non-binding, but required for sanity):
- Per micro-sprint typical ranges:
  - modified: 5–20
  - created: 3–10
  - deleted: 0–5
Values outside these ranges are allowed ONLY with a one-line justification in the envelope.

## 8. Contract-grade intent
Intent is contract-grade if:
- scope and non-goals are explicit
- key terms are defined or referenced
- acceptance criteria are binary/testable
- open questions are tagged BLOCKING/NON-BLOCKING
- every requirement is sourced or flagged `[INFERRED]`

## 9. Source traceability
Every non-trivial requirement must include a source tag:
- `[SOURCE:RAW]` for raw brief
- `[SOURCE:REF:<path>]` for referenced doc
- `[INFERRED]` for agent-introduced requirement

Any `[INFERRED]` requirement is BLOCKING until human-approved.

## 10. Artifact canon / versions
Canonical artifact is the non-suffixed filename in the current run pack.
Artifacts must include:
- `## Version` (v1, v2, …)
- `## Change Log`

## 11. Change Log entry format (HARD)
Each change log must use:
- `- vN (YYYY-MM-DD): <one-line summary>`

## 12. Placeholder rule (HARD)
No placeholders may remain in final artifacts, including:
- `YYYY-MM-DD`, `HH:MM`, `<RUN_ID>`, `<SPRINT_ID>`, `<X>`, `...`
If a value is unknown at creation time, it must be explicitly marked as:
- `BLOCKING` (and treated as a failure until resolved)

## 13. Iteration metadata rule (HARD)
Cycle artifacts and handoffs must include:
- `Iteration: k of max 2`
Applicable to: STAGE_B, STAGE_C, STAGE_I artifacts and their handoffs.

## 14. Execution prompt (HARD)
Execution mode defaults to `PLANNING_ONLY` and must be persisted in run-root `EXECUTION_MODE.txt`. The Root Planner MUST produce `EXECUTION_PROMPT.md` only when all of the following are true: STAGE_I2 PASS, explicit human "Go", and `EXECUTION_MODE.txt = EXECUTION_ENABLED`. For planning-only runs, execution prompt generation is skipped by contract. When applicable, `EXECUTION_PROMPT.md` is produced at run root using `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md` as a self-contained instruction set covering read order, micro-sprint sequence, detailed data shapes, hard guardrails, troubleshooting guidance, exit checklist, and deterministic skill routing. See `ORCHESTRATION.md` §6.1 for full specification.

## 15. Schema extension guidance (HARD)
When a sprint adds new top-level fields to the request payload (e.g., `auth_context`, `tool_call`), the raw brief MUST explicitly list these fields and flag them as schema extensions. The verification plan MUST include a backward-compatibility test (run existing test suite) immediately after any schema change. This prevents the pattern observed in Sprint A where the strict schema validator rejected new fields, causing cascading test failures that were diagnosable but avoidable.

## 16. Mission wrapper constraints (HARD)
Mission Mode is additive and must not mutate per-unit sprint contracts.

Mission hard constraints:
1. Mission does not bypass or weaken A→I2 stage gates for any unit.
2. Mission must have one explicit consolidated checkpoint decision (`GO` or `NO-GO`).
3. Mission scope ledger must be explicit and immutable during execution unless human re-approval is recorded.
4. Any unit-level policy or verification failure triggers mission halt.
5. Mission restart from a failed unit is allowed only if scope ledger, prior evidence integrity, and authorization checkpoint remain valid.
