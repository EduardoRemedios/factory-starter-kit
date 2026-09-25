# Receipt integrity and pilot compatibility

This unreleased candidate combines receipt-integrity maintenance with the
verification-definition guard already in upstream `17b2244`. It retains the
0.3.5 package label; use the qualification run's full package path and digest
manifest to identify its exact bytes. It introduces no keys, accounts,
dependencies or v1 receipt conversion. Publication requires a separately
reviewed version/release decision. Never replace an installed same-version
cache to test these candidate bytes.

## The core test-drive path stays the same

```bash
claude plugin marketplace add EduardoRemedios/factory-starter-kit
claude plugin install conductor@factory-starter-kit
```

Projects using an upstream adapter keep their existing companion install
command; this core maintenance does not change the companion or its dependency.
Start Claude Code CLI in the repository and use `/conductor:doctor` and
`/conductor:progress`, or the companion's existing Doctor front door. The
[guide](GUIDE.md), [exercise](FIRST_EXERCISE.md), and
[friction log](FRICTION_LOG_TEMPLATE.md) stay at their existing paths. Adapter
roots, lane policy and upstream skill discovery are unchanged.

## What the checks prove

Lint verifies the receipt payload digest, each retained stdout/stderr file's
bytes and digest, command or target identity, working directory, expected exit,
derived outcome, and any manifest result exit code or timestamp. Manual receipts
keep the existing attestation format. Retained streams are bounded to 64 KiB;
the receipt does not prove the contents of discarded output beyond that limit.

These are consistency checks, not authentication. A writer controlling the logs,
receipt and references can recompute their hashes. The supported workflow uses
the runner, fresh-context review and human approval. Independent assurance of
runner identity would require a separate trusted execution or signing boundary;
this maintenance does not supply one.

## Existing evidence

Untouched, consistent v1 runner receipts require no conversion or rerun. The
optional `expected_exit` field still defaults to zero, and optional manifest
result metadata may remain absent. A schema-valid receipt with inconsistent
evidence fails explicitly; there is no grandfathering of a false PASS.

If a log, command or result no longer agrees, preserve the historical run and
its countersigns. Do not repair evidence by editing hashes, delete a failed
receipt, or silently overwrite a completed pilot run. Record the discrepancy
for review and, if renewed verification is authorized, use a new run with the
unchanged commands and fresh receipts. A changed check needs renewed review of
the verification intent. The deliberate tamper exercise may restore its own
exercise receipt using the runner before completion, as the exercise specifies.
