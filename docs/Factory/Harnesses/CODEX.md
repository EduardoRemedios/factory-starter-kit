# Codex Harness Adapter

## Version
v0.1

## Change Log
- v0.1 (2026-04-26): Initial Codex adapter for GPT-5.5 local work, Codex App/Desktop, Codex CLI, Codex Cloud, skills, plugins, hooks, and connector-backed evidence.

## Purpose

Use this adapter when running Factory with Codex App/Desktop, Codex CLI, Codex Cloud, the Codex IDE extension, or GitHub PR review.

This adapter may tune Codex behavior. It must not change the Factory Core stage contracts.

## Model Routing

Recommended default for local Codex Factory work:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
model_verbosity = "medium"
```

Use `gpt-5.5` for:
- Stage A intent hardening
- Purple gates
- architecture and migration planning
- cross-run synthesis
- execution prompt generation
- complex implementation work after human Go

Use lower-cost or faster local models only when the task is routine and bounded:
- formatting
- mechanical docs updates
- narrow test fixes
- small grep-and-patch changes

Important current limitation:
- Codex cloud tasks and code review currently run on `GPT-5.3-Codex`, not `gpt-5.5`.
- Do not claim local GPT-5.5 parity for cloud tasks or PR review unless that is re-verified in current Codex docs.

## Local Factory Profile

Project-scoped `.codex/config.toml` may be used in adopting repos after trust is established.

Suggested local profile:

```toml
model = "gpt-5.5"
model_reasoning_effort = "high"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[features]
multi_agent = true
codex_hooks = true
apps = true
```

Use `approval_policy = "never"` only for non-interactive CI-style checks that cannot require human intervention.

## Codex CLI Terminal Flow

Use Codex CLI when:
- you want a terminal-native Factory run
- you need repeatable validator commands
- the work will be driven by shell scripts, CI-like gates, or local automation
- the repo is on Linux or a remote development host
- you want an easy transcript of commands and outputs

Recommended CLI posture:

```bash
codex --cd /path/to/repo
```

For a Factory run, start with a prompt that names the run mode and asks Codex to load the repo contract:

```text
Read AGENTS.md, docs/Factory/ORCHESTRATION.md, and docs/Factory/SCRATCHPAD.md Active Pitfalls.
Run bash scripts/knowledge_lint.sh before initializing Stage A.
Keep this run PLANNING_ONLY unless I explicitly authorize EXECUTION_ENABLED.
```

CLI run checklist:
1. `bash scripts/knowledge_lint.sh`
2. `./scripts/factoryctl context-index`
3. `./scripts/factoryctl context-report --profile stage-a --scope <RUN_ID> --output docs/Factory/runs/<RUN_ID>/CONTEXT_RECALL_REPORT.md`
4. run stages `A -> I2`
5. `./scripts/factoryctl pack-lint --run <RUN_ID>`

For unattended or scripted validation, use the CLI only for deterministic checks:

```bash
bash scripts/knowledge_lint.sh
./scripts/factoryctl pack-lint --run <RUN_ID>
```

Do not use unattended CLI execution for scope decisions, intent unlocks, or human Go authorization.

## Factory Stage Mapping

| Factory Work | Codex Surface | Model / Mode | Notes |
|---|---|---|---|
| Stage A through I2 full planning pack | App/Desktop local or CLI | `gpt-5.5`, high reasoning | Preferred path for full Factory runs |
| Pack validation | CLI or local terminal in App/Desktop | deterministic scripts | Run `knowledge_lint`, context report, and `pack-lint` |
| Execution after human Go | App/Desktop local, CLI, IDE, or Cloud | local `gpt-5.5` where available; Cloud uses its configured model | Pass the execution envelope explicitly |
| PR review | GitHub/Codex review | current Codex review model | Review against pack, checklist, tests, and merge gate evidence |
| Background implementation | Codex Cloud | current Codex cloud model | Use only after pack completion and explicit execution authorization |

## Skills

Create Factory skills when the workflow is repeatable and narrow.

Highest-value generic skills:
- `factory-root-planner`
- `factory-intent-contractor`
- `factory-purple-gate`
- `factory-pack-consolidator`
- `factory-execution-closeout`

Skill rules:
- one skill per job
- clear trigger phrases in the description
- required inputs and outputs listed explicitly
- optional scripts only when they improve reliability
- repo-specific skills live in `.agents/skills`
- personal cross-repo skills live outside the repo

Factory Starter Kit should contain only generic skills. Product or customer-specific skills belong in the adopting repo.

## Plugins And Apps

Use plugins when the workflow needs bundled skills, app integrations, or MCP servers.

Useful generic plugin categories:
- GitHub for issues, PRs, review comments, and CI status
- Slack or Gmail for decision recall and follow-up drafting
- browser testing for UI verification
- docs or drive connectors for requirement source material

Connector rules:
- connectors provide evidence, not authority
- summarize decisions into Factory artifacts
- cite source paths, threads, or PRs where practical
- do not paste private connector data into this public starter kit

## Hooks

Hooks are useful for deterministic Factory guardrails.

Recommended hook opportunities:
- `SessionStart`: remind Codex to read `AGENTS.md` and Factory read order
- `UserPromptSubmit`: warn on execution requests without `EXECUTION_ENABLED`
- `PreToolUse`: block destructive shell commands unless explicitly approved
- `PostToolUse`: flag failed validator output immediately
- `Stop`: require unresolved Factory defects to be reported before ending a turn

Starter example:

```toml
[features]
codex_hooks = true

