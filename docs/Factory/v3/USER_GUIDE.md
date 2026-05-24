# Factory V3 User Guide

## Version
v1.1

## Change Log
- v1.1 (2026-05-24): Added pre-envelope fallback guidance and a Phase 1 trial prompt for ordinary adopting repositories.
- v1 (2026-05-22): Initial Codex user guide for optional `V3-OP-001` operational use.

## Status
Operational for optional `V3-OP-001 Bounded Code Change` use only.

Factory v2 remains supported and available as fallback. Factory v3 is not the default Factory mode.

This guide is based on the approved research evidence and remains non-enforcing for required repository gates.

## What V3 Is For
Use `V3-OP-001` when the work is already bounded enough for Codex to execute with a compact mission envelope.

Good V3 work has:

- a clear objective,
- known files or modules,
- explicit allowed commands,
- no new broad architecture,
- no unclear dependencies,
- runnable verification,
- halt-on-failure rules,
- V2 fallback triggers.

## What V3 Is Not For
Do not use `V3-OP-001` for:

- broad product discovery,
- ambiguous architecture choices,
- unresolved stakeholder decisions,
- production deployment,
- payment flows,
- authentication policy,
- compliance or regulated-action decisions,
- real-money gambling behavior,
- infrastructure authority,
- runtime-kernel behavior,
- work that requires a new framework or broad abstraction.

Route those to Factory v2 or a future heavier profile.

## How V3 Relates To V2
If you know V2, think of V3 as a smaller operational envelope for work that no longer needs the full A-to-I2 planning pack.

V3 can start first when the task is bounded.

V3 can also act as a front door:

1. classify the request,
2. decide whether `V3-OP-001` applies,
3. create a mission envelope for bounded work,
4. fall back to V2 when the work is not eligible.

Using V3 to route work back to V2 is a successful outcome, not a failure.

## Pre-Envelope Fallback
V3 does not need to create a mission envelope for every request.

If the request does not identify a bounded code-changing objective, authorized files, forbidden scope, allowed commands, and verification, Codex should stop before the envelope and record why the work should use V2 or ordinary planning instead.

This is the correct response for prompts like:

```text
Proceed with the next step.
```

That kind of prompt may be enough conversational authority to continue discussion, but it is not enough authority for a `V3-OP-001` execution mission.

## Quick Start In Codex
Use this prompt:

```text
Use Factory V3 profile V3-OP-001 if eligible.

Task:
<describe the task>

Before editing, classify whether this task is eligible for V3-OP-001.
If eligible, create a mission envelope with objective, authorized files, forbidden scope, allowed commands, verification, halt rules, and V2 fallback triggers.
If not eligible, stop and explain why this should use Factory V2.
```

## Phase 1 Trial Prompt
Use this when testing V3 in an ordinary project repository.

```text
Use Factory V3 profile V3-OP-001 if eligible.

Factory source:
https://github.com/EduardoRemedios/factory-starter-kit

Context:
I am running a Phase 1 V3 real-project trial. V3 is optional and bounded. Factory V2 remains the fallback. Do not make V3 the default, do not add required CI gates, and do not create broad governance infrastructure.

Task:
<describe one small bounded code change>

Candidate authorized files:
- <file or directory>

Forbidden scope:
- no payment, authentication, compliance, deployment, infrastructure, or runtime-kernel changes
- no dependency additions unless explicitly approved
- no broad architecture changes
- no files outside the authorized scope unless you stop and ask

Allowed commands:
- <project lint/test/build command>

Before editing:
1. Fetch or inspect the latest Factory V3 guidance from the Factory source if this repo does not already have it.
2. Classify whether this task is eligible for V3-OP-001.
3. If eligible, create a compact mission envelope with objective, authorized files, forbidden scope, allowed commands, verification, halt rules, and V2 fallback triggers.
4. If not eligible, stop before creating the envelope and explain why this should use Factory V2.

During execution:
- make the smallest clear behavior-preserving change,
- avoid speculative abstraction,
- avoid dependency creep,
- run the allowed verification,
- halt if verification fails or scope expands.

Closeout:
Record files changed, commands run, verification result, SIMPLE-CODE-GATE review, fallback review, friction notes, and whether the trial should influence future V3 mission-record design.
```

