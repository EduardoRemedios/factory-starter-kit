# Factory BMAD 0.2.3 Evidence Index

Last updated: 2026-08-15

## Purpose

This index classifies the retained Factory-BMAD 0.2.3 recovery evidence after
live qualification. It does not replace the artifacts; it explains which files
are canonical, which are supporting diagnostics, and which bulky files should
move to external archive storage in future runs.

## Policy Decision

Keep the current pushed evidence intact. Do not rewrite history or delete the
recovery artifacts immediately after qualification.

For future runs, commit canonical verdict files, run metadata, manifests, and
artifact digests. Store full protected-root inventories and large pre/post image
JSON files outside ordinary source history unless the sponsor explicitly asks
for full in-git preservation.

## Canonical Evidence

These files are sufficient to prove the 0.2.3 live-recovery verdict:

| Artifact | Classification | SHA-256 |
| --- | --- | --- |
| `artifacts/verification/factory_bmad_023_recovery/VM-008.json` | canonical | `290b09b3c8240e440708f59516419859f891557380ce2fe82851d5591b4986c2` |
| `artifacts/verification/factory_bmad_023_recovery/VM-012.json` | canonical | `743299b49bb20dc2d8ac82f557fa8abf0137e6577fa5ed37c9ec7ae147015b97` |
| `artifacts/verification/factory_bmad_023_recovery/VM-013.json` | canonical | `229a763d8a4f16c3527d7086a5d716c15cf30864b5c7ad6aff7534f3594aecac` |
| `docs/Factory/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/RUN_INTEGRITY_REPAIR.md` | canonical | `f5930ede92e7445c5156cdc038e078fe53decea051a477cc2b61926ad3b7c7e6` |
| `docs/Factory/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/pack/verification_manifest.yaml` | canonical | manifest-owned |
| `docs/Factory/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/pack/fixtures/source_coupling.json` | canonical | source-boundary fixture |
| `docs/Factory/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/pack/fixtures/live_verifier_contract.json` | canonical | live-verifier contract |

## Supporting Evidence

Retain these while the recovery remains under review:

- `artifacts/verification/factory_bmad_023_recovery/VM-001.txt` through
  `VM-015.txt` or `.json`
- `artifacts/verification/factory_bmad_023_recovery/VM-013-*.json`
- `artifacts/verification/factory_bmad_023_recovery/VM-012-*.json`
- `artifacts/verification/factory_bmad_023_recovery/MS-*.json`
- `artifacts/verification/factory_bmad_023_recovery/MS-*.txt`
- `docs/Factory/runs/RUN_20260814_0932_factory_bmad_022_repair/`
- `docs/Factory/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/`

## Bulky Retained Evidence

The recovery evidence root is approximately 46 MB. The largest files are full
protected-root pre/post inventories, especially:

- `artifacts/verification/factory_bmad_023_recovery/live_preimages/**/normal_claude_runtime.json`
- `artifacts/verification/factory_bmad_023_recovery/live_preimages/**/unrelated_state.json`
- `artifacts/verification/factory_bmad_023_recovery/live_postimages/**/normal_claude_runtime.json`
- `artifacts/verification/factory_bmad_023_recovery/live_postimages/**/unrelated_state.json`
- `artifacts/verification/factory_bmad_023_recovery/preimages/normal-claude-dir.json`

These files are valid audit evidence for this recovery. For future releases,
prefer committing a digest summary plus the exact comparison result and storing
the complete inventories in an external evidence archive.

## External Archive Candidates

If this branch later becomes long-lived source history, archive the following
outside git after recording their digests and archive location:

- full `live_preimages/`
- full `live_preimages_after_claude_update/`
- full `live_postimages/`
- full `live_postimages_after_final_live/`
- full `preimages/`

Do not remove these from this branch until the release reviewer explicitly
accepts the archive location and verifies digest parity.
