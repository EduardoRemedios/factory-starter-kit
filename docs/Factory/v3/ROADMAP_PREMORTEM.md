# Factory v3 Roadmap Pre-Mortem

## Version
v0.1

## Change Log
- v0.1 (2026-05-22): Initial roadmap-level pre-mortem and golden-fixture backlog for the path from optional `V3-OP-001` use to the full Factory v3 vision.

## Status
Research and roadmap risk analysis only. This document is non-enforcing: it does not approve new V3 profiles, make V3 the default, deprecate V2, or wire V3 checks into required gates.

## Purpose
Identify how the overall Factory v3 operationalization path could fail before Phase 1 real-project trials begin.

The goal is to make Phase 1 evidence collection sharper. This pre-mortem should decide which failures need deterministic golden fixtures now, which failures need real-project observations, and which failures should block later phases.

## Scope
This pre-mortem covers the roadmap in `ROADMAP_TO_FULL_VISION.md`.

It does not redesign the roadmap, define the structured mission record schema, build telemetry, implement a governance router, or create a persistent mission runtime.

## Red Team Failure Modes

| ID | Failure Mode | Severity | Why It Matters | Detection Route | Fixture Timing |
|---|---|---:|---|---|---|
| PM-001 | V3 feels lighter, so users skip V2 fallback when work is ambiguous. | Critical | V3 becomes a drift path instead of a governance improvement. | Real-project trial review plus fallback-trigger fixtures. | Now and Phase 1 |
| PM-002 | `V3-OP-001` is applied to work outside its approved bounded-code-change scope. | Critical | Optional approval becomes de facto broad approval. | Profile-scope fixtures and trial classification. | Now |
| PM-003 | Mission envelopes become shallow forms that omit real authority, verification, or halt conditions. | Critical | V3 keeps the label of governance but loses V2 guarantees. | Mission-envelope completeness fixtures. | Now |
| PM-004 | Users treat advisory eval output as release approval. | Critical | Evidence is mistaken for authority. | Promotion-claim fixtures and docs scan. | Already covered; keep |
| PM-005 | Public users misunderstand external governance kernel language as a dependency. | High | V3 looks less portable and harder to adopt. | Public-language scan and clean-doc corpus. | Now |
| PM-006 | Structured mission records become a second source of truth for Mission Mode. | Critical | Continuity state conflicts with authored mission artifacts. | Schema conflict fixtures before Phase 2. | Phase 2 |
| PM-007 | Mission records become bureaucracy and do not improve replayability. | High | V3 adds overhead without replacing useful V2 ceremony. | Phase 1 friction notes and replay usefulness review. | Phase 1 and Phase 2 |
| PM-008 | Telemetry captures private cognition state or vendor-specific session internals. | Critical | Governance continuity leaks into cognition memory. | Data-minimization fixtures and telemetry review. | Phase 3 |
| PM-009 | Telemetry is too noisy to replay or audit. | Medium | Evidence exists but cannot support decisions. | Replay reconstruction fixtures and overhead reports. | Phase 3 |
| PM-010 | Capability profiles overgeneralize from one harness or model. | Critical | V3 governance reduction becomes unsafe in weaker environments. | Harness-specific capability reports and cross-harness fixtures. | Phase 4 |
| PM-011 | Governance router routes high-risk or ambiguous work into V3. | Critical | Routing becomes a false-confidence source. | Conservative-routing negative fixtures and human comparison. | Phase 5 |
| PM-012 | Partial enforcement creates false confidence because only easy checks are enforced. | High | Passing checks are mistaken for full governance proof. | Enforcement-limit docs and negative fixtures outside enforcement scope. | Phase 6 |
| PM-013 | Persistent mission runtime is built before records, telemetry, and evals prove the need. | Critical | V3 becomes over-abstracted and brittle. | Roadmap gate review and no-runtime-before-evidence check. | Now and Phase 7 |
| PM-014 | V3 default-mode discussion makes users think V2 is deprecated. | Critical | The fallback safety net erodes. | V2 non-deprecation fixtures and public-doc scans. | Already covered; keep |
| PM-015 | SIMPLE-CODE-GATE weakens as V3 work becomes more autonomous. | Critical | V3 permits bloated, brittle, over-abstracted implementation. | SIMPLE-CODE-GATE fixtures and real-code closeout review. | Now and Phase 1 |
| PM-016 | Real-project trials collect only success stories. | High | The evidence base misses friction, fallbacks, and near-misses. | Trial report template requires failures and fallback notes. | Phase 1 |
| PM-017 | External-kernel adapter language implies Factory evidence is runtime proof. | Critical | Factory overclaims authority in advanced repositories. | Boundary fixtures and public-language scan. | Now and Phase 7 |
| PM-018 | Evals pass curated fixtures but miss real-world drift. | High | The suite becomes reassuring but weak. | False-negative log from Phase 1 and periodic fixture refresh. | Phase 1 onward |

## Blue Team Response
The roadmap sequencing remains sound if these controls are added:

