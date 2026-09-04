# Intent Synthesis — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Blue synthesis resolving all nine Red findings without scope expansion.

## Resolutions

- RT-01 (Critical, resolved): intent v2 defines **live drivers** as the repository's existing dedicated commands — `scripts/verify_factory_bmad_claude_composition.sh`, `scripts/verify_factory_bmad_live_pilot.sh`, and `scripts/verify_factory_bmad_live_preflight.py` — digest-pinned at activation. Live proof claims are valid only when produced through a pinned driver; simulated substitutes halt the run.
- RT-02 (Critical, resolved): intent v2 requires the disposable root to be a fresh, empty, non-symlinked directory outside every protected root, verified before seeding, with symlinks from the disposable repository into protected paths forbidden and checked.
- RT-03 (Critical, resolved): intent v2 sequences promotion-evidence export (digest-pinned copies to the external evidence root) strictly before teardown; teardown of unexported promotion evidence halts.
- RT-04 (High, resolved): intent v2 pins BMAD acquisition to a pre-existing, digest-pinned local BMAD 6.10.0 tree named at activation; execution-time network fetches are forbidden.
- RT-05 (High, resolved): intent v2 names the two live hook paths: the packaged PreToolUse hook and the CLI hook entrypoint, each exercised by a pinned driver.
- RT-06 (High, resolved): intent v2 applies the bounded-evidence rule to live output: complete logs go only to the external evidence root, the harness receives bounded digests and verdicts, and live output is scanned for secrets before retention.
- RT-07 (Medium, resolved): intent v2 states the human reviews the concrete snapshot during the activation window; absence of that review is a halt, never default approval.
- RT-08 (Medium, resolved): intent v2 extends the no-touch inventory to harness plugin caches and worktree/registration state, matching the residue claim to what is actually proven.
- RT-09 (Medium, resolved): intent v2 adds the partial-success rule: any missing or failed proof yields `NO_GO` (or `BLOCKED` when a proof could not run); no qualified-with-exceptions status exists.

## Scope Expansion Review
- None of the resolutions adds scope; each binds an existing claim to a checkable mechanism. No `[SCOPE EXPANSION]` items exist.

## Inferred Requirements Review
- No `[INFERRED]` requirement remains; every v2 addition traces to a Red finding against the approved brief.

## Residual Disagreements
- None. Red's blocking findings RT-01 through RT-03 are fully absorbed; no accepted-risk waiver was needed.
