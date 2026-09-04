# Execution Authorization

## Version

v1

## Change Log

- v1 (2026-09-03): Recorded corrected MS-01 retry authorization with stable `unrelated_state` protected root.

## Authorization

- Human Go: RECORDED
- Human authorization text: "Authorize a corrected MS-01 retry using a stable unrelated_state protected root that is not mutated by Codex app internal Git refs, with fresh protected preimage capture, VM-001/VM-002 rerun, disposable Factory-only provisioning, evidence capture, PLANNING_ONLY restoration, and stop before MS-02. No candidate source/test/package changes, Git actions, BMAD invocation, MS-02/MS-03, publication, pilot, release, or rollout."
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

## Corrected Preimage Pins

- Preimage output directory: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/protected_preimages_20260903T185700Z`
- `PREIMAGE_DIGEST_REPORT.json`: `dd6b2e8436d4fa212cfb9ca085d4c65c7d6ea352b5cd68428cf04c89cabf59c9`
- `normal_claude_profile.json`: `1ebf932172fd1e77c09f78eac02237f2881d69dc50c356f2c7c17375c86f5747`
- `normal_claude_runtime.json`: `71aa51138f058fdac52f11055a3b6ab0aff9a1f3584d1dccbeb7123f4b4ad59e`
- `failed_0_2_2_candidate.json`: `04c45105707d8dac916a9671036a1ff06cfaea06c4df926c5874d2c33b712396`
- `failed_0_2_2_test_root.json`: `80a9b8cb09722d9bdc4273f84b812d71f9d7f01e64ce033ce24147a481731411`
- `failed_0_2_2_config.json`: `bb01cd32840d4adc306285bb777ad46e2e15da378e2b1dc9c7f712ca2e33a380`
- `odyssey.json`: `7eaa4073ef8e51ce9fe8388e8a5670eaf30e8092d80e1ed7d5f1c57f809a43d3`
- `unrelated_state.json`: `26f30fed459fea7f214c71a1de9d79e8cf3b76d322f6a2ed41e8b4fc8121e08f`
- Corrected `unrelated_state` root: `/Users/eduardodosremedios/factory-starter-kit/docs`
- Corrected `unrelated_state` entries: `245`
- Corrected `unrelated_state` aggregate SHA-256: `73090a0004b63210df0c54b9e75e73f394f9287dd0cd680d303fca6ed63af73b`

## Activation-Pinned Disposable Paths

- Disposable activation root: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1`
- Config root: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/config`
- Preflight evidence root: `/Users/eduardodosremedios/factory-bmad-025-solution-context-evidence/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/live_preflight_20260903T1957WEST`
- Journey root `greenfield`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/greenfield`
- Journey root `brownfield-neither`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/brownfield-neither`
- Journey root `brownfield-bmad`: `/Users/eduardodosremedios/factory-bmad-025-ms06-disposable/RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification/MS-01-corrective1/brownfield-bmad`

## Authority Boundary

- Authorized micro-sprint: corrected MS-01 retry only.
- Authorized checks: VM-001 pin revalidation and VM-002 containment preflight rerun.
- Authorized disposable action: provision and seed one Factory-only disposable repository from the qualified candidate's packaged Factory payload.
- Authorized evidence/control writes: this authorization, the matching corrective execution prompt, `EXECUTION_MODE.txt` transition/restoration, and bounded corrected MS-01 evidence.
- No candidate source, tests, generated packages, donor roots, protected roots, Git actions, BMAD invocation, MS-02, MS-03, AuditEdge access, publication, pilot, release, or rollout is authorized.
- Stop after corrected MS-01 evidence and restore `PLANNING_ONLY`.
