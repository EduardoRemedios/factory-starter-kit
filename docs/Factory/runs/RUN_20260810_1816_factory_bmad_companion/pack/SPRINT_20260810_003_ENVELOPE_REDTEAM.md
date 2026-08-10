# Envelope Red Team — Factory BMAD Companion

## Version

v3

## Change Log

- v1 (2026-08-10): Attacked envelope v1 and verified its v2 repairs.
- v2 (2026-08-10): Added the canonical-doc payload propagation finding and verified envelope v3.
- v3 (2026-08-10): Confirmed envelope v4 public-safe pilot naming.

## Iteration

Iteration: 1 of max 2

## Inputs Reviewed

- `SPRINT_20260810_003_ENVELOPE.md` v1
- `verification_plan.md`
- `traceability_matrix.md`
- `micro_sprints.md`

## Cross-Reference: Intent Red Team

- IR-01 recovery and IR-03 dependency risks resurface as execution-boundary checks; v2 resolves both.

## Executive Verdict

- PASS after the minimal v2 repairs below.
- The envelope is executable, bounded, and traceable without widening the intent.

## Severity-Ranked Findings

| ID | Severity | Category | Finding | Why it matters | Fix recommendation |
|---|---|---|---|---|---|
| ER-01 | High | Write boundary | v1 listed feature scope but not exact allowed roots/no-touch package digests | Implementation could alter Factory Core or unrelated work | Add exact allowed paths and protect existing Factory package digests |
| ER-02 | High | Live isolation | v1 did not separate repository, npm cache, Claude config, and authenticated profile effects | A live test could mutate the operator environment | Require synthetic repo, isolated Claude config, separate cache inventories, and explicit auth boundary |
| ER-03 | High | Dependency | v1 said dependency must pass but lacked required negative states | Installed-but-disabled or version-unsatisfied behavior could be missed | Bind absent, disabled, and incompatible cases to VM-006 |
| ER-04 | Medium | Support claims | v1 could allow generated Codex package to imply live support | Public docs could overpromise | Require portable/unverified wording and Claude Code CLI-only claim |
| ER-05 | Medium | Harness settings | v1 did not prohibit self-induced settings hashing | Validation could repeat the pilot's permission churn | Explicitly forbid settings-only digest commands |
| ER-06 | High | Generated payload | Canonical root docs are embedded in both existing Factory packages | A blanket package no-touch rule contradicts the required canonical update | Allow only exact doc mirrors plus regenerated payload ownership digests; protect every other package file |

## Agent Failure Modes

- Touches existing Factory package while adding the companion; protected digest gate halts.
- Uses the real application pilot as the live fixture; prohibited-path gate halts.
- Treats successful strict validation as dependency runtime proof; VM-006 remains required.
- Publishes Codex support because a manifest exists; docs scan rejects the claim.

## Verification Holes

- None after envelope v3 and VM-006/VM-008/VM-009 bindings.

## Scope / Drift Checks

- Scope expansion detected: NO.

## Minimal Patch Set

- Added exact paths/no-touch digests, live-state isolation, negative dependency cases, support wording, and settings-hash prohibition to envelope v2.
- Added the narrow canonical-doc mirror exception to envelope v3.
