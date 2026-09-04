# Conductor Design Pack — 05 Per-File Disposition

Dispositions: **keep** (unchanged, possibly renamed) · **rewrite** (same responsibility, new contract) · **demote** (optional module, not pilot scope) · **delete** (after ablation note) · **archive** (frozen evidence). Source tree: `main` after the 0.2.5 candidate merge (`7d0d20e`).

## Root

| Path | Disposition | Reason |
|---|---|---|
| `AGENTS.md` | rewrite | Managed block + project block; read order shrinks to 2 files; Hard Guardrails and SIMPLE-CODE-GATE move to INVARIANTS verbatim |
| `CLAUDE.md` | keep | `@AGENTS.md` bridge |
| `README.md` | rewrite | Conductor naming, three gates, install path |
| `CHANGELOG.md`, `requirements.txt`, `LICENSE`, `.gitattributes`, `.gitignore` | keep | |
| `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json` | keep | Plugin display names → Conductor; versions → 0.3.0 |

## docs/Factory → docs/Conductor

| Path | Disposition | Reason |
|---|---|---|
| `ARCHITECTURE.md` | rewrite → `INVARIANTS.md` + `GATES.md` | Stage narrative replaced by principle + gates |
| `ORCHESTRATION.md` | delete | Stage-by-stage runner guide is choreography; its hard rules (execution mode, no-touch, evidence bounds) move to GATES.md |
| `MISSION_MODE.md` | demote → `modules/mission-mode/` | Optional |
| `MERGE_PROTOCOL.md` | keep | |
| `SIMPLE_CODE_GATE_SEVERITY_POLICY.md` | keep | Referenced by INVARIANTS |
| `TASK_MEMORY.md` | demote → `modules/task-memory/` | Optional today, stays optional |
| `SCRATCHPAD.md` | demote → `modules/scratchpad/`; active pitfalls summarized in INVARIANTS | Read-order item removed |
| `Spec/STAGE_CONTRACTS.md` | delete | Replaced by GATES.md + schemas; stage letters kept as a checklist appendix in GATES.md |
| `Spec/DEFINITIONS.md` | rewrite | Keep handoff-size caps only where they bound evidence; drop stage vocabulary |
| `Spec/NAMING_CONVENTIONS.md` | keep | Run/snapshot id rules reused by schemas |
| `Spec/PURPLE_GATE_CHECKLIST.md` | rewrite → G3 verifier prompt | Becomes the fresh-context verifier's checklist |
| `templates/HANDOFF_STAGE_TEMPLATE.md` | delete | No handoffs |
| `templates/INTENT_LOCK_REPORT_TEMPLATE.md` | delete | Intent Pack + countersign |
| `templates/SPRINT_ENVELOPE_TEMPLATE.md`, `SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md` | delete | Content → Intent Pack constraints; SIMPLE-CODE-GATE text preserved in INVARIANTS |
| `templates/TRACEABILITY_MATRIX_TEMPLATE.md` | delete | Intent Pack `verification_requirements[].requirement_ids` is the matrix |
| `templates/VERIFICATION_MANIFEST_TEMPLATE.yaml` | rewrite → v2 | Adds `result` |
| `templates/PACK_MANIFEST_TEMPLATE.md`, `PACK_CHECKLIST_TEMPLATE.md`, `PACK_AUDIT_REPORT_TEMPLATE.md` | delete | Schema-validated run layout |
| `templates/EXECUTION_PROMPT_TEMPLATE.md` | rewrite → autonomy block in AGENTS.md managed section | Human Go becomes `countersign/EXECUTION_GO.json` |
| `templates/EXECUTION_AUTHORIZATION_TEMPLATE.md` | rewrite → `countersign.schema.json` | |
| `templates/EXECUTION_CLOSEOUT_TEMPLATE.json` | rewrite → `statement_of_completion.schema.json` | |
| `templates/HOST_CAPABILITIES_TEMPLATE.json` | keep | Referenced from Project Config |
| `templates/RUN_METRICS_TEMPLATE.md` | demote | Optional |
| `templates/CONTEXT_RECALL_REPORT_TEMPLATE.md` | rewrite → recall receipt | Sources-read evidence shape kept |
| `templates/MISSION_*` (5) | demote → `modules/mission-mode/` | |
| `ProductOwner/**` (7 files) | demote → `modules/product-owner/` | Brief Review folds into G1 for pilot scope |
| `Harnesses/README.md`, `CODEX.md` | rewrite → `adapters/` | Add `claude-code.md`, `cursor.md` |
| `Harnesses/KILO.md`, `KILO_EXTERNAL_LANE_PROMPT.md` | demote → `modules/kilo/` | |
| `Harnesses/AGENT_LOOP_BRIDGE*.md` | demote → `modules/agent-loop-bridge/` | |
| `Research/*.md` | archive | Decision records |
| `runs/RUN_20260902_0725_*`, `runs/RUN_20260903_1750_*` | archive → `tests/golden_packs/` (copy) + keep in place | Golden-pack fixtures; V2-lineage qualification evidence |

