# Factory BMAD Bootstrap Recovery

BMAD bootstrap intentionally runs the pinned external installer first and audits
the resulting repository state afterward. If post-audit fails, Factory-BMAD
blocks and preserves the receipt instead of guessing which external writes are
safe to undo.

## When This Applies

Use this guide when `/conductor-bmad:bootstrap` returns:

- `CONDUCTOR_BMAD_BOOTSTRAP_POST_AUDIT_FAILED`
- a non-zero installer return code
- unexpected paths in the bootstrap receipt
- an audit state other than `READY`

## Immediate Rule

Do not retry bootstrap blindly. Do not delete generated files to force a clean
second attempt. Preserve the repository exactly as it is until the maintainer
classifies the receipt.

## Evidence To Capture

From the target repository:

```bash
git status --short
find docs/upstream/bmad/install-receipts -type f -maxdepth 1 -print
```

Save or cite the exact receipt path returned by the command. The receipt records
the plan ID, return code, changed paths, unexpected paths, stdout/stderr
digests, and module audit result.

## Recovery Paths

Use one of these paths after reviewing the receipt:

- **Expected BMAD drift:** update the Factory-BMAD policy only through a normal
  source repair and fresh verification. Do not locally edit the adopting repo to
  hide the drift.
- **Installer transient failure:** reset the target only from verified version
  control or an owner-approved backup, then rerun rollout preflight before a new
  bootstrap attempt.
- **Unexpected user-owned conflict:** keep the repository blocked and ask the
  project owner whether to preserve, move, or merge the conflicting file.
- **Unsupported environment:** repair the local prerequisites first, usually
  `python3`, `npx`, or the Claude Code version.

## What Success Looks Like

The next valid attempt must start from a known repository state, produce a new
preview plan, receive exact approval for that current plan ID, and finish with
`CONDUCTOR_BMAD_BOOTSTRAP_APPLIED`.
