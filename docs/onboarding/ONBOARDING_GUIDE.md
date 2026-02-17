# Onboarding Guide — Agentic-First Development with the Harmony Factory

> **Audience:** New contributor joining the Harmony project who will work with AI coding agents in Cursor.
>
> **Goal:** After working through this guide you should be able to run a governed agentic workflow independently — writing intent before code, verifying before merging, and catching agent drift before it becomes technical debt.
>
> **Last updated:** 2026-02-17

---

## Part 1: The Philosophy — Why We Work This Way

### 1.1 The Problem with Unstructured Agentic Coding

AI coding agents are powerful. They can write hundreds of lines of working code in seconds. That speed is also the danger:

- They **expand scope silently**. You ask for a login form; they add password-reset, OAuth, and a user-settings page.
- They **skip edge cases** unless you force them to think about them.
- They **use ambiguous language** where precision is required ("e.g." instead of a canonical list).
- They **drift on naming, paths, and contracts** across a long session.
- They **don't verify their own work** unless the workflow demands it.

None of these are bugs in the AI. They are natural consequences of an agent optimizing for "helpful and complete" without external governance. Our workflow exists to provide that governance.

### 1.2 The Three Pillars

Everything in our process comes back to three ideas:

**Intent** — What are we building, and what are we NOT building?

Before any code is written, we produce a locked intent document. It defines the goal, the scope, the non-goals, and the acceptance criteria. Every requirement is sourced: either it came from the brief (`[SOURCE:RAW]`) or the agent inferred it (`[INFERRED]`). Inferred requirements get flagged for human review. Nothing slips in silently.

**Constraints** — What must never be violated?

Constraints are the guardrails. In Harmony, these include things like:
- Fail-closed behavior: if something is ambiguous or broken, the system denies rather than guesses.
- Schema-locked boundaries: unknown fields are rejected, not silently accepted.
- Evidence-chain integrity: every decision produces a tamper-evident record.
- Closed-world registries: if an action or reason code isn't in the registry, it's denied.

Constraints are non-negotiable. They don't get relaxed because a deadline is tight.

**Verification** — How do we prove it works?

Not "it seems to work" or "the tests pass." Verification means:
- Every Critical and High constraint has at least one test or fixture that proves it holds.
- A traceability matrix maps constraints to tests, so nothing falls through the cracks.
- Verification is designed *before* implementation, not bolted on after.

### 1.3 Planning-First, Execution-Last

Our default operating principle (documented in `docs/Factory/ORCHESTRATION.md` section 0.1):

1. **Intent framing first** — define outcomes, non-goals, acceptance boundaries.
2. **Constraint lock second** — make invariants and fail-closed requirements explicit.
3. **Verification design third** — define checks, fixtures, and traceability.
4. **Research spikes fourth** — time-box unknowns with explicit questions.
5. **Execution last** — start coding only after planning artifacts pass review.

This order exists because decision quality has higher leverage than raw execution speed. A well-scoped sprint with clear constraints executes cleanly. A poorly-scoped sprint produces code that has to be rewritten.

---

## Part 2: The Factory Pipeline — How Sprints Are Planned

The Factory is our sprint planning pipeline. It does NOT write code. It produces the *contract* that governs code writing.

Think of it like this:

| Analogy | Factory equivalent |
|---------|-------------------|
| Customer order | Raw brief (written by Eduardo) |
| Engineering review + design + test plan | Factory pipeline (Stages A through I2) |
| Approved blueprint | Sprint pack |
| Building to the blueprint | Sprint execution |

### 2.1 The Stages

The pipeline has specialist roles, each played by a separate agent (or the same agent wearing a different hat). The separation enforces different perspectives:

