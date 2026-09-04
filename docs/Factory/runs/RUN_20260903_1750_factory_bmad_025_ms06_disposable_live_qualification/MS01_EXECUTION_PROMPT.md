# Execution Prompt - MS-01 Disposable Live Qualification

## Version

v1

## Change Log

- v1 (2026-09-03): Instantiated for the digest-bound MS-01 activation.

## Run Metadata

- RUN_ID: `RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification`
- Sprint ID: `SPRINT_20260903_001`
- Created: 2026-09-03 19:27 WEST
- Source Pack: `docs/Factory/runs/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/pack/`
- Human Go: RECORDED

## Purpose

Run MS-01 only: revalidate all activation pins, run the containment preflight with the generated protected-preimage manifests, provision a contained disposable root, seed one Factory-only disposable repository from the qualified candidate's packaged Factory payload, record bounded evidence for VM-001 and VM-002, restore `PLANNING_ONLY`, and stop for human review.

## Hard Guardrails

- Stop on any pin mismatch, missing preimage, root overlap, symlinked root, non-empty disposable root, preflight failure, protected-root postimage mismatch, or authority ambiguity.
- Do not invoke BMAD, run MS-02/MS-03 drivers, access AuditEdge, change the candidate, mutate donors/protected roots, commit, merge, push, publish, pilot, release, or roll out.
- Keep `greenfield` absent after MS-01 so the later MS-02 composition driver can still create and verify it under a separate authorization.

## Micro-sprint Execution Sequence

1. Transition `EXECUTION_MODE.txt` from `PLANNING_ONLY` to `EXECUTION_ENABLED`.
2. VM-001: revalidate candidate commit, pack digests, driver digests, contract fixtures, plugin package digests, local BMAD tree digest, Claude binary path/version, and protected-preimage manifest hashes.
3. VM-002: run `./scripts/factory-python scripts/verify_factory_bmad_live_preflight.py` with the activation-pinned roots and seven `--protected-preimage role=path` arguments.
4. Provision: seed `brownfield-neither` as a Factory-only disposable repository from the candidate's packaged Factory payload. Leave BMAD absent.
5. Confirm protected roots remain preimage-equal using aggregate digest comparison against `PREIMAGE_DIGEST_REPORT.json`.
6. Record `MS01_SUMMARY.txt`, restore `EXECUTION_MODE.txt` to `PLANNING_ONLY`, and stop.

## Verification Contract

- VM-001 evidence path: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/VM-001.txt`
- VM-002 evidence path: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/VM-002.txt`
- Summary evidence path: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS01_SUMMARY.txt`

## Final Exit Checklist

- [ ] VM-001 PASS.
- [ ] VM-002 PASS.
- [ ] Factory-only disposable repository exists at the activation-pinned `brownfield-neither` root.
- [ ] `greenfield` remains absent for the later MS-02 composition driver.
- [ ] Protected roots compare equal to pinned preimages.
- [ ] `EXECUTION_MODE.txt` restored to `PLANNING_ONLY`.
- [ ] Stop before MS-02.
