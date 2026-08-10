# Intent — Factory BMAD Companion Plugin

## Version

v2

## Change Log

- v1 (2026-08-10): Contracted the raw brief into a bounded companion-plugin intent.
- v2 (2026-08-10): Hardened install recovery, authority evidence, output, dependency, and ownership boundaries after Red Team review.

## Purpose

Create a separate, customer-neutral Claude Code companion that lets BMAD supply
reviewed upstream evidence while Factory remains the sole downstream SDLC and
execution authority. [SOURCE:RAW]

## Goal

Deliver a technical `REVIEW_READY` companion release candidate that diagnoses
five adoption states, plans a pinned BMAD 6.10.0 Core+BMM installation, audits
BMAD policy, promotes approved immutable evidence, and enforces Factory intake
through the existing project-preflight seam. [SOURCE:RAW]

## Principles

1. Factory owns downstream planning, verification governance, sequencing,
   authorization, and closeout. [SOURCE:RAW]
2. BMAD output is untrusted draft evidence until a human promotes an immutable
   snapshot. [SOURCE:RAW]
3. The companion composes with Factory 0.2.x and never copies Factory Core.
   [SOURCE:RAW]
4. Diagnosis and preview are zero-write; writes are explicit, bounded,
   stale-safe, receipt-backed, and validated. [SOURCE:RAW]
5. Human-first output is concise; deterministic JSON is opt-in evidence.
   [SOURCE:RAW]
6. Existing user files and modules are reported, never silently changed.
   [SOURCE:RAW]

## Roles

- Human sponsor: approves setup/promotion plans and Factory execution. [SOURCE:RAW]
- Companion plugin: diagnoses, previews, audits, promotes, and prepares intake evidence. [SOURCE:RAW]
- BMAD 6.10.0: produces upstream discovery artifacts only for Factory-bound work. [SOURCE:RAW]
- Factory plugin/Core: owns the canonical A–I2 pipeline and execution gates. [SOURCE:RAW]
- Project preflight: deterministically verifies cited promoted evidence before Stage A. [SOURCE:RAW]

## Definitions

- **Factory-bound work:** any initiative whose implementation will enter a
  Factory `raw_brief.md` and A–I2 run. [SOURCE:RAW]
- **Draft evidence:** BMAD output under `_bmad-output/`; never directly citable. [SOURCE:RAW]
- **Promoted snapshot:** immutable selected evidence under
  `docs/upstream/bmad/<SNAPSHOT_ID>/` with manifest, review record, and one stable
  aggregate digest. [SOURCE:RAW]
- **Dual-use BMAD:** BMM may remain installed with downstream workflows, but the
  companion never invokes or treats those workflows as authority for
  Factory-bound work. [SOURCE:RAW]
- **Concise output:** stable state, reason code, essential evidence, and one next
  legal action; full machine JSON requires an explicit flag. [SOURCE:RAW]

## Scope

### In Scope

- One authored companion source and deterministic Claude Code package. [SOURCE:RAW]
- Portable Codex packaging only when mechanically generated from the same source
  and excluded from the live support claim. [SOURCE:RAW]
- Five-state read-only diagnosis and routing. [SOURCE:RAW]
- Previewed BMAD 6.10.0 Core+BMM Claude Code bootstrap. [SOURCE:RAW]
- Module/workflow authority audit covering BMM, loop, and TEA. [SOURCE:RAW]
- Immutable reviewed snapshot promotion with receipt/recovery. [SOURCE:RAW]
- Embedded-checklist raw-brief template and project preflight adapter. [SOURCE:RAW]
- Concise output, onboarding, fixtures, tests, and isolated live Claude proof. [SOURCE:RAW]
- Canonical project state, roadmap, and changelog updates. [SOURCE:RAW]

### Domain Areas

- plugin-composition
- bmad-bootstrap
- authority-policy
- upstream-promotion
- factory-intake
- claude-code-ux

## Non-goals

- No Factory Core stage or authority changes. [SOURCE:RAW]
- No copied or vendored BMAD runtime/workflow content. [SOURCE:RAW]
- No BMAD solution architecture, stories, implementation loop, or review gate
  for Factory-bound work. [SOURCE:RAW]
