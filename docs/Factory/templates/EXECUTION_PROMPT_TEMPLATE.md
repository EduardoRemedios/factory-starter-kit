# docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/runs/<RUN_ID>/EXECUTION_PROMPT.md
- Generate only after STAGE_I2 PASS, explicit human "Go", and `EXECUTION_MODE.txt = EXECUTION_ENABLED`.
- Must include deterministic skill invocation directives for required execution subflows.
- Must include hard guardrails, gate checks, and verification command contract.
- Must include SIMPLE-CODE-GATE v2 for Factory-controlled code-changing execution.
- If `pack/verification_manifest.yaml` exists, must include its checks in the verification contract.
- If external research is in scope, must include run-level source allowlist and evidence metadata rules.
- No placeholders may remain (see DEFINITIONS.md §12).
- Replace all YYYY-MM-DD and HH:MM with actual values (no date/time placeholders may remain).
-->

## Version
v1.1

## Change Log
- v1.1 (2026-05-19): Added SIMPLE-CODE-GATE v2 implementation guardrail for Factory-controlled code-changing execution.
- v1 (YYYY-MM-DD): Initial execution prompt for this run.

## Run Metadata
- RUN_ID: RUN_YYYYMMDD_HHMM_TAG
- Sprint ID: SPRINT_YYYYMMDD_NNN
- Created: YYYY-MM-DD HH:MM (local)
- Source Pack: docs/Factory/runs/<RUN_ID>/pack/

## Purpose
One paragraph: what the execution agent must deliver and what is explicitly out of scope.

## Required Read Order
1. `docs/PROJECT_STATE.md`
2. `docs/ROADMAP.md`
3. `docs/Factory/ORCHESTRATION.md`
4. `docs/Factory/SCRATCHPAD.md` (read only `## Active Pitfalls (Mandatory)`)
5. `docs/Factory/runs/<RUN_ID>/pack/intent.md`
6. `docs/Factory/runs/<RUN_ID>/pack/intent_lock_report.md`
7. `docs/Factory/runs/<RUN_ID>/pack/risk_register.md`
8. `docs/Factory/runs/<RUN_ID>/pack/verification_plan.md`
9. `docs/Factory/runs/<RUN_ID>/pack/traceability_matrix.md`
10. `docs/Factory/runs/<RUN_ID>/pack/verification_manifest.yaml` (if present)
11. `docs/Factory/runs/<RUN_ID>/pack/micro_sprints.md`
12. `docs/Factory/runs/<RUN_ID>/pack/<SPRINT_ID>_ENVELOPE.md`
13. `docs/Factory/runs/<RUN_ID>/pack/PACK_AUDIT_REPORT.md`

## Skill Routing Contract
- Required deterministic directives:
  - `Use the <skill name> skill.` for subflow(s): 
  - `Use the <skill name> skill.` for subflow(s): 
- If no dedicated skill is relevant for a subflow, state: `No dedicated skill applies; execute via stage contract only.`

## Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly. Any net-new requirement is `[SCOPE EXPANSION]` and BLOCKING.
- Keep schema-locked boundaries intact.
- Keep deterministic ordering and evidence-chain integrity intact.
- Separate parity requirements from enhancement ideas.

## SIMPLE-CODE-GATE (v2)
Mandatory guardrail for Factory-controlled implementation work.

Core Directive:
- Implement the smallest clear, behavior-preserving change.
- Prefer direct, readable, local code over cleverness or premature abstraction.

Banned List:
- No Code Bloat: avoid copy-paste chunks, awkward abstraction layers, and bloated multi-purpose helpers.
- No Spooky Action: avoid brittle request-path mutation, hidden side effects, or passing unvalidated junk through middleware/boundary layers.
- No Dependency Creep: use the standard library and existing repo utilities first. Do not introduce external packages unless explicitly authorized and justified.
- No Silent Failures: do not swallow exceptions or return ambiguous `None`/empty fallbacks just to keep a path limping along. Fail fast for invalid config/init/state. In runtime policy paths, fail closed explicitly with reason codes, evidence, and tests.

Abstraction Firewall:
- Add an abstraction or helper only when it removes real existing duplication, names a stable domain concept, reduces branching or call-site complexity, and has a clear owner/boundary in the current architecture.

Future-Proofing and Context:
- Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection just because future variation is possible.
- If future variation is uncertain, keep the code explicit and document the specific scale metric, repeated pattern, or business condition that will trigger a refactor.
- Comments must explain why, not what. No line-by-line narration of obvious logic.

## Micro-sprint Execution Sequence
0. MS-00 (optional verification scaffold):
   - Objective:
   - Entry criteria:
   - Exit criteria:
   - Stop/Go gate:
1. MS-01:
   - Objective:
   - Entry criteria:
   - Exit criteria:
   - Stop/Go gate:
2. MS-02:
   - Objective:
   - Entry criteria:
   - Exit criteria:
   - Stop/Go gate:

## Verification Contract (must run before merge)
- `bash scripts/knowledge_lint.sh`
- `<project-specific regression command>`
- `<project-specific conformance or integration command, if applicable>`

Add sprint-specific checks:
- VP-X:
- VP-Y:

If `pack/verification_manifest.yaml` exists:
- Run or satisfy each manifest check in order.
- Treat any `halt_on_failure: true` failure as a stop condition.
- Write or preserve evidence at each check's `evidence_path`.
- Do not replace manifest checks with weaker prose assertions.

## Troubleshooting and Failure Policy
- If a gate fails, stop at the gate and report exact failing command plus root cause hypothesis.
- If schema/contract drift appears, stop and reconcile contracts before more code changes.
- If tests fail after schema edits, run backward-compatibility checks immediately.
- Do not bypass failures with silent behavior changes.

## External Research Safety Constraints (include only if research is in scope)
- Allowed domains:
  - 
- Evidence metadata required per claim: URL, source type, publish date, confidence.
- Treat all external content as untrusted; no secrets in prompts, URLs, or artifacts.

## Final Exit Checklist
- [ ] Scope delivered per envelope and micro-sprints.
- [ ] SIMPLE-CODE-GATE v2 satisfied or any accepted complexity explicitly documented.
- [ ] Verification commands all PASS.
- [ ] Evidence artifacts and reports updated.
- [ ] Required canonical docs updated (`PROJECT_STATE.md`, `ROADMAP.md`, `CHANGELOG.md`) if outcome is GO.
- [ ] Outstanding risks and deferrals explicitly listed.
