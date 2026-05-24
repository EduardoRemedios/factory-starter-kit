# Factory v3 Roadmap To Full Vision

## Version
v0.5

## Change Log
- v0.5 (2026-05-24): Added Phase 2 v0 shadow mission-record design artifacts and trial-derived fixtures.
- v0.4 (2026-05-24): Recorded Phase 1 decision review result and unblocked Phase 2 shadow mission-record design.
- v0.3 (2026-05-24): Aligned Phase 1 with completed trial-batch evidence, owner waiver, and decision-review gate before Phase 2.
- v0.2 (2026-05-22): Removed private-kernel naming, added a self-contained public boundary, and clarified that V3 remains useful without any external governance kernel.
- v0.1 (2026-05-22): Initial phased roadmap from optional `V3-OP-001` use to the full Factory v3 mission-governance runtime vision.

## Status
Roadmap. This document does not approve new V3 profiles, make V3 the default, deprecate V2, or wire V3 into required gates.

## Purpose
Define the practical path from the current Factory v3 bridgehead to the full mission-governance runtime vision.

The roadmap is intentionally gated. Each phase must produce evidence before the next one can become operational.

## Starting Point
Current state:

- Factory v2 is the default and fallback process.
- Factory v3 `V3-OP-001 Bounded Code Change` is approved for optional operational use.
- V3 has user guidance, templates, advisory evals, seeded fixtures, and pilot evidence.
- Phase 1 real-project trial evidence has reached decision-review readiness: 5 trial records, 2 fallback/pre-envelope trials, 3 completed happy-path trials across Harmony and Temper, and an owner waiver for the non-author user trial requirement in a solo AI-native development context.
- V3 does not yet have persistent mission state, enforced authority leases, structured telemetry, dynamic governance routing, continuous verification, capability profiling, or replayable execution graphs.
- This plan does not authorize promotion beyond the already approved optional `V3-OP-001` profile.

Interpretation:

Factory v3 has achieved an operational bridgehead, not the full platform.

## Target End State
Factory v3 becomes the normal way to govern suitable autonomous coding missions when:

- mission records are machine-readable,
- authority leases are explicit and at least partially enforceable,
- execution telemetry is recorded,
- verification and halt behavior are observable,
- evals measure drift, scope discipline, recovery, and verification quality,
- governance routing is based on mission risk and harness capability,
- V2 remains available for heavy, ambiguous, high-risk, or unsuitable work.

## Public Boundary
This roadmap is written for public starter-kit users.

Some adopting repositories may have external, private, or project-specific autonomy governance kernels that enforce production policy, runtime authority, proof, or regulated-action controls. Factory v3 must not depend on those systems or expose their private design.

For ordinary repositories, Factory v3 should work through documents, templates, validators, command evidence, project-specific tests, and optional harness adapters.

For repositories that do have a separate governance kernel, Factory v3 remains the coding-mission governance layer. Any mapping to that kernel must happen through a project adapter, and the kernel remains the authority and proof layer for runtime system behavior.

## Phase 0 - Current Bridgehead

Status: Done.

Evidence:

- `OPERATIONAL_RELEASE_APPROVAL_V3_OP_001.md`
- `OPERATIONAL_PROFILE_V3_OP_001_BOUNDED_CODE_CHANGE.md`
- `USER_GUIDE.md`
- `templates/`
- operational-readiness eval runner and fixtures
- real halt, reentry, fallback, and advisory detection pilot evidence

Decision:

`V3-OP-001` may be used optionally for bounded code-changing work.

Constraint:

No default-mode promotion. No required-gate integration. V2 remains fallback.

## Phase 1 - Real-Project Trial Loop

Status: Complete.

Goal:

Use `V3-OP-001` in real projects and learn where the guidance, templates, fallback triggers, and evals are weak.

Work:

1. Run `V3-OP-001` on several real bounded code changes across different repos.
2. Record mission envelope, closeout, fallback review, command evidence, and advisory eval output.
3. Capture friction from users with V2 experience and users new to Factory.
4. Track every fallback trigger and every case where the user expected V3 but V2 was safer.
5. Refine `USER_GUIDE.md` and templates only from observed evidence.

Required evidence:

- at least 5 real project `V3-OP-001` trials,
- at least 2 projects that do not use a separate autonomy governance kernel,
- at least 1 trial by a user other than the V3 doc author, or an explicit owner waiver for a solo AI-native development context,
- false-positive, false-negative, and fallback notes for each trial,
- update recommendations for docs and templates.

