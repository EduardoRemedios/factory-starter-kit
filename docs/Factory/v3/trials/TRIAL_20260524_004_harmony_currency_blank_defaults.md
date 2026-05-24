# V3 Phase 1 Trial: Harmony Currency Blank Defaults

## Status
Phase 1 `V3-OP-001` trial record. This record is research and evidence capture only; it is non-enforcing for required repository gates and does not approve any V3 profile beyond optional `V3-OP-001`.

## Trial Metadata
- Trial ID: `TRIAL_20260524_004_harmony_currency_blank_defaults`
- Date: 2026-05-24
- Repository: Harmony
- Branch: not recorded in returned trial note
- Commit before trial: not recorded in returned trial note
- Commit after trial: not recorded in returned trial note
- User or reviewer: Eduardo Remedios / Harmony Codex session
- Coding harness: Codex
- Model: Codex session model not recorded in repository evidence
- Project type: Harmony project repository using Factory v2
- Separate governance kernel present: unknown from returned trial note; forbidden scope excluded governance-kernel/runtime authority changes
- User familiarity with Factory v2: high

## Trial Decision
- Trial outcome: COMPLETED_WITH_V3
- Profile selected: `V3-OP-001`
- Why V3 was selected: The task had a concrete objective, exact authorized files, explicit forbidden scope, a named verification command, no dependency changes, and no forbidden authority surface.
- Why V3 was rejected or stopped, if applicable: not applicable
- V2 fallback used: no
- V2 fallback reason, if used: not applicable

## Scope Classification
- Requested task: Make `CurrencyConfig.from_display_config()` fall back to GBP defaults when `currency_code` or `currency_symbol` is present but blank after stripping.
- Bounded-code-change fit: yes
- Files or modules expected to change:
  - `/Users/eduardodosremedios/harmony/runtime/currency_formatter.py`
  - `/Users/eduardodosremedios/harmony/tests/test_currency_formatter.py`
- Forbidden files or modules: no `runtime/pack_loader.py`, no `runtime/response_composer.py`, no operator profile YAML, no policy semantics, no monetary calculation behavior, no server wiring, no dependency additions, no files outside authorized scope.
- Out-of-scope concerns checked:
  - payment: not implicated
  - authentication: not implicated
  - compliance or regulated action: not implicated
  - production deployment: not implicated
  - infrastructure: not implicated
  - runtime-kernel authority: excluded by forbidden scope
  - broad architecture change: excluded by forbidden scope

## Mission Evidence
- Mission envelope path or thread-local reference: thread-local Harmony chat mission envelope; no file artifact created.
- If no mission envelope was created, why: authorized file scope allowed only `runtime/currency_formatter.py` and `tests/test_currency_formatter.py`, so creating a repository mission-envelope artifact would have expanded scope.
- Closeout path: returned Harmony chat closeout, summarized in this trial record.
- Fallback review path: returned Harmony chat closeout, summarized in this trial record.
- SIMPLE-CODE-GATE review path: returned Harmony chat closeout, summarized in this trial record.
- Advisory eval output path: not run in Harmony; the Harmony session inspected upstream Factory V3 guidance.
- Command evidence path: returned Harmony chat closeout, summarized in this trial record.
- Pull request or commit link: not recorded in returned trial note.

## Authority And Verification
| Area | Trial Evidence | Result |
|---|---|---|
| Objective clear | Blank stripped `currency_code` and `currency_symbol` should fall back to GBP defaults. | PASS |
| Allowed files named | `runtime/currency_formatter.py` and `tests/test_currency_formatter.py`. | PASS |
| Forbidden scope named | Pack loader, response composer, operator profile YAML, policy semantics, monetary calculation behavior, server wiring, dependencies, and files outside authorized scope were forbidden. | PASS |
| Allowed commands named | `python3 -m unittest tests.test_currency_formatter -v`. | PASS |
| Dependency policy explicit | No new dependencies. | PASS |
| Verification commands run | Allowed verification command passed with 17 tests. | PASS |
| Halt behavior followed | No halt condition fired; scope stayed bounded and verification passed. | PASS |
| Evidence paths preserved | Harmony closeout recorded files changed, command run, verification, SIMPLE-CODE-GATE review, fallback review, and friction. | PASS |
| V2 fallback triggers explicit | Fallback would trigger on scope expansion, verification failure, forbidden authority surface, or dependency need. | PASS |