- No TEA installation, test-framework decision, or automation-suite delivery. [SOURCE:RAW]
- No Claude Desktop, Cursor, Windows, Linux, or organization rollout claim. [SOURCE:RAW]
- No automatic deletion or uninstallation. [SOURCE:RAW]
- No live application-pilot installation, merge, tag, or publication. [SOURCE:RAW]

## Contract Requirements

- C-01 Critical: Factory remains sole downstream authority and the companion
  contains no copied Factory runtime or gate. [SOURCE:RAW]
- C-02 Critical: diagnosis/preview make no repository writes and select exactly
  one legal next action for each starting state. [SOURCE:RAW]
- C-03 Critical: BMAD bootstrap is pinned to official 6.10.0, Core+BMM, Claude
  Code, and excludes loop/TEA by default. [SOURCE:RAW]
- C-04 Critical: upstream-installer execution requires exact target/command/
  module/prefix approval; pre-state and post-state are audited. Automatic
  cleanup is allowed only for paths proven transaction-created and unchanged;
  otherwise recovery halts for human review. [SOURCE:RAW]
- C-05 Critical: existing BMAD modules are never silently changed; loop blocks
  Factory intake and TEA is classified only as optional Stage F evidence.
  [SOURCE:RAW]
- C-06 Critical: promotion rejects unapproved workflow classes, direct draft
  citations, stale sources, symlinks, traversal, mutable destinations, and
  existing snapshot changes. [SOURCE:RAW]
- C-07 Critical: each snapshot includes exact source/output hashes, BMAD
  provenance, human review evidence, aggregate digest, transaction receipt,
  and guarded rollback. [SOURCE:RAW]
- C-08 Critical: project preflight uses the existing Factory declaration and
  fixed command; it fails closed on authority, citation, hash, path, snapshot,
  and review-evidence violations without adding a gate. [SOURCE:RAW]
- C-09 High: BMM workflow availability is not evidence of compliant use;
  preflight verifies only promoted citations and authority language, while the
  companion routes no downstream BMAD workflow. [SOURCE:RAW]
- C-10 High: the raw-brief template embeds one checklist and binds snapshot ID
  plus digest; BMAD context freezes at Brief Purple PASS. [SOURCE:RAW]
- C-11 High: the Claude plugin declares a same-marketplace Factory dependency
  compatible with 0.2.x and fails closed on absent/disabled/incompatible state;
  live tag/constraint behavior is revalidated before packaging. [SOURCE:RAW]
- C-12 High: project-adapter files have explicit companion ownership and cannot
  overwrite user-owned policy, preflight, brief, or snapshot content. [SOURCE:RAW]
- C-13 High: default output is concise; JSON evidence is opt-in; commands avoid
  hashing volatile Claude settings merely to prove exclusion. [SOURCE:RAW]
- C-14 High: public files and retained evidence are customer-neutral and free of
  private paths, credentials, account names, and session state. [SOURCE:RAW]
- C-15 High: implementation applies SIMPLE-CODE-GATE v2 and adds no dependency
  without explicit envelope approval. [SOURCE:RAW]

## Acceptance Criteria

- AC-01 through AC-12 in `raw_brief.md` are binary and retained unchanged.
  [SOURCE:RAW]
- All Critical/High constraints map to V1–V4 proof before execution. [SOURCE:RAW]
- Live Claude/BMAD checks run only in isolated temporary state before the
  application pilot. [SOURCE:RAW]
- Technical completion is `REVIEW_READY`, never rollout authority. [SOURCE:RAW]

## Open Questions

### BLOCKING

- None for planning; execution halts on failed current plugin dependency or
  BMAD installer conformance. [SOURCE:RAW]

### NON-BLOCKING

- Final customer-neutral plugin display name and patch version may be chosen
  during implementation within the `factory-bmad` namespace. [SOURCE:RAW]
- Codex live support remains a later release decision. [SOURCE:RAW]

## Go or No-Go Rule

Go only after I2 and pack-lint PASS plus exact human authorization bound to this
pack digest. No-Go on authority duplication, unsafe installer cleanup, mutable
promotion, weak preflight, unverified dependency composition, private data, or
unsupported platform claims. [SOURCE:RAW]
