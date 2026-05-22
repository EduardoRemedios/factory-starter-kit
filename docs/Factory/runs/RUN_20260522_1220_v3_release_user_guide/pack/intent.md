# Intent - V3-OP-001 Release Approval And User Guide

## Version
v2

## Change Log
- v1 (2026-05-22): Initial Stage A intent.
- v2 (2026-05-22): Stage C synthesis clarified the release is optional-profile-only and user guide must explain V2 fallback.

## Purpose
Record explicit human release approval for optional operational use of `V3-OP-001`, then provide the first Codex user guide and starter templates.

## Goal
Make `V3-OP-001` usable by Codex users in ordinary repositories while preserving Factory v2 as supported fallback and keeping all operational limits explicit.

## Non-goals
- Do not make V3 the default mode.
- Do not approve any profile beyond `V3-OP-001`.
- Do not deprecate Factory v2.
- Do not wire V3 into required gates, CI, `factoryctl`, or merge preflight.
- Do not claim runtime-kernel proof, production mediation, payment authorization, compliance approval, or deployment authority.

## Principles
- Approval is narrow: optional use of `V3-OP-001` only.
- V3 can be the front door for triage, but it must fall back to V2 when work is ambiguous, high-risk, or outside the profile.
- User docs must explain direct V3 use, V3 triage, and V2 fallback.
- Templates must be lightweight and copyable into adopting repositories.
- Apply SIMPLE-CODE-GATE: direct docs and templates, no new framework.

## Roles
- Root Planner: this run.
- Release Recorder: record approval and update C-10.
- User Guide Author: create user-facing Codex guidance.
- Red Team: check for overbroad release, missing fallback, and unsafe slot-game wording.
- Purple Gate: decide whether the bounded documentation update is safe.

## Acceptance Criteria
- Release approval artifact exists and names `V3-OP-001`, commit `f07fa11`, V2 fallback, and accepted residual risks.
- C-10 is marked DONE and the decision report records the approver.
- User guide explains direct V3 use, V3 intake/triage, V2 fallback, and a new online slot game example.
- Starter templates exist under `docs/Factory/v3/templates/`.
- Verification evidence is saved under this run root.

## Go Or No-Go Rule
GO only if the release remains optional-profile-only, V2 fallback remains explicit, user docs do not imply regulated/payment/deployment approval, and verification passes.

## Open Questions
- NON-BLOCKING: Later feedback from real project trials should be captured in follow-up evidence and guide revisions.
