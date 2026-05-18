# docs/Factory/MERGE_PROTOCOL.md — Tool-Agnostic Merge Authorization Protocol

## Version
v1.0

## Change Log
- v1.0 (2026-05-18): Added generic merge authorization protocol for AI-assisted repositories.

## Purpose
Define one merge authorization process that is identical regardless of which AI tool did the work.

## Scope
Applies to any code change that an agent wants to merge to the repository's mainline branch.

## Project Adapter
Each adopting repository should define its own merge preflight command. The command should be project-native and should write evidence artifacts.

Recommended command name:
- `bash scripts/merge_preflight.sh`

Recommended evidence path:
- `artifacts/merge_preflight/<UTC timestamp>/SUMMARY.md`

## Candidate Preconditions
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
- If merge preflight fails: do not ask to merge. Fix blockers or report them.
- If merge preflight passes: report the summary path and ask exactly:
  - `Merge preflight passed. Would you like to merge?`
- Only merge after explicit human authorization such as `YES`.

## CI Contract
CI should use the same regression gate logic as local preflight wherever practical.

If a project uses known-failure or merge-gate-exclude files, those files should be the source of truth for both local preflight and CI.
