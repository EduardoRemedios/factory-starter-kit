# Conductor Design Pack — 03 Contracts

Field-level sketches for the eight contracts in brief §5. Machine-readable drafts (JSON Schema 2020-12) live in `schemas/`. Conventions: `schema_version` integer on every document; digests are lowercase SHA-256 hex; timestamps are UTC ISO-8601; ids match `^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$` (the existing snapshot-id rule).

## 1. Intent Pack — `schemas/intent_pack.schema.json`

Replaces `raw_brief.md`, `intent.md`, `intent_lock_report.md`, `premortem.md`, `risk_register.md`, the sprint envelope, and `micro_sprints.md`.

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 1 | |
| `run_id` | id | matches run directory |
| `goal` | string (≤ 1200 chars) | one paragraph; what and why |
| `requirements[]` | `{id, statement, acceptance, severity}` | `id` is the key the Statement of Completion rows reference; `severity ∈ {blocking, high, normal}` |
| `constraints[]` | `{id, statement, source}` | includes SIMPLE-CODE-GATE applicability flag as a constraint |
| `scope_in[]`, `scope_out[]` | string[] | explicit; `scope_out` items need no justification here |
| `sources[]` | `{kind ∈ {human_brief, bmad_snapshot, spec, prior_run}, ref, sha256}` | every BMAD ref must resolve to `docs/upstream/bmad/<id>/SNAPSHOT_MANIFEST.json` with matching `aggregate_sha256` |
| `verification_requirements[]` | `{id, requirement_ids[], tier ∈ V0..V4, description}` | ids must equal the manifest check ids (replaces the three-way id-set check) |
| `budget` | `{model, effort_g2, effort_g3, max_wall_minutes?}` | effort recorded *with* model id; not normative across models |
| `risks[]` | `{statement, mitigation}` | optional (premortem content) |
| `execution_mode` | `PLANNING_ONLY \| EXECUTION_ENABLED` | mirrors `EXECUTION_MODE.txt` |
| `done_definition` | string | one sentence the Statement of Completion must satisfy |

Lint (G1): schema valid; no placeholder tokens; every `sources[]` digest resolves; `verification_requirements[].requirement_ids` ⊆ `requirements[].id`; `budget.model` non-empty.

## 2. Verification Manifest v2 — `schemas/verification_manifest_v2.schema.json`

Existing v1 fields preserved. Additions:

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 2 | |
| `checks[].result` | `{status ∈ {PASS, FAIL, SKIPPED, NOT_RUN}, receipt_path, exit_code?, utc?}` | written only by `conductorctl receipts run`; agent edits to `result` are detected by receipt digest mismatch |
| `checks[].requirement_ids[]` | id[] | replaces `constraint_ids` naming; both accepted in v2 for golden-pack compatibility |

Rule change: missing manifest on an `EXECUTION_ENABLED` run, or on any run whose Intent Pack has `verification_requirements`, is an **error**.

## 3. Statement of Completion — `schemas/statement_of_completion.schema.json`

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 1 | |
| `run_id`, `intent_pack_sha256` | | binds to the locked intent |
| `rows[]` | `{requirement_id, status, evidence[], limitation?, residual_gap?, decision_ref?}` | one row per Intent Pack requirement; no missing, no extra |
| `rows[].status` | `verified \| partial \| not_done \| out_of_scope` | |
| `rows[].evidence[]` | `{check_id, receipt_path, receipt_sha256}` | required non-empty when `verified`; each must exist, be non-empty, and record PASS |
| `rows[].decision_ref` | path | required when `out_of_scope`; must point to a human-written file under `countersign/` or a Gap Request resolution |
| `verifier` | `{report_path, report_sha256, fresh_context: true}` | G3 subagent report |
| `derived_state` | `READY \| BLOCKED \| NEEDS_HUMAN_DECISION` | **computed by lint**, never authored: all verified → READY; any not_done without decision_ref → BLOCKED; any partial or out_of_scope without decision_ref → NEEDS_HUMAN_DECISION |
| `handoff_state` | `REVIEW_READY \| MERGE_READY` | per merge protocol; MERGE_READY only with a merge-preflight summary path |

Countersign lives in `countersign/COMPLETION.json` (§8 shape), not inside this file.

## 4. Gap Request — `schemas/gap_request.schema.json`

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 1 | |
| `gap_id` | id | |
| `run_id`, `intent_pack_sha256` | | |
| `origin_snapshot_id`, `origin_snapshot_sha256` | | the BMAD snapshot the intent was built from, if any |
| `requirement_id` | id | the Statement row that spawned it |
| `gap_type` | `requirement \| architecture \| ux \| product_context \| constraint` | |
| `question` | string | |
| `proposed_resolution` | string? | agent may propose; never decides |
| `supersession_impact` | `active_scope \| future_only \| unknown` | agent's assessment; human confirms |
| `resolution` | `{decided_by, utc, decision, new_snapshot_id?, new_snapshot_sha256?}`? | human-written; presence closes the gap |

Rule: a Gap Request with `supersession_impact = active_scope` and a resolution that introduces a new snapshot **reopens G1** for the run.

