# Agent Loop Bridge

## Version
v1

## Change Log
- v1 (2026-05-18): Added generic review-only Agent Loop Bridge pattern for structured handoffs across agent lanes.

## Purpose
Define a governed relay for agent lanes where a collaboration channel carries structured handoff events, Git hosting and CI provide review evidence, Factory artifacts provide governance truth, and humans retain authority over merge, scope expansion, execution authorization, policy/runtime/schema changes, and sensitive decisions.

This is a harness pattern. It does not change Factory Core stage contracts, merge protocol, validator semantics, or human Go requirements.

## Phase 1 Boundary
Phase 1 is review-only.

Allowed:
- read structured handoff events
- inspect linked PR metadata, diff, and CI status
- inspect local Factory run artifacts
- verify Stage I2 verdict, execution mode, human Go evidence where relevant, no-touch boundaries, test evidence, and docs sync
- post a structured review result when explicitly requested and permitted

Forbidden:
- auto-merge
- autonomous patching
- opening downstream runs
- generating `EXECUTION_PROMPT.md`
- policy, runtime, evidence, schema, adapter, server, or CI workflow changes
- reacting to casual chat text
- treating chat or connector state as approval authority

## Recommended Architecture
| Layer | Responsibility | Phase 1 implementation |
|---|---|---|
| Producer | One agent lane emits a structured handoff after Factory run completion and PR creation. | Message containing one fenced JSON event plus human-readable summary. |
| Transport | Collaboration tool carries event text and thread context. | Dedicated channel or thread; no casual text triggers. |
| Reviewer | Another agent validates event shape, gathers PR/CI/Factory evidence, and issues a verdict. | Manual invocation or scheduled/polling run; no autonomous writes except review result posting when requested. |
| Evidence | PR, CI, local repo artifacts, Factory pack, merge protocol. | Connector or CLI for PR/diff/status; local filesystem for artifacts. |

## Reviewer Processing Contract
1. Run a capability preflight for the active session: collaboration channel read/write, PR metadata/diff/status access, local repo access, and optional PR comment write access.
2. Read only the configured channel or thread.
3. Extract messages with exactly one fenced JSON block and `event_type: "factory.handoff.v1"`.
4. Reject malformed JSON, missing required fields, unknown required checks, or conflicting action permissions before touching remote systems.
5. Resolve `(event_id, repo.full_name, pull_request.number, pull_request.head_sha)` as the idempotency key.
6. Check a local audit ledger before reviewing. Recommended Phase 1 path: `artifacts/agent_loop_bridge/reviewed_events.jsonl`.
7. Gather PR, CI, and Factory evidence without changing repo state.
8. Produce one `factory.review_result.v1` payload.
9. Append the result payload, message reference, PR URL, head SHA, and evidence summary to the audit ledger.
10. Post the review result only when write capability exists and `allowed_actions` permits it.

If the same event ID appears with a different PR number or head SHA, treat it as `NEEDS_HUMAN`.

## Handoff Event Schema
The handoff message must include exactly one fenced JSON block with `event_type: "factory.handoff.v1"`.

