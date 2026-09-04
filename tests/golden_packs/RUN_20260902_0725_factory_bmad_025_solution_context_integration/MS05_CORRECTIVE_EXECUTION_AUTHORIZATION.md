# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-03): Recorded digest-bound MS-05 corrective activation after the NO_GO qualification attempt.

## Authorization

- Human Go: RECORDED
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `d1b411ed8c3b980190833618450f5836dbfd844378e2aed53d42688afad4e987`
- Authorized Pack Audit SHA-256: `9cd093288f447f03bb6ea2403948dca9041540ae9e4579b44f9fd7d5c1b047c3`

## Human Decision Reference

- Explicit human Go recorded 2026-09-03 in the operator session, approving the corrective path presented after the NO_GO closeout: one stale test expectation reconciled, full qualification re-run, closeout superseded, control ceiling expanded from 13 to 15 persistent files.

## Additional Pins

- Base HEAD: `70dc4e4a31caebe28983dc7581afef5672e1ef7b` on `codex/factory-bmad-0.2.5-solution-context`
- `pack/verification_manifest.yaml`: `88deca23d0c433f037393a5ffd9ed6d9449d82b2bbf9882e1ad48e90196269c4`
- `scripts/factory_execution_closeout.py`: `e443fbb75dd1aed3752611e1602339594f72070d87cd082c149f21cd48d86160`
- `scripts/factory_pack_lint.py`: `db6614f92f1b0bd338e9cdf1f7302084218dad885f28d4483b7ea7691d7d6a86`

## Authority Boundary

- Exactly one implementation write is authorized: `tests/test_factory_bmad_bootstrap.py`, reconciling `test_partial_state_blocks` to the locked contract (public `FACTORY_BMAD_NON_CANONICAL_LAYOUT` with subordinate `layout_reason_code` `FACTORY_BMAD_PARTIAL_STATE`). No other implementation, source, generated, documentation, fixture, or pack change.
- Further permitted writes, exhaustively: the two live controls, `EXECUTION_MODE.txt` transitions, the 16 bounded evidence files under `artifacts/verification/RUN_20260902_0725_factory_bmad_025_solution_context_integration/` (refreshed for this activation after the first attempt's set is archived externally), and `EXECUTION_CLOSEOUT.json`.
- Closeout supersession: the recorded NO_GO `EXECUTION_CLOSEOUT.json` is archived byte-exactly with its digest into the external MS-05 evidence root and then removed from the run root, after which the final closeout is recorded only through the canonical validator while `EXECUTION_ENABLED` with live controls.
- Accounting decision: the persistent run-root control ceiling is expanded, not silently, from 13 to 15 files - seven archived authorization-plus-prompt pairs (MS01, MS02, MS02-corrective, MS03, MS04, MS05, MS05-corrective) plus `EXECUTION_CLOSEOUT.json`.
- External evidence: at most 30 files total in the pinned external MS-05 evidence root.
- No MS-06, BMAD invocation, AuditEdge, commit, merge, push, publication, pilot, release, or rollout authority.
- After closeout recording: restore `PLANNING_ONLY`, archive this pair as `MS05_CORRECTIVE_EXECUTION_AUTHORIZATION.md` and `MS05_CORRECTIVE_EXECUTION_PROMPT.md`, and stop for human evidence review.
