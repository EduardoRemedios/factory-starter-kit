# Raw Brief - V3-OP-001 Release Approval And User Guide

## Request
Record explicit approval for Factory V3 `V3-OP-001 Bounded Code Change` to be used operationally as an optional profile, then add the user/setup guide and templates that let Codex users start using V3.

## Approval Text
The human sponsor approved operational use in the current thread after reviewing the proposed approval wording.

Recorded approval:

> I approve Factory V3 `V3-OP-001 Bounded Code Change` for optional operational use. Factory V2 remains supported and available as fallback. Approval applies at commit `f07fa11`. I accept the residual risks recorded in `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`.

## Execution Mode
EXECUTION_ENABLED

## Scope
- Add `docs/Factory/v3/OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`.
- Update the C-10 decision report and checklist to record approval.
- Add `docs/Factory/v3/USER_GUIDE.md`.
- Add V3 starter templates under `docs/Factory/v3/templates/`.
- Update project state, roadmap, and changelogs.

## Non-goals
- Do not make V3 the default Factory mode.
- Do not deprecate Factory v2.
- Do not wire V3 checks into required gates.
- Do not approve profiles beyond `V3-OP-001`.
- Do not claim runtime-kernel proof, production mediation, payment authorization, compliance approval, or production deployment authority.
