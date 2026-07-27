# docs/Factory/MERGE_PROTOCOL.md — Tool-Agnostic Merge Authorization Protocol

## Version
v1.1

## Change Log
- v1.1 (2026-06-24): Added `REVIEW_READY` versus `MERGE_READY` handoff states and a final sync window to reduce async mainline churn without weakening merge preflight.
- v1.0 (2026-05-18): Added generic merge authorization protocol for AI-assisted repositories.

## Purpose
Define one merge authorization process that is identical regardless of which AI tool did the work.

## Scope
Applies to any repository change that an agent wants to merge to the repository's mainline branch.

## Project Adapter
Each adopting repository should define its own merge preflight command. The command should be project-native and should write evidence artifacts.

Recommended command name:
- `bash scripts/merge_preflight.sh`

Recommended evidence path:
- `artifacts/merge_preflight/<UTC timestamp>/SUMMARY.md`

## Handoff States
Agents should label repository handoffs with one of these states:

- `REVIEW_READY`: the branch is ready for human or maintainer review, but it is not yet asking for merge authorization. Pack/stage/content evidence should be current for review. Final base synchronization and merge preflight may be absent or stale because the mainline branch can move while review is pending.
- `MERGE_READY`: the branch is ready for immediate merge authorization. It has passed the merge preconditions below against the current configured base branch.

`REVIEW_READY` must never be represented as merge approval evidence. It allows useful review to start without forcing repeated final merge-preflight runs each time another maintainer merges the base branch.

## Review-Ready Preconditions
A `REVIEW_READY` handoff should include:
- The candidate state committed at `HEAD`.
- The tracked working tree clean, unless the handoff explicitly says it is a draft and lists dirty paths.
- Relevant Factory validators for the changed artifacts, such as `stage-lint`, `pack-lint`, knowledge lint, no-secret checks, or focused tests.
- Known open issues, stale evidence, or base-sync risk called out explicitly.

## Final Sync Window
The final sync window is the short period when a maintainer intends to move a reviewed branch from `REVIEW_READY` to `MERGE_READY`.

Rules:
- Open the final sync window only after review blockers are resolved and the maintainer intends to merge next.
- During the window, sync the branch with the latest configured base branch, rerun merge preflight, and refresh the evidence summary.
- Avoid merging unrelated base-branch changes during the window unless the candidate is rejected, delayed, or the window is closed.
- If the configured base branch moves after merge preflight passes, `MERGE_READY` is stale and the branch falls back to `REVIEW_READY` until final sync and merge preflight are rerun.

## Merge-Ready Preconditions
The merge candidate should satisfy all of the following before an agent asks for merge authorization:
- The candidate state is committed at `HEAD`.
- The tracked working tree is clean.
- `HEAD` contains the latest configured base branch.
- Knowledge lint passes.
- The project's conformance or contract harness passes, if one exists.
- The project's regression gate passes with no unexpected failures beyond an explicit allowlist.
- Any merge-gate excludes are explicit, documented, and narrow.

## Evidence Contract
A merge preflight should write a summary artifact that records:
- timestamp
- branch
- `HEAD` commit
- base ref
- tracked working tree status
- changed-file count
- each command run
- each command result
- evidence log paths
- final PASS or FAIL result

## Agent Behavior
- For `REVIEW_READY`: report review evidence and open issues, but do not ask to merge.
- For `MERGE_READY`: confirm final sync window status and then apply the merge-preflight behavior below.
- If merge preflight fails: do not ask to merge. Fix blockers or report them.
- If merge preflight passes: report the summary path and ask exactly:
  - `Merge preflight passed. Would you like to merge?`
- Only merge after explicit human authorization such as `YES`.

## CI Contract
CI should use the same regression gate logic as local preflight wherever practical.

If a project uses known-failure or merge-gate-exclude files, those files should be the source of truth for both local preflight and CI.