| Stage | Role | What happens |
|-------|------|-------------|
| **A** | Intent Contractor | Converts the raw brief into a contract-grade `intent.md`. Sources every requirement. Tags open questions. |
| **B** | Red Team | Attacks the intent for gaps, contradictions, ambiguity, and verification holes. Findings only — no solutions. |
| **C** | Blue Team | Hardens the intent based on Red Team findings. No scope expansion allowed. |
| **D** | Purple Gate | Adjudicates Red/Blue disputes. Evaluates a checklist. Issues PASS / CONDITIONAL PASS / FAIL. |
| **E** | Risk Analyst | Produces a pre-mortem and risk register from the locked intent. |
| **F** | Verification Specialist | Creates fixtures, verification plan, and traceability matrix. |
| **G** | Sprint Planner | Sequences micro-sprints with entry/exit criteria and stop/go gates. |
| **H** | Envelope Author | Produces the sprint envelope — the execution contract with file-touch budgets. |
| **I** | Red/Blue on Envelope | Attacks and hardens the execution plan (not just the intent). |
| **J** | Pack Consolidator | Mechanical packaging: manifest + checklist. No adjudication. |
| **I2** | Purple Audit | Final gate. Evaluates the complete pack against the checklist. PASS or FAIL. |

**Key insight:** Stages B and C cycle up to 2 times (Red attacks, Blue hardens, Red attacks again, Blue hardens again). After the cap, Purple adjudicates whatever remains. This prevents infinite loops while ensuring adversarial review.

**Key insight:** Stage J runs *before* I2. This was a bug fix from the first live run — Purple needs the checklist to audit against, and the Pack Consolidator is the one who produces it. Getting the dependency order right matters.

### 2.2 The Human Gate

After Stage I2, the complete pack goes to Eduardo for review. He reads:

1. `PACK_CHECKLIST.md` — binary go/no-go items
2. `PACK_AUDIT_REPORT.md` — Purple's verdict
3. `intent.md` — the locked scope
4. The envelope — the execution contract
5. `micro_sprints.md` — the execution sequence

Eduardo says "Go" or "No-go with feedback." No code is written until he says Go.

### 2.3 Execution Mode

Every Factory run defaults to `PLANNING_ONLY`. This is persisted in a file called `EXECUTION_MODE.txt` at the run root. In planning-only mode:

- No execution prompt is generated.
- No downstream runs are initialized.
- The pack is terminal planning evidence.

To enable execution, the raw brief must explicitly include:
- `Execution Mode: EXECUTION_ENABLED`
- `Execution Authorization: <human-approved reference>`

This prevents agents from running ahead of the plan.

### 2.4 The Execution Prompt

When a run is execution-enabled and passes all gates, the pipeline produces an execution prompt — a self-contained document that can be pasted into a fresh agent session. It includes:

- The file reading order (all pack artifacts + product context docs)
- The micro-sprint sequence with gate checks
- Hard guardrails (explicit "do not violate" rules)
- Verification commands to run before merge
- Troubleshooting guidance
- An exit checklist

This bridges the planning output and the execution session. Without it, the execution agent has to navigate 15+ documents independently, which increases the risk of missed constraints.

---

## Part 3: Key Documents and Where They Live

### 3.1 The Doc Spine (project-level)

| Document | Path | What it does |
|----------|------|-------------|
| AGENTS.md | `AGENTS.md` (repo root) | Context map for any agent entering the project. Read order, commands, guardrails. |
| HARMONY_STATE.md | `docs/HARMONY_STATE.md` | Single source of truth for what exists today. Updated after every sprint. |
| ROADMAP.md | `docs/ROADMAP.md` | Sprint-level plan and milestone sequence. Strategic counterpart to STATE. |
| CHANGELOG.md | `docs/CHANGELOG.md` | Version history for all canonical documents. |

**Rule:** When a sprint outcome is GO, all three (STATE, ROADMAP, CHANGELOG) must be updated in the same cycle. This prevents stale-planning drift (see pitfall FP-006).

### 3.2 The Factory (pipeline-level)

| Item | Path | What it does |
|------|------|-------------|
| Orchestration guide | `docs/Factory/ORCHESTRATION.md` | How to run the pipeline end-to-end. The operational playbook. |
| Scratchpad | `docs/Factory/SCRATCHPAD.md` | Cross-run pitfalls index. Mandatory reading before any run. |
| Stage contracts | `docs/Factory/Spec/STAGE_CONTRACTS.md` | Entry/exit criteria for every stage. |
| Definitions | `docs/Factory/Spec/DEFINITIONS.md` | Size caps, impact rubric, bounded deferral rules, placeholder rules. |
| Purple Gate Checklist | `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md` | The canonical checklist Purple evaluates against. |
| Templates | `docs/Factory/templates/` | Skeleton files for every artifact the pipeline produces. |
| Runs | `docs/Factory/runs/<RUN_ID>/` | One folder per pipeline run, containing the raw brief and the full pack. |

