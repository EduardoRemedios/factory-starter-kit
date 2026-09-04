# Execution Prompt — MS-04 Only

## Version

v1

## Change Log

- v1 (2026-09-03): Activated the approved one-builder MS-04 boundary.

## Run Metadata

- RUN_ID: `RUN_20260902_0725_factory_bmad_025_solution_context_integration`
- Sprint ID: `SPRINT_20260902_001`
- Created: `2026-09-03 14:15 WEST`
- Source Pack:
  `docs/Factory/runs/RUN_20260902_0725_factory_bmad_025_solution_context_integration/pack/`
- Human Go: RECORDED

## Purpose

Regenerate the Codex and Claude Factory-BMAD packages exactly once from the
accepted authored 0.2.5 source, prove the exact 18-modified generated topology
and required package behavior, preserve every non-generated surface, and close
back to planning mode before MS-05.

## Execution Sequence

1. Revalidate every authorization pin, accepted protected-main delta,
   repository/ref, generated preimage, donor, protected path, registration,
   evidence-root, and control-budget condition.
2. Capture complete activation preimages, including the accepted current
   45,473-record protected-main snapshot.
3. Invoke `./scripts/factory-python scripts/build_factory_bmad_plugins.py`
   exactly once.
4. Verify exactly nine modified generated files under each authorized package
   root, with no created or deleted files and no manual generated edit.
5. Run the exact post-builder MS-04 gate from `pack/verification_plan.md`.
6. Revalidate every no-touch surface and record bounded evidence.
7. Archive controls byte-identically as `MS04_*`, remove live controls, restore
   `PLANNING_ONLY`, run `pack-lint`, and stop before MS-05.

## Hard Guardrails

- SIMPLE-CODE-GATE v2 applies.
- Only generated files under `plugins/factory-bmad` and
  `plugins/factory-bmad-claude` may change, and only through the authorized
  builder invocation.
- Preserve authored source, fixtures, documentation, the pack, Factory Core,
  dependencies, donors, pilot roots, protected paths, registrations,
  Git/configuration, the canonical starter-kit protected-main activation
  snapshot, and every unlisted path.
- Do not invoke BMAD, run MS-05, access AuditEdge, mutate Git, publish, pilot,
  roll out, or fan out downstream work.
- Stop on the first mismatch and preserve failure evidence without silently
  repairing or expanding authority.

## Exit Checklist

- [ ] Builder invoked exactly once.
- [ ] Exactly 18 generated files modified; zero created or deleted.
- [ ] Exact generated-package gate passes.
- [ ] All no-touch surfaces match activation preimages.
- [ ] External evidence remains within 30 files and 10 MiB.
- [ ] Controls archived byte-identically and live controls removed.
- [ ] `PLANNING_ONLY` restored and final `pack-lint` passes.
- [ ] Stopped before MS-05.
