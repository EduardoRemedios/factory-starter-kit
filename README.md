# Factory Starter Kit

A self-contained copy of the Factory pipeline framework for learning and practice. Drop this into your own repo and use it to plan and govern agentic development work.

## What This Is

The Factory is a sprint planning pipeline for agentic-first development. It does NOT write code. It produces the *contract* that governs code writing — a sprint pack containing locked intent, constraints, risk analysis, verification plans, and an execution envelope.

The pipeline enforces three principles:
1. **Intent** — Define what you're building and what you're NOT building before writing code.
2. **Constraints** — Make invariants and fail-closed requirements explicit before design details.
3. **Verification** — Design checks, fixtures, and traceability before implementation.

## What's Included

```
your-repo/
├── AGENTS.md                          <-- Context map for agents (adapt to your project)
├── scripts/
│   └── knowledge_lint.sh              <-- Pre-run validation script (adapt to your project)
├── docs/
│   ├── PROJECT_STATE.md               <-- You create this: what exists today
│   ├── ROADMAP.md                     <-- You create this: where you're going
│   ├── CHANGELOG.md                   <-- You create this: version history
│   └── Factory/
│       ├── ORCHESTRATION.md           <-- How to run the pipeline end-to-end
│       ├── SCRATCHPAD.md              <-- Cross-run pitfalls index
│       ├── Spec/
│       │   ├── DEFINITIONS.md         <-- Size caps, impact rubric, deferral rules
│       │   ├── STAGE_CONTRACTS.md     <-- Entry/exit criteria for every stage
│       │   ├── NAMING_CONVENTIONS.md  <-- File naming rules
│       │   └── PURPLE_GATE_CHECKLIST.md <-- Quality gate checklist
│       ├── templates/                 <-- Artifact skeletons (9 templates)
│       │   ├── EXECUTION_PROMPT_TEMPLATE.md
│       │   ├── HANDOFF_STAGE_TEMPLATE.md
│       │   ├── INTENT_LOCK_REPORT_TEMPLATE.md
│       │   ├── PACK_AUDIT_REPORT_TEMPLATE.md
│       │   ├── PACK_CHECKLIST_TEMPLATE.md
│       │   ├── PACK_MANIFEST_TEMPLATE.md
│       │   ├── SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md
│       │   ├── SPRINT_ENVELOPE_TEMPLATE.md
│       │   └── TRACEABILITY_MATRIX_TEMPLATE.md
│       └── runs/
│           └── RUN_20260208_1400_factory/  <-- Example completed run (read-only reference)
└── docs/
    └── onboarding/
        └── ONBOARDING_GUIDE.md        <-- The learning guide
```

## Setup Instructions

### 1. Copy the kit into your repo

Run the export script from the Harmony repo:

```bash
bash scripts/export_factory_starter_kit.sh /path/to/your-repo
```

Or manually copy the files following the structure above.

### 2. Create your project's doc spine

The Factory pipeline expects these documents to exist. Create them as simple stubs to start:

**`docs/PROJECT_STATE.md`** — What exists in your project today.
```markdown
# PROJECT_STATE.md — Canonical Build State
> Last updated: YYYY-MM-DD

## What Exists
(Describe your current codebase, tests, and capabilities)

## What Does NOT Exist Yet
(List known gaps)
```

**`docs/ROADMAP.md`** — Where your project is going.
```markdown
# ROADMAP.md — Development Roadmap
> Last updated: YYYY-MM-DD

## Sprints
(Will be populated as you plan and complete sprints)
```

**`docs/CHANGELOG.md`** — Version history for your documents.
```markdown
# Changelog
(Add entries as documents are created or updated)
```

### 3. Adapt AGENTS.md

Edit `AGENTS.md` at your repo root to match your project's structure. Update:
- The read order to reference your actual documents
- The canonical commands to match your test runner
- The change hygiene section to list your canonical docs

### 4. Adapt the knowledge lint script

Edit `scripts/knowledge_lint.sh` to list your project's required files in the `required_files` array. The script validates these files exist and are non-empty before any Factory run starts.

Make it executable:
```bash
chmod +x scripts/knowledge_lint.sh
```

### 5. Verify the setup

```bash
bash scripts/knowledge_lint.sh
```

If it passes, you're ready to run your first Factory pipeline.

## Running Your First Factory Pipeline

1. **Write a raw brief.** One page describing what you want to build, what's in scope, what's out of scope, and your hard constraints. See `docs/Factory/runs/RUN_20260208_1400_factory/raw_brief.md` for an example.

2. **Start a fresh agent session** (Claude Code CLI, Cursor, or similar).

3. **Prompt the agent to act as Root Planner.** Give it:
   - `docs/Factory/ORCHESTRATION.md` (the operational playbook)
   - `docs/Factory/SCRATCHPAD.md` (read Active Pitfalls only)
   - Your raw brief
   - Tell it to initialize a run and execute the pipeline stage by stage.

4. **Follow the stages.** The agent will work through A → B → C → D → E → F → G → H → I → J → I2, producing artifacts at each stage.

5. **Review the pack.** When the pipeline completes, review the pack — especially `PACK_CHECKLIST.md`, `PACK_AUDIT_REPORT.md`, and the intent/envelope.

6. **Say Go or No-go.** If the pack is sound, authorize execution. If not, provide feedback and re-run affected stages.

## The Example Run

The `docs/Factory/runs/RUN_20260208_1400_factory/` directory contains a complete, real Factory run. Use it as a reference to understand what each stage produces. Read the artifacts in this order:

1. `raw_brief.md` — The input
2. `pack/intent.md` — The locked intent
3. `pack/intent_redteam.md` — Red Team findings
4. `pack/intent_synthesis.md` — Blue Team hardening
5. `pack/intent_lock_report.md` — Purple's verdict
6. `pack/premortem.md` — Failure scenarios
7. `pack/risk_register.md` — Risks and mitigations
8. `pack/verification_plan.md` — What to test
9. `pack/traceability_matrix.md` — Constraint-to-test mapping
10. `pack/micro_sprints.md` — Execution sequence
11. The envelope — The execution contract
12. `pack/PACK_AUDIT_REPORT.md` — Final Purple gate

## Key Concepts

- **Fail-closed**: When something is ambiguous, the system denies rather than guesses.
- **Purple Gate**: Quality gate with a checklist of Critical items. All must be YES for PASS.
- **Bounded deferral**: Something deferred to a future sprint with a hook ID, owner, and scope boundary.
- **File-touch budget**: The explicit list of files a micro-sprint may create or modify.
- **Execution mode**: Runs default to `PLANNING_ONLY`. Execution requires explicit authorization.

For the full glossary and learning path, see `docs/onboarding/ONBOARDING_GUIDE.md`.
