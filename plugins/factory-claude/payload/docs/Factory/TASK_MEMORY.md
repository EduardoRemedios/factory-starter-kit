# docs/Factory/TASK_MEMORY.md — Optional Task Memory Helper

## Version
v1

## Change Log
- v1 (2026-05-18): Added generic optional task-memory helper contract.

## Purpose
Task memory is an optional local helper for repeat work. It stores reusable runbooks and a lightweight outcome journal so agents can start common tasks with better checklists.

Task memory is advisory only. It does not replace Factory artifacts, `AGENTS.md`, stage-lint, pack-lint, merge preflight, or human Go/No-go.

## Commands
Initialize default runbooks and the local journal:

```bash
./scripts/factoryctl memory-init
```

Suggest a runbook for a task:

```bash
./scripts/factoryctl memory-suggest --task "Run a Factory planning sprint"
```

Log an outcome:

```bash
./scripts/factoryctl memory-log --task "Run a Factory planning sprint" --outcome partial --notes "Stage A recall was weak until required refs were added."
```

Review journal patterns:

```bash
./scripts/factoryctl memory-review
```

## Files
- Runbooks: `ops/runbooks/*.yaml`
- Journal: `artifacts/task_memory/task_journal.jsonl`
- Reports: `artifacts/task_memory/reports/`

## Guardrails
- Do not treat task-memory suggestions as authority.
- Keep private or customer-specific lessons in the adopting repo, not in the public starter kit.
- If task memory contradicts current Factory artifacts, the Factory artifacts win.
