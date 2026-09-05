---
name: conductor-purple-gate
description: Perform Factory Purple Gate adjudication against evidence. Use when Codex is asked to review Stage D or Stage I2, decide PASS, CONDITIONAL PASS, or FAIL, evaluate PACK_CHECKLIST.md, resolve Red/Blue disputes, assess whether scope expansion remains unapproved, or produce PACK_AUDIT_REPORT.md from completed Factory artifacts.
---

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

# Factory Purple Gate

## Workflow

1. Read `docs/Conductor/Spec/STAGE_CONTRACTS.md`, `docs/Conductor/Spec/PURPLE_GATE_CHECKLIST.md`, and the stage inputs marked `LOAD`.
2. Verify every required input exists before judging substance.
3. Evaluate evidence, not intent or confidence. Cite artifact paths for each conclusion.
4. Record unresolved scope expansion, missing verification, weak recall, or unapproved assumptions as blockers.
5. Issue one verdict only: `PASS`, `CONDITIONAL PASS`, or `FAIL`.
6. If reviewing I2, ensure `PACK_CHECKLIST.md` and `PACK_MANIFEST.md` are complete and aligned before producing `PACK_AUDIT_REPORT.md`.

## Verdict Rules

- `PASS`: all critical checklist items are satisfied, no unapproved scope expansion remains, and evidence is complete.
- `CONDITIONAL PASS`: critical items pass, but bounded deferrals or non-critical quality gaps remain with explicit follow-up hooks.
- `FAIL`: any critical item fails, evidence is missing, scope expansion is unapproved, or the pack cannot be executed/reviewed safely.

## Outputs

Return:
- verdict
- critical findings
- conditional findings
- evidence paths
- required fixes before retry, if any
- handoff update path