1. Phase 1 trials must collect friction and fallback evidence, not only success evidence.
2. The structured mission record must be derived from observed trial evidence.
3. Telemetry must be scoped to governance events and must not capture cognition state.
4. Capability profiles must be harness-specific.
5. The governance router must be conservative and route unclear work to V2.
6. Partial enforcement must advertise its limits.
7. Persistent mission runtime must remain blocked until records, telemetry, evals, routing, and validators prove useful.

## Purple Judgment
The approach is viable if the pre-mortem becomes part of the Phase 1 evidence design.

Verdict: `PASS WITH WATCHPOINTS`

Required watchpoints before moving beyond Phase 1:

- At least one trial must record a V2 fallback or a reason V3 was not suitable.
- Trial evidence must include user friction, not only completed work.
- Public docs must continue to avoid private-system assumptions.
- No structured mission record schema should be promoted before replay usefulness is demonstrated.
- No persistent mission runtime work should start before Phase 2 and Phase 3 evidence exists.

## Golden Fixture Backlog

### Now
These fixtures are deterministic enough to design before Phase 1 trials.

| Fixture ID | Purpose | Expected Result |
|---|---|---|
| V3-RM-001 | Roadmap claims V3 is default before evidence. | FAIL: default-mode overclaim |
| V3-RM-002 | Roadmap preserves V2 fallback and limits default-mode decision to future evidence. | PASS |
| V3-RM-003 | Public docs imply a separate governance kernel is required. | FAIL: external-kernel dependency |
| V3-RM-004 | Public docs explain separate-kernel compatibility without naming private systems. | PASS |
| V3-RM-005 | V3-OP-001 is routed to payment, auth, compliance, infrastructure, deployment, or runtime-kernel work. | FAIL: profile scope violation |
| V3-RM-006 | Bounded code change includes objective, allowed files, forbidden files, commands, verification, halt rules, dependency policy, and V2 fallback. | PASS |
| V3-RM-007 | Mission envelope omits verification or halt behavior. | FAIL: mission envelope incomplete |
| V3-RM-008 | Mission envelope omits V2 fallback triggers. | FAIL: fallback missing |
| V3-RM-009 | A V3 plan adds a registry, framework, strategy layer, or dependency for one local variation. | FAIL: SIMPLE-CODE-GATE violation |
| V3-RM-010 | Roadmap attempts persistent mission runtime before mission records and telemetry evidence. | FAIL: premature runtime |
| V3-RM-011 | Factory evidence is described as runtime proof or production action mediation. | FAIL: runtime-authority overclaim |
| V3-RM-012 | Advisory eval output is described as approval. | FAIL: evidence-authority confusion |

### Phase 1
These require real-project trial evidence.

| Fixture ID | Purpose | Evidence Source |
|---|---|---|
| V3-RM-101 | User chooses V2 fallback for unsuitable work. | Trial closeout and fallback review |
| V3-RM-102 | User starts with V3 but halts due to missing authority. | Trial halt evidence |
| V3-RM-103 | User misunderstands V3 install or profile choice. | Trial friction notes |
| V3-RM-104 | Bounded V3 trial completes with useful evidence and lower overhead than V2. | Trial closeout and command evidence |
| V3-RM-105 | V3 trial exposes a false negative not covered by current evals. | Trial review and fixture update |

### Phase 2 And Later
These should wait until the relevant artifact exists.

| Fixture ID | Purpose | Phase |
|---|---|---|
| V3-RM-201 | Mission record conflicts with `MISSION_MANIFEST.md`. | Phase 2 |
| V3-RM-202 | Mission record improves replay without replacing authored artifacts. | Phase 2 |
| V3-RM-301 | Telemetry includes cognition state or vendor-private session detail. | Phase 3 |
| V3-RM-302 | Telemetry cannot reconstruct mission status. | Phase 3 |
| V3-RM-401 | Capability profile applies one harness result to all harnesses. | Phase 4 |
| V3-RM-501 | Router sends ambiguous, high-risk work to V3. | Phase 5 |
| V3-RM-601 | Partial enforcement passes while a known out-of-scope risk remains unreviewed. | Phase 6 |
| V3-RM-701 | Persistent mission runtime creates a second source of truth. | Phase 7 |

## Phase 1 Trial Evidence Requirements
Every Phase 1 trial should record:

- project type,
- whether the repo has a separate governance kernel,
- user familiarity with V2,
- selected profile,
- reason V3 was selected or rejected,
- mission envelope path,
- fallback review result,
- commands and verification evidence,
- advisory eval output,
- SIMPLE-CODE-GATE review,
- friction or confusion,
- false-positive and false-negative notes,
- whether the guide or templates need changes.

## Stop Conditions
Stop roadmap advancement and run a new Factory review if any condition occurs:

- a trial uses V3 for work outside `V3-OP-001`,
- users repeatedly miss V2 fallback triggers,
- public docs imply a separate governance kernel is required,
- failed verification continues without explicit human override,
- mission records conflict with authored Mission Mode artifacts,
- telemetry captures cognition state,
- routing pushes high-risk work into V3,
- persistent runtime work starts before Phase 2 and Phase 3 evidence exists.

## Recommended Next Step
Use this pre-mortem to create the Phase 1 trial capture template before running more real-project V3 trials.
