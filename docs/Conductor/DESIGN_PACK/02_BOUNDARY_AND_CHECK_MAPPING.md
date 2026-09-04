# Conductor Design Pack — 02 Boundary Classification and Check Mapping

## 1. Per-boundary classification

Every place where Factory V2 stops the agent, classified by *why* the stop exists. Only "model-weakness pause" is obsoleted by frontier models (brief §3 rows 1–2). "Human-authority gate" and "hard envelope" are kept.

| Factory boundary / preflight | Why it exists today | Class | Conductor disposition |
|---|---|---|---|
| Knowledge lint before any run | Ensure doc spine exists so the model reads the right files | Model-weakness (context reconstruction) | Fold into `contract-lint intent` as a Project Config check; not a separate preflight |
| Mandatory 8-document read order | Same | Model-weakness | Trim to PROJECT_STATE + INVARIANTS; rest on demand |
| Stage A recall report (HARD rule) | Surface prior BLOCKING / GO / scope-expansion decisions | **Mixed**: governance content, model-weakness mechanism | Reclassify as G1 *input*; risk-triggered (index non-empty or mission context); WEAK verdict blocks G1 exit, not run start |
| Direct-source repair path | Let the agent prove it read sources when recall is WEAK | Model-weakness mechanism with a good evidence shape | Keep the evidence shape (sources read + summaries) as the G1 recall receipt; drop the two-step choreography |
| Project preflight (declared) | Project-specific fail-closed gate | Human-authority (project policy) | Keep; becomes a Project Config entry evaluated at G1 |
| A→B→C Red/Blue iteration on intent, max 2 | Force the weak model to critique itself | Model-weakness | Remove as boundaries; the fresh-context verifier at G3 plus human at G1 replace them |
| D Purple Gate intent lock | Human locks intent | **Human-authority** | **Keep** as G1 |
| E premortem + risk register | Force risk thinking | Model-weakness | Optional Intent Pack section (`risks[]`), not a gate |
| F verification assets + manifest | Declare what will prove done | **Hard envelope** | **Keep**; manifest v2 required at G2 entry when runnable checks exist |
| G micro-sprint sequencing | Chunk work into small supervised steps | Model-weakness | Remove as artifact; agent may sequence internally |
| H sprint envelope + SIMPLE-CODE-GATE | Bound the code change | **Hard envelope** (content) | Content moves into Intent Pack `constraints[]`; SIMPLE-CODE-GATE verbatim in INVARIANTS |
| I Red/Blue on envelope, max 2 | Self-critique | Model-weakness | Remove |
| J pack consolidation | Make the pack listable | Model-weakness (bookkeeping) | Replaced by schema-validated run layout |
| I2 Purple audit + pack-lint | Adversarial audit before human Go | **Human-authority + hard** | **Keep** as G3; verifier subagent + `contract-lint completion` |
| POST_GATE execution prompt + `- Human Go: RECORDED` | Human authorizes execution against exact pack | **Human-authority** | **Keep** as `countersign/EXECUTION_GO.json` at G2 entry (EXECUTION_ENABLED only) |
| Stage-lint after every handoff | Catch malformed handoffs | Model-weakness | Remove; no handoff documents exist |
| Per-stage word caps | Contain verbosity | Model-weakness | Remove |
| "Use the <skill> skill." prompt rule at D/J/I2 | Force skill invocation | Model-weakness (harness quirk) | Remove |
| Execution closeout JSON | Record outcome deterministically | **Hard** | Folded into Statement of Completion |
| Merge preflight + REVIEW_READY/MERGE_READY | Merge authorization | **Human-authority** | **Keep** unchanged |
| Mission lint / mission cursor lint | Continuity across multi-sprint chains | Continuity, optional today | Optional module; unchanged |
| BMAD hook (lane enforcement) | Prevent authority collision | **Hard envelope** | Keep, narrowed to lanes (see 04) |
| Exact plan-ID approval for adopt/update | Human authorizes repository mutation | **Human-authority** | **Keep** unchanged |

Result: 8 boundaries kept (G1, G2 entry envelope, G3, execution Go, merge, adopt/update approval, BMAD lane hook, project preflight), 9 removed, 3 reclassified.

## 2. Check-family → gate mapping

