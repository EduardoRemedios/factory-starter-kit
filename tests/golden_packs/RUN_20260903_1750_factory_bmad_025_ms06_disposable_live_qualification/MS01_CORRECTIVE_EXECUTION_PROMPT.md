# Execution Prompt - Corrected MS-01 Disposable Live Qualification

## Version

v1

## Change Log

- v1 (2026-09-03): Instantiated for the corrected digest-bound MS-01 retry.

## Run Metadata

- RUN_ID: `RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification`
- Sprint ID: `SPRINT_20260903_001`
- Created: 2026-09-03 19:57 WEST
- Source Pack: `docs/Factory/runs/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/pack/`
- Human Go: RECORDED

## Purpose

Run the corrected MS-01 retry only: use the fresh protected preimages with `unrelated_state` rooted at `/Users/eduardodosremedios/factory-starter-kit/docs`, rerun VM-001 and VM-002, provision one Factory-only disposable repository, prove protected roots remain byte-identical, restore `PLANNING_ONLY`, and stop before MS-02.

## Hard Guardrails

- Stop on any pin mismatch, missing preimage, root overlap, symlinked root, non-empty corrected disposable root, preflight failure, protected-root postimage mismatch, or authority ambiguity.
- Do not invoke BMAD, run MS-02/MS-03 drivers, access AuditEdge, change the candidate, mutate donors/protected roots, commit, merge, push, publish, pilot, release, or roll out.
- Keep the prior blocked MS-01 root and evidence intact.

## Micro-sprint Execution Sequence

1. Transition `EXECUTION_MODE.txt` from `PLANNING_ONLY` to `EXECUTION_ENABLED`.
2. VM-001 corrective: revalidate candidate commit, pack digests, driver digests, contract fixtures, Claude binary/version, and corrected preimage manifest hashes.
3. VM-002 corrective: run `./scripts/factory-python scripts/verify_factory_bmad_live_preflight.py` with the corrected activation roots and seven corrected `--protected-preimage role=path` arguments.
4. Provision: seed `brownfield-neither` as a Factory-only disposable repository from the candidate's packaged Factory payload. Leave BMAD absent.
5. Confirm protected roots remain preimage-equal against the corrected `PREIMAGE_DIGEST_REPORT.json`.
6. Record `MS01_CORRECTIVE_SUMMARY.txt`, restore `EXECUTION_MODE.txt` to `PLANNING_ONLY`, and stop.

## Evidence Paths

- VM-001 corrective: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/VM-001-corrective1.txt`
- VM-002 corrective: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/VM-002-corrective1.txt`
- Protected postimage corrective: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/protected_postimage_compare_ms01_corrective1.json`
- Summary: `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS01_CORRECTIVE_SUMMARY.txt`

## Final Exit Checklist

- [ ] VM-001 corrective PASS.
- [ ] VM-002 corrective PASS.
- [ ] Factory-only disposable repository exists at the corrected `brownfield-neither` root.
- [ ] Protected roots compare equal to corrected preimages.
- [ ] `EXECUTION_MODE.txt` restored to `PLANNING_ONLY`.
- [ ] Stop before MS-02.
