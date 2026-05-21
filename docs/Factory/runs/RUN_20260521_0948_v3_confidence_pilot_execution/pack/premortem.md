# Premortem

## Version
v1

## Change Log
- v1 (2026-05-21): Stage E premortem.

| ID | Scenario | Impact | Mitigation |
|---|---|---|---|
| PM-01 | Pilot reports sound like operational V3 approval. | Premature adoption. | Repeat advisory-only and no-promotion status in reports and rollup. |
| PM-02 | Real shadow scans return clean but prove too little. | Overconfidence. | Classify clean scans as false-positive evidence only. |
| PM-03 | Positive routing pass cases are ignored. | V3 fallback behavior remains undervalued. | Include V3-G012 and V3-G013 in rollup. |
| PM-04 | Trigger-marker seeded pilots are overstated. | Broad drift discovery remains unproven. | Record trigger-marker limitation explicitly. |
| PM-05 | Natural-language design creates implementation pressure. | Scope creep. | Keep design-only and require later pack for code changes. |

## Exit Criteria Status
- PASS
