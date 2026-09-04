# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-03): Recorded digest-bound MS-01 activation using externally generated protected-preimage manifests.

## Authorization

- Human Go: RECORDED
- Human authorization text: "Authorize MS-01 only, using the generated protected-preimage manifests as pinned inputs."
- Prior Execution Mode: `PLANNING_ONLY`
- Activated Execution Mode: `EXECUTION_ENABLED`
- Authorized Pack Manifest SHA-256: `6c0e9c34287630b966f2558baaa85ac1c8f102ce8a16d5334ba389e4914c953d`
- Authorized Pack Audit SHA-256: `48f4c683c0e8f828810a191dc23b47ae0e0369d967b04034af2695acce591604`
- Authorized Verification Manifest SHA-256: `a64bff70a66c85199287774e4afb8be8fc8e5f2692e3fc183766a4b9532c2966`

## Candidate and Driver Pins

- Candidate root: `/Users/eduardodosremedios/factory-bmad-0.2.5-solution-context`
- Candidate commit: `c23be98034215c17c9c49a7e9b6302cb2ad1f18d`
- Claude binary: `/Users/eduardodosremedios/.local/bin/claude`
- Claude observed version: `2.1.259`
- Claude supported version prefix: `2.1.`
- Permission mode: `dontAsk`
- Permission rule: `Bash(python3 *)`
- `scripts/verify_factory_bmad_live_preflight.py`: `bd10994c1dbe597de10befc34a9aaadcadf6e3539741e6d973e63cbe7e99da16`
- `scripts/verify_factory_bmad_claude_composition.sh`: `6c3d23ecf94ccc5dced0ebb2495e2e0385da63632363514ca1285f354653d82d`
- `scripts/verify_factory_bmad_live_pilot.sh`: `a4b65bf09035e59af673d035a595696b681d7a8e0e56c8ed8681fd9fd70e0ce6`
- `tests/plugin_fixtures/factory_bmad_live_verifier_contract.json`: `b5998ab5c1822de4d2ee867a9bcbdfaada2beb34bb396cfff82d98e811042168`
- `tests/plugin_fixtures/factory_bmad_025_source_coupling.json`: `17f7a7d1752ad5ab6dde3b11e1916a76f8d3fe2c658407333926d744c8f5d7cb`
- `pack/fixtures/live/qualification_contract/input.json`: `6af648ecef2ecd4e0429851b22b6e023810139df58420684d49b1494c6d92b65`
- `pack/fixtures/live/qualification_contract/expected.json`: `34623d8453186f6ea3aba12906c175d85bc6902d282b3673f259bb6ad88eacc3`

## Package and BMAD Pins

- `plugins/factory`: entries `128`, aggregate SHA-256 `a71d277e06a0151ecea348036afba5daa5524b937907a16e8b4e61b3ecce629c`
- `plugins/factory-bmad`: entries `36`, aggregate SHA-256 `5bf13da10ab38ca9bfb0e1aabc13298a1ecd2cc868654b09f8922e2674b91014`
- `plugins/factory-claude`: entries `128`, aggregate SHA-256 `ef19171372459798634f6ac39dc54da48048cc659c21fa9fa98fd4125110ae9c`
- `plugins/factory-bmad-claude`: entries `28`, aggregate SHA-256 `d7ab2358b9903c0867907cb0e9c1b50349d88206c3136dbe79c9d51d75781bed`
- `plugin-src/factory`: entries `19`, aggregate SHA-256 `9ddf835719ef25d79e3999b376b710c302a7a5d5e311be256a6d6f48573fa719`
- `plugin-src/factory-bmad`: entries `34`, aggregate SHA-256 `2f3b7fed818514067c5bff9d1a7fcffc8aca6c4855326e0504afae29d872eeb5`
- Local BMAD tree: `/Users/eduardodosremedios/odyssey_v2/_bmad`
- Local BMAD tree entries: `22`
- Local BMAD tree aggregate SHA-256: `08feedeadc4ef9c404752834c12b03af0b503aff8aec2de92f88e68ab2df02f0`
- Local BMAD manifest SHA-256: `b7f00c838b1f1470cdcccd0a808e1c4d8b69a134fff2e676dcfbc3df63de54bd`

## External Preimage Pins

- Preimage output directory: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/protected_preimages_20260903T182148Z`
- `PREIMAGE_DIGEST_REPORT.json`: `16b99c972516af27094ee656049f015f3d0ee76d4d73463a275286b73e3c1ef1`
- `normal_claude_profile.json`: `1ebf932172fd1e77c09f78eac02237f2881d69dc50c356f2c7c17375c86f5747`
- `normal_claude_runtime.json`: `71aa51138f058fdac52f11055a3b6ab0aff9a1f3584d1dccbeb7123f4b4ad59e`
- `failed_0_2_2_candidate.json`: `04c45105707d8dac916a9671036a1ff06cfaea06c4df926c5874d2c33b712396`
- `failed_0_2_2_test_root.json`: `80a9b8cb09722d9bdc4273f84b812d71f9d7f01e64ce033ce24147a481731411`
- `failed_0_2_2_config.json`: `bb01cd32840d4adc306285bb777ad46e2e15da378e2b1dc9c7f712ca2e33a380`
- `odyssey.json`: `7eaa4073ef8e51ce9fe8388e8a5670eaf30e8092d80e1ed7d5f1c57f809a43d3`
- `unrelated_state.json`: `1aa7226b9b54e038f28f343602ea9bfc0ff55f7b7baee3e5bc09533557aec56e`

## Activation-Pinned Disposable Paths

- Disposable activation root: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01`
- Config root: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/config`
- Preflight evidence root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/live_preflight_20260903T1927WEST`
- Journey root `greenfield`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/greenfield`
- Journey root `brownfield-neither`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/brownfield-neither`
- Journey root `brownfield-bmad`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01/brownfield-bmad`

## Authority Boundary

- Authorized micro-sprint: MS-01 only.
- Authorized checks: VM-001 pin revalidation and VM-002 containment preflight.
- Authorized external/disposable actions: provision a contained disposable root and seed a Factory-only disposable repository from the qualified candidate's packaged Factory payload.
- Authorized run-root writes: `EXECUTION_MODE.txt` transition, this authorization file, the matching MS-01 execution prompt, and bounded VM-001/VM-002/MS-01 evidence under `artifacts/verification/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/`.
- No candidate source, test, generated package, donor, Factory Core, protected-root, or Git mutation is authorized.
- No BMAD workflow invocation, MS-02, MS-03, AuditEdge access, commit, merge, push, publication, pilot, release, or rollout is authorized.
- Stop after MS-01 evidence. Restore `EXECUTION_MODE.txt` to `PLANNING_ONLY` before handoff for human review.