```json
{
  "event_type": "factory.handoff.v1",
  "event_id": "fh-YYYYMMDD-001",
  "created_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "producer": {
    "lane": "producer_agent",
    "actor": "person_or_agent",
    "tool": "codex"
  },
  "repo": {
    "full_name": "owner/repo",
    "default_branch": "main",
    "working_tree_path_hint": "/path/to/repo"
  },
  "pull_request": {
    "url": "https://example.com/owner/repo/pull/123",
    "number": 123,
    "branch": "codex/example-branch",
    "head_sha": "abc123"
  },
  "factory": {
    "run_id": "RUN_YYYYMMDD_HHMM_factory",
    "sprint_id": "SPRINT_YYYYMMDD_NNN",
    "execution_mode": "PLANNING_ONLY",
    "stage_i2_verdict": "PASS",
    "human_go_required": false,
    "human_go_artifact": null
  },
  "allowed_actions": [
    "read_handoff",
    "inspect_pr",
    "inspect_ci_status",
    "inspect_factory_pack",
    "post_review_result"
  ],
  "forbidden_actions": [
    "merge",
    "push_commits",
    "patch_code",
    "open_downstream_run",
    "generate_execution_prompt",
    "change_policy_runtime_schema_evidence"
  ],
  "required_checks": [
    "pr_diff",
    "ci_status",
    "factory_pack_lint_evidence",
    "stage_i2_verdict",
    "execution_mode_and_human_go",
    "no_touch_boundary",
    "test_evidence",
    "docs_sync"
  ],
  "evidence_paths": {
    "pack": "docs/Factory/runs/RUN_YYYYMMDD_HHMM_factory/pack/",
    "pack_audit": "docs/Factory/runs/RUN_YYYYMMDD_HHMM_factory/pack/PACK_AUDIT_REPORT.md",
    "pack_checklist": "docs/Factory/runs/RUN_YYYYMMDD_HHMM_factory/pack/PACK_CHECKLIST.md",
    "execution_completion": null,
    "merge_preflight_summary": null
  },
  "no_touch_paths": [
    "runtime/**",
    "server/**",
    "schemas/**"
  ],
  "docs_sync_required": [
    "docs/PROJECT_STATE.md",
    "docs/ROADMAP.md",
    "docs/CHANGELOG.md"
  ]
}
```

Schema rules:
- `event_id` must be unique and stable.
- `head_sha` is required for CI status checks.
- `allowed_actions` and `forbidden_actions` are both required; forbidden actions win on conflict.
- `required_checks` must be selected from a closed vocabulary. Unknown checks are `NEEDS_HUMAN`, not silently ignored.
- `execution_mode` must match the run-root `EXECUTION_MODE.txt` when a Factory run path exists.

## Review Result Schema
The reviewer produces one structured result.

```json
{
  "event_type": "factory.review_result.v1",
  "handoff_event_id": "fh-YYYYMMDD-001",
  "reviewed_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "reviewer": {
    "lane": "reviewer_agent",
    "actor": "person_or_agent",
    "tool": "codex"
  },
  "verdict": "PASS_WITH_NOTES",
  "summary": "CI is green and the Factory pack is coherent; docs sync is not required for this planning-only handoff.",
  "checks": [
    {
      "id": "pr_diff",
      "status": "PASS",
      "evidence": "PR diff inspected at the handoff head SHA.",
      "notes": []
    }
  ],
  "blocking_findings": [],
  "human_questions": [],
  "forbidden_actions_observed": [],
  "next_allowed_action": "human_review"
}
```

Verdict vocabulary:
- `PASS`
- `PASS_WITH_NOTES`
- `BLOCKING`
- `NEEDS_HUMAN`

Per-check status vocabulary:
- `PASS`
- `FAIL`
- `NOTE`
- `NOT_APPLICABLE`
- `NEEDS_HUMAN`

## Local Validator
The starter kit ships a deterministic JSON fixture validator:

```bash
python3 scripts/agent_loop_bridge_validate.py path/to/fixture.json --json
```

Fixture shape:

```json
{
  "kind": "handoff",
  "live_pr_head_sha": "abc123",
  "input": {},
  "expected": {
    "valid": true,
    "verdict_floor": "review_may_continue"
  }
}
```

Supported fixture kinds:
- `handoff`
- `review_result`
- `posting_permissions`
- `docs_sync_branches`
- `no_touch_diff`

## Guardrails
- Collaboration messages are triggers and evidence pointers, not approval authority.
- PR/CI systems are evidence sources, not scope authority.
- Factory run artifacts remain the governance source of truth.
- The bridge must fail closed on malformed JSON, stale SHAs, unknown required checks, ambiguous repo/PR identity, missing Factory run artifacts, or conflicting allowed/forbidden actions.
- The reviewer must never patch, commit, push, merge, rerun Factory stages, or open downstream work during Phase 1.
- Duplicate events are idempotent: if the same `event_id` and `head_sha` were already reviewed, post a duplicate notice or update only when explicitly requested.
