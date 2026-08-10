# Verification Plan — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Defined V1–V4 proof for every Critical/High constraint.

## Strategy

Verification is left-shifted. MS-00 creates the fixture and test skeleton before
runtime implementation. Every enabled check halts execution on failure and
writes customer-neutral evidence under the run-specific verification root.

## Checks

- **VM-001 (V2): Source/package contract.** Validate companion manifest,
  namespace, allowed journeys, Factory non-duplication, ownership, and
  deterministic package generation. Covers C-01, C-11, C-12, C-15.
- **VM-002 (V2): Starting-state and bootstrap matrix.** Exercise five routes,
  exact 6.10.0 Core+BMM command, preview no-write, approved prefixes, existing
  state conflicts, partial install, and proof-bounded cleanup. Covers C-02–C-04.
- **VM-003 (V2): Policy matrix.** Prove allowed upstream classifications,
  prohibited Factory authority, loop blocking, TEA evidence-only status, and
  no downstream companion routing. Covers C-01, C-03, C-05, C-09.
- **VM-004 (V2): Promotion transaction matrix.** Positive promotion and
  negative stale, symlink, traversal, existing snapshot, digest drift,
  interruption, receipt, reuse, and guarded rollback cases. Covers C-06, C-07.
- **VM-005 (V2): Intake/preflight matrix.** Validate embedded checklist and
  PASS plus missing policy/snapshot/review, direct draft citation, digest,
  symlink, mutability, malformed output, and prohibited-authority failures.
  Covers C-08–C-10, C-12.
- **VM-006 (V4): Claude dependency composition.** Strictly validate companion
  and marketplace, then test Factory 0.2.x dependency success plus absent,
  disabled, and version-unsatisfied states in isolated configuration. Covers C-11.
- **VM-007 (V1): Documentation/privacy/support scan.** Check canonical docs,
  allowed source metadata, prohibited private/customer strings, unsupported
  platform claims, and absence of vendored BMAD content. Covers C-01, C-14.
- **VM-008 (V3): Protected-state/no-touch regression.** Run full existing tests
  and prove Factory authored/generated packages and protected user paths are
  unchanged outside the envelope. Covers C-02, C-12, C-15.
- **VM-009 (V2): Concise-output goldens.** Compare default human summaries and
  opt-in JSON from the same results; assert one next action and no settings-only
  hash command. Covers C-13.
- **VM-010 (V3): Complete companion regression.** Run all companion tests,
  package-current check, whitespace check, and knowledge lint. Covers all
  Critical/High constraints.
- **VM-011 (V4): Isolated BMAD 6.10.0 journey.** Install pinned Core+BMM into a
  disposable repository, audit manifest/paths, promote synthetic product-brief
  evidence, run preflight, and prove no loop/TEA or real-profile mutation.
  Covers C-03–C-13.

## Evidence Rules

- Capture exact command, versions, exit status, source metadata, and bounded output.
- Use synthetic temporary paths in public evidence.
- Record unexpected mutation as failure; never delete it merely to pass.
- V4 network/auth failures are blockers, not inferred success.

## Go Rule

All VM-001–VM-011 checks must PASS before technical `REVIEW_READY`. No check
grants application installation, merge, publication, or rollout authority.