### 3.3 Why Templates Exist

Templates enforce structural consistency across runs. Every `intent.md` has the same sections. Every envelope has file-touch budgets. Every handoff has the same fields. This means:

- Agents can't skip sections or invent their own structure.
- Purple can audit against a known schema.
- You can compare artifacts across runs because they have the same shape.

The templates live in `docs/Factory/templates/` and include:
- `EXECUTION_PROMPT_TEMPLATE.md` — skeleton for the execution prompt
- `HANDOFF_STAGE_TEMPLATE.md` — skeleton for stage handoffs
- `PACK_CHECKLIST_TEMPLATE.md` — skeleton for the go/no-go checklist
- `PACK_AUDIT_REPORT_TEMPLATE.md` — skeleton for Purple's audit report
- `PACK_MANIFEST_TEMPLATE.md` — skeleton for the pack manifest
- `SPRINT_ENVELOPE_TEMPLATE.md` — skeleton for the execution contract
- `SPRINT_ENVELOPE_REDTEAM_TEMPLATE.md` — skeleton for Red Team's envelope attack
- `TRACEABILITY_MATRIX_TEMPLATE.md` — skeleton for constraint-to-test mapping
- `INTENT_LOCK_REPORT_TEMPLATE.md` — skeleton for Purple's intent lock verdict

### 3.4 How Runs Work

Each Factory run creates a timestamped folder:

```
docs/Factory/runs/RUN_20260208_1400_factory/
  raw_brief.md            <-- Eduardo's input (the seed)
  KNOWLEDGE_LINT.txt      <-- pre-run lint evidence
  EXECUTION_MODE.txt      <-- PLANNING_ONLY or EXECUTION_ENABLED
  RETRO.md                <-- run-local retrospective (optional)
  SPRINT_ID.txt           <-- assigned during Stage H
  pack/
    intent.md             <-- locked intent (versioned, sourced)
    intent_redteam.md     <-- Red Team findings
    intent_synthesis.md   <-- Blue Team hardening summary
    intent_lock_report.md <-- Purple's verdict on intent
    premortem.md          <-- failure scenarios
    risk_register.md      <-- risks with mitigations
    verification_plan.md  <-- what to test and how
    traceability_matrix.md <-- constraint-to-test mapping
    micro_sprints.md      <-- execution sequence
    <SPRINT_ID>_ENVELOPE.md      <-- the execution contract
    <SPRINT_ID>_ENVELOPE_REDTEAM.md <-- Red Team attack on envelope
    PACK_AUDIT_REPORT.md  <-- Purple's final verdict
    PACK_MANIFEST.md      <-- list of all artifacts
    PACK_CHECKLIST.md     <-- go/no-go checklist
    fixtures/             <-- golden test inputs/outputs
    HANDOFF/              <-- stage-to-stage handoff records
```

Runs are immutable records. Once a pack is produced, it doesn't get edited — it's the evidence trail for how decisions were made.

---

## Part 4: The Scratchpad — Learning from Mistakes

The Scratchpad (`docs/Factory/SCRATCHPAD.md`) is a governed list of cross-run pitfalls. It is NOT a diary or a narrative. Each entry is one sentence describing a mistake that happened, with evidence pointing to the run where it occurred.

**You must read the Active Pitfalls section before any Factory run, sprint execution, or brief drafting.**

Here are some pitfalls and what they teach:

| Pitfall | Lesson |
|---------|--------|
| FP-001 (scope) | When execution reveals contract ambiguity, fix the contract first. Don't build features on top of drift. |
| FP-003 (contracts) | Prefer extending existing contracts with optional fields over adding new enum values. Less breaking change risk. |
| FP-005 (verification) | Test the actual invariant, not a proxy. "No clock reads in the engine" should be tested by checking for clock reads, not by banning a module import. |
| FP-007 (contract_lock) | In contract-locking sprints, don't use hedging language like "e.g." — use one canonical form everywhere. |
| FP-008 (verification) | If intent claims multiple corruption classes (tamper, reorder, delete, link-break), provide a dedicated fixture for each one. Don't bundle them. |

