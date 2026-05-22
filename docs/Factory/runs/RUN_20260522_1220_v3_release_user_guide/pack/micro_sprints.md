# Micro-sprints - V3-OP-001 Release Approval And User Guide

## Version
v1

## Change Log
- v1 (2026-05-22): Stage G micro-sprints.

## MS-01 Release Approval
- Objective: Record explicit release approval for optional `V3-OP-001` operational use.
- Inputs: locked intent, decision report, human approval.
- Outputs: release approval artifact and checklist/report updates.
- Entry Criteria: intent lock PASS.
- Exit Criteria: approval names profile, commit `f07fa11`, V2 fallback, and residual-risk acceptance.
- Stop Or Go: stop if approval is broadened beyond `V3-OP-001`.

## MS-02 User Guide And Templates
- Objective: Add Codex user guide and starter templates.
- Inputs: release approval and V3 profile.
- Outputs: `USER_GUIDE.md` and templates under `docs/Factory/v3/templates/`.
- Entry Criteria: MS-01 complete.
- Exit Criteria: guide explains V3 direct use, V3 triage, V2 fallback, and slot-game example boundaries.
- Stop Or Go: stop if guide implies real-money, compliance, payments, deployment, or runtime-kernel authority is approved.

## MS-03 Tracking And Verification
- Objective: Update tracking docs and verify.
- Inputs: release and guide docs.
- Outputs: project state, roadmap, changelogs, verification evidence, closeout.
- Entry Criteria: MS-02 complete.
- Exit Criteria: verification plan passes.
- Stop Or Go: stop on failed lint, advisory scan, or inconsistent release status.
