# V3 Phase 1 Trial: Harmony FAQ Ingestion UTF-8

## Status
Phase 1 `V3-OP-001` trial record. This record is research and evidence capture only; it is non-enforcing for required repository gates and does not approve any V3 profile beyond optional `V3-OP-001`.

## Trial Metadata
- Trial ID: `TRIAL_20260524_003_harmony_faq_ingestion_utf8`
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
- Requested task: Wrap CSV decode failures in `IngestionError` so malformed uploaded CSV bytes fail through the same typed ingestion boundary as malformed JSON.
- Bounded-code-change fit: yes
- Files or modules expected to change:
  - `/Users/eduardodosremedios/harmony/runtime/faq_ingestion.py`
  - `/Users/eduardodosremedios/harmony/tests/test_faq_ingestion.py`
- Forbidden files or modules: no FAQ retrieval changes, no corpus store changes, no server routes, no evidence store changes, no policy packs, no auth/session behavior, no dependency additions, no files outside the authorized scope.
- Out-of-scope concerns checked:
  - payment: not implicated
  - authentication: excluded by forbidden scope
  - compliance or regulated action: not implicated
  - production deployment: not implicated
  - infrastructure: not implicated
  - runtime-kernel authority: excluded by forbidden scope
  - broad architecture change: excluded by forbidden scope

## Mission Evidence
- Mission envelope path: thread-local Harmony chat mission envelope; no file artifact created.
- If no mission envelope was created, why: authorized file scope allowed only `runtime/faq_ingestion.py` and `tests/test_faq_ingestion.py`, so creating a repository mission-envelope artifact would have expanded scope.
- Closeout path: returned Harmony chat closeout, summarized in this trial record.
- Fallback review path: returned Harmony chat closeout, summarized in this trial record.
- SIMPLE-CODE-GATE review path: returned Harmony chat closeout, summarized in this trial record.
- Advisory eval output path: not run in Harmony; the Harmony session inspected upstream Factory V3 guidance.
- Command evidence path: returned Harmony chat closeout, summarized in this trial record.
- Pull request or commit link: not recorded in returned trial note.

## Authority And Verification
| Area | Trial Evidence | Result |
|---|---|---|
| Objective clear | Wrap CSV `UnicodeDecodeError` failures in `IngestionError`. | PASS |
| Allowed files named | `runtime/faq_ingestion.py` and `tests/test_faq_ingestion.py`. | PASS |
| Forbidden scope named | Retrieval, corpus store, server routes, evidence store, policy packs, auth/session, dependencies, and files outside authorized scope were forbidden. | PASS |
| Allowed commands named | `python3 -m unittest tests.test_faq_ingestion -v`. | PASS |
| Dependency policy explicit | No new dependencies. | PASS |
| Verification commands run | Allowed verification command passed with 14 tests. | PASS |
| Halt behavior followed | No halt condition fired; scope stayed bounded and verification passed. | PASS |
| Evidence paths preserved | Harmony closeout recorded files changed, command run, verification, SIMPLE-CODE-GATE review, fallback review, and friction. | PASS |
| V2 fallback triggers explicit | Fallback would trigger on scope expansion, verification failure, forbidden authority surface, or dependency need. | PASS |

## Command Evidence
| Command | Result | Evidence Path |
|---|---|---|
| `python3 -m unittest tests.test_faq_ingestion -v` | PASS, 14 tests | returned Harmony chat closeout |

## Advisory Eval Evidence
| Check | Result | Evidence Path | Human Classification |
|---|---|---|---|
| `factory_v3_advisory_lint.py` | not run in Harmony | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py` | not run in Harmony | returned Harmony chat closeout | not_run |
| `factory_v3_operational_readiness_eval.py --nl-pilot` | not run in Harmony | returned Harmony chat closeout | not_run |

## SIMPLE-CODE-GATE Review
- Smallest clear behavior-preserving change: PASS; change was local and direct.
- Code bloat avoided: yes; no abstraction added.
- Spooky action avoided: yes; no hidden side effects or boundary mutation reported.
- Dependency creep avoided: yes; no dependency changes.
- Silent failures avoided: yes; malformed CSV bytes now fail through the typed ingestion boundary.
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
- What was slower than V2: the user needed a separate V2-governed intake pass to choose a concrete candidate before execution.
- What was faster than V2: once the candidate was concrete, the bounded V3 execution avoided a full A-to-I2 planning pack.
- Which guide step was missing or unclear: the guide should explicitly allow a thread-local mission envelope when repository artifact files are outside authorized scope.
- Which template field was missing or unclear: mission evidence should distinguish thread-local envelope from repository-file envelope.
- Install/setup friction: none reported.
- Suggested guide or template update: add thread-local envelope guidance for strictly bounded file scopes.

## False Positive And False Negative Notes
- Advisory false positives: none observed; advisory checks were not run in Harmony.
- Advisory false negatives: none observed; advisory checks were not run in Harmony.
- Missed fallback triggers: none observed.
- Drift that was caught: none; trial stayed within scope.
- Drift that was missed: none observed.
- New fixture recommended: natural-language fixture for a successful V3 bounded code trial with thread-local mission envelope.

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
- Reason: Phase 2 mission records should allow a thread-local envelope or external closeout reference when the authorized mutation scope intentionally excludes Factory artifact files.

## Follow-Ups
| Follow-Up | Owner | Target |
|---|---|---|
| Add guide/template note that thread-local mission envelopes are acceptable when artifact files are outside authorized scope. | Factory maintainer | Completed in `SPRINT_20260524_038` |
| Consider a natural-language fixture for successful bounded V3 execution with thread-local envelope. | Factory maintainer | Future eval fixture backlog |