The scratchpad has a hard cap of 12 entries. Entries are deprecated only when superseded by a locked test, stage contract update, or policy change. This keeps it compact and actionable.

---

## Part 5: Key Concepts Glossary

| Term | Meaning |
|------|---------|
| **Fail-closed** | When something is ambiguous, broken, or missing, the system denies/blocks rather than guessing or proceeding. This is the default posture for all regulated and consequential actions. |
| **Schema-locked** | Input and output shapes are validated against a closed schema. Unknown fields are rejected. This prevents silent contract drift. |
| **Closed-world registry** | If an action or reason code isn't explicitly registered, it's denied. No "catch-all" or "other" categories. |
| **UVS (User Verification Snapshot)** | A parameter-bound, time-bound, user-bound snapshot that must be confirmed before an irreversible action executes. Prevents stale or tampered state from reaching execution. |
| **Evidence chain** | The ordered sequence of records (PolicyDecisionRecord, ToolExecutionRecord, ConfirmationRecord, ReceiptRecord) that proves what happened and why. Tamper-evident via hash chaining. |
| **Purple Gate** | The quality gate where an adjudicator evaluates a checklist of Critical items. PASS means all Critical items are YES. FAIL halts the pipeline. |
| **Bounded deferral** | Something explicitly deferred to a future micro-sprint, with a hook ID, an owner, and a scope boundary. Unbounded deferrals (no hook, no owner) block PASS. |
| **File-touch budget** | The explicit list of files a micro-sprint is allowed to create or modify. Prevents scope creep at the file level. |
| **Raw brief** | Eduardo's short document describing what to build. The seed input to the Factory. |
| **Sprint pack** | The complete set of planning artifacts produced by a Factory run. The contract that governs execution. |
| **Execution prompt** | A self-contained document generated after all gates pass, designed to be pasted into a fresh agent session for implementation. |
| **Knowledge lint** | A pre-run script (`scripts/knowledge_lint.sh`) that validates the repo's doc spine is intact before a Factory run starts. |
| **Red Team** | The adversarial role that attacks artifacts for gaps, contradictions, and verification holes. Findings only — no solutions. |
| **Blue Team** | The hardening role that fixes Red Team findings without expanding scope. |
| **Traceability matrix** | A mapping from every Critical/High constraint to the test or fixture that verifies it. If a constraint has no test, it's a gap. |

---

## Part 6: Your First Week — Reading List and Exercises

### 6.1 Reading List (in order)

Read these in exactly this order. Don't skip ahead.

