# Factory Plugin Compatibility Matrix

## Version
v2

## Change Log
- v2 (2026-07-24): Recorded strict manifest validation, executable path/worktree conformance, and retained live-loader gates.
- v1 (2026-07-24): Revalidated Claude Code, Codex, and Agent Skills packaging contracts for the initial Factory plugin release.

## Research Contract
- Run: `RUN_20260724_1448_factory_plugin`
- Retrieved: 2026-07-24
- Authority order: official platform documentation, Agent Skills specification, local platform validators, then comparative projects.
- Release revalidation trigger: any platform version change, manifest/marketplace schema change, skill naming change, or failed official validator/loader.

## Compatibility Matrix

| Topic | Codex | Claude Code | Conclusion | Confidence |
|---|---|---|---|---|
| Plugin manifest | `.codex-plugin/plugin.json` | `.claude-plugin/plugin.json` | Separate generated manifests required. | High |
| Skill root | `skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` | Skill bodies can share one authored source. | High |
| Skill metadata | Agent Skills `name` and `description` required; `name` matches directory | Claude accepts `name`/`description`; plugin command uses plugin namespace plus skill name | Generate platform-specific skill names from shared bodies. | High |
| Public invocation | `$conductor-doctor` or implicit matching | `/conductor:doctor` | One unchanged skill tree cannot provide both preferred names. | High |
| Plugin namespace | Component/plugin identifier | Manifest name prefixes plugin skills | Both manifests use plugin name `factory`. | High |
| Local validation | Plugin Creator `validate_plugin.py` passes; Codex app install test retained | Claude plugin and marketplace pass `claude plugin validate --strict`; supported-version invocation retained | Schemas and deterministic semantics pass; live invocation remains a release gate. | High |
| Marketplace | `.agents/plugins/marketplace.json` with policy metadata | `.claude-plugin/marketplace.json` with Claude source schema | Separate marketplace files required. | High |
| Repository guidance | `AGENTS.md` native | `CLAUDE.md`/Claude instructions | Claude setup may create only an `@AGENTS.md` bridge after conflict review. | Medium |
| Update behavior | Marketplace-backed cached install; local development may need cachebuster/reinstall | Marketplace update/install; `/reload-plugins` for development | Keep plugin update separate from project-asset migration. | High |
| Extra integrations | Optional apps/MCP/hooks | Optional MCP/hooks/agents | Excluded from initial release. | High |

## Official Sources

### OpenAI Codex
- URL: https://learn.chatgpt.com/docs/build-plugins
- Source type: Official Codex manual source.
- Retrieved: 2026-07-24.
- Material conclusion: Codex plugins require `.codex-plugin/plugin.json`; skills live at plugin-root `skills/`; plugins are the team distribution surface.
- Revalidation trigger: Codex plugin manifest or marketplace documentation changes.

- URL: https://learn.chatgpt.com/docs/build-skills
- Source type: Official Codex manual source.
- Retrieved: 2026-07-24.
- Material conclusion: Codex skills use Agent Skills-style `SKILL.md`, activate explicitly with `$` or implicitly by description, and require concise names/descriptions.
- Revalidation trigger: Codex skill discovery or invocation behavior changes.

### Anthropic Claude Code
- URL: https://code.claude.com/docs/en/plugins
- Source type: Official Claude Code documentation.
- Retrieved: 2026-07-24.
- Material conclusion: Claude plugins use `.claude-plugin/plugin.json`, root `skills/`, namespaced commands, `--plugin-dir` testing, and `claude plugin validate`.
- Revalidation trigger: Claude plugin structure, validation, or command namespace changes.

- URL: https://code.claude.com/docs/en/plugin-marketplaces
- Source type: Official Claude Code documentation.
- Retrieved: 2026-07-24.
- Material conclusion: Claude marketplaces use `.claude-plugin/marketplace.json`; relative plugin sources start `./`; install flow is marketplace add, plugin install, then reload/restart as documented.
- Revalidation trigger: marketplace source or installation schema changes.

- URL: https://code.claude.com/docs/en/skills
- Source type: Official Claude Code documentation.
- Retrieved: 2026-07-24.
- Material conclusion: plugin skills are namespaced; frontmatter `name` controls the final segment; behavior before Claude Code 2.1.216 differed for plugin frontmatter naming/autocomplete.
- Revalidation trigger: skill namespace or minimum-version behavior changes.

### Agent Skills
- URL: https://agentskills.io/specification
- Source type: Open Agent Skills specification.
- Retrieved: 2026-07-24.
- Material conclusion: `name` and `description` are required; name is lower-case hyphen-case, at most 64 characters, and must match its parent directory.
- Revalidation trigger: specification version or required-field changes.

## Comparative Input
- URL: https://github.com/open-gsd/gsd-core/blob/next/docs/COMMANDS.md
- Source type: Comparative open-source project; non-authoritative.
- Retrieved: 2026-07-24.
- Accepted lesson: expose a small journey-oriented command surface and provide progress/diagnosis.
- Rejected lesson: do not copy the full command catalogue or let commands bypass Factory governance.

## Local Capability Evidence
- Claude Code: `2.1.218`; the supported-version gate is met and live namespaced-command conformance remains to be run.
- Codex app: the generated plugin is installed through the repository marketplace; fresh-task Doctor, Progress, and Brownfield invocation passed.
- Codex CLI: local npm wrapper fails because its native binary is missing; Codex CLI is not part of the initial pilot support claim.
- Python: standard-library implementation is available; existing PyYAML remains available for current Factory validators but is not required by the plugin runtime.
- Claude strict plugin manifest validation: PASS.
- Claude strict marketplace manifest validation: PASS.
- Codex Plugin Creator validation: PASS.
- macOS path with spaces: PASS.
- nested invocation with Git-root resolution: PASS.
- macOS Git worktree root resolution: PASS.
- generated Claude/Codex progress semantics over the same A-to-I2 fixture: PASS.

## Initial Support Boundary
- Supported pilot host: macOS with Git and Python 3.11 or newer.
- Supported Codex surface: Codex app/Desktop with the plugin installed from the repo marketplace.
- Supported Claude surface: Claude Code 2.1.216 or newer after official plugin validation.
- Supported repository: a Git worktree with a resolvable root and writable project scope.
- Paths with spaces, nested invocation, and Git worktrees: verified on the supported macOS host by VM-009.
- Windows and Linux: unverified for the initial pilot; doctor must return `CONDUCTOR_ENVIRONMENT_UNVERIFIED` until VM-009 evidence exists for those environments.
- Codex CLI: unverified for the initial pilot because the current local CLI installation is broken.

## Uncertainties
- Official documents do not jointly guarantee a single physical directory containing both vendor manifests.
- The Codex app has no independent local CLI validator available in the current environment; Plugin Creator validation is the schema gate and app installation is the live gate.
- Claude repository bridge behavior must be verified against the supported Claude version before mutation is enabled.

## Research Verdict
- VM-001: PASS WITH RETAINED LIVE GATES.
- VM-006 deterministic cross-package semantics: PASS.
- VM-009 supported-host path and worktree checks: PASS.
- No blocking incompatibility prevents implementation.
- Required package layout: `generated_platform_packages`.
- Live release remains blocked until the Claude CLI/Desktop loader journeys and normalized cross-surface results pass.