## docs/adapters/bmad, docs/integration, docs/onboarding

| Path | Disposition | Reason |
|---|---|---|
| `docs/adapters/bmad/*` (14) | rewrite | Lane model; declared root; legacy-evidence namespace unchanged |
| `docs/integration/FACTORY_BMAD_ROUTING_MATRIX.md` | rewrite | Conductor naming; lanes |
| `docs/onboarding/FACTORY_PLUGIN_QUICK_START.md`, `_REFERENCE.md` | rewrite → `onboarding/GUIDE.md` | One page |
| `docs/onboarding/FACTORY_PLUGIN_CLI_ROLLOUT_PLAYBOOK.md`, `FACTORY_FIRST_TESTER_HANDOFF.md` | rewrite → `onboarding/INSTALL.md` + `FIRST_EXERCISE.md` | GitHub marketplace path; preflight is maintainer-only |
| `docs/onboarding/FACTORY_PLUGIN_PILOT_RUNBOOK.md` | rewrite → `onboarding/FRICTION_LOG_TEMPLATE.md` + maintainer runbook | |
| `docs/onboarding/FACTORY_PLUGIN_ROLLBACK.md`, `_TROUBLESHOOTING.md` | keep (rename, new reason codes) | |
| `docs/onboarding/ONBOARDING_GUIDE.md`, `NON_TECHNICAL_STARTER_GUIDE.md` | keep (rename) | |
| `docs/PROJECT_STATE.md`, `ROADMAP.md`, `CHANGELOG.md` | keep | PROJECT_STATE is read 1 of 2 |

## .agents/skills (repo-level Codex skills)

| Path | Disposition | Reason |
|---|---|---|
| `factory-root-planner/` | rewrite → `conductor-run/` | Drives G1→G2→G3 instead of A→I2 |
| `factory-purple-gate/` | rewrite → `conductor-verifier/` | Fresh-context G3 verifier |
| `factory-pack-consolidator/` | delete | No pack consolidation |
| `factory-execution-closeout/` | rewrite → part of `conductor-run/` (completion) | Statement of Completion |

## scripts

| Path | Disposition | Reason |
|---|---|---|
| `factoryctl` | rewrite → `conductorctl` | Subcommands: contract-lint, receipts, postimage, doctor, context-index |
| `factory-python` | keep | Bytecode guard |
| `factory_pack_lint.py` | rewrite → `conductor_contract_lint.py` | ~70% of checks reused (02 §2) |
| `factory_stage_lint.py` | delete | Orphaned families; `_check_declared_outputs` logic folds into contract-lint |
| `factory_execution_closeout.py` | rewrite → merged into contract-lint completion | Primitives reused |
| `factory_host_capability.py` | keep | Called from contract-lint execution |
| `factory_context_index.py` | keep | G1 input, risk-triggered |
| `factory_project_preflight.py` | keep | Project Config `project_preflight` |
| `factory_run_metrics.py` | demote | Optional |
| `factory_task_memory.py`, `cartographer`, `tools/repo_cartographer/` | demote | Optional modules |
| `factory_kilo_stage.py` | demote → `modules/kilo/` | |
| `agent_loop_bridge_validate.py` | demote → `modules/agent-loop-bridge/` | |
| `knowledge_lint.sh` | rewrite → Project Config `required_docs` check inside contract-lint intent | ~50 pattern assertions orphaned |
| `mission_lint.sh`, `mission_cursor_lint.sh` | demote → `modules/mission-mode/` | |
| `merge_preflight.sh` | keep | |
| `build_factory_plugins.py`, `build_factory_bmad_plugins.py` | rewrite → `build_plugins.py` | One builder, Conductor names |
| `verify_factory_cli_rollout.py`, `verify_factory_bmad_cli_rollout.py`, `verify_factory_bmad_live_preflight.py`, `verify_factory_bmad_publication.py` | keep (rename) | Maintainer preflights |
| `verify_factory_bmad_*.sh` (6) | keep (rename); extend enforcement verifier with PT-09 | |
| **new** `conductor_receipts.py` | create | Runner that executes manifest checks and writes signed receipts |
| **new** `conductor_postimage.py` | create | Harvested from MS-01 protected-postimage comparison |

