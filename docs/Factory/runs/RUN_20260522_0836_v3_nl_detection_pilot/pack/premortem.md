# Premortem

## Version
v1

## Change Log
- v1 (2026-05-22): Stage E premortem.

| ID | Scenario | Impact | Mitigation |
|---|---|---|---|
| PM-01 | Pilot mode breaks default expected JSON. | Existing regression fails. | Do not change default output shape. |
| PM-02 | Natural-language patterns overmatch clean docs. | Trust in advisory signal drops. | Require zero false positives across clean corpus for this pilot. |
| PM-03 | Pilot findings are treated as blockers. | Unauthorized gate behavior. | Preserve `blocking_effect: none` and advisory-only status. |
| PM-04 | Matching becomes over-abstracted. | Hard-to-review brittle code. | Keep direct pattern functions and standard library only. |

## Exit Criteria Status
- PASS
