<div align="center">

# Factory

### Governed software delivery for AI coding agents

Lock intent with a human, let the agent run, and accept nothing as done
without a receipt. Three gates, deterministic validators, no choreography.

[![Release](https://img.shields.io/badge/release-0.3.4--pilot-4f46e5)](#release-status)
[![Claude Code CLI](https://img.shields.io/badge/Claude_Code_CLI-pilot-D97757)](#install)
[![Codex](https://img.shields.io/badge/Codex-packaged-111827?logo=openai&logoColor=white)](#install)
[![License](https://img.shields.io/badge/license-Apache--2.0-0f766e)](LICENSE)

[What it governs](#what-factory-governs) ·
[Three gates](#three-gates) ·
[Install](#install) ·
[First hour](#first-hour) ·
[Upstream tools](#upstream-tools-and-lanes) ·
[Documentation](#documentation)

</div>

Factory 0.3 is the third generation of this repository's governed delivery
process. Earlier Factory releases took AI-assisted work through explicit scope,
adversarial review, verification, and human approval, and were designed for
models that needed small supervised steps. Current frontier models run long
tasks well with little procedural guidance, and their vendors now document
that skills written for earlier models are often too prescriptive. Factory 0.3
keeps everything that was durable, the validators, the guardrails, the merge
protocol, the evidence model, and removes the stage-by-stage choreography that
existed to compensate for weaker models.

The 0.3 line was designed under the working name **Conductor**, which survives
as the plugin id and command namespace (`conductor`, `conductor-bmad`,
`/conductor:...`, `conductorctl`) and in the `docs/Conductor/` tree. The
product is Factory.

## What Factory governs

Less supervision is not less governance. The vendors say so themselves:
OpenAI reports that its newest model's written reasoning is harder to monitor
than its predecessor's, and Anthropic reports that instructing the model to
audit its progress claims against actual tool results nearly eliminated
fabricated status reports. So Factory trusts the model with the *how* and
never with the *proof*. It governs exactly three things:

| Authority | Proof | Write boundary |
| --- | --- | --- |
| A human locks intent and countersigns completion against an exact SHA-256. Nothing proceeds on a draft. | Every completion claim points to a receipt written by the runner, never by the agent. The Statement of Completion's state is computed by lint, not asserted. | Protected paths are digested before and after the run. A changed protected file blocks. |

Everything in between, ordering, decomposition, self-review, is the agent's
job. Instruction prose is soft in every harness; only schemas, validators,
hooks, and CI are hard, and Factory puts every rule that must hold in the
hard layer.

## Three gates

```
G1 Intent Lock ──(human countersign)──▶ G2 Governed Execution ──(receipts, postimage)──▶ G3 Review + Completion ──(human countersign)──▶ REVIEW_READY
```

- **G1 Intent Lock.** The agent drafts `intent_pack.json`: goal, requirements
  with acceptance, constraints, scope in and out, sources with digests,
  verification requirements, model and effort. `conductorctl contract-lint
  intent` must pass. A human writes `countersign/INTENT_LOCK.json`.
- **G2 Governed Execution.** One autonomous run inside the locked scope.
  Declared checks run through `conductorctl receipts run`, which writes signed
  receipts; `conductorctl postimage capture` and `compare` prove no protected
  file changed. Manual checks are attested by a human.
- **G3 Adversarial Review and Completion.** A fresh-context verifier that did
  not do the work audits every claim against its receipt. The Statement of
  Completion maps every requirement to evidence; `contract-lint completion`
  derives READY, BLOCKED, or NEEDS_HUMAN_DECISION. A human countersigns. Merge
  authorization then follows the merge protocol, unchanged from Factory.

Questions only a human can answer become Gap Requests
(`conductorctl gap open`), not chat questions. A gap whose resolution
supersedes active scope reopens G1 instead of drifting it.

## Install

One command per harness. The marketplace is this repository.

**Claude Code CLI** (pilot surface):

```bash
claude plugin marketplace add EduardoRemedios/factory-starter-kit
claude plugin install conductor-bmad@factory-starter-kit   # pulls conductor as a dependency
```

Install `conductor@factory-starter-kit` alone if your repository has no
upstream product-context tool.

**Codex desktop app:** the repository ships `.agents/plugins/marketplace.json`;
select the `factory-starter-kit` source in the Plugins Directory and install
`conductor`. **Cursor:** nothing to install; Cursor reads the `AGENTS.md`
managed block that adoption writes. Both are packaged but not yet part of the
pilot's verified surface.

Then, inside the repository: `/conductor:doctor` tells you the one next legal
action. Adoption (`/conductor:greenfield` or `/conductor:brownfield`) previews
first and applies only by quoting the exact plan ID. An existing `AGENTS.md`
or `CLAUDE.md` is never overwritten: your guide is preserved byte for byte
under a small managed block, and `CLAUDE.md` becomes a one-line bridge.

Requirements: macOS, Git, Python 3.11 or newer, and
`python3 -m pip install -r requirements.txt` in the adopted repository.

## First hour

1. `docs/Conductor/onboarding/INSTALL.md`
2. `docs/Conductor/onboarding/GUIDE.md`, one page
3. `docs/Conductor/onboarding/FIRST_EXERCISE.md`, about 45 minutes through all
   three gates with expected outputs at every step, including a deliberate
   receipt tamper so you see the hard layer refuse it
4. `docs/Conductor/onboarding/FRICTION_LOG_TEMPLATE.md`, one line per "what
   now?" moment; that log decides the next release

## Upstream tools and lanes

Teams that develop product context in an upstream tool install its adapter
alongside Factory. The BMAD adapter (`conductor-bmad`) expresses policy by
responsibility, not per workflow:

- **Product-context lane, open:** research, brief, PRD, UX, architecture,
  spec, persona agents, and helpers such as reviews, editorial passes,
  advanced elicitation, and party mode. Helpers nest freely.
- **Delivery lane, closed for Factory-bound work:** stories, sprints,
  dev-story, quick-dev, loop, code review, QA automation, CI.
- Unknown workflows are denied by default. The hook judges the skill being
  invoked, not its parent, so party mode cannot reach dev-story.
- A denial is one line: reason code, lane, layout state, what is still
  allowed, and the next command.
- The BMAD installation can stay where it is: declare its root in
  `docs/Conductor/PROJECT_CONFIG.json`. Legacy trees are inert evidence, never
  a second active root.

Upstream output has no Factory authority until a human promotes it to an
immutable, hash-pinned snapshot, and even then G1 may accept, reject, or
defer it. Details: `docs/adapters/bmad/BMAD_POLICY.md` and
`docs/adapters/bmad/FIRST_EXERCISE_WITH_BMAD.md`.

## Release status

Current pilot candidate: **Factory 0.3.4** on `main`, tag
`conductor-v0.3.4-pilot`. The 0.2 line closed at `factory-lineage-v0.2.5`.
Repositories with a 0.2-era install migrate
through `/conductor:update`, which plans the path move, refreshes untouched
seeds, composes a customised `AGENTS.md`, and writes a rollback receipt.

Verified so far: the full test suite (contracts, golden Factory packs, gate
lints, receipts, lanes, adoption and update lifecycles), the GitHub
marketplace install path, and a rehearsal on a real brownfield repository with
a nested BMAD installation through all three gates. Not yet verified: live
hook behaviour in an interactive Claude Code session, the Codex desktop app,
and Cursor.

## Repository map

```
docs/Conductor/INVARIANTS.md        the second of the two mandatory reads
docs/Conductor/contracts/           JSON Schemas for every artifact Conductor validates
docs/Conductor/templates/           templates that validate against them
docs/Conductor/onboarding/          install, guide, first exercise, friction log
docs/Conductor/DESIGN_PACK/         why 0.3 is shaped this way, and the rehearsal results
docs/Conductor/MERGE_PROTOCOL.md    merge authorization, unchanged
docs/adapters/bmad/                 BMAD adapter policy, lane contract, exercises
scripts/conductorctl                contract-lint · receipts · postimage · gap · pack-lint (0.2-era runs)
plugin-src/conductor{,-bmad}/       authored plugin sources; plugins/ are generated
tests/golden_packs/                 qualified 0.2-era runs that must keep linting
```

The 0.2-era process documents (`ORCHESTRATION.md`, `Spec/STAGE_CONTRACTS.md`, the
stage templates) remain in the tree for the archived runs and are scheduled
for retirement after the pilot.

## Development and verification

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests
bash scripts/knowledge_lint.sh
python3 scripts/build_conductor_plugins.py --check
python3 scripts/build_conductor_bmad_plugins.py --check
bash scripts/merge_preflight.sh
```

Plugin packages under `plugins/` are generated; edit `plugin-src/` and
rebuild. Pull requests that touch a 0.3 run trigger
`.github/workflows/conductor-contract-lint.yml`.

## Documentation

- `docs/Conductor/onboarding/GUIDE.md`: Factory 0.3 in one page
- `docs/Conductor/DESIGN_PACK/README.md`: design pack index
- `docs/Conductor/DESIGN_PACK/08_REHEARSAL_RESULTS.md`: what was proven and what was not
- `docs/onboarding/`: plugin reference, troubleshooting, and rollback, still valid for lifecycle operations
- `docs/CHANGELOG.md` and `docs/PROJECT_STATE.md`

## License

Apache-2.0. See `LICENSE`.
