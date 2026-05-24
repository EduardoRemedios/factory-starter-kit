# Factory v3 Phase 1 Trial Plan

## Version
v0.3

## Change Log
- v0.3 (2026-05-24): Added thread-local mission-envelope guidance for trials whose authorized file scope excludes Factory artifacts.
- v0.2 (2026-05-24): Added explicit pre-envelope fallback guidance for unsuitable `V3-OP-001` trial requests.
- v0.1 (2026-05-24): Initial Phase 1 real-project trial operating plan for optional `V3-OP-001` use.

## Status
Research trial operating plan only. This document is non-enforcing: it does not approve new V3 profiles, make V3 the default, deprecate V2, or wire V3 checks into required gates.

## Purpose
Define how to run the first real-project trial batch for `V3-OP-001 Bounded Code Change`.

The purpose of Phase 1 is not to prove that V3 is ready to become default. The purpose is to learn whether optional `V3-OP-001` is understandable, bounded, useful, and safe enough to refine before Phase 2 structured mission records are designed.

## Trial Target
Minimum trial batch:

- 5 real-project `V3-OP-001` trial records.
- At least 2 trials in ordinary repositories without a separate governance kernel.
- At least 1 trial by a user other than the V3 doc author.
- At least 1 trial that records V2 fallback or explains why V3 was not suitable.
- Every trial must record friction, fallback review, advisory eval output, and SIMPLE-CODE-GATE review.

## Trial Record Location
Store trial records under:

```text
docs/Factory/v3/trials/
```

Recommended naming:

```text
TRIAL_YYYYMMDD_NNN_<short_slug>.md
```

Use:

```text
docs/Factory/v3/templates/V3_PHASE1_TRIAL_CAPTURE_TEMPLATE.md
```

Track all trials in:

```text
docs/Factory/v3/trials/TRIAL_INDEX.md
```

## Trial Selection Rules
Use `V3-OP-001` only when all are true:

- the requested change is a bounded code change,
- the objective is clear,
- likely files or modules can be named,
- forbidden scope can be named,
- verification commands are known,
- dependency policy is explicit,
- V2 fallback triggers are understood,
- no payment, authentication, compliance, regulated-action, production deployment, infrastructure, or runtime-kernel authority is implicated.

Route to V2 instead when any condition applies:

- mission intent is ambiguous,
- scope is broad or likely to expand,
- allowed files, commands, tools, or dependencies are unclear,
- verification cannot be run or recorded,
- the user expects V3 to replace V2,
- the work touches core governance, runtime authority, proof, policy, evidence, auth, payment, deployment, or infrastructure.

## Required Trial Evidence
Each trial record must include:

- project and harness metadata,
- why V3 was selected or rejected,
- mission envelope path, or an explicit pre-envelope fallback reason when no envelope was created,
- closeout path,
- fallback review path,
- SIMPLE-CODE-GATE review path,
- command and verification evidence,
- advisory eval output,
- user friction or confusion,
- false-positive and false-negative notes,
- whether the trial should influence Phase 2 mission record design.

## Pre-Envelope Fallback Trials
A useful trial can stop before mission-envelope creation.

Record a pre-envelope fallback when the user request is conversationally clear but insufficient for `V3-OP-001`, such as a vague continuation request, broad feature request, missing verification command, missing authorized files, or a task that touches forbidden scope.

This should count as a V2 fallback or V3-unsuitable trial only when the record includes:

- the missing authority or scope element,
- the reason no mission envelope was created,
- the V2 fallback path,
- friction notes,
- false-positive and false-negative notes for any advisory checks that ran.

## Thread-Local Mission Envelopes
A completed V3 trial does not need to create repository Factory artifacts when those artifacts are outside the authorized mutation scope.

Use a thread-local mission envelope when all are true:

- the code-change scope is otherwise eligible for `V3-OP-001`,
- authorized files intentionally exclude Factory artifact paths,
- creating a mission-envelope file would expand the approved file scope,
- closeout records the envelope contents or states that the envelope remained in-thread,
- command evidence and fallback review are preserved in the trial record.

Do not widen authorized files solely to persist Factory paperwork.

## Required Checks
Run these checks when they exist in the adopting repo:

```bash
python3 scripts/factory_v3_advisory_lint.py --target docs/Factory/v3 --json
python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --json
python3 scripts/factory_v3_operational_readiness_eval.py --target docs/Factory/v3 --nl-pilot --json
```

If the adopting repo does not have these scripts, record that clearly in the trial. Do not treat missing optional advisory scripts as a V3 failure unless the trial depended on them.

Always run the adopting repo's normal lint, test, or build command when available.

## Review Cadence
Review after each trial:

- Was V3 appropriate?
- Did V2 fallback trigger?
- Did the user understand the profile?
- Did the template capture the important evidence?
- Did advisory checks miss anything?
- Did SIMPLE-CODE-GATE catch complexity risk?

Review after the first 5 trials:

- Keep `V3-OP-001` unchanged.
- Refine user guide or templates.
- Add or tune fixtures.
- Start Phase 2 structured mission record design.
- Pause V3 expansion and route more work through V2.

## Stop Conditions
Stop Phase 1 advancement and run a new Factory review if any condition occurs:

- a trial uses V3 outside `V3-OP-001`,
- users repeatedly miss V2 fallback triggers,
- public docs imply a separate governance kernel is required,
- failed verification continues without explicit human override,
- SIMPLE-CODE-GATE issues are treated as acceptable without evidence,
- advisory evals miss material real-world drift,
- trial evidence records success but not friction, fallback review, or residual risk.

## Phase 1 Exit Criteria
Phase 1 is ready for a decision review only when:

- at least 5 trial records exist,
- the trial index is current,
- fallback and friction evidence is present,
- at least one unsuitable or fallback case has been recorded,
- false-positive and false-negative notes have been reviewed,
- guide/template update recommendations are explicit,
- a recommendation is made for Phase 2 structured mission records.

## Expected Decision Outputs
After the first trial batch, produce one of:

- `REFINE_V3_OP_001`: improve guide/templates but keep profile scope unchanged.
- `ADD_FIXTURES`: add deterministic or natural-language fixtures before more trials.
- `START_PHASE_2`: design a shadow structured mission record.
- `PAUSE_V3_EXPANSION`: keep V3 optional but collect more V2-governed evidence.
- `FALLBACK_TO_V2`: V3-OP-001 is not yet reliable enough for continued optional trials.
