# Premortem — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Identified likely companion failure scenarios and mitigations.

## Failure Scenarios

### PM-01 — The companion becomes a second SDLC

- Scenario: skills start producing architecture, stories, implementation plans, or completion gates.
- Signal: companion artifacts are cited as binding downstream authority.
- Mitigation: expose only diagnose/bootstrap/audit/promote/intake journeys; policy and preflight reject prohibited authority language and draft citations.

### PM-02 — BMAD installation damages user state

- Scenario: a partial upstream install writes unexpected files and automated recovery deletes uncertain state.
- Signal: changed paths exceed approved prefixes or pre-existing digests differ.
- Mitigation: audit before/after inventories; clean only exact transaction-created unchanged paths; otherwise halt with retained evidence and recovery instructions.

### PM-03 — Evidence promotion is mutable or forged

- Scenario: a cited snapshot changes after review, follows a symlink, or mismatches its source.
- Signal: aggregate digest, file digest, or path type differs at preflight.
- Mitigation: real-path containment, no-symlink ancestry, immutable destination, exact source/output hashes, review record, stale-plan rejection, and preflight verification.

### PM-04 — BMM downstream workflows leak into Factory work

- Scenario: Claude sees installed architecture/stories/dev skills and invokes them.
- Signal: raw brief cites implementation artifacts or claims BMAD decisions bind Factory.
- Mitigation: companion never routes downstream workflows; intake template and preflight reject their authority/citation use; installed capability alone is not treated as compliant evidence.

### PM-05 — Plugin dependency works in fixtures but fails in enterprise Claude

- Scenario: Factory dependency is absent, disabled, version-unsatisfied, or cannot resolve tags.
- Signal: plugin list reports dependency errors or companion namespace is unavailable.
- Mitigation: strict validation plus isolated positive and three negative live cases against the exact Claude binary; halt packaging on mismatch.

### PM-06 — “Frictionless” hides audit evidence or floods users

- Scenario: terse output omits reason codes, or JSON walls and permission prompts trigger rejection.
- Signal: first journey requires author coaching or settings-only measurement commands.
- Mitigation: one stable summary schema with state/reason/evidence/next action and opt-in JSON; golden-output fixtures; no unnecessary local-settings hashing.

### PM-07 — Public release leaks customer or machine context

- Scenario: fixtures, receipts, docs, or transcripts contain private names, paths, sessions, or tokens.
- Signal: privacy scan matches known customer and home-path patterns.
- Mitigation: synthetic fixtures, temporary roots, bounded scan, no real-profile transcripts, and customer-neutral canonical docs.

## Execution Stop Rule

Stop immediately on authority duplication, unexpected write, uncertain cleanup,
mutable snapshot, failed preflight, dependency error, private-data match, or any
Critical/High verification failure.
