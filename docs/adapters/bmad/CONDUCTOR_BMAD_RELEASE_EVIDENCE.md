# Factory BMAD Companion 0.2.3 — Release Evidence

Status: amended-source live-qualified maintenance candidate plus CLI rollout
hardening; not merged, tagged, published, or approved for rollout.

The public candidate is constructed from an exact positive manifest in a
detached disposable worktree. Every added or modified regular file binds its
mode, source digest, and base preimage where applicable. Internal Factory run
and verification evidence is never part of the publication delta.

Verification requires exact staged-tree equality, privacy and credential
scanning, authored/generated package currency, marketplace and plugin validity,
the complete repository regression suite, knowledge lint, diff hygiene, a
clean-clone proof, and unchanged source branch/index/refs/remotes.

Current live-qualified adapter-repair candidate commit:
`334df09ffde87a6f7ba96cd92501a185af213372`.

Initial committed evidence artifact commit:
`02c44dc32b8cd6b02ea7141d06a761efb3cac802`.

Canonical live-recovery evidence:

- `artifacts/verification/conductor_bmad_023_recovery/VM-008.json`
- `artifacts/verification/conductor_bmad_023_recovery/VM-012.json`
- `artifacts/verification/conductor_bmad_023_recovery/VM-013.json`
- `docs/Conductor/runs/RUN_20260815_0714_factory_bmad_023_live_recovery/RUN_INTEGRITY_REPAIR.md`

Commit, merge, tag, release, marketplace publication, fresh-project pilot, and
organization rollout remain separate human decisions.