## Command Evidence
| Command | Result | Evidence Path |
|---|---|---|
| `python3 -m unittest tests.test_currency_formatter -v` | PASS, 17 tests | returned Harmony chat closeout |

## Advisory Eval Evidence
| Check | Result | Evidence Path | Human Classification |
|---|---|---|---|
| `factory_v3_advisory_lint.py` | not run in Harmony | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py` | not run in Harmony | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py --nl-pilot` | not run in Harmony | returned Harmony chat closeout | not_run |

## SIMPLE-CODE-GATE Review
- Smallest clear behavior-preserving change: PASS; small local change in a display utility and focused test.
- Code bloat avoided: yes; no abstraction added.
- Spooky action avoided: yes; no pack loader, response composer, server, profile, policy, or hidden boundary behavior changed.
- Dependency creep avoided: yes; no dependency changes.
- Silent failures avoided: yes; blank display fields now resolve through explicit default behavior.
- Speculative abstraction avoided: yes.
- Any accepted complexity: none reported.
- Refactor trigger, if complexity was deferred: not applicable.

## Fallback And Halt Review
- Any ambiguity discovered: no.
- Any scope expansion attempted: no.
- Any missing authority found: no.
- Any verification failure: no.
- Any stale or conflicting reentry state: no.
- Any user-requested fallback: no.
- Action taken: completed bounded V3 execution and closeout; no V2 fallback trigger fired.

## Friction And Usability
- What was confusing: the compact mission envelope stayed in-thread because the authorized file list did not permit creating Factory artifact files.
- What was slower than V2: the user needed V2-governed candidate selection before the first Harmony happy-path trial; this second happy-path prompt was direct once the candidate was known.
- What was faster than V2: the bounded V3 execution avoided a full A-to-I2 planning pack.
- Which guide step was missing or unclear: no new guide gap; this reinforces existing thread-local envelope guidance.
- Which template field was missing or unclear: no new template gap; this reinforces the existing mission evidence field for thread-local references.
- Install/setup friction: none reported.
- Suggested guide or template update: no immediate change; carry thread-local envelope support into Phase 2 mission-record design.

## False Positive And False Negative Notes
- Advisory false positives: none observed; advisory checks were not run in Harmony.
- Advisory false negatives: none observed; advisory checks were not run in Harmony.
- Missed fallback triggers: none observed.
- Drift that was caught: none; trial stayed within scope.
- Drift that was missed: none observed.
- New fixture recommended: natural-language fixture for repeated successful V3 bounded code trials with thread-local mission envelopes.

## Roadmap Pre-Mortem Watchpoints
| Watchpoint | Observed? | Evidence |
|---|---|---|
| V3 used outside `V3-OP-001` | no | Task matched bounded-code profile and stayed within two authorized files. |
| V2 fallback missed or delayed | no | No fallback trigger fired. |
| Trial captured friction, not only success | yes | Friction note records thread-local envelope behavior. |
| Public docs caused separate-kernel confusion | no | No confusion reported; forbidden scope excluded governance-kernel/runtime authority. |
| Failed verification continued without approval | no | Verification passed. |
| SIMPLE-CODE-GATE weakness observed | no | SIMPLE-CODE-GATE review passed. |
| Eval missed real-world drift | no | No drift observed; advisory checks were not run in Harmony. |

## Trial Judgment
- Trial classification: USEFUL_SIGNAL
- Pre-envelope decision captured: not_applicable
- Should this trial influence Phase 2 mission record design: yes
- Reason: Phase 2 mission records should support thread-local envelopes for narrow code trials or a separately authorized mission-record path when persistence is required.

## Follow-Ups
| Follow-Up | Owner | Target |
|---|---|---|
| Carry thread-local envelope support into Phase 2 mission-record design. | Factory maintainer | Phase 2 structured mission record |
| Consider a natural-language fixture for repeated successful bounded V3 execution with thread-local envelopes. | Factory maintainer | Future eval fixture backlog |
