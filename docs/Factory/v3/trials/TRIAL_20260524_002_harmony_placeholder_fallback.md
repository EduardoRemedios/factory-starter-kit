# V3 Phase 1 Trial: Harmony Placeholder Fallback

## Status
Phase 1 `V3-OP-001` trial record. This record is research and evidence capture only; it is non-enforcing for required repository gates and does not approve any V3 profile beyond optional `V3-OP-001`.

## Trial Metadata
- Trial ID: `TRIAL_20260524_002_harmony_placeholder_fallback`
- Date: 2026-05-24
- Repository: Harmony
- Branch: not recorded in returned trial note
- Commit before trial: not recorded in returned trial note
- Commit after trial: no Harmony file changes reported
- User or reviewer: Eduardo Remedios / Harmony Codex session
- Coding harness: Codex
- Model: Codex session model not recorded in repository evidence
- Project type: Harmony project repository using Factory v2
- Separate governance kernel present: unknown from returned trial note
- User familiarity with Factory v2: high

## Trial Decision
- Trial outcome: FALLBACK_TO_V2
- Profile selected: `V3-OP-001`
- Why V3 was selected: The user initiated the first Harmony Phase 1 V3 trial using the Phase 1 ordinary-repo trial prompt.
- Why V3 was rejected or stopped, if applicable: The pasted prompt still contained placeholders for the actual bounded change, authorized file scope, and allowed verification command.
- V2 fallback used: yes
- V2 fallback reason, if used: Missing objective/file/command authority is a pre-envelope fallback trigger under `V3-OP-001`.

## Scope Classification
- Requested task: Run a Harmony Phase 1 V3 trial using the ordinary-repo prompt, but without replacing the task, file, and command placeholders.
- Bounded-code-change fit: no
- Files or modules expected to change: none; no eligible mission existed.
- Forbidden files or modules: no governance-kernel/runtime authority, no policy/evidence/lease/action-execution changes, no auth, payment, deployment, infrastructure, compliance, dependency, or broad architecture changes.
- Out-of-scope concerns checked:
  - payment: not implicated
  - authentication: not implicated
  - compliance or regulated action: not implicated
  - production deployment: not implicated
  - infrastructure: not implicated
  - runtime-kernel authority: excluded by prompt; not assessed beyond pre-envelope rejection
  - broad architecture change: not authorized

## Mission Evidence
- Mission envelope path: not created; V3 rejected before mission-envelope creation.
- If no mission envelope was created, why: unchanged placeholders meant the request lacked a concrete bounded objective, authorized files, and allowed verification command.
- Closeout path: returned Harmony chat closeout, summarized in this trial record.
- Fallback review path: returned Harmony chat closeout, summarized in this trial record.
- SIMPLE-CODE-GATE review path: returned Harmony chat closeout, summarized in this trial record.
- Advisory eval output path: not run in this repository; the Harmony session inspected upstream Factory V3 guidance.
- Command evidence path: returned Harmony chat closeout, summarized in this trial record.
- Pull request or commit link: none; no Harmony file changes reported.

## Authority And Verification
| Area | Trial Evidence | Result |
|---|---|---|
| Objective clear | The actual bounded code-change objective remained a placeholder. | FAIL |
| Allowed files named | The authorized file scope remained a placeholder. | FAIL |
| Forbidden scope named | Prompt excluded sensitive scope, including runtime authority, auth, payment, deployment, infrastructure, compliance, dependencies, and broad architecture. | PASS |
| Allowed commands named | The allowed verification command remained a placeholder. | FAIL |
| Dependency policy explicit | Prompt prohibited dependency additions unless explicitly approved. | PASS |
| Verification commands run | No task-specific verification ran because no eligible mission existed. | PASS |
| Halt behavior followed | The Harmony session stopped before creating a mission envelope or editing files. | PASS |
| Evidence paths preserved | Returned chat closeout preserved the reason for pre-envelope fallback. | PASS |
| V2 fallback triggers explicit | Missing file and command authority were cited as V2 fallback triggers. | PASS |