| Day | Document | Why |
|-----|----------|-----|
| 1 | This guide (you're reading it) | Get the mental model. |
| 1 | `docs/Factory/ORCHESTRATION.md` sections 0, 0.1, 0.2, 0.3 | Understand the operating principles. |
| 1 | `docs/Factory/SCRATCHPAD.md` Active Pitfalls section | Learn from real mistakes. |
| 1 | `docs/Factory/ORCHESTRATION.md` section 11 | Lessons from the first live run. |
| 2 | `docs/Factory/Spec/DEFINITIONS.md` | Size caps, impact rubric, bounded deferral rules. |
| 2 | `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md` | What the quality gate actually checks. |
| 2 | `docs/Factory/Spec/STAGE_CONTRACTS.md` | Entry/exit criteria for every stage. |
| 3 | Walk through `docs/Factory/runs/RUN_20260208_1400_factory/pack/` | Trace a real run from intent to audit report. Read: `intent.md`, `intent_redteam.md`, `intent_synthesis.md`, `intent_lock_report.md`, `verification_plan.md`, `traceability_matrix.md`, `micro_sprints.md`, the envelope, `PACK_AUDIT_REPORT.md`. |
| 4 | `docs/Factory/templates/` (all 9 templates) | Understand the structural contracts. |
| 4 | `AGENTS.md` (repo root) | The context map every agent reads first. |
| 5 | `docs/HARMONY_STATE.md` | What the project has built so far. |
| 5 | `docs/ROADMAP.md` | Where the project is going. |

### 6.2 Comprehension Checks

After completing the reading list, you should be able to answer these questions. If you can't, re-read the relevant section.

1. What is the difference between a `PLANNING_ONLY` run and an `EXECUTION_ENABLED` run?
2. Why does Stage J run before Stage I2?
3. What makes a deferral "bounded" vs "unbounded"?
4. What happens if a Purple Gate evaluates to FAIL?
5. Why do we design verification before writing implementation code?
6. What is the maximum number of Red/Blue cycles before Purple adjudicates?
7. What does `[INFERRED]` mean on a requirement, and why does it matter?
8. Name three things an AI agent tends to do that our workflow is designed to catch.
9. What is the purpose of the knowledge lint script?
10. Why does the execution prompt exist instead of just handing the agent the envelope?

### 6.3 Sandbox Exercise

**Do this in your own repo. Do not touch the Harmony repo.**

1. Create a fresh GitHub repo for a small project (a CLI tool, a simple API, a utility library — your choice).
2. Write a raw brief: one paragraph describing a feature you want to build.
3. Use Cursor's agent to play Intent Contractor:
   - Prompt it to produce an `intent.md` following the structure from our templates.
   - Review: Are requirements sourced? Are non-goals explicit? Are acceptance criteria binary (yes/no, not "seems good")?
4. Use Cursor's agent to play Red Team:
   - Prompt it to attack your intent for gaps, contradictions, and missing edge cases.
   - Review: Did it find real issues, or just cosmetic ones?
5. Harden the intent based on Red Team findings (play Blue Team yourself).
6. Write a verification plan *before* writing any code:
   - For each Critical constraint, define at least one test or fixture.
   - Build a simple traceability matrix (constraint -> test).
7. Only now: write the implementation.
8. Run your verification plan. Does everything pass? Did you miss anything?

The goal is not to produce a perfect Factory run on your first try. The goal is to internalize the habit: **intent before code, constraints before features, verification before merge.**

---

## Part 7: Common Mistakes to Avoid

| Mistake | Why it's a problem | What to do instead |
|---------|--------------------|--------------------|
| Starting to code before intent is locked | You'll build the wrong thing, or build the right thing with the wrong boundaries. | Write and review intent first. Always. |
| Letting the agent expand scope | The agent will helpfully add features you didn't ask for. Each one is a maintenance burden and a potential bug surface. | Watch for `[SCOPE EXPANSION]` tags. If the agent adds something you didn't ask for, remove it or flag it BLOCKING. |
| Writing tests after implementation | Tests written after code tend to test what the code does, not what it should do. They miss the edge cases. | Design verification from the constraints, not from the implementation. |
| Using vague acceptance criteria | "The feature works correctly" is not an acceptance criterion. It's a wish. | Make criteria binary: "Given X input, the output is Y" or "When Z fails, the system returns deny with reason code W." |
| Ignoring the Scratchpad | Every pitfall entry represents a real mistake that cost time. | Read Active Pitfalls before every run. It takes 2 minutes. |
| Trusting agent output without review | Agents are confident even when wrong. They will state incorrect paths, invent reason codes, and claim tests pass when they don't. | Verify. Run the commands. Check the paths. Read the output. |

---

## Part 8: When You're Ready for More

Once you've completed the sandbox exercise and can confidently answer the comprehension checks, the next steps are:

1. **Read access to Harmony.** You'll review completed sprint packs and write critiques.
2. **Shadow a Factory run.** Watch a run from raw brief to pack completion. Take notes on what each stage produces and why.
3. **Run a Factory pipeline on a bounded, low-risk sprint.** Eduardo will write the brief. You'll orchestrate the pipeline.
4. **Execute a sprint against a pack.** With the pack as your contract, implement the code changes and run verification.

Each step requires demonstrating competence at the previous level. There's no shortcut, but there's also no ceiling — once you internalize the discipline, you'll be faster and more reliable than any unstructured approach.

---

## Appendix: Canonical Commands

These are the commands you'll use regularly:

```bash
# Pre-run knowledge lint (must pass before any Factory run)
bash scripts/knowledge_lint.sh

# Run the conformance harness
python3 -m harmony.conformance_harness \
  --matrix docs/CONFORMANCE_TEST_MATRIX.md \
  --profile baseline_adapter \
  --report artifacts/conformance/conformance_report.json

# Run the full test suite
python3 -m unittest discover -s tests
```

---

*This guide is a living document. As the workflow evolves, it will be updated. If something is unclear or seems wrong, ask — don't guess.*
