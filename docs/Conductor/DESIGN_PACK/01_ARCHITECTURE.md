# Conductor Design Pack — 01 Architecture

Source brief: `docs/Conductor/CONDUCTOR_DESIGN_BRIEF.md` v1.0. This pack was written as design only; steps 1-11 and 14 of 06 were implemented in 0.3.0-0.3.2 and the shipped code is authoritative where they differ.

## 1. Governing principle

**Govern authority, outcomes, and write boundaries. Do not govern steps.**

Conductor constrains three things and nothing else:

| Constraint | Question it answers | Hard mechanism |
|---|---|---|
| Authority | Who may authorize what, and against which exact artifact digest? | Human countersign files, hash-pinned intent and snapshots, default-deny lane policy |
| Proof | What evidence proves a claim? | Runner-produced receipts, Statement of Completion lint, fresh-context verifier |
| Write boundary | Where may writes land? | Protected roots, protected-postimage compare, BMAD workspace containment, hooks |

Everything that told the model *how* to think between those constraints (stage handoff choreography, Red/Blue iteration caps, mandatory eight-document read order, per-stage word caps, "Use the skill" prompt rules) is removed or demoted. Rationale and sources: brief §3.

Corollary (both vendors document that user instructions override skill text): **skill and instruction prose is soft; only validators, hooks, and CI are hard.** Any rule that must hold is implemented in the hard layer and merely explained in prose.

## 2. Three layers

```
Layer 1  Upstream intent          Intent Pack ← human brief + promoted BMAD snapshot(s) + SPEC(s)
Layer 2  Contract core (durable)  schemas · contract-lint · receipts · postimage · SoC · Gap Request · merge protocol
Layer 3  Harness adapters (thin)  Claude Code plugin · Codex plugin · Cursor (AGENTS.md + CLI) · BMAD lane adapter · CI action
```

Layer 2 is the investment. Layer 3 is expected to churn with harness releases and is versioned independently. Layer 1 is small: one schema and one template.

## 3. The three gates

Stage letters A–I2 survive only as an *internal checklist* the agent may use inside G2. They are no longer handoff boundaries, produce no handoff files, and are not linted.

### G1 — Intent Lock (human)

| | |
|---|---|
| Purpose | Freeze *what* and *why* before any governed work. |
| Entry | Project Config validates. Intent Pack draft exists. Recall index consulted if non-empty (risk-triggered, see 02 §3). Every cited BMAD snapshot resolves to an immutable manifest with matching aggregate digest. |
| Exit | `contract-lint intent` PASS. Human writes `countersign/INTENT_LOCK.json` containing the Intent Pack digest, signer, UTC. Effort for G2 and G3 declared with model id. |
| Enforced by | `conductorctl contract-lint intent`; countersign file digest match. |
| Human involvement | Mandatory. This is the first of two human authority points. |
| Replaces | Stages A–D, Brief Review, Purple Gate (intent), knowledge lint as a preflight, mandatory Stage A recall report. |

### G2 — Governed Execution (autonomous)

| | |
|---|---|
| Purpose | Do the work, end to end, inside the locked envelope. |
| Entry | `INTENT_LOCK.json` present and digest matches the Intent Pack. `EXECUTION_MODE` ∈ {PLANNING_ONLY, EXECUTION_ENABLED}; EXECUTION_ENABLED additionally requires `countersign/EXECUTION_GO.json` against the Intent Pack digest. Verification manifest present when the Intent Pack declares runnable verification requirements (error, not warning). Autonomy block and SIMPLE-CODE-GATE loaded via AGENTS.md managed section. Protected-root preimage captured. |
| Exit | Every manifest check has a runner-produced receipt (§5 of 03). Protected-postimage compare PASS. No write outside declared boundaries. Draft Statement of Completion written. |
| Enforced by | `conductorctl contract-lint execution`; `conductorctl receipts run`; `conductorctl postimage compare`; harness hooks (BMAD lane, protected paths). |
| Human involvement | None during the run. The autonomy block instructs the agent not to pause for already-authorized work. |
| Replaces | Stages E–J, POST_GATE execution prompt, micro-sprint sequencing as a mandatory artifact, sprint envelope as a separate document (its content moves into the Intent Pack). |

### G3 — Adversarial Review and Completion

| | |
|---|---|
| Purpose | Prove the claims, not narrate them. |
| Entry | Draft Statement of Completion. Fresh-context verifier report (a subagent that did not perform the work audits every `verified` row against its receipt). |
| Exit | `contract-lint completion` PASS: every `verified` row → existing, non-empty, PASS receipt; every `out_of_scope` row → human decision reference; closeout state derived, not asserted. Human writes `countersign/COMPLETION.json`. Handoff state becomes `REVIEW_READY`; `MERGE_READY` follows the unchanged merge protocol. |
| Enforced by | `conductorctl contract-lint completion`; CI action on pull requests; `scripts/merge_preflight.sh`. |
| Human involvement | Mandatory countersign. Second and last human authority point per run. |
| Replaces | Stage I2 Purple Audit, PACK_AUDIT_REPORT, execution closeout JSON (its fields fold into the Statement of Completion), Mission Completion Report for single runs. |

### Gate boundary rule

A gate boundary exists only where a human must exercise authority (G1, G3) or where autonomy needs a hard envelope to run inside (G2 entry). No boundary exists to compensate for model weakness. The per-boundary classification that produced this rule is in `02_BOUNDARY_AND_CHECK_MAPPING.md`.

