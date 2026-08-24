<div align="center">

# Factory

### Governed software delivery for AI coding agents

Turn rough product intent into an execution-ready contract, with scope, risk,
verification, human approval, and delivery evidence built into the workflow.

[![Release candidate](https://img.shields.io/badge/release-0.2.5--cli--pilot-4f46e5)](#release-status)
[![Codex](https://img.shields.io/badge/Codex-supported-111827?logo=openai&logoColor=white)](#chatgpt--codex-desktop-app-on-macos)
[![Claude Code CLI](https://img.shields.io/badge/Claude_Code_CLI-pilot_supported-D97757)](#claude-code-cli)
[![License](https://img.shields.io/badge/license-Apache--2.0-0f766e)](LICENSE)

[Why Factory](#why-factory) ·
[How it works](#how-factory-works) ·
[Install](#install-factory) ·
[Quick start](#quick-start-your-first-repository) ·
[Developer FAQ](#developer-faq) ·
[Documentation](#documentation)

</div>

Factory gives engineering teams a repeatable way to plan, challenge, authorize,
and verify AI-assisted software work before implementation begins. It combines
contract-grade intent, adversarial review, risk analysis, executable
verification, and human approval in one repository-native workflow.

Built for teams that want the speed of coding agents without surrendering
engineering control.

## Why Factory?

AI coding tools can produce code quickly. Reliable delivery still depends on
knowing what is authorized, what must not change, which risks matter, how the
result will be tested, and who can approve execution.

Factory makes those decisions explicit and reviewable.

| Controlled scope | Adversarial review | Evidence-first delivery | One portable core |
| --- | --- | --- | --- |
| Lock intent, constraints, non-goals, and acceptance criteria before code changes. | Red, Blue, and Purple responsibilities challenge assumptions and resolve disagreements. | Deterministic validators and project-native tests turn completion claims into inspectable proof. | The same Factory contracts work through Codex and Claude Code, with tool-specific adapters. |

Factory is not a code generator, test framework, CI service, security scanner,
or replacement for engineering judgment. It is the process, evidence, and
authorization layer that coordinates those capabilities.

## Release Status

The current Claude Code CLI pilot candidate is `0.2.5` on `main`.

- Factory Core is the existing, portable process.
- The plugin is a distribution and lifecycle layer around that core.
- Codex and Claude Code packages are generated from one authored source.
- The initial verified rollout surface is macOS with Claude Code CLI.
- Factory-BMAD is the companion path for teams that use BMAD upstream and
  Factory downstream in one repository.
- Claude Desktop remains unsupported until a separate Desktop validation lane
  passes.
- Greenfield, brownfield, update, and rollback operations are preview-first and
  require approval of an exact plan ID before repository files are changed.

The plugin does not introduce a second Factory implementation.

## The delivery questions Factory answers

AI coding agents are good at producing code, but a repository still needs
answers to engineering questions that are larger than code generation:

- What exactly is authorized?
- What is explicitly out of scope?
- Which constraints and risks must survive implementation?
- What evidence will prove the result?
- Which checks are mandatory?
- Who decides whether execution can begin?
- How can another developer reconstruct what happened?
- What happens when repository state contradicts a status report?

Factory answers them with versioned artifacts, deterministic validators,
adversarial review, explicit authorization, and an evidence-backed closeout.

## How Factory Works

```text
Brief → Intent → Challenge → Risk → Verification → Plan → Human Go → Execute → Prove
```

The canonical planning sequence is:

```text
A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2
```

In practical terms:

1. Convert the raw brief into contract-grade intent.
2. Red-team and harden the intent.
3. Lock scope, constraints, non-goals, and acceptance criteria.
4. Run a premortem and build the risk register.
5. Design fixtures, verification tiers, and traceability.
6. Sequence bounded micro-sprints.
7. Produce and attack the execution envelope.
8. Consolidate and deterministically audit the pack.
9. Stop for human Go or No-go.
10. Execute only the approved scope and preserve verification evidence.

Every stage handoff can be validated immediately. The final pack must pass
`pack-lint` before it is presented for execution approval.

## Install Factory

Factory has two layers: install the plugin once in your AI coding client, then
initialize Factory separately in each repository. This keeps reusable workflow
logic centrally updatable while project rules, tests, decisions, and evidence
remain with the codebase.

Choose your client:

| Client | Installation surface | First repository check |
| --- | --- | --- |
| ChatGPT / Codex desktop | macOS Terminal, then a new Codex task | `$factory-doctor` |
| Claude Code CLI, Factory only | Terminal | `/factory:doctor` |
| Claude Code CLI, BMAD + Factory | Terminal | `/factory-bmad:doctor` |
| Claude Desktop | Pending validation | Do not pilot yet |

### ChatGPT / Codex desktop app on macOS

The Factory plugin runs in **Codex** or **ChatGPT Work**, not a normal ChatGPT
Chat conversation.

1. Update and restart the ChatGPT desktop app.
2. Open Terminal.
3. Clone this repository at the approved pilot commit or branch, then register
   that durable local checkout and install the plugin:

   ```bash
   git clone https://github.com/EduardoRemedios/factory-starter-kit.git
   cd factory-starter-kit
   git checkout main

   /Applications/ChatGPT.app/Contents/Resources/codex \
     plugin marketplace add "$PWD"

   /Applications/ChatGPT.app/Contents/Resources/codex \
     plugin add factory@factory-starter-kit
   ```

4. Quit and reopen the ChatGPT app so it loads the installed skills.
5. Select **Codex**, create a new task, and choose the repository folder.
6. In the agent prompt, type:

   ```text
   $factory-doctor
   ```

7. Follow Doctor's `next_legal_action`. For an existing repository this will
   normally lead to `$factory-brownfield`; for an empty repository it will lead
   to `$factory-greenfield`.

The app-bundled executable is used above because a different, older `codex`
binary may appear earlier on `PATH`. If `codex plugin --help` works in your
terminal, the shorter equivalent is:

```bash
codex plugin marketplace add EduardoRemedios/factory-starter-kit \
  --ref main
codex plugin add factory@factory-starter-kit
```

You can inspect installed plugins in the desktop app under **Plugins**. Plugin
skills are loaded into new tasks.

### Claude Desktop

Claude Desktop is not part of the current supported pilot. Do not roll Factory
or Factory-BMAD into a Desktop team workflow until the separate Desktop
validation lane passes.

### Claude Code CLI

1. Update Claude Code and verify the installed version:

   ```bash
   claude update
   claude --version
   ```

2. Clone this repository into a durable local path:

   ```bash
   mkdir -p "$HOME/Code"
   git clone https://github.com/EduardoRemedios/factory-starter-kit.git \
     "$HOME/Code/factory-starter-kit"
   cd "$HOME/Code/factory-starter-kit"
   git checkout main
   ```

3. Run the read-only rollout preflight:

   ```bash
   ./scripts/factory-python scripts/verify_factory_cli_rollout.py \
     --marketplace-root "$PWD" \
     --target-root /path/to/your/repository \
     --json
   ```

   Stop on `BLOCKED`.

4. Add the marketplace and install Factory for your user account:

   ```bash
   claude plugin marketplace add "$PWD"
   claude plugin install factory@factory-starter-kit --scope user
   ```

5. Change to the repository you want to use and start Claude Code:

   ```bash
   cd /path/to/your/repository
   claude
   ```

6. In the Claude Code session, run:

   ```text
   /reload-plugins
   /factory:doctor
   ```

Use `--scope project` instead of `--scope user` only when the repository team
has intentionally chosen a project-scoped plugin declaration.

### Claude Code CLI with BMAD and Factory

For teams using BMAD and Factory together, install only the companion. It
declares Factory `~0.2.5` as its protected dependency.

```bash
cd "$HOME/Code/factory-starter-kit"
claude plugin marketplace list
# If factory-starter-kit points at an old or missing path:
# claude plugin marketplace remove factory-starter-kit
claude plugin uninstall factory-bmad@factory-starter-kit
claude plugin uninstall factory@factory-starter-kit
claude plugin prune
./scripts/factory-python scripts/verify_factory_bmad_cli_rollout.py \
  --marketplace-root "$PWD" \
  --target-root /path/to/team/repository \
  --json
claude plugin marketplace add "$PWD"
claude plugin install factory-bmad@factory-starter-kit --scope user
```

If the rollout preflight reports a `claude_cache_*` blocker, remove only the
stale `~/.claude/plugins/cache/factory-starter-kit` directory and rerun the
preflight before installing. `claude plugin prune` may leave cached payload
directories on disk.

Start Claude Code in the target repository and run:

```text
/reload-plugins
/factory-bmad:doctor
```

Follow only the single `next_legal_action` returned by Doctor. Every setup or
bootstrap action previews first and must be approved by quoting the exact full
current plan ID.

### Confirm the installation

Successful installation only makes the commands available. Doctor is the
read-only compatibility check for the current repository:

```text
# Codex
$factory-doctor

# Claude Code CLI
/factory:doctor
```

Do not start by copying Factory files manually. Let Greenfield or Brownfield
produce the exact setup plan for the repository.

## First Tester Handoff

For Factory-only testing, use the Factory-only Claude Code CLI path and keep the
scope deliberately small. The goal is to validate installation, discovery,
Greenfield setup, Doctor, Validate, Progress, and the human approval flow.

Use the handoff checklist in
[`docs/onboarding/FACTORY_FIRST_TESTER_HANDOFF.md`](docs/onboarding/FACTORY_FIRST_TESTER_HANDOFF.md).
The tester should preserve the preflight JSON, Claude version, plugin list,
Doctor/Validate/Progress output, final `git status --short`, and a short
friction log.

For BMAD + Factory testing, use
[`docs/adapters/bmad/FACTORY_BMAD_FIRST_TESTER_HANDOFF.md`](docs/adapters/bmad/FACTORY_BMAD_FIRST_TESTER_HANDOFF.md)
and
[`docs/adapters/bmad/FACTORY_BMAD_CLI_ROLLOUT_PLAYBOOK.md`](docs/adapters/bmad/FACTORY_BMAD_CLI_ROLLOUT_PLAYBOOK.md).

## Quick Start: Your First Repository

Installing the plugin makes Factory available globally. Each repository still
needs its own Factory Core, project adapter, and evidence history.

Start with Doctor:

```text
# Codex
$factory-doctor

# Claude
/factory:doctor
```

For a new repository containing nothing except `.git`:

```text
$factory-greenfield
/factory:greenfield
```

For any existing repository:

```text
$factory-brownfield
/factory:brownfield
```

Greenfield and brownfield return an exact per-file plan before writing. Review
that plan and approve its full plan ID. A generic "approve" is not sufficient.

After setup:

```text
$factory-validate
$factory-progress
$factory-run
```

Use the `/factory:...` equivalents in Claude Code.

## Plugin Commands

| Journey | Codex | Claude Code | Repository writes |
| --- | --- | --- | --- |
| Diagnose installation | `$factory-doctor` | `/factory:doctor` | Never |
| Set up an empty repository | `$factory-greenfield` | `/factory:greenfield` | Preview and exact approval |
| Adopt an existing repository | `$factory-brownfield` | `/factory:brownfield` | Preview and exact approval |
| Inspect run state | `$factory-progress` | `/factory:progress` | Never |
| Continue the next legal action | `$factory-run` | `/factory:run` | State-dependent |
| Run applicable validators | `$factory-validate` | `/factory:validate` | Validator evidence only |
| Update or roll back | `$factory-update` | `/factory:update` | Preview and exact approval |

## Design Principles

- **Intent before implementation.** Code is downstream of reviewed scope,
  constraints, risks, and acceptance criteria.
- **Evidence over status prose.** Disk state and validator output outrank a
  narrative claim of success.
- **Fail closed.** Missing authorization, contradictory evidence, failed
  checks, weak recall, or unresolved scope halts the workflow.
- **Human authority is explicit.** A completed plan is not permission to
  execute it.
- **Project-native engineering remains authoritative.** Factory invokes the
  repository's actual tests, linters, security checks, and merge preflight.
- **One portable core, multiple harnesses.** Codex and Claude use the same stage
  contracts and repository instructions.
- **No silent replacement of project-owned files.** Brownfield adoption
  preserves existing instructions and halts on ambiguous ownership.

## Developer FAQ

### Is Factory a rewrite of the development process?

No. Factory Core remains the source of the stage contracts, roles, artifacts,
validators, and authorization rules. The Codex and Claude plugins add
installation, discovery, safe project adoption, update, rollback, and
human-friendly entry points.

The packages are deterministically generated from `plugin-src/factory/`.

### Does Factory have skills, agents, and orchestration?

Yes. Factory defines Root Planner, Intent Contractor, Red Team, Blue
Team/Synthesis, Purple Gate, Risk Analyst, Verification Specialist, Sprint
Planner, Envelope Author, Pack Consolidator, and Execution Closeout
responsibilities.

Repository-scoped skills implement the major planning, review, consolidation,
and closeout roles. The plugin exposes the public lifecycle journeys without
duplicating those role contracts.

### Does Factory work in Claude Code, or only in Codex?

Both packages use the same Factory Core.

Codex reads the authoritative repository `AGENTS.md`. Claude project setup
previews a one-line `CLAUDE.md` bridge:

```md
@AGENTS.md
```

This gives Claude the same repository read order, coding guardrails, stage
contracts, and validation rules. If a repository already has a different
`CLAUDE.md`, setup reports a conflict for owner review instead of overwriting
it.

### Which models perform Red, Blue, and Purple review?

By default, the selected session model serves all Factory roles. Selecting a
high-capability model for the session therefore applies it to Red, Blue, and
Purple work as well.

Separate per-role routing is an optional harness concern. It is not required
for the review responsibilities or gates to exist.

### Does Factory enforce coding standards?

Yes. Factory-controlled code-changing work is subject to
`SIMPLE-CODE-GATE v2`, which requires:

- the smallest clear, behavior-preserving change;
- no code bloat or awkward multi-purpose abstractions;
- no hidden side effects or brittle boundary mutation;
- no unnecessary dependency growth;
- no swallowed failures or ambiguous fallbacks;
- no speculative frameworks or indirection;
- an explicit reason and verification hook for accepted complexity.

Material violations block execution or closeout under the Factory severity
policy.

Factory intentionally does not hard-code one language's formatter, linter, or
architecture conventions into the portable core. Those belong in the adopting
repository's `AGENTS.md`, project adapter, CI, and merge preflight.

### Does Factory require regression testing?

Yes. Factory defines `V3` as the regression/conformance verification tier. Its
merge protocol requires the project's regression gate to pass without
unexpected failures, and CI should use the same gate where practical.

Factory cannot invent a universal regression command. The adopting repository
must define its canonical unit, integration, end-to-end, smoke, regression,
security, and release checks. Factory plans, invokes, records, and enforces the
applicable checks.

For execution-enabled work, runnable checks can be recorded in
`pack/verification_manifest.yaml`. A check marked `halt_on_failure: true` is a
hard stop.

### Does Factory create specifications and documentation?

Yes. A normal run produces a raw brief, contract-grade intent, adversarial
review, intent synthesis, risk register, verification plan, traceability
matrix, micro-sprint plan, execution envelope, pack manifest, audit report, and
stage handoffs.

The exact artifact set depends on execution mode and which optional lanes are
active.

### Does Factory create `VISION.md`?

No. Factory does not create or require `VISION.md`.

Product vision is upstream, human-owned input from a Product Owner, project
owner, or sponsor. An agent may help structure or challenge it, but must not
invent the vision or claim stakeholder approval.

For greenfield product work, keep the approved vision with the project—for
example as `docs/PRODUCT_VISION.md`—and use it to seed either:

- a human-authored Phase Brief in the optional Product Owner lane; or
- the initial `raw_brief.md` that enters Factory Stage A directly.

The resulting Phase Intent, sprint briefs, and Factory run should remain
traceable to that approved source.

### Are non-functional requirements and constraints handled?

Yes, provided they are supplied or discovered before intent is locked. Factory
records constraints, acceptance criteria, risks, verification coverage, and
scope boundaries in the run pack.

Research, product discovery, regulatory analysis, and stakeholder alignment may
happen upstream. Factory does not pretend that every business or technical
decision must originate inside its pipeline.

### Why keep Factory artifacts in Git instead of only Jira, Confluence, or Notion?

Git provides versioning, reviewable changes, repository-local availability,
and a durable link between the plan, the code, and the verification evidence.
That is an intentional design choice, not an accidental storage limitation.

External systems can remain sources for requirements, research, tickets, and
decisions. A project adapter may connect them through APIs, MCP, export, or
controlled synchronization. Factory still needs a stable, reviewable evidence
boundary for the work it authorizes.

### Is Factory deterministic if the underlying model is probabilistic?

The model's wording and reasoning path are not deterministic. Factory's control
surface is.

Stage order, required files, ownership rules, schema checks, plan identifiers,
version compatibility, stage validation, pack validation, reason codes, and
authorization state are evaluated from deterministic repository evidence.

Factory constrains and checks model output; it does not claim to make a
generative model deterministic.

### Does Factory replace tests, CI/CD, security tools, or release engineering?

No. Factory requires projects to identify and run their real engineering
controls. The portable core cannot know whether a repository uses pytest,
JUnit, Playwright, Xcode, Terraform, a mobile release pipeline, or a regulated
security scanner.

Factory's responsibility is to make the required controls explicit, trace them
to risks and acceptance criteria, stop on mandatory failures, and preserve the
evidence.

### Is Factory too heavy for small changes?

Factory is optimized for work where scope drift, missed constraints, weak
verification, or unclear authorization would be costly. It intentionally adds
more discipline than an unstructured coding prompt.

Planning-only runs can stop after a validated pack. Roles may be collapsed for
smaller teams, but the responsibilities and evidence boundaries remain. A
project should apply ceremony in proportion to consequence without silently
removing mandatory gates.

### Is installing the plugin enough for every project?

The plugin is installed once per user environment. Repository adoption happens
once per project.

That separation is intentional:

- the plugin supplies reusable commands and lifecycle logic;
- Factory Core supplies the portable process;
- the repository supplies project state, engineering commands, domain rules,
  and its own evidence history.

### Is brownfield adoption safe?

Brownfield setup inventories the repository and produces a deterministic
per-file plan. Files are classified as release-owned, project-owned, or
generated/pinned.

Existing project instructions are preserved. Conflicting or ambiguous paths
halt the plan. Nothing is applied until the exact current plan ID is approved,
and a repository change invalidates a stale plan.

### How is Factory different from GSD and BMAD?

The projects overlap, but their primary optimization targets differ:

- [GSD](https://github.com/open-gsd/gsd-core) focuses on developer workflow,
  context engineering, phase execution, verification, and shipping.
- [BMAD](https://docs.bmad-method.org/workflow-map-diagram.html) focuses on a
  role-based product and agile delivery method spanning analysis, planning,
  architecture, stories, and implementation.
- Factory focuses on governed intent, adversarial review, risk, traceability,
  deterministic evidence, explicit execution authority, and auditable
  closeout.

GSD may be a better fit for a developer seeking a lightweight, highly automated
execution loop. BMAD may be a better fit for teams that want familiar
product/agile roles and extensive planning workflows. Factory is designed for
work that needs a controlled answer to:

```text
What was authorized?
What was excluded?
Which risks and constraints were preserved?
Who approved execution?
Which evidence proves the result?
```

This is not a claim that the tools are mutually exclusive. A project can use
specialized planning or execution tools inside an approved Factory boundary if
their behavior, write scope, and evidence are explicitly governed.

### Is prior use of another workflow evidence that it is a better organizational standard?

No. Familiarity and successful local use are useful adoption signals, but they
do not establish superiority for a different operating context.

An organizational comparison should pin exact versions and run the same
repository, brief, model, constraints, acceptance criteria, test suite, time
budget, and scoring rubric through each candidate. Installation polish should
be scored, but it should not be confused with scope control, verification, or
auditability.

### What should a fair comparison measure?

At minimum:

1. requirements and scope accuracy;
2. architecture rationale;
3. risk and NFR coverage;
4. code quality and regression results;
5. traceability and audit evidence;
6. authorization and change control;
7. context continuity;
8. onboarding and usability;
9. elapsed time and token consumption;
10. final delivery quality.

## Repository Architecture

Factory separates reusable process from project-specific state:

1. **Factory Core** — stage contracts, templates, execution rules, Product
   Owner lane, Mission Mode, and pack audit.
2. **Harness adapters** — Codex, Claude, and other tool-specific invocation.
3. **Validators** — deterministic checks for artifacts, evidence, and state.
4. **Extension packs** — optional skills and integrations.
5. **Project adapters** — repository-owned instructions, tests, domain rules,
   state, roadmap, and change history.

See [`docs/Factory/ARCHITECTURE.md`](docs/Factory/ARCHITECTURE.md).

## Repository Map

```text
factory-starter-kit/
├── .agents/plugins/                 # Codex marketplace
├── .claude-plugin/                  # Claude marketplace
├── plugin-src/factory/              # authored plugin source
├── plugins/
│   ├── factory/                     # generated Codex package
│   └── factory-claude/              # generated Claude package
├── AGENTS.md                        # authoritative repository instructions
├── docs/
│   ├── PROJECT_STATE.md
│   ├── ROADMAP.md
│   ├── onboarding/
│   └── Factory/
│       ├── ARCHITECTURE.md
│       ├── ORCHESTRATION.md
│       ├── MERGE_PROTOCOL.md
│       ├── MISSION_MODE.md
│       ├── ProductOwner/
│       ├── Spec/
│       └── templates/
├── scripts/
│   ├── build_factory_plugins.py
│   ├── factoryctl
│   ├── factory_stage_lint.py
│   ├── factory_pack_lint.py
│   └── knowledge_lint.sh
├── tests/
└── tools/repo_cartographer/
```

Distributable packages intentionally exclude adopter run history, installation
state, private project evidence, and local release artifacts.

## Development and Verification

Install script dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the full repository test suite and package checks:

```bash
bash scripts/knowledge_lint.sh
python3 -m unittest discover -s tests
python3 scripts/build_factory_plugins.py --check
python3 scripts/agent_loop_bridge_validate.py \
  tests/fixtures/agent_loop_bridge/valid_handoff.json --json
```

Validate the platform packages:

```bash
python3 \
  ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py \
  plugins/factory

claude plugin validate --strict plugins/factory-claude
claude plugin validate --strict .claude-plugin/marketplace.json
```

## Documentation

- [OpenAI plugins](https://learn.chatgpt.com/docs/plugins)
- [Claude Desktop docs - pending Factory validation](https://code.claude.com/docs/en/desktop)
- [Claude Code plugin installation](https://code.claude.com/docs/en/discover-plugins)
- [Plugin quick start](docs/onboarding/FACTORY_PLUGIN_QUICK_START.md)
- [First tester handoff](docs/onboarding/FACTORY_FIRST_TESTER_HANDOFF.md)
- [Plugin reference](docs/onboarding/FACTORY_PLUGIN_REFERENCE.md)
- [Pilot runbook](docs/onboarding/FACTORY_PLUGIN_PILOT_RUNBOOK.md)
- [Troubleshooting](docs/onboarding/FACTORY_PLUGIN_TROUBLESHOOTING.md)
- [Rollback](docs/onboarding/FACTORY_PLUGIN_ROLLBACK.md)
- [Factory architecture](docs/Factory/ARCHITECTURE.md)
- [Orchestration](docs/Factory/ORCHESTRATION.md)
- [Stage contracts](docs/Factory/Spec/STAGE_CONTRACTS.md)
- [Coding-quality severity policy](docs/Factory/SIMPLE_CODE_GATE_SEVERITY_POLICY.md)
- [Merge protocol](docs/Factory/MERGE_PROTOCOL.md)

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
