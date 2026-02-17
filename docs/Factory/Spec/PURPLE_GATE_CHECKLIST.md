# docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.2

## Version
v3.2

## Change Log
- v3.2 (2026-02-11): Added Critical item C9 requiring successful knowledge-lint preflight evidence before PASS/CONDITIONAL PASS.
- v3.1 (2026-02-08): Confirmed compatibility with Stage J → I2 reordering (STAGE_CONTRACTS v4). No item changes — PACK_CHECKLIST is now produced by STAGE_J (before Purple audit), which is the correct dependency order.
- v3 (2026-02-06): Clarified that PACK_CHECKLIST is the run-specific instantiation of this spec and is the source-of-truth for item answers.

Answer YES/NO for each item in the run-specific `pack/PACK_CHECKLIST.md`.
This spec defines the canonical item set; the run-specific checklist must match 1:1.

## Critical (must all be YES for PASS or CONDITIONAL PASS)
C1. All required artifacts exist at required paths and are non-empty.
C2. intent.md is contract-grade per DEFINITIONS.md §8.
C3. No unresolved Critical findings remain from intent or envelope red teams.
C4. Every Critical/High constraint has verification coverage (traceability complete).
C5. Sprint envelope includes file-touch budgets and they are non-empty.
C6. Micro-sprints include entry/exit criteria and stop/go gates.
C7. No unbounded deferrals exist.
C8. No [SCOPE EXPANSION] items remain unapproved (none BLOCKING).
C9. Knowledge lint preflight passed and evidence artifact is present in run root (`KNOWLEDGE_LINT.txt`).

## Conditional (required for CONDITIONAL PASS)
K1. Every deferral is bounded per DEFINITIONS.md §5.
K2. Each bounded deferral is hooked in micro_sprints.md with a micro-sprint ID.

## Quality (can be NO, but must be explained)
Q1. Size caps satisfied for all artifacts.
Q2. Scope boundaries match across intent, envelope, and micro-sprints.
Q3. No [INFERRED] requirements remain unapproved.
