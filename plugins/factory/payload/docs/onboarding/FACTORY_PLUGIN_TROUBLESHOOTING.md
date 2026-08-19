# Factory Plugin Troubleshooting

Treat a blocked state as a safety result, not as a prompt to force the operation.

| Reason code | Meaning | Next action |
|---|---|---|
| `FACTORY_ENVIRONMENT_UNVERIFIED` | Host or version is outside the tested pilot boundary | Use supported macOS, Git, Python 3.11+, and supported harness version |
| `FACTORY_GIT_ROOT_REQUIRED` | Doctor or another established-project command was invoked outside a Git worktree | For a new empty target, run Greenfield first; otherwise open the intended Git repository and rerun doctor |
| `FACTORY_PROJECT_NOT_CONFIGURED` | Factory is not installed in the project | Preview greenfield or brownfield setup |
| `FACTORY_PROJECT_INCOMPLETE` | Some required Factory files are missing | Review the missing paths; do not invent replacements |
| `FACTORY_CONFLICT_USER_OWNED` | A planned path has different existing content | Review and merge with the owner; do not overwrite |
| `FACTORY_UNSAFE_PATH` | A path traverses or uses a symlinked target | Repair the repository path and preview again |
| `FACTORY_GREENFIELD_NOT_EMPTY` | The target contains content outside the exact Greenfield bootstrap allowance | Use Brownfield only for an existing Git project; otherwise choose an empty target or review non-project harness content without deleting user work |
| `FACTORY_PLAN_APPROVAL_REQUIRED` | Apply did not receive the exact previewed plan ID | Review and approve that plan, or preview again |
| `FACTORY_PLAN_STALE` | Files changed after preview | Generate and review a fresh plan |
| `FACTORY_ROLLBACK_GIT_STATE_CHANGED` | Factory-created Git changed after setup | Preserve Git and project files; recover manually |
| `FACTORY_EVIDENCE_CONTRADICTION` | Passing prose disagrees with required disk evidence | Repair the named stage and rerun its validator |
| `FACTORY_WEAK_RECALL` | Recall is weak without a valid direct-source repair | Refresh recall and resolve material gaps |
| `FACTORY_HUMAN_GO_REQUIRED` | Planning is complete but execution is not authorized | Obtain explicit human Go |
| `FACTORY_SKILL_COLLISION` | A repository skill declares the same name as a plugin skill | Rename or remove only with the skill owner's approval |
| `FACTORY_DOWNGRADE_UNSUPPORTED` | Update points to an older package | Use the separately approved rollback path |
| `FACTORY_ROLLBACK_UNAVAILABLE` | No recoverable update receipt is recorded | Stop and recover from version control or an owner-approved backup |
| `FACTORY_ROLLBACK_EVIDENCE_MISMATCH` | Installation state and transaction receipt do not agree | Stop; preserve evidence and recover manually |
| `FACTORY_PROJECT_PREFLIGHT_FAILED` | The declared project preflight returned FAIL | Inspect its repository-relative evidence and fix the project prerequisite |
| `FACTORY_EXECUTION_CLOSEOUT_INVALID` | A present closeout record failed strict schema, identity, pin, coverage, outcome, path, or digest validation | Preserve the record and evidence; repair through the approved run boundary and never delete it to obtain legacy fallback |

## Claude Command Is Missing

1. Run `claude --version`.
2. Run `claude plugin --help`; update Claude Code if marketplace, install, or
   validation commands are absent.
3. Re-run strict plugin and marketplace validation.
4. Confirm `factory@factory-starter-kit` is installed.
5. Restart Claude Code.
6. Invoke `/factory:doctor`.

If multiple `claude` executables are installed, confirm that every command uses
the same supported executable. Do not diagnose namespaced command behavior with
a binary that lacks the plugin interface.

## Codex Skill Is Missing

1. Open the Factory plugin from the repo marketplace link.
2. Confirm it is installed.
3. Start a new Codex task.
4. Invoke `$factory-doctor`.

The initial pilot uses the Codex app. A broken local Codex CLI does not prove that the app plugin failed.

## Failed Setup or Update

The transaction reports a blocker and restores its captured prior state. Preserve the JSON result, repository diff, `docs/Factory/installation/INSTALLATION_STATE.json`, and durable transaction receipt for the pilot defect log. Do not remove recovery evidence.

## Greenfield Reports Git Root Required

1. Confirm the installed plugin contains the current `0.2.3` release candidate.
2. Start Claude Code from the intended empty directory and invoke
   `/factory:greenfield`; Doctor is a post-setup check for new projects.
3. For an absent or different target, provide the exact absolute path and require
   the same quoted `--root` value for preview and apply.
4. If Greenfield still reports `FACTORY_GIT_ROOT_REQUIRED`, preserve the output
   as a plugin-version or stale-installation defect; do not initialize Git manually
   to hide the failure.

## Claude Local State Makes Greenfield Look Non-empty

Claude Code may create `.claude/settings.local.json` and
`.claude/hooks/.state/**` in a new working directory. Current Greenfield treats
the settings file as read-only preserved harness evidence and ignores volatile
hook state for emptiness and plan IDs. It does not parse, manage, modify, or
remove either path family.

If Greenfield still blocks:

1. Confirm `.claude` is a real directory rather than a symlink.
2. Confirm `settings.local.json` is a regular non-symlink file.
3. Confirm there are no other entries under `.claude` except optional
   `.claude/hooks/.state/**`, and no other project content at the target.
4. Do not delete user-owned content to force Greenfield. Use an empty target, or
   prepare a genuine existing project as a Git worktree before Brownfield.
5. If the settings file or mode changed after preview, rerun Greenfield and
   approve only the new exact full plan ID.
