# V3 Phase 1 Trial Capture Template

## Status
Template for Phase 1 `V3-OP-001` real-project trials. This template is research and evidence capture only; it is non-enforcing for required repository gates and does not approve any V3 profile beyond optional `V3-OP-001`.

## Trial Metadata
- Trial ID:
- Date:
- Repository:
- Branch:
- Commit before trial:
- Commit after trial:
- User or reviewer:
- Coding harness:
- Model:
- Project type:
- Separate governance kernel present: yes | no | unknown
- User familiarity with Factory v2: none | low | medium | high

## Trial Decision
- Trial outcome: COMPLETED_WITH_V3 | FALLBACK_TO_V2 | BLOCKED | ABANDONED
- Profile selected: `V3-OP-001`
- Why V3 was selected:
- Why V3 was rejected or stopped, if applicable:
- V2 fallback used: yes | no
- V2 fallback reason, if used:

## Scope Classification
- Requested task:
- Bounded-code-change fit: yes | no | uncertain
- Files or modules expected to change:
- Forbidden files or modules:
- Out-of-scope concerns checked:
  - payment:
  - authentication:
  - compliance or regulated action:
  - production deployment:
  - infrastructure:
  - runtime-kernel authority:
  - broad architecture change:

## Mission Evidence
- Mission envelope path:
- If no mission envelope was created, why:
- Closeout path:
- Fallback review path:
- SIMPLE-CODE-GATE review path:
- Advisory eval output path:
- Command evidence path:
- Pull request or commit link:

## Authority And Verification
| Area | Trial Evidence | Result |
|---|---|---|
| Objective clear |  | PASS | FAIL | UNCLEAR |
| Allowed files named |  | PASS | FAIL | UNCLEAR |
| Forbidden scope named |  | PASS | FAIL | UNCLEAR |
| Allowed commands named |  | PASS | FAIL | UNCLEAR |
| Dependency policy explicit |  | PASS | FAIL | UNCLEAR |
| Verification commands run |  | PASS | FAIL | UNCLEAR |
| Halt behavior followed |  | PASS | FAIL | UNCLEAR |
| Evidence paths preserved |  | PASS | FAIL | UNCLEAR |
| V2 fallback triggers explicit |  | PASS | FAIL | UNCLEAR |

## Command Evidence
| Command | Result | Evidence Path |
|---|---|---|
|  |  |  |

## Advisory Eval Evidence
| Check | Result | Evidence Path | Human Classification |
|---|---|---|---|
| `factory_v3_advisory_lint.py` |  |  | accepted | false_positive | needs_more_context | not_run |
| `factory_v3_operational_readiness_eval.py` |  |  | accepted | false_positive | needs_more_context | not_run |
| `factory_v3_operational_readiness_eval.py --nl-pilot` |  |  | accepted | false_positive | needs_more_context | not_run |

## SIMPLE-CODE-GATE Review
- Smallest clear behavior-preserving change:
- Code bloat avoided:
- Spooky action avoided:
- Dependency creep avoided:
- Silent failures avoided:
- Speculative abstraction avoided:
- Any accepted complexity:
- Refactor trigger, if complexity was deferred:

## Fallback And Halt Review
- Any ambiguity discovered:
- Any scope expansion attempted:
- Any missing authority found:
- Any verification failure:
- Any stale or conflicting reentry state:
- Any user-requested fallback:
- Action taken:

## Friction And Usability
- What was confusing:
- What was slower than V2:
- What was faster than V2:
- Which guide step was missing or unclear:
- Which template field was missing or unclear:
- Install/setup friction:
- Suggested guide or template update:

## False Positive And False Negative Notes
- Advisory false positives:
- Advisory false negatives:
- Missed fallback triggers:
- Drift that was caught:
- Drift that was missed:
- New fixture recommended:

## Roadmap Pre-Mortem Watchpoints
| Watchpoint | Observed? | Evidence |
|---|---|---|
| V3 used outside `V3-OP-001` | yes | no |  |
| V2 fallback missed or delayed | yes | no |  |
| Trial captured friction, not only success | yes | no |  |
| Public docs caused separate-kernel confusion | yes | no |  |
| Failed verification continued without approval | yes | no |  |
| SIMPLE-CODE-GATE weakness observed | yes | no |  |
| Eval missed real-world drift | yes | no |  |

## Trial Judgment
- Trial classification: USEFUL_SIGNAL | NEEDS_GUIDE_UPDATE | NEEDS_TEMPLATE_UPDATE | NEEDS_EVAL_UPDATE | UNSUITABLE_FOR_V3
- Pre-envelope decision captured: yes | no | not_applicable
- Should this trial influence Phase 2 mission record design: yes | no
- Reason:

## Follow-Ups
| Follow-Up | Owner | Target |
|---|---|---|
|  |  |  |
