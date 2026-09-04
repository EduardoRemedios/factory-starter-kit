# Intent Red Team — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): First Red iteration attacking containment, drivers, teardown, promotion, and evidence assumptions.

## Method
Attack the v1 intent as a hostile executor looking for authority leaks, containment escapes, unprovable claims, and evidence gaps. Each finding names severity and the weakest sentence it exploits.

## Findings

### RT-01 (Critical) — Undefined live driver makes "live proof" unfalsifiable
The intent demands proof "through the candidate's installed hook paths" but never names the mechanism that drives a live harness session. An executor could substitute scripted simulations and truthfully claim the commands ran. The repository already owns dedicated live verification commands (`scripts/verify_factory_bmad_claude_composition.sh`, `scripts/verify_factory_bmad_live_pilot.sh`, `scripts/verify_factory_bmad_live_preflight.py`); the contract must bind live proofs to named, digest-pinned drivers or the claim is theater.

### RT-02 (Critical) — Disposable-repository containment is asserted, not specified
"Created outside this worktree at an activation-pinned path" permits a disposable root inside a donor, under a symlink, or overlapping an existing registration. The contract must require a fresh, empty, non-symlinked directory outside every protected root, verified before seeding, and must forbid symlinks from the disposable repository back into protected paths.

### RT-03 (Critical) — Teardown can destroy the only promotion evidence
AC-04 creates the promoted snapshot inside the disposable repository and AC-06 destroys that repository. Unless promotion evidence is copied out with digests before teardown, success destroys its own proof. Sequence and retention must be explicit.

### RT-04 (High) — BMAD 6.10.0 acquisition is unpinned
The intent pins "capability digests" but not where the live BMAD 6.10.0 installation comes from. A network fetch at execution time would introduce unpinned bytes into the proof. The source must be a pre-existing, digest-pinned local BMAD 6.10.0 tree named at activation.

### RT-05 (High) — "Both hook paths" is inherited jargon without a live definition
Deterministic tests define the two hook paths precisely; the intent does not say what they mean live. Name them: the packaged PreToolUse hook and the CLI hook entrypoint, each exercised by the named drivers.

### RT-06 (High) — Live workflow output can blow the evidence budget and leak content
Real authoring workflows can emit large or sensitive text. Without an explicit bounded-evidence rule for live output (full logs external, bounded digests inline, no secrets), the run can violate the harness evidence boundary that AGENTS.md mandates.

### RT-07 (Medium) — Human promotion review timing is ambiguous
"Human-reviewed promotion inside the activation" could be read as pre-delegated consent. The contract must state the human reviews the concrete candidate snapshot during the activation window, and that a missing review is a halt, not a default-approve.

### RT-08 (Medium) — Residue proof is narrower than the claim
AC-06 proves protected paths byte-identical but the teardown claim ("no residue") also covers harness state, caches, and registrations. The no-touch inventory must explicitly include harness plugin caches and worktree/registration state, or the claim must be narrowed.

### RT-09 (Medium) — Status ceiling lacks a partial-success rule
If authoring proofs pass but promotion is declined by the human, the run has neither full success nor failure. Define the outcome: any missing proof yields `NO_GO` or `BLOCKED`, never a qualified-with-exceptions status.

## Attack Summary
- Authority boundaries and non-goals are strong; no finding grants BMAD authority.
- The exploitable surface is operational: drivers, containment, sequencing, acquisition, and evidence bounds.
- No scope expansion is proposed; every finding hardens the existing goal.

## Verdict
- Verdict: REVISE
- Blocking findings: RT-01, RT-02, RT-03 must be resolved before lock; RT-04 through RT-09 must be resolved or explicitly accepted by Blue with rationale.