## plugin-src

| Path | Disposition | Reason |
|---|---|---|
| `factory/manifest.json` | rewrite | Name `conductor`, version 0.3.0 |
| `factory/runtime/factory_plugin.py` | rewrite (targeted) | `evaluate_progress` reads Conductor run layout; setup adds AGENTS.md managed-block composition; doctor/update/rollback unchanged |
| `factory/skills/{doctor,progress,update,validate}.md` | keep (rename, new reason codes) | |
| `factory/skills/{greenfield,brownfield}.md` | rewrite → `adopt.md` | One entry point; mode auto-detected as today |
| `factory/skills/run.md` | rewrite | Drives G1→G2→G3 |
| `factory/project-seeds/**` | rewrite | Seeds INVARIANTS, GATES, Project Config |
| `factory-bmad/manifest.json`, `hooks/hooks.json` | keep (rename) | |
| `factory-bmad/runtime/factory_bmad_policy.py` | rewrite (targeted) | Lane classification, declared root, unsafe-layout narrowing, message |
| `factory-bmad/runtime/factory_bmad.py` | keep; add `gap` command | Promotion/intake/rollback/bootstrap verbatim |
| `factory-bmad/project-adapter/BMAD_POLICY.md` | rewrite → `LANE_POLICY.md` + `lane_policy.json` | |
| `factory-bmad/project-adapter/PROJECT_PREFLIGHT.json` | rewrite → folded into Project Config | |
| `factory-bmad/project-adapter/factory_bmad_policy_lint`, `factory_project_preflight` | keep (rename) | CI-callable |
| `factory-bmad/project-adapter/RAW_BRIEF_TEMPLATE.md` | delete | Intent Pack template replaces it |
| `factory-bmad/skills/{doctor,audit,bootstrap,promote,intake}/` | keep (rename); **new** `gap/` | |
| `plugins/**` (4 generated) | regenerate | Never edited by hand |

## tests

| Path | Disposition | Reason |
|---|---|---|
| `test_factory_stage_lint.py` | delete | Validator deleted |
| `test_factory_pack_lint_core.py`, `test_factory_pack_lint_activation_verification.py` | rewrite → contract-lint tests | Check families retained |
| `test_factory_execution_closeout.py` | rewrite → Statement of Completion tests | |
| `test_context_recall_repair.py`, `test_factory_context_upstream.py` | keep | |
| `test_factory_host_capability.py`, `test_factory_project_preflight.py`, `test_factory_python_launcher.py`, `test_merge_preflight.py` | keep | |
| `test_factory_plugin_*.py` (13), `test_factory_cli_rollout.py` | keep; rename entry points; `docs` test string lists updated | |
| `test_factory_bmad_enforcement.py` | rewrite (3 inverted tests, lane fixtures, PT-09) | 02 §2 |
| `test_factory_bmad_policy.py`, `_policy_parity.py` | rewrite against Lane Policy | |
| remaining `test_factory_bmad_*.py` (17) | keep (rename) | |
| `plugin_fixtures/**` | keep; add `lane_policy/golden.json`, `statement_of_completion/golden.json` | Fixture families become 11 |
| **new** `golden_packs/` | create | Archived V2 packs must keep linting under compatibility mode |
| **new** `test_schemas.py` | create | Every `schemas/*.json` validates its template and rejects its negative fixtures |

## Counts

| Disposition | Files (approx.) |
|---|---|
| keep | 58 |
| rewrite | 41 |
| demote | 24 |
| delete | 13 |
| archive | 4 groups |
| create | 6 |

## Working-tree drift (brief §9)

Closed. `scripts/factory_project_preflight.py`, the `factoryctl project-preflight` subcommand, and the STAGE_CONTRACTS/AGENTS.md references are all present at `7d0d20e`. The drift observed on 2026-09-04 existed only in the uncommitted `codex/factory-video-deck` working tree and does not affect the Conductor branch.

## Compatibility intersection with the 0.2.5 candidate (brief §9)

Not applicable: the candidate is merged and is the base of this branch. Protection of its packs is provided by `tests/golden_packs/` (06 §1, step 1).
