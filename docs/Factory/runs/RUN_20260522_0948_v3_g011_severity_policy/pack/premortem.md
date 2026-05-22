# Pre-mortem - V3-G011 Severity Policy

## Version
v1

## Change Log
- v1 (2026-05-22): Stage E pre-mortem.

## Failure Scenarios
- Policy is written as V3-only and weakens V2 consistency.
- Policy assumes AEGIS exists in most repos.
- Blocker class is too vague to guide operational closeout.
- Policy accidentally implies V3 operational promotion.
- Verification misses advisory lint noise in current V3 docs.

## Mitigations
- Place policy under `docs/Factory/`.
- State ordinary repos are the default case.
- Define concrete severity classes.
- Keep V3 checklist language decision-prep only.
- Run V3 advisory and operational-readiness scans.
