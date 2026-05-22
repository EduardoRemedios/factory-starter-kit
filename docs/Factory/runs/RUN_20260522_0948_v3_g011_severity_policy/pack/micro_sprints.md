# Micro-sprints - V3-G011 Severity Policy

## Version
v1

## Change Log
- v1 (2026-05-22): Stage G micro-sprints.

## MS-01 Policy Draft
- Objective: Add the cross-version severity policy.
- Inputs: locked intent, risk register.
- Outputs: `docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md`.
- Entry Criteria: intent lock PASS.
- Exit Criteria: policy defines blocker, advisory-high, and no-finding classes.
- Stop Or Go: stop if policy is V3-only or AEGIS-centric.

## MS-02 V3 Checklist Update
- Objective: Mark C-04 complete without promoting V3.
- Inputs: policy doc, V3 operational decision checklist.
- Outputs: updated `docs/Factory/v3/OPERATIONAL_DECISION_CHECKLIST.md`.
- Entry Criteria: policy exists.
- Exit Criteria: checklist cites evidence and keeps C-05 through C-10 open.
- Stop Or Go: stop if V2 fallback or V3 research posture is weakened.

## MS-03 Tracking And Verification
- Objective: Update tracking docs and verify.
- Inputs: docs changes.
- Outputs: project state, roadmap, changelogs, verification evidence.
- Entry Criteria: policy and checklist updates complete.
- Exit Criteria: verification plan passes.
- Stop Or Go: stop on failed lint or advisory scan.