## Command Evidence
| Command | Result | Evidence Path |
|---|---|---|
| Read-only inspection of Harmony `docs/HARMONY_STATE.md`, `docs/ROADMAP.md`, `docs/Factory/ORCHESTRATION.md`, `docs/Factory/SCRATCHPAD.md`, `docs/Factory/ProductOwner/PO_PROCESS.md`, and local V3 docs/templates | completed in Harmony session | returned Harmony chat closeout |
| Task-specific verification | not run because no eligible mission existed | returned Harmony chat closeout |

## Advisory Eval Evidence
| Check | Result | Evidence Path | Human Classification |
|---|---|---|---|
| `factory_v3_advisory_lint.py` | not run in this repository | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py` | not run in this repository | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py --nl-pilot` | not run in this repository | returned Harmony chat closeout | not_run |

## SIMPLE-CODE-GATE Review
- Smallest clear behavior-preserving change: not applicable; no code-changing V3 mission was run.
- Code bloat avoided: yes; no speculative code was introduced.
- Spooky action avoided: yes; no runtime or boundary behavior was introduced.
- Dependency creep avoided: yes; no dependency change was made.
- Silent failures avoided: yes; fallback was explicit.
- Speculative abstraction avoided: yes; no abstraction was created from unresolved placeholders.
- Any accepted complexity: none.
- Refactor trigger, if complexity was deferred: not applicable.

## Fallback And Halt Review
- Any ambiguity discovered: yes; the actual task, file scope, and allowed verification command were unresolved placeholders.
- Any scope expansion attempted: no.
- Any missing authority found: yes; code-change authority, file authority, and command authority were missing.
- Any verification failure: no.
- Any stale or conflicting reentry state: no.
- Any user-requested fallback: no.
- Action taken: stopped before mission-envelope creation or file edits and routed back to V2/resubmission with concrete authority.

## Friction And Usability
- What was confusing: the trial prompt was paste-ready in structure but still required the user to replace placeholders before sending it as an execution request.
- What was slower than V2: the trial produced a pre-envelope fallback instead of exercising the V3 happy path.
- What was faster than V2: the missing authority was detected before planning or implementation work began.
- Which guide step was missing or unclear: the guide should explicitly say that unchanged placeholders are expected to trigger pre-envelope fallback.
- Which template field was missing or unclear: no additional template field is required; the existing pre-envelope field is sufficient.
- Install/setup friction: none reported.
- Suggested guide or template update: add a warning before the Phase 1 trial prompt that every placeholder must be replaced before submitting a V3 execution request.

## False Positive And False Negative Notes
- Advisory false positives: none observed; advisory checks were not run.
- Advisory false negatives: none observed; advisory checks were not run.
- Missed fallback triggers: none; placeholder detection triggered fallback.
- Drift that was caught: attempted mission-envelope creation without concrete task, file, or command authority was stopped.
- Drift that was missed: none observed.
- New fixture recommended: natural-language fixture for an unchanged Phase 1 trial prompt containing placeholders.

## Roadmap Pre-Mortem Watchpoints
| Watchpoint | Observed? | Evidence |
|---|---|---|
| V3 used outside `V3-OP-001` | no | V3 was not used for execution; fallback happened before mission-envelope creation. |
| V2 fallback missed or delayed | no | Fallback happened at classification time. |
| Trial captured friction, not only success | yes | Friction notes record placeholder-submission ambiguity. |
| Public docs caused separate-kernel confusion | no | No separate-kernel confusion was reported. |
| Failed verification continued without approval | no | No verification failure occurred. |
| SIMPLE-CODE-GATE weakness observed | no | No code-changing execution occurred. |
| Eval missed real-world drift | no | No advisory miss observed; advisory checks were not run. |

## Trial Judgment
- Trial classification: NEEDS_GUIDE_UPDATE
- Pre-envelope decision captured: yes
- Should this trial influence Phase 2 mission record design: yes
- Reason: Phase 2 mission records should treat unresolved placeholders as an explicit pre-envelope rejection reason before any authority lease or mission state is created.

## Follow-Ups
| Follow-Up | Owner | Target |
|---|---|---|
| Add guide warning that unchanged placeholders should trigger pre-envelope fallback. | Factory maintainer | Completed in `SPRINT_20260524_037` |
| Consider a natural-language fixture for unchanged Phase 1 trial prompts. | Factory maintainer | Future eval fixture backlog |