## 5. Project Config — `schemas/project_config.schema.json`

Single file `docs/Conductor/PROJECT_CONFIG.json`. Replaces `PROJECT_PREFLIGHT.json`, the knowledge-lint required-files list, and the hard-coded BMAD root.

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 1 | |
| `product_name` | string | display name (Conductor) |
| `bmad.declared_root` | path? | exactly one; repo-relative; must contain `_config/manifest.yaml`; no symlink components; not under `docs/`; default `_bmad` |
| `bmad.legacy_evidence_root` | path | default `docs/adapters/bmad/legacy-evidence` |
| `protected_roots[]` | path[] | postimage compare set |
| `allowed_harnesses[]` | `claude-code \| codex \| cursor` | |
| `default_budget` | `{model, effort_g2, effort_g3}` | |
| `agents_md.mode` | `managed_block \| full_ownership` | default `managed_block` |
| `agents_md.project_owned_sha256` | sha256? | digest of the project-owned block, verified on update |
| `required_docs[]` | path[] | shrunk knowledge-lint list |
| `project_preflight` | `{enabled, timeout_seconds ≤ 300}`? | fixed command as today |
| `recall.trigger` | `always \| when_index_nonempty \| never` | default `when_index_nonempty` |

## 6. Lane Policy — `schemas/lane_policy.schema.json`

| Field | Type | Notes |
|---|---|---|
| `schema_version` | int = 1 | |
| `policy_version` | semver | |
| `bmad_version` | exact | `6.10.0` today; any other version fails closed |
| `lanes.product_context.workflows[]` | skill names | see 04 §2 |
| `lanes.product_context.write_roots[]` | path[] | default `[_bmad-output]` |
| `lanes.delivery.workflows[]` | skill names | prohibited for Conductor-bound work |
| `helpers[]` | skill names | same-lane nesting allowed (review, elicitation, editorial, party mode) |
| `evidence_only[]` | skill names | TEA design-level; promotable as EVIDENCE_ONLY |
| `unknown_default` | `deny` | constant |
| `unsafe_layout_blocks[]` | `intake \| promote \| solution_context_authoring` | discovery is never in this list |
| `profiles{}` | per-skill `{logical_path, skill_sha256, customize_sha256}` | existing pinned profiles |

## 7. Evidence Receipt — `schemas/evidence_receipt.schema.json`

Written only by `conductorctl receipts run`. Agent-authored receipts are detectable: the runner signs `payload_sha256` over the fields and the manifest lint recomputes it.

| Field | Type |
|---|---|
| `schema_version` | int = 1 |
| `run_id`, `check_id` | |
| `command[]` | argv (shell=False) |
| `cwd` | repo-relative |
| `exit_code` | int |
| `stdout_sha256`, `stderr_sha256`, `stdout_bytes`, `stderr_bytes` | bounded capture (64 KiB each, as project preflight does) |
| `stdout_path`, `stderr_path` | under `receipts/logs/` |
| `started_utc`, `finished_utc` | |
| `status` | `PASS \| FAIL` derived from `exit_code == 0` unless the check declares `expected_exit` |
| `payload_sha256` | digest over all fields above |

## 8. Countersign files and AGENTS.md composition

Countersign (`countersign/INTENT_LOCK.json`, `EXECUTION_GO.json`, `COMPLETION.json`), one shape:

| Field | Type |
|---|---|
| `schema_version` | int = 1 |
| `kind` | `INTENT_LOCK \| EXECUTION_GO \| COMPLETION` |
| `subject_path`, `subject_sha256` | the artifact being signed |
| `decision` | `GO \| NO_GO` |
| `signer` | string |
| `utc` | |
| `note` | string? |

Lint rule: `subject_sha256` must equal the current digest of `subject_path`; a stale countersign is an error, mirroring "base moved → MERGE_READY is stale".

AGENTS.md composition (Project Config `agents_md.mode = managed_block`):

```
<!-- conductor:managed:start v=<plugin_version> sha256=<block_digest> -->
... Conductor block: read order (2 files), autonomy contract, lane summary, canonical commands ...
<!-- conductor:managed:end -->

... project-owned content, preserved byte-for-byte; digest recorded in Project Config ...
```

Update rewrites only the managed block. Brownfield adoption never deletes existing content; it inserts the block at the top and records the project-owned digest. Verified in Claude Code, Codex, and Cursor as part of qualification (06 §4).

## Addendum (2026-09-04, step 2b)

Implementation moved two things relative to the sketches above, both forced by the existing rule that the core plugin payload is customer- and domain-neutral:

- **Project Config §5** no longer has a `bmad` block. It has a generic `adapters.<name>` object whose values are validated by each adapter's own schema. The BMAD block (declared root, legacy evidence root) is `docs/adapters/bmad/contracts/bmad_adapter_config.schema.json`.
- **Lane Policy §6** lives at `docs/adapters/bmad/contracts/lane_policy.schema.json` and ships with the `conductor-bmad` plugin only.

Two schema corrections from the v1 compatibility test: ids allow up to 127 characters (real run ids are ~70), and the manifest check type set includes `manual`, which pack-lint already accepted.