## 4. Run layout

```
docs/Conductor/runs/<RUN_ID>/
  intent_pack.json                 Layer 1, schema-validated
  EXECUTION_MODE.txt               PLANNING_ONLY | EXECUTION_ENABLED (unchanged semantics)
  verification_manifest.yaml       v2: checks + result blocks
  receipts/<CHECK_ID>.json         runner-produced, never agent-authored
  postimage/                       protected-root pre/post digests and compare result
  statement_of_completion.json     G3 artifact
  gap_requests/<GAP_ID>.json       optional, returns to product-context lane
  countersign/INTENT_LOCK.json     human-written
  countersign/EXECUTION_GO.json    human-written, EXECUTION_ENABLED only
  countersign/COMPLETION.json      human-written
  notes/                           free-form agent working notes; not linted, not authority
```

Everything an agent writes is either schema-validated or explicitly labeled non-authority (`notes/`). There is no free-form handoff document that can carry a claim.

## 5. Proposed repository tree (target state)

Internal identifier rename (`Factory` → `Conductor` in paths and CLI) is Open Question 1. The tree below shows the target names; the migration sequence in 06 stages the rename.

```
.
├── AGENTS.md                         composed: <!-- conductor:managed --> block + project-owned block
├── CLAUDE.md                         "@AGENTS.md" bridge (unchanged)
├── docs/
│   ├── PROJECT_STATE.md              mandatory read 1 of 2
│   ├── ROADMAP.md · CHANGELOG.md
│   └── Conductor/
│       ├── INVARIANTS.md             mandatory read 2 of 2: principle, Hard Guardrails (verbatim),
│       │                             SIMPLE-CODE-GATE v2 (verbatim), lane summary, autonomy block
│       ├── GATES.md                  G1/G2/G3 reference (on demand)
│       ├── MERGE_PROTOCOL.md         unchanged
│       ├── contracts/                JSON Schemas (see 03 and schemas/)
│       ├── templates/                intent_pack, statement_of_completion, gap_request, project_config,
│       │                             verification_manifest_v2, countersign files
│       ├── adapters/
│       │   ├── claude-code.md · codex.md · cursor.md
│       │   └── bmad/                 LANE_POLICY.md, BMAD_POLICY.md (rewritten on lanes), legacy-evidence/
│       ├── modules/                  optional, not pilot scope: mission-mode/, kilo/, product-owner/,
│       │                             task-memory/, agent-loop-bridge/, cartographer/
│       ├── onboarding/               GUIDE.md, FIRST_EXERCISE.md, FRICTION_LOG_TEMPLATE.md, INSTALL.md
│       ├── DESIGN_PACK/              this pack (archived after build)
│       └── runs/<RUN_ID>/            see §4
├── scripts/
│   ├── conductorctl                  contract-lint {intent|execution|completion} · receipts · postimage ·
│   │                                 doctor · context-index (optional)
│   ├── conductor_contract_lint.py    harvested from factory_pack_lint.py + factory_execution_closeout.py
│   ├── conductor_receipts.py         new: runner that executes manifest checks and writes receipts
│   ├── conductor_postimage.py        harvested from the MS-01 protected-postimage comparison
│   ├── factory-python                bytecode guard (keep, rename later)
│   ├── merge_preflight.sh            unchanged
│   └── build_plugins.py              merged from the two build scripts
├── plugin-src/
│   ├── conductor/                    skills: doctor, adopt (greenfield+brownfield), run, validate, progress, update
│   └── conductor-bmad/               runtime (lane policy), hooks, skills: doctor, audit, bootstrap, promote, intake, gap
├── plugins/                          generated (Claude + Codex for both plugins)
├── .github/workflows/
│   └── conductor-contract-lint.yml   G3 enforcement at the merge boundary
└── tests/
    ├── golden_packs/                 archived RUN_20260902_0725 and RUN_20260903_1750 packs; must keep linting
    └── ...
```

## 6. What is preserved verbatim

- Hard Guardrails (AGENTS.md §3) and SIMPLE-CODE-GATE v2 (§3.1): moved into `INVARIANTS.md` byte-for-byte.
- Merge protocol and `merge_preflight.sh`.
- BMAD snapshot promotion, immutability, supersession, and rollback semantics.
- Installation state, ownership classes, transaction receipts, exact-plan-ID approval.
- Protected-path baseline test and the no-bytecode guard.
- Fail-closed reason-code style (`CONDUCTOR_*`, renamed from `FACTORY_*` in the rename step).

## 7. Autonomy contract block (Layer 1 → AGENTS.md managed section)

Composed from the two vendor blocks the brief verifies (§3 rows 2, 3, 6). Loaded for every G2 run:

```
You are operating under Conductor governance. The Intent Pack sets the scope and the scope is the deliverable:
do not narrow, widen, or swap it. For reversible actions inside the locked intent, proceed without asking.
Stop only for a destructive action, a genuine scope change, or input only a human can provide; record such a
stop as a Gap Request, not as a question in chat. Before reporting progress, audit each claim against a receipt
from this run; report only what a receipt proves, and say explicitly what is not yet verified. Before ending
your turn, check your last paragraph: if it is a plan, a question, or a promise, do that work now. Implement
the smallest clear change (SIMPLE-CODE-GATE v2 applies). Do not write tests for reversible, low-impact changes
beyond what the verification manifest requires.
```
