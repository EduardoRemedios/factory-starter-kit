# Factory Plugin Troubleshooting

Treat a blocked state as a safety result, not as a prompt to force the operation.

| Reason code | Meaning | Next action |
|---|---|---|
| `CONDUCTOR_ENVIRONMENT_UNVERIFIED` | Host or version is outside the tested pilot boundary | Use supported macOS, Git, Python 3.11+, and supported harness version |
| `CONDUCTOR_GIT_ROOT_REQUIRED` | Doctor or another established-project command was invoked outside a Git worktree | For a new empty target, run Greenfield first; otherwise open the intended Git repository and rerun doctor |
| `CONDUCTOR_PROJECT_NOT_CONFIGURED` | Factory is not installed in the project | Preview greenfield or brownfield setup |
| `CONDUCTOR_PROJECT_INCOMPLETE` | Some required Factory files are missing | Review the missing paths; do not invent replacements |
| `CONDUCTOR_CONFLICT_USER_OWNED` | A planned path has different existing content | Review and merge with the owner; do not overwrite. If the path is `CLAUDE.md`, use the recovery steps below |
| `CONDUCTOR_UNSAFE_PATH` | A path traverses or uses a symlinked target | Repair the repository path and preview again |
| `CONDUCTOR_GREENFIELD_NOT_EMPTY` | The target contains content outside the exact Greenfield bootstrap allowance | Use Brownfield only for an existing Git project; otherwise choose an empty target or review non-project harness content without deleting user work |
| `CONDUCTOR_PLAN_APPROVAL_REQUIRED` | Apply did not receive the exact previewed plan ID | Review and approve that plan, or preview again |
| `CONDUCTOR_PLAN_STALE` | Files changed after preview | Generate and review a fresh plan |
| `CONDUCTOR_ROLLBACK_GIT_STATE_CHANGED` | Factory-created Git changed after setup | Preserve Git and project files; recover manually |
| `CONDUCTOR_EVIDENCE_CONTRADICTION` | Passing prose disagrees with required disk evidence | Repair the named stage and rerun its validator |
| `CONDUCTOR_WEAK_RECALL` | Recall is weak without a valid direct-source repair | Refresh recall and resolve material gaps |
| `CONDUCTOR_HUMAN_GO_REQUIRED` | Planning is complete but execution is not authorized | Obtain explicit human Go |
| `CONDUCTOR_SKILL_COLLISION` | A repository skill declares the same name as a plugin skill | Rename or remove only with the skill owner's approval |
| `CONDUCTOR_DOWNGRADE_UNSUPPORTED` | Update points to an older package | Use the separately approved rollback path |
| `CONDUCTOR_ROLLBACK_UNAVAILABLE` | No recoverable update receipt is recorded | Stop and recover from version control or an owner-approved backup |
| `CONDUCTOR_ROLLBACK_EVIDENCE_MISMATCH` | Installation state and transaction receipt do not agree | Stop; preserve evidence and recover manually |
| `CONDUCTOR_PROJECT_PREFLIGHT_FAILED` | The declared project preflight returned FAIL | Inspect its repository-relative evidence and fix the project prerequisite |
| `CONDUCTOR_EXECUTION_CLOSEOUT_INVALID` | A present closeout record failed strict schema, identity, pin, coverage, outcome, path, or digest validation | Preserve the record and evidence; repair through the approved run boundary and never delete it to obtain legacy fallback |

## Claude Command Is Missing

1. Run `claude --version`.
2. Run `claude plugin --help`; update Claude Code if marketplace, install, or
   validation commands are absent.
3. Re-run strict plugin and marketplace validation.
4. Confirm `conductor@factory-starter-kit` is installed.
5. Restart Claude Code.
6. Invoke `/conductor:doctor`.

If multiple `claude` executables are installed, confirm that every command uses
the same supported executable. Do not diagnose namespaced command behavior with
a binary that lacks the plugin interface.

## Codex Skill Is Missing

1. Open the Factory plugin from the repo marketplace link.
2. Confirm it is installed.
3. Start a new Codex task.
4. Invoke `$conductor-doctor`.

The initial pilot uses the Codex app. A broken local Codex CLI does not prove that the app plugin failed.

## Brownfield Blocks on CLAUDE.md

Claude Code needs `CLAUDE.md`, but Factory expects that file to be a one-line
bridge to the shared repository guidance:

```md
@AGENTS.md
```

If Brownfield reports `CONDUCTOR_CONFLICT_USER_OWNED` for `CLAUDE.md`, do not
apply the blocked plan. Preserve the existing `CLAUDE.md` content in a
project-owned document such as `docs/project/CLAUDE_GUIDE.md`, then replace
`CLAUDE.md` with exactly the one-line bridge above. Rerun Brownfield, review the
new plan ID, and apply only by quoting that new exact plan ID.

After Factory is installed, merge any still-useful project-specific Claude
guidance into `AGENTS.md` or keep it in the preserved project document and link
to it from `AGENTS.md`. Do not put the full project guide back into
`CLAUDE.md`; it should remain the Claude Code bridge.

## Failed Setup or Update

The transaction reports a blocker and restores its captured prior state. Preserve the JSON result, repository diff, `docs/Conductor/installation/INSTALLATION_STATE.json`, and durable transaction receipt for the pilot defect log. Do not remove recovery evidence.

## Greenfield Reports Git Root Required

1. Confirm the installed plugin contains the current `0.3.2` pilot candidate.
2. Start Claude Code from the intended empty directory and invoke
   `/conductor:greenfield`; Doctor is a post-setup check for new projects.
3. For an absent or different target, provide the exact absolute path and require
   the same quoted `--root` value for preview and apply.
4. If Greenfield still reports `CONDUCTOR_GIT_ROOT_REQUIRED`, preserve the output
   as a plugin-version or stale-installation defect; do not initialize Git manually
   to hide the failure.

## Claude Reinstall Still Uses Old Code

Claude Code may keep a marketplace package under
`~/.claude/plugins/cache/factory-starter-kit/<plugin>/<version>`. If a candidate
is rebuilt without a version bump, reinstalling can silently reuse those cached
bytes. Before retesting a candidate, uninstall the affected Factory plugin, run
`claude plugin prune`, and rerun the rollout preflight. Prune may leave cached
payload directories on disk. If the preflight reports a `claude_cache_*`
blocker, remove only the stale
`~/.claude/plugins/cache/factory-starter-kit` cache directory and rerun
preflight before reinstalling.

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