Granularity: validator function or check family, with the enumerated count from the 657-check inventory. Every family appears exactly once below or in §4 (orphans).

### `scripts/factory_stage_lint.py` (32 checks)

| Family | Count | Gate / disposition |
|---|---|---|
| `_check_handoff_shape` (HANDOFF_STAGE_* headers, sections) | ~12 | **Orphan** — no handoffs in Conductor |
| `_check_declared_outputs` (stage output files exist, non-placeholder) | ~15 | Partially → G1 (`intent_pack.json` exists, non-placeholder) and G2 (`verification_manifest.yaml`); rest orphan |
| `check_stage_output_word_cap` | ~5 | **Orphan** |

### `scripts/factory_pack_lint.py` (123 checks)

| Family | Count | Gate |
|---|---|---|
| `_check_required_files` | ~14 | G3 (`contract-lint completion` run-layout completeness) |
| `_check_text_contracts` (intent lock digest, envelope markers, audit verdict) | ~20 | G1 (intent digest) / G3 (verdict); envelope-specific markers → orphan |
| `check_verification_manifest_presence` | 3 | G2 entry (upgraded from warning to error) |
| `check_execution_mode_contract` | ~8 | G2 entry |
| `_check_artifact_shapes` | ~6 | G1/G2 (schema validation replaces shape heuristics) |
| `check_context_recall_report` + `_has_source_summary` | ~12 | G1 (recall receipt) |
| `_check_verification_manifest` (schema, tiers, types, constraint ids, evidence paths) | ~30 | G2 |
| `_check_execution_order` | ~4 | **Orphan** (micro-sprint order) |
| `_check_verification_id_sets` (plan vs manifest vs traceability) | ~6 | G2 (Intent Pack `verification_requirements[]` ids = manifest ids) |
| `_check_no_touch_preimages` | ~6 | G2 (folds into postimage compare) |
| `check_host_capability_contract` (+ `factory_host_capability.py`, 20) | ~8 + 20 | G2 entry (host capabilities declared in Project Config) |
| `_check_placeholders`, `_check_required_headers`, `check_word_cap`, `_check_handoff` | ~6 | Placeholders → all gates via schema; headers/word caps/handoff → **orphan** |

### `scripts/knowledge_lint.sh` (72 checks)

| Family | Count | Gate |
|---|---|---|
| Required-file sweep (59 paths) | 1 sweep | G1 as Project Config `required_docs[]` check; list shrinks to the Conductor spine |
| `has_pattern` assertions (AGENTS.md mentions each CLI command, etc.) | 59 | Mostly **orphan**; keep only "INVARIANTS present verbatim" and "AGENTS.md managed block present" |
| Active pitfall count bounds, bridge fixture probe, CLI help probes | 12 | CLI help probes → build tests; pitfall bounds → optional module (SCRATCHPAD) |

### `scripts/mission_lint.sh` (25), `scripts/mission_cursor_lint.sh` (57)

Optional module, unchanged. Not pilot scope. Mapped to "G2 continuity input" when the module is enabled.

### `scripts/factory_execution_closeout.py` (44)

| Family | Gate |
|---|---|
| `exact_object`, `unique_strings`, `safe_run_root`, `safe_file`, `validate_digest`, `validate_reference` | G3 — reused as Statement of Completion primitives |
| `parse_verification_ids`, `parse_micro_sprint_ids` | G3 (verification ids) / **orphan** (micro-sprint ids) |
| `validate_authorization_reference` | G2 entry (`EXECUTION_GO.json`) |
| `validate_closeout`, `record_closeout` | G3 — becomes `contract-lint completion` + record |

### `scripts/merge_preflight.sh` (7)

G3 → MERGE_READY. Unchanged.

### `scripts/factory_context_index.py` verdict logic (11)

G1 input. `WEAK`/`SUFFICIENT` verdict kept; `--fail-on-weak-coverage` becomes the G1 rule when recall is triggered.

### `scripts/verify_factory_cli_rollout.py` (22)

Layer 3 (Claude Code adapter) maintainer preflight. Unchanged; renamed.

### `plugin-src/factory/runtime/factory_plugin.py` (82)

