# Pre-mortem

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E pre-mortem.

## Failure Modes
- PM-01: Runner is over-abstracted and hard to audit.
- PM-02: Clean fixture pass is mistaken for V3 promotion approval.
- PM-03: V2 deprecation language is not detected.
- PM-04: AEGIS boundary violation is missed.
- PM-05: Halt-on-failure semantics are not checked.
- PM-06: Expected JSON omits reviewer classification fields.
- PM-07: Fixture files become too synthetic to reflect real V3 artifacts.

## Mitigations
- Keep checks explicit and local.
- Emit advisory-only status and no promotion authorization.
- Include V2 fallback and AEGIS negative fixtures.
- Include failed verification and missing evidence fixtures.
- Require review fields in output shape.
- Add at least one real-doc smoke command after fixture verification.