Current evidence:

- 5 Phase 1 trial records exist.
- 2 fallback/pre-envelope trials exist.
- 3 completed happy-path implementation trials exist.
- Harmony and Temper provide real-project evidence outside the Factory starter kit.
- The owner waiver for the non-author user trial requirement is recorded at `docs/Factory/v3/trials/PHASE1_REQUIREMENT_WAIVER_20260524.md`.

Promotion gate:

Approve a `V3-OP-001` refinement release only if real-project evidence shows the profile is understandable, bounded, and does not cause V2 deprecation confusion.

Decision:

`START_PHASE_2` for shadow mission-record design only. Evidence is recorded at `docs/Factory/v3/PHASE1_DECISION_REVIEW_V3_OP_001.md`.

## Phase 2 - Structured Mission Record

Status: In progress. v0 shadow template and trial-derived fixtures exist.

Goal:

Move from prose-only mission evidence to a machine-readable governance record.

Primary artifact:

```text
docs/Factory/v3/templates/V3_MISSION_RECORD_TEMPLATE.json
```

The record should capture:

- mission id,
- profile id,
- objective,
- authority lease,
- forbidden scope,
- allowed commands,
- dependency policy,
- verification requirements,
- halt rules,
- fallback triggers,
- command evidence,
- file-touch summary,
- human decisions,
- closeout status,
- residual risks.

Work:

1. Design the JSON schema as a shadow artifact. Status: v0 template exists at `docs/Factory/v3/templates/V3_MISSION_RECORD_TEMPLATE.json`.
2. Backfill the schema against existing V3 pilot evidence where practical. Status: first five Phase 1 trials are backfilled under `tests/fixtures/factory_v3_mission_record/`.
3. Add fixture coverage for valid records, missing authority, verification-halt outcomes, stale reentry, and V2 fallback. Status: pre-envelope fallback and happy-path fixtures exist; verification-halt, stale reentry, and malformed-record fixtures remain future work.
4. Add an advisory validator that reads the record and emits structured findings.
5. Keep the authored Markdown envelope and closeout as the human-readable source until the schema has enough evidence.

Required evidence:

- valid and invalid golden fixtures,
- at least 3 real or historical mission records,
- advisory validator output,
- no conflict with Mission Mode's existing `MISSION_MANIFEST.md` source-of-truth rule.

Promotion gate:

Approve structured mission records for optional use only after they improve replayability without creating a second conflicting mission-state source.

## Phase 3 - Telemetry And Evidence Replay

Goal:

Make execution events observable enough to evaluate governance quality.

Work:

1. Define append-only telemetry events for command runs, file changes, verification, halt, reentry, fallback, human approval, and closeout.
2. Add a lightweight telemetry log format that can be emitted by Codex today and adapted for other harnesses later.
3. Add replay checks that reconstruct mission status from the mission record plus telemetry log.
4. Measure overhead against normal V2 and `V3-OP-001` use.

Required evidence:

- telemetry fixture corpus,
- replay pass/fail fixtures,
- at least 3 real mission telemetry logs,
- overhead report,
- data-minimization review confirming no chain-of-thought or vendor-private cognition state is stored.

Promotion gate:

Telemetry becomes recommended only when it provides better replay and diagnosis without adding disproportionate user burden.

## Phase 4 - Eval Expansion And Capability Profiling

Goal:

Judge when a harness is capable enough for reduced V2 decomposition.

Work:

1. Expand evals from document drift to execution reliability.
2. Add profiles for Codex, Claude Code, Cursor, and future harnesses.
3. Measure completion quality, verification execution, recovery after failed checks, interruption handling, scope discipline, and evidence quality.
4. Maintain seeded negative fixtures for scope expansion, weak authority, failed verification continuation, stale reentry, brittle abstractions, missing evidence, and V2 deprecation language.

Required evidence:

- harness capability report template,
- golden fixture expansion,
- real-run result corpus,
- false-positive and false-negative rollup,
- thresholds for autonomous, light, standard, and heavy governance routing.

Promotion gate:

No governance reduction is allowed until capability thresholds are evidence-backed for the relevant harness and mission profile.

## Phase 5 - Governance Router

Goal:

Route work to the right governance level based on risk, authority, verification, and harness capability.

Modes:

- `AUTONOMOUS`: low-risk, high-confidence, strongly bounded, fully verified.
- `LIGHT`: docs, fixtures, examples, small UI polish, low blast radius.
- `STANDARD`: bounded code changes with known verification.
- `HEAVY`: core policy, auth, payment, compliance, runtime-kernel, evidence, temporal, or infrastructure work.
- `V2_FALLBACK`: ambiguous, high-risk, weak evidence, missing authority, or human-requested fallback.

