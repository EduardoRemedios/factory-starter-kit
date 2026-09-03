# Execution Prompt — MS-02 Corrective Gate Only

## Version

v1

## Change Log

- v1 (2026-09-02): Activated the approved one-line MS-02 corrective boundary.

## Run Metadata

- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Created: `2026-09-02 09:27 WEST`
- Source Pack: `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/`
- Human Go: RECORDED

## Purpose

Correct one stale test expectation in the preserved MS-02 candidate, run exactly the repaired 53-test authored gate, prove all no-touch boundaries, and close back to planning mode before MS-03.

## Skill Routing Contract

- Use the `factory-run` skill for the bounded corrective action.
- Use the `factory-execution-closeout` skill for diff, verification, evidence, and control-lifecycle checks.

## Authorized Path and Change

- Modify only `tests/test_factory_bmad_activation.py`.
- Replace expected `review_or_migrate_bmad_layout_with_human_approval` with `review_zero_write_remediation_preview`.
- Maximum implementation delta during this activation: one modified file, zero created files, zero deleted files.

## Execution Sequence

1. Revalidate all activation pins, the six preserved candidate hashes, generated aggregate, donors, protected paths, registrations, and the safe empty evidence root.
2. Capture preimages and confirm the run contains no live mutation beyond the previously preserved six-file MS-02 candidate and authorized controls.
3. Apply only the one-line expected-value correction.
4. Verify the five other candidate files remain byte-identical and no implementation path was created or deleted.
5. Run Gate A and Gate B exactly as written in `pack/verification_plan.md`; require 6 plus 47 equals exactly 53 PASS.
6. Revalidate every no-touch surface and pack pin, record PASS or FAIL evidence within 40 files and 10 MiB, archive controls byte-identically, and restore `PLANNING_ONLY`.
7. Run final `pack-lint` and stop for human evidence review before MS-03.

## Hard Guardrails

- Preserve Factory/Conductor and explicit human approval as the sole implementation authority.
- Do not change runtime policy, capabilities/enforcement/support tests, fixtures, generated packages, dependencies, Factory Core, donors, protected paths, registrations, documentation, pack artifacts, AuditEdge, or any other implementation path.
- Do not invoke the builder, BMAD, MS-03, Git mutation, publication, pilot, rollout, MS-06, AuditEdge, or downstream fan-out.
- Stop on the first pin, write-set, test-count, test-result, no-touch, residue, evidence-budget, or lifecycle mismatch; preserve evidence and do not attempt another repair.

## Exit Checklist

- [ ] Exactly one implementation file modified during this activation; zero created and zero deleted.
- [ ] Gate A reports 6 PASS and Gate B reports 47 PASS, totaling exactly 53 PASS.
- [ ] The other five candidate files and every generated/protected/unlisted surface remain unchanged.
- [ ] Controls archived byte-identically, live controls absent, and `PLANNING_ONLY` restored.
- [ ] Final `pack-lint` PASS with zero warnings.
- [ ] Stopped before MS-03.
