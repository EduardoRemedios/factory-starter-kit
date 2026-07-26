# Agent Loop Bridge Manual Runbook

## Version
v1

## Change Log
- v1 (2026-05-18): Initial generic manual runbook for the review-only Agent Loop Bridge pattern.

## Purpose
Run a governed, manual review-only relay between agent lanes using structured handoffs, PR/CI evidence, and Factory artifacts.

This runbook does not authorize a webhook, scheduled poller, GitHub Action, auto-merge, autonomous patching, or policy/runtime/schema/evidence changes.

## Producer Plane Preflight
Before a producer agent posts a handoff, confirm one of these is true:
- Collaboration-channel write capability is enabled in the active agent session.
- A human will manually post the exact structured handoff message.

Also confirm:
- The producer can identify the PR URL, PR number, branch, and head SHA.
- The producer can reference the Factory run ID and sprint ID.
- The producer can point to relevant Factory pack artifacts.

If those checks fail, do not post a machine-actionable handoff. Use a human note instead.

## Reviewer Plane Preflight
Before the reviewer agent reviews a handoff, confirm:
- Collaboration-channel read capability is enabled for the handoff channel or thread.
- Local repo access is available for referenced Factory artifacts.
- PR metadata, diff, and status access is enabled through a connector or CLI fallback.
- Write capability is enabled only if the result will be posted back.
- PR comment write capability is enabled only if the event allows `post_pr_comment`.

If a required capability is missing, return `NEEDS_HUMAN` or use an explicit manual fallback. Do not claim evidence was inspected.

## Manual Review Steps
1. Read only the agreed channel or thread.
2. Extract one fenced JSON block with `event_type: "factory.handoff.v1"`.
3. Save the JSON into a local fixture file if using the validator directly.
4. Run the local validator:

```bash
python3 scripts/agent_loop_bridge_validate.py path/to/fixture.json --json
```

5. If validation fails, stop and return `NEEDS_HUMAN` or `BLOCKING` based on validator output.
6. Confirm the PR head SHA in the handoff matches the live PR head.
7. Inspect PR diff and CI status through a connector or CLI fallback.
8. Inspect referenced Factory artifacts locally.
9. Check no-touch boundaries against the PR diff.
10. Check docs sync only if the handoff claims a closed sprint GO.
11. Produce a `factory.review_result.v1` payload.
12. Post the review result only when posting is allowed and write capability exists.
13. Append review metadata to `artifacts/agent_loop_bridge/reviewed_events.jsonl` when operating a real review.

## Verdict Rules
- `PASS`: all required checks pass and no material caveats remain.
- `PASS_WITH_NOTES`: no blocker, but non-blocking caveats remain.
- `BLOCKING`: required evidence failed or governance boundary was breached.
- `NEEDS_HUMAN`: required access, approval, or policy judgment is missing.

## Hard Stops
- No casual chat text triggers.
- No posting without explicit allowed action.
- No patching, committing, pushing, approving, or merging.
- No webhook, scheduled automation, or GitHub Action in Phase 1.
- No runtime, server, policy-pack, schema, evidence, adapter, or CI workflow edits.