Work:

1. Define routing criteria.
2. Add routing fixtures.
3. Run the router in advisory mode against historical and real work.
4. Compare router recommendations against human decisions.
5. Tune only from classified evidence.

Required evidence:

- routing matrix,
- fixture corpus,
- human-classified real-run comparisons,
- disagreement rollup,
- fallback-safety review.

Promotion gate:

The router may become recommended only when it is conservative on high-risk work and does not push unsuitable work into V3.

## Phase 6 - Partial Enforcement

Goal:

Convert the safest authority and verification rules into enforceable checks.

Preferred enforcement order:

1. file-touch budgets,
2. forbidden path checks,
3. dependency-change detection,
4. required verification command presence,
5. halt-on-failure closeout validation,
6. stale reentry detection,
7. telemetry completeness.

Work:

1. Add validators before runtime services.
2. Keep enforcement local and repo-portable.
3. Avoid speculative registries or plugin frameworks.
4. Preserve project adapters for repo-specific commands and protected paths.

Required evidence:

- validator fixtures,
- real-run smoke reports,
- false-positive and false-negative classification,
- rollback path to advisory-only behavior.

Promotion gate:

Required-gate integration needs a separate Factory run and explicit human approval.

## Phase 7 - Persistent Mission Runtime

Goal:

Introduce persistent mission-state behavior only after structured records, telemetry, evals, routing, and partial enforcement prove useful.

Possible artifacts:

- `V3_MISSION_RECORD.json`
- `V3_AUTHORITY_LEASE.json`
- `V3_TELEMETRY.jsonl`
- `V3_VERIFICATION_STATE.json`
- `V3_ESCALATION_LOG.json`

Work:

1. Decide which state is authored versus derived.
2. Preserve the existing Mission Mode source-of-truth rule.
3. Define pause, resume, revocation, renewal, and completion semantics.
4. Add migration guidance for repos using only V2.
5. Add adapter guidance for repos with a private or project-specific governance kernel.

Required evidence:

- runtime-state schema,
- conflict tests against Mission Mode,
- pause/resume pilots,
- halt/reentry pilots,
- external-kernel boundary review,
- ordinary-repo adoption review.

Promotion gate:

Persistent state can become operational only if it improves continuity without creating a second source of truth or requiring a separate governance kernel.

## Phase 8 - Default-Mode Decision

Goal:

Decide whether Factory v3 can become the default for specific mission classes while V2 remains available.

Decision inputs:

- approved profile inventory,
- real-project trial evidence,
- mission record adoption evidence,
- telemetry and replay evidence,
- eval and capability profile evidence,
- governance router performance,
- validator false-positive and false-negative rollups,
- V2 fallback usage and reasons,
- user guide maturity,
- external-kernel boundary confirmation.

Possible decisions:

- `NO-GO`: keep V3 optional only.
- `LIMITED DEFAULT`: make V3 default for named low-risk profiles only.
- `STANDARD DEFAULT`: make V3 default for named ordinary coding profiles with V2 fallback.
- `RESEARCH CONTINUE`: defer decision and collect named missing evidence.

Hard no-go conditions:

- V2 fallback is unclear,
- users think V2 is deprecated,
- V3 cannot explain preserved V2 guarantees,
- mission state conflicts with existing Mission Mode,
- V3 claims production runtime authority or proof without an external kernel or project-owned verifier,
- failed verification can continue without explicit human override,
- capability evidence is harness-specific but presented as universal.

## High-Level Checklist

Before any decision to operationalize V3 beyond `V3-OP-001`, confirm:

- [ ] real-project trial evidence exists,
- [ ] structured mission record exists and has fixtures,
- [ ] telemetry/replay format exists and has pilots,
- [ ] evals cover both positive and negative cases,
- [ ] capability profiles exist for the target harness,
- [ ] governance router has human-classified evidence,
- [ ] enforceable validators exist for basic authority and verification rules,
- [ ] V2 fallback remains explicit,
- [ ] external-kernel boundary remains intact,
- [ ] human approval names the exact profile and release level.

## Recommended Next Move
Start Phase 1.

Run real-project `V3-OP-001` trials using the current `USER_GUIDE.md`, then use the evidence to design Phase 2's structured mission record. Do not design the full persistent runtime first; the record format should emerge from observed operational evidence.
