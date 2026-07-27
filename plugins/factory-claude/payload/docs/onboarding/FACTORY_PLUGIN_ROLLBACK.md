# Factory Plugin Rollback Guide

Rollback is for restoring the project payload after an applied update. Reinstalling the harness plugin and rolling back project files are separate operations.

## Preconditions

- `docs/Factory/installation/INSTALLATION_STATE.json` exists and names the last successful transaction receipt
- doctor can resolve the repository root
- the receipt target version matches the installation-state version
- the project owner explicitly approves rollback

If any precondition fails, stop. Do not manufacture rollback metadata.

## Procedure

1. Invoke `$factory-update` in Codex or `/factory:update` in Claude and ask it to preview rollback.
2. Review the installed version, target prior version, and affected paths.
3. Give separate explicit rollback approval.
4. The bundled lifecycle tool restores prior file bytes and the prior installation receipt.
5. It marks the durable update receipt `ROLLED_BACK` only after restoration succeeds.
6. Run doctor, Factory validation, and the project test command.
7. Record the result in pilot evidence.

## Expected Result

Successful rollback returns:

- state `ROLLED_BACK`
- reason `FACTORY_ROLLBACK_APPLIED`
- the restored version
- the affected paths
- the next action `run_factory_doctor_and_validation`

## Failure

On `FACTORY_ROLLBACK_EVIDENCE_MISMATCH` or a write failure:

- stop further updates
- preserve `docs/Factory/installation/INSTALLATION_STATE.json` and `docs/Factory/installation/receipts/`
- capture `git status --short` and the error JSON
- recover only from verified version control or an owner-approved backup
- log a High defect for the pilot
