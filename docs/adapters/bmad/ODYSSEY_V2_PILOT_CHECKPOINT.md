# Odyssey v2 Factory-BMAD Pilot Checkpoint

Checkpoint date: 2026-08-13

## North-star objective

The project objective is to make the Factory-BMAD companion work correctly,
safely, and with minimal operator friction for an adopting organization.
Odyssey is a test instrument, not the product objective.

The companion must provide one coherent Claude Code plugin journey for:

1. a greenfield repository with neither Factory nor BMAD;
2. a brownfield repository with neither Factory nor BMAD; and
3. a brownfield repository with BMAD 6.10.0 but no Factory.

In every state, Factory must remain the downstream SDLC authority while allowed
BMAD discovery can seed reviewed, immutable evidence. Repairs and resume choices
must be judged by whether they improve that reusable companion journey—not by
how much of the hypothetical Odyssey application is planned or built.

## Decision

The human sponsor paused the pilot after Factory Stage F. Closing the terminal
and quitting Claude Code is safe. No interactive process must remain running.

Do not resume Stage G, start implementation, publish the plugins, or begin an
organizational rollout until the P1 pilot backlog has been repaired and retested.

## Workspaces and candidate

- Pilot repository: the isolated Odyssey v2 pilot worktree
- Factory-BMAD development repository: the current repository
- Installed local candidate source: the pinned detached `0.2.1` candidate
- Candidate commit: `a00b70d4df48791e9d4338a0fa413b0224596c7e`
- Isolated Claude configuration: the pilot-owned configuration root
- Claude Code pilot surface: CLI, not Claude Desktop
- Factory and companion version: `0.2.1`
- BMAD version/modules: `6.10.0`, Core+BMM; TEA and `bmad-loop` absent

Do not delete, normalize, reinstall, or update these paths merely to resume the
conversation. Reinspect them first because other local work may have changed.

## Factory run state

- Run: `RUN_20260813_1333_tripops`
- Run root: `docs/Factory/runs/RUN_20260813_1333_tripops` in the pilot repository
- Execution mode: `PLANNING_ONLY`
- Downstream fan-out: not approved
- Completed and stage-lint-passed stages: A, B, C, D, E, F
- Next stage not started: G
- `pack/micro_sprints.md`: absent
- `SPRINT_ID.txt`: absent
- Application code and test-suite implementation: not created
- Execution authorization or human implementation Go: absent
- Repository commit: baseline only, `f61716e` (`chore: initialize Factory and
  BMAD companion`); pilot artifacts remain uncommitted

## Locked intent

- Artifact: `pack/intent.md`
- Version: v4
- SHA-256:
  `01e079d35cd1988273add6b6547613ef9d302d9aadb904bef411ddbc4e91db3f`
- Purple evidence: `pack/intent_lock_report.md` v3, verdict `PASS`
- Intent synthesis: v3, iteration 2 of max 2; v3 is compression maintenance,
  not a third Red/Blue iteration
- Sponsor authority: `SPONSOR_DECISIONS.md` v1
- Compression authority: `INTENT_UNLOCK_AUTHORIZATION.md` v1
- Equivalence evidence: `INTENT_EQUIVALENCE_REPORT.md` v1

The bounded compression restored the hard caps without changing the acceptance
criteria, verification obligations, open questions, candidate capabilities,
non-goals, source tags, or seven sponsor predicates. Stages C through F
re-passed afterward.

## BMAD-to-Factory proof achieved

The pilot has already demonstrated:

1. one companion installation resolving the Factory dependency;
2. pinned BMAD Core+BMM bootstrap;
3. allowed upstream discovery and prohibited architecture enforcement;
4. human-reviewed immutable evidence promotion;
5. raw-brief intake and fail-closed project preflight;
6. promoted Markdown recall into Stage A;
7. independent Factory Red/Blue/Purple intent hardening;
8. human resolution of ambiguous upstream concepts;
9. locked Factory-owned intent; and
10. Factory-owned risk and verification governance through Stage F, including
    planned UI/API automation without TEA becoming a competing gate.

The primary BMAD handover hypothesis is therefore proven. Continuing Odyssey
under the known candidate would add less value to the Factory-BMAD objective
than repairing the reusable companion defects.

## Persistent defect and UX record

The authoritative working list is
`docs/adapters/bmad/FACTORY_BMAD_PILOT_BACKLOG.md`.

P1 repairs before resume:

- `FB-D001`: raw-brief checklist triggers its own citation guard.
- `FB-D002`: JSON manifest was incorrectly treated as a Markdown recall ref.
- `FB-D003`: normal Promote skill invocation can hit malformed hook input.
- `FB-D006`: Progress recommends Stage E after a failed Stage D lock gate.
- `FB-D007`: stage-lint omits hard caps on stage-produced artifacts.
- `FB-UX003`: allowed BMAD workflows advertise prohibited follow-ons.

Important P2 operator improvements include concise output, explicit Claude
restart/reload guidance, command-discovery clarity, a fast handover route,
preflight/recall responsibility guidance, stable approval handling, promotion
review qualifiers, and classification of retained Python bytecode (`FB-D008`).

## Retained state requiring care

- The pilot repository currently has untracked pilot evidence and BMAD output.
- Twelve `.pyc` files are retained under `scripts/__pycache__/` and
  `tools/repo_cartographer/__pycache__/`. Do not delete them before the
  `FB-D008` root-cause comparison records their exact state.
- The real Claude profile is outside the pilot boundary. Resume with the
  isolated configuration path above and do not infer permission to modify or
  normalize the real profile.
- The Factory-BMAD development repository has extensive existing uncommitted
  work. Preserve unrelated changes and do not perform a broad commit or cleanup.

## Required repair sequence

1. Reinspect all three workspaces and capture current Git/filesystem state.
2. Treat this checkpoint and the backlog as planning inputs; do not rewrite the
   Odyssey evidence to make failures disappear.
3. Repair the P1 source defects and UX conflict in the development repository.
4. Add focused regressions, including generated Claude/Codex package parity.
5. Attribute `FB-D008` without deleting its retained evidence.
6. Regenerate both Factory-BMAD packages and run the complete repository suite,
   package-current, privacy, policy, and knowledge-lint checks.
7. Build a new stable detached candidate; do not overwrite the pinned 0.2.1
   candidate.
8. Run a short clean-project smoke covering installation, bootstrap, restart,
   discovery, promotion, preflight, recall, prohibited workflow, failed-Purple
   progress behavior, and local cap enforcement.
9. Preview an update of Odyssey v2 to the repaired candidate and require exact
   approval before mutation.
10. Revalidate the affected Odyssey prerequisites and Stages A through F.
11. Resume at Stage G only when the repaired candidate passes and the locked v4
    intent digest remains valid, or follow the Intent Unlock Protocol if a
    substantive contradiction is discovered.

## Safe first action on return

Start in the Factory-BMAD development repository, read this checkpoint and the
backlog, and perform read-only status checks. Do not start Claude, update
Odyssey, or run Stage G as the first action.

Suggested instruction:

> Resume from `docs/adapters/bmad/ODYSSEY_V2_PILOT_CHECKPOINT.md`. Reinspect the
> recorded workspaces read-only, reconcile any state difference, and propose one
> bounded repair run for the P1 backlog. Do not invoke Claude, mutate Odyssey,
> publish, or begin Stage G.
