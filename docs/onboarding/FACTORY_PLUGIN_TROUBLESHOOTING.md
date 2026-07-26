# Factory Plugin Troubleshooting

Treat a blocked state as a safety result, not as a prompt to force the operation.

| Reason code | Meaning | Next action |
|---|---|---|
| `FACTORY_ENVIRONMENT_UNVERIFIED` | Host or version is outside the tested pilot boundary | Use supported macOS, Git, Python 3.11+, and supported harness version |
| `FACTORY_GIT_ROOT_REQUIRED` | Invocation is not inside a Git worktree | Open the intended repository and rerun doctor |
| `FACTORY_PROJECT_NOT_CONFIGURED` | Factory is not installed in the project | Preview greenfield or brownfield setup |
| `FACTORY_PROJECT_INCOMPLETE` | Some required Factory files are missing | Review the missing paths; do not invent replacements |
| `FACTORY_CONFLICT_USER_OWNED` | A planned path has different existing content | Review and merge with the owner; do not overwrite |
| `FACTORY_UNSAFE_PATH` | A path traverses or uses a symlinked target | Repair the repository path and preview again |
| `FACTORY_GREENFIELD_NOT_EMPTY` | Greenfield was selected for an existing project | Use brownfield |
| `FACTORY_PLAN_APPROVAL_REQUIRED` | Apply did not receive the exact previewed plan ID | Review and approve that plan, or preview again |
| `FACTORY_PLAN_STALE` | Files changed after preview | Generate and review a fresh plan |
| `FACTORY_EVIDENCE_CONTRADICTION` | Passing prose disagrees with required disk evidence | Repair the named stage and rerun its validator |
| `FACTORY_WEAK_RECALL` | Recall is weak without a valid direct-source repair | Refresh recall and resolve material gaps |
| `FACTORY_HUMAN_GO_REQUIRED` | Planning is complete but execution is not authorized | Obtain explicit human Go |
| `FACTORY_SKILL_COLLISION` | A repository skill declares the same name as a plugin skill | Rename or remove only with the skill owner's approval |
| `FACTORY_DOWNGRADE_UNSUPPORTED` | Update points to an older package | Use the separately approved rollback path |
| `FACTORY_ROLLBACK_UNAVAILABLE` | No recoverable update receipt is recorded | Stop and recover from version control or an owner-approved backup |
| `FACTORY_ROLLBACK_EVIDENCE_MISMATCH` | Installation state and transaction receipt do not agree | Stop; preserve evidence and recover manually |

## Claude Command Is Missing

1. Run `claude --version`.
2. Update to Claude Code 2.1.216 or newer.
3. Re-run strict plugin and marketplace validation.
4. Confirm `factory@factory-starter-kit` is installed.
5. Restart Claude Code.
6. Invoke `/factory:doctor`.

Do not diagnose namespaced command behavior using an older unsupported Claude version.

## Codex Skill Is Missing

1. Open the Factory plugin from the repo marketplace link.
2. Confirm it is installed.
3. Start a new Codex task.
4. Invoke `$factory-doctor`.

The initial pilot uses the Codex app. A broken local Codex CLI does not prove that the app plugin failed.

## Failed Setup or Update

The transaction reports a blocker and restores its captured prior state. Preserve the JSON result, repository diff, `docs/Factory/installation/INSTALLATION_STATE.json`, and durable transaction receipt for the pilot defect log. Do not remove recovery evidence.
