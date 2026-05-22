# Operational Release Approval For V3-OP-001

## Version
v1

## Change Log
- v1 (2026-05-22): Initial operational release approval for optional `V3-OP-001` use.

## Approval
Approved.

This approval accepts the research evidence for optional `V3-OP-001` use. It remains non-enforcing for required repository gates.

## Approval Text
The human sponsor approved the following release decision in the Codex thread on 2026-05-22:

> I approve Factory V3 `V3-OP-001 Bounded Code Change` for optional operational use. Factory V2 remains supported and available as fallback. Approval applies at commit `f07fa11`. I accept the residual risks recorded in `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`.

## Scope Approved
- Profile: `V3-OP-001 Bounded Code Change`
- Release level: optional operational use
- Approval commit: `f07fa11`
- Factory v2 fallback: required and retained
- Default Factory mode: unchanged
- Required-gate wiring: not approved

## Not Approved
- Factory v3 as default Factory mode
- Any Factory v3 profile other than `V3-OP-001`
- Factory v2 deprecation
- Required-gate integration
- CI or merge-preflight integration
- Runtime-kernel authority
- Production action mediation
- separate governance kernel dependency
- Payment, authentication, regulated-action, compliance, infrastructure, or production deployment authority

## Residual Risks Accepted
The approval accepts the residual risks recorded in:

- `docs/Factory/v3/OPERATIONAL_READINESS_DECISION_REPORT_V3_OP_001.md`

Key accepted limits:

- Broad production false-negative discovery is not measured.
- `V3-OP-001` is optional profile use, not default Factory mode.
- V3 checks remain standalone advisory only.
- No live external governance kernel adapter was tested.
- User guidance must be followed before broad adoption.

## Rollback And Fallback Rule
Route work to Factory v2 when any condition applies:

- mission intent is ambiguous,
- scope expands beyond the mission envelope,
- file, command, dependency, or tool authority is missing,
- verification fails or evidence is missing,
- reentry state conflicts with authored artifacts,
- SIMPLE-CODE-GATE blocker remains unresolved,
- runtime-kernel, payment, authentication, compliance, production deployment, or infrastructure authority is implicated,
- the human sponsor requests V2 fallback.

## First-Use Monitoring
Early operational use should record:

- mission envelope path,
- branch and commit,
- verification outputs,
- advisory eval output,
- fallback review result,
- closeout residual risks,
- any user friction or missed guidance.
