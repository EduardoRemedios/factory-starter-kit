# Raw Brief - V3-G011 Severity Policy

## Source
User approved proceeding on 2026-05-22 after reviewing the proposed next step for deciding when SIMPLE-CODE-GATE findings remain advisory versus become operational blockers.

## Execution Authorization
- Execution Mode: EXECUTION_ENABLED
- Execution Authorization: user message "ok proceed" on 2026-05-22.
- Downstream Fan-Out: not approved.

## Goal
Create a generic Factory-first severity policy for V3-G011 SIMPLE-CODE-GATE findings.

## Required Outcome
- Add a V3 policy document that works for ordinary adopting repos, not only repos with AEGIS or another runtime kernel.
- Clarify when SIMPLE-CODE-GATE findings are blockers, advisory-high findings, or no findings.
- Keep AEGIS/runtime-kernel handling as an optional additional boundary case, not the center of the policy.
- Update the V3 operational decision checklist so C-04 is complete only if the policy is explicit enough for future operational profiles.
- Update project tracking docs and changelogs.

## Non-goals
- Do not promote Factory v3 operationally.
- Do not deprecate Factory v2.
- Do not wire V3 evals into required gates.
- Do not change current runtime-kernel or AEGIS boundary ownership.
- Do not change matcher severities in the standalone eval runner during this policy sprint.