| Family | Disposition |
|---|---|
| `evaluate_doctor` (7) | Layer 3, keep |
| `evaluate_progress` / validate (21) | Layer 3; rewrite to read the Conductor run layout (Intent Pack digest instead of `intent_lock_report.md`) |
| greenfield/brownfield (30) | Layer 3, keep; add AGENTS.md composition contract |
| update/rollback (24) | Layer 3, keep |
| `validate.md` skill guardrails (8) | Layer 3, keep (prose, mirrored by tests) |

### `plugin-src/factory-bmad/runtime/*` (92)

| Family | Disposition |
|---|---|
| `policy_classify` (discovery / solution-context / TEA / downstream / unknown) | Rewrite on lanes (04 §2); default-deny retained |
| `assess_bmad_layout` (9 states) | Keep; add `declared_root` state; unsafe → blocks authority actions only |
| `enforcement_activation` | Keep; message rewrite |
| `solution_context_authorization` (7 digest/version/override checks) | Keep verbatim |
| `hook_decision` deny shape | Rewrite message; carry reason code + layout finding |
| `capability_audit` (9), `reconcile_brownfield`, `_remediation_previews` | Keep |
| `promotion_plan` / `promote` / `snapshot_inventory` / supersession (≈20) | Keep verbatim |
| `bootstrap`, `intake`, `rollback` (≈15) | Keep; intake seeds Lane Policy + Project Config instead of BMAD_POLICY v1.1 |
| `safe_relative`, `_load_policy` no-bytecode | Keep |

### `tests/` contract-rule modules (62)

| Family | Disposition |
|---|---|
| Protected baseline, fixture families, conformance, merge preflight, no-bytecode, privacy, public release | Keep |
| `test_denial_says_doctor_was_not_run` | **Invert**: assert the message carries the real reason code |
| `test_nested_bmad_layout_blocks_even_allowed_upstream_invocation` | **Invert**: nested layout blocks authority actions, permits discovery with warning |
| `test_parent_permission_is_non_transitive` | **Rewrite**: lane of the invoked skill decides; same-lane nesting permitted |
| `test_exact_upstream_allowlist` | Rewrite against Lane Policy |
| docs tests naming `factory:` entry points | Rename step |

## 3. Continuity machinery classification

| Component | Today | Conductor |
|---|---|---|
| Context recall report | Mandatory HARD rule before Stage A | **G1 input, risk-triggered**: required when the recall index is non-empty or the run belongs to a mission; skipped on a first greenfield run. WEAK blocks G1 exit unless the recall receipt shows sources read. |
| Direct-source repair | Lint-enforced two-step fallback | Evidence shape kept as the recall receipt; choreography dropped |
| Mission Cursor | Optional Codex adapter | Optional module (`modules/mission-mode/`), Layer 3; unchanged |
| Mission lint / manifest / checkpoint | Optional, mission-only | Optional module; unchanged |
| Task memory | Optional, advisory | Unchanged; reshaped toward one-lesson-per-file if the pilot friction log asks for it |
| SCRATCHPAD active pitfalls | Mandatory read (one section) | Folded into INVARIANTS as a short "known pitfalls" list; optional module keeps the full index |
| Repo Cartographer | Optional | Optional module |

## 4. Orphans (checks with no gate)

Flagged as the brief requires. All are model-weakness controls; each is deleted only after the ablation note in 06 §3 is recorded.

| Orphan check family | Source | Count (approx.) |
|---|---|---|
| Handoff shape (`HANDOFF_STAGE_*` headers, sections, `Iteration: k of max 2`) | stage-lint, pack-lint `_check_handoff` | ~16 |
| Stage/pack word caps | stage-lint, pack-lint | ~8 |
| Micro-sprint execution order and ids | pack-lint `_check_execution_order`, closeout `parse_micro_sprint_ids` | ~6 |
| Envelope-specific text markers (Red/Blue cycle markers, envelope headers) | pack-lint `_check_text_contracts` | ~8 |
| `has_pattern` AGENTS.md command-mention assertions | knowledge_lint | ~50 |
| "Use the <skill name> skill." prompt-rule presence | stage contracts / docs tests | ~3 |
| **Total orphaned** | | **~91 of 657 (≈14%)** |

Everything else (≈566 checks) has a home in G1, G2, G3, Layer 3, or an optional module.
