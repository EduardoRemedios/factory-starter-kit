# Micro-sprints

## Version
v1

## Change Log
- v1 (2026-05-18): Initial micro-sprint sequence for Factory v3 research planning.

## MS-01 - Research Namespace
- Objective: Add a lightweight v3 research namespace without changing v2 behavior.
- Inputs: This pack, `docs/Factory/AEGIS_BOUNDARY.md`, `README.md`.
- Outputs:
  - `docs/Factory/v3/README.md`
  - `docs/Factory/v3/STRATEGY.md`
  - `docs/Factory/v3/NON_GOALS_AND_BOUNDARIES.md`
- Entry criteria: This planning pack passes I2 and human review authorizes doc edits.
- Exit criteria: Each new doc says research/design only and no v2 validator or stage contract changes are made.
- Stop or go gate: Stop if any draft says v3 replaces v2.

## MS-02 - Concept Candidates
- Objective: Capture candidate v3 concepts without enforcing schemas.
- Inputs: MS-01 docs and AEGIS boundary.
- Outputs:
  - `docs/Factory/v3/CONCEPT_CANDIDATES.md`
  - `docs/Factory/v3/SHADOW_SCHEMA_CANDIDATES.md`
- Entry criteria: MS-01 docs merged or available in the same approved branch.
- Exit criteria: Candidate concepts are marked non-enforcing and out of `docs/Factory/Spec/`.
- Stop or go gate: Stop if candidates duplicate kernel-owned authority, evidence, or runtime policy.

## MS-03 - Advisory Validator Plan
- Objective: Define optional v3 validation before implementing any check.
- Inputs: `verification_plan.md` and `traceability_matrix.md`.
- Outputs:
  - `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`
  - candidate command name such as `factoryctl v3-advisory-lint`
- Entry criteria: MS-02 concepts exist.
- Exit criteria: The validator is explicitly non-blocking and not wired into v2 required gates.
- Stop or go gate: Stop if a required v2 validator would fail due to missing v3 research files.

## MS-04 - Evals And Pilot Profile
- Objective: Define stress tests for v3 ideas against real or historical Factory runs.
- Inputs: advisory validator plan and promotion fixture.
- Outputs:
  - `docs/Factory/v3/PILOT_PROFILE_PLAN.md`
  - `docs/Factory/v3/PROMOTION_CRITERIA.md`
- Entry criteria: MS-03 plan is reviewed.
- Exit criteria: Eval fields include false positives, false negatives, drift caught, overhead, boundary violations, and user clarity.
- Stop or go gate: Stop if promotion can occur without eval evidence and human release approval.

## MS-05 - README Split Language
- Objective: Make public posture clear to starter-kit adopters.
- Inputs: MS-01 through MS-04 docs.
- Outputs:
  - README edits saying v2 is current and v3 is research/design only.
- Entry criteria: Research docs are present.
- Exit criteria: README keeps Quick Start and Process Layers grounded in v2.
- Stop or go gate: Stop if README implies AEGIS is required.

## MS-06 - Future Runtime Integration Adapter
- Objective: Defer runtime integration until v3 promotion evidence exists.
- Inputs: pilot evidence and explicit release approval.
- Outputs:
  - project-adapter mapping guidance, not Factory Core runtime behavior.
- Entry criteria: Promotion criteria pass.
- Exit criteria: Any kernel integration remains adapter-based and optional.
- Stop or go gate: Stop if Factory claims runtime proof without a lower-level kernel verifier.

