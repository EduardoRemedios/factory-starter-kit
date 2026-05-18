# Risk Register

## Version
v1

## Change Log
- v1 (2026-05-18): Initial risk register for Factory v3 research planning.

| ID | Severity | Risk | Mitigation | Verification Hook |
|---|---|---|---|---|
| R-001 | Critical | v3 replaces or rewrites v2 pipeline behavior. | Isolate v3 research docs and add v2-protection lint candidates. | V1-CHECK-001 |
| R-002 | Critical | Factory duplicates AEGIS or another runtime kernel. | Maintain explicit non-goals and adapter-only integration language. | V0-REVIEW-001 |
| R-003 | High | Shadow schemas become required too early. | Keep them under v3 research namespace and out of required validators. | V1-CHECK-002 |
| R-004 | High | README confuses users about current process. | Add concise public split language. | V0-REVIEW-002 |
| R-005 | High | Promotion lacks objective evidence. | Require evals, pilot results, and explicit release approval. | V2-FIXTURE-001 |
| R-006 | Medium | Research docs become too heavy for public adopters. | Prefer short docs and portable examples. | V0-REVIEW-003 |

## Required Verification
- Critical and High risks require verification coverage before the pack can pass.
- Runnable checks are advisory candidates because this run is `PLANNING_ONLY`.