## Required Mission Envelope
Every V3 mission should record:

- profile ID: `V3-OP-001`,
- objective,
- success criteria,
- eligible-work rationale,
- non-goals,
- authorized files and directories,
- forbidden files and directories,
- allowed commands,
- dependency policy,
- verification commands,
- halt-on-failure rules,
- interruption and reentry rules,
- V2 fallback triggers,
- SIMPLE-CODE-GATE review status.

Use `docs/Factory/v3/templates/V3_MISSION_ENVELOPE_TEMPLATE.md`.

## During Execution
Codex should:

1. read the mission envelope,
2. make the smallest clear change,
3. avoid speculative abstraction,
4. avoid new dependencies unless explicitly authorized,
5. run the listed verification,
6. halt on failed halt-on-failure checks,
7. preserve evidence,
8. close out with fallback review and SIMPLE-CODE-GATE review.

## Fallback To V2
Fallback to V2 when:

- the objective is unclear,
- scope expands,
- required authority is missing,
- verification fails,
- evidence is stale or missing,
- ownership boundaries are unclear,
- new dependencies are proposed without approval,
- payment, auth, compliance, deployment, runtime-kernel, or infrastructure concerns appear,
- the human sponsor asks for V2.

Use `docs/Factory/v3/templates/V3_FALLBACK_REVIEW_TEMPLATE.md`.

## Example: New Online Slot Game
A broad request like this is not automatically a V3 implementation mission:

```text
Build a new online slot game.
```

V3 can still help as the front door.

First, ask Codex to classify and slice the work:

```text
Use Factory V3 profile V3-OP-001 as an intake step.

Goal:
Create a new online slot game.

Classify what parts are eligible for V3-OP-001 and what must route to V2.
Do not implement yet.
Call out any real-money gambling, payment, authentication, compliance, production RNG, deployment, or infrastructure concerns.
```

Expected routing:

| Slice | Route | Reason |
|---|---|---|
| Game concept, market positioning, compliance assumptions | V2 | Product and regulatory shape is not bounded implementation. |
| Free-play reel prototype in an existing frontend | Possibly V3 | Bounded if files, commands, and verification are known. |
| Deterministic payline evaluator with tests | Possibly V3 | Bounded local code with clear tests. |
| Visual polish for an existing demo screen | Possibly V3 | Bounded UI work if scope is named. |
| Real-money wallet, payments, auth, KYC, regulated RNG, deployment | V2 or heavier profile | Outside `V3-OP-001`. |

Example bounded V3 mission:

```text
Use Factory V3 profile V3-OP-001.

Objective:
In the existing free-play slot demo, implement a deterministic payline evaluator.

Authorized files:
- src/game/paylines.ts
- src/game/paylines.test.ts

Forbidden scope:
- no payments
- no authentication
- no real-money behavior
- no production deployment
- no dependency additions
- no changes outside the listed files

Allowed commands:
- npm test -- paylines
- npm run lint

Verification:
- tests cover winning and losing paylines
- lint passes

Fallback:
Return to Factory V2 if the rules are ambiguous, files need to expand, dependencies are requested, or verification cannot run.
```

## Closeout
Use `docs/Factory/v3/templates/V3_CLOSEOUT_TEMPLATE.md`.

Closeout should record:

- branch and commit,
- files changed,
- commands run,
- verification outputs,
- advisory eval output if used,
- SIMPLE-CODE-GATE review,
- fallback review,
- residual risks.

## Starter Templates
- `docs/Factory/v3/templates/V3_MISSION_ENVELOPE_TEMPLATE.md`
- `docs/Factory/v3/templates/V3_CLOSEOUT_TEMPLATE.md`
- `docs/Factory/v3/templates/V3_FALLBACK_REVIEW_TEMPLATE.md`
- `docs/Factory/v3/templates/V3_SIMPLE_CODE_GATE_REVIEW_TEMPLATE.md`
