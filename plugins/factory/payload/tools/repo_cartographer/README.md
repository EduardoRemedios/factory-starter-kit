# Repo Cartographer

Manual advisory repository scan for Factory starter-kit adopters.

Run the default read-only scan:

```bash
./scripts/cartographer
```

Reports are written to:

```text
artifacts/cartographer/<timestamp>/
```

Default mode harvests existing evidence and does not run verification commands. To opt in to approved verification commands:

```bash
./scripts/cartographer --execute-verification --verification-command knowledge_lint --verification-command factoryctl_help
```

Coverage status is scoped:
- `COMPLETE`: every approved starter-kit verification command ran and passed in this scan.
- `PARTIAL`: some verification execution was skipped, such as the default evidence-only scan or a subset of approved commands.
- `DEGRADED`: one or more selected verification commands failed.

Deployment state remains separate and is not assessed by Cartographer v0.

Cartographer reports are advisory only. Canonical repository truth remains in human-approved docs and Factory artifacts.