[[hooks.PostToolUse]]
matcher = "^Bash$"

[[hooks.PostToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/factory_post_tool_use.py"'
timeout = 30
statusMessage = "Checking Factory command output"
```

Hook caveats:
- hooks are guardrails, not complete enforcement boundaries
- multiple matching hooks can run concurrently
- project-local hooks require the project `.codex/` layer to be trusted
- keep hook scripts in the adopting repo, not in Factory Core, until the pattern is proven generic

## Multi-Agent Use

Use multi-agent work only when subtasks are independent and outputs can be reviewed against the same Factory artifacts.

Good candidates:
- one agent inspects tests while another updates docs
- one agent reviews the pack while another prepares implementation notes
- one agent researches external evidence while the main agent edits artifacts

Bad candidates:
- splitting a single locked artifact across agents
- letting agents create competing sources of truth
- delegating a stage gate without shared inputs and explicit exit criteria

All sub-agent results must be integrated by the owner of the Factory run.

## Cloud And GitHub Review

Codex Cloud is useful after Factory planning is complete.

Before sending work to Cloud:
1. `pack-lint` passes.
2. Human Go is explicit.
3. `EXECUTION_MODE.txt` is `EXECUTION_ENABLED`.
4. The cloud task prompt includes the execution envelope, micro-sprints, verification plan, file-touch budget, and stop/go rules.

For PR review:
- ask review to compare the diff against the pack and verification plan
- require evidence paths for claimed compliance
- do not treat PR review as a substitute for project tests or merge preflight

## External Signals

High-signal inputs for Codex-assisted Factory decisions:
- open issues linked to the sprint goal
- recent PRs touching planned files
- failing CI checks
- support or incident summaries
- customer or stakeholder decisions captured in Slack or email
- product analytics or observability summaries, when relevant

Factory artifacts should record:
- what was confirmed
- what was inferred
- what remains blocking
- which external sources were consulted

## Source Notes

Checked against official OpenAI docs on 2026-04-26:
- Codex setup surfaces: https://developers.openai.com/codex/quickstart
- Codex config keys including `model`, `model_reasoning_effort`, apps, hooks, skills, and multi-agent flags: https://developers.openai.com/codex/config-reference
- Hooks behavior and event support: https://developers.openai.com/codex/hooks
- Plugin composition: https://developers.openai.com/codex/plugins
- Skill authoring and progressive disclosure: https://developers.openai.com/codex/concepts/customization
- Current model availability and cloud/review model note: https://developers.openai.com/codex/pricing
