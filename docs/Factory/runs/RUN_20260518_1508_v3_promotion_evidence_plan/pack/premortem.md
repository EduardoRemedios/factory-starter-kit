# Premortem - Promotion-Evidence Advisory Lint Planning

## Version
v1

## Change Log
- v1 (2026-05-18): Initial premortem for the planning pack.

## Top Failure Scenarios

### PM-001 - Temporary promotion claim remains in docs
- Severity: High
- Scenario: A future pilot mutates `docs/Factory/v3/PROMOTION_CRITERIA.md` to trigger `V3-A006` but forgets to remove the unsafe wording.
- Mitigation: Require final advisory lint over `docs/Factory/v3` to return `ADVISORY_PASS` after remediation.

### PM-002 - A clean pilot is treated as release approval
- Severity: Critical
- Scenario: Accepted advisory findings are misread as evidence that Factory v3 can move beyond Level 0 research.
- Mitigation: Envelope must state the pilot is signal-quality evidence only and does not promote Factory v3.

### PM-003 - Required-gate wiring slips into implementation
- Severity: Critical
- Scenario: A future implementation changes `factoryctl`, CI, or required lint while testing advisory behavior.
- Mitigation: File-touch budget must exclude required gate files and verification must include a no-touch diff review.

### PM-004 - Matcher tuning happens without a false-positive signal
- Severity: High
- Scenario: Agent edits matcher patterns because a warning exists, even when the warning is accepted.
- Mitigation: Tuning is forbidden unless evidence shows false positive, false negative, ambiguity, or missed signal.

### PM-005 - Promotion evidence warning is too broad to classify
- Severity: Medium
- Scenario: The pilot mutation produces multiple findings, making `V3-A006` signal hard to isolate.
- Mitigation: Use the smallest temporary release/promotion wording that lacks evidence and human release approval.

## Summary
The future pilot is safe only if it is treated as reversible evidence capture and the final branch state remains clean, research-only, and non-blocking.

