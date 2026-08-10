# Risk Register — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Registered execution risks against locked intent v2.

| ID | Severity | Risk | Mitigation | Verification hook |
|---|---|---|---|---|
| R-01 | Critical | Companion duplicates Factory authority | Limit public journeys; scan runtime/docs for prohibited stage orchestration | VM-001, VM-007 |
| R-02 | Critical | Upstream installer writes outside approval or partial state is deleted unsafely | Before/after inventory, approved prefixes, proof-bounded cleanup, halt otherwise | VM-002 |
| R-03 | Critical | Existing BMAD/Claude files or modules are silently changed | Ownership/digest conflicts and exact no-touch fixtures | VM-002, VM-008 |
| R-04 | Critical | Snapshot permits traversal, symlink escape, mutation, stale source, or hash drift | Safe-path checks, immutable destination, exact plan/digests, receipt/rollback | VM-004 |
| R-05 | Critical | Factory intake cites `_bmad-output` or prohibited authority | Embedded checklist plus fail-closed project preflight matrix | VM-005 |
| R-06 | High | BMM downstream skill availability is mistaken for permitted use | Route only upstream journeys; lint citations/authority rather than installed BMM skill list | VM-003, VM-005 |
| R-07 | High | `bmad-loop` or TEA is misclassified | Loop blocks intake; TEA is optional evidence only and absent by default | VM-003 |
| R-08 | High | Factory plugin dependency is missing, disabled, or incompatible | Version constraint, strict schema, positive/negative isolated Claude checks | VM-006 |
| R-09 | High | Concise UX loses determinism or emits raw JSON by default | Shared result schema and human/JSON golden snapshots | VM-009 |
| R-10 | High | Generated packages drift from authored source | Deterministic builder and package-current rerun | VM-001, VM-010 |
| R-11 | High | Customer/private state enters public artifacts | Synthetic roots and privacy scan | VM-007 |
| R-12 | High | Core regression or existing Factory package changes unintentionally | Allow only canonical-doc mirrors plus payload ownership digest refresh; protect every other Factory package file | VM-008, VM-010 |
| R-13 | Medium | Codex packaging implies untested support | Label portable package unverified and omit live support claims | VM-007 |
| R-14 | Medium | Canonical docs overstate rollout readiness | State only technical REVIEW_READY and retain application/rollout gates | VM-007 |

## Residual Risk

BMAD and Claude are external versioned systems. The release can prove the pinned
versions and supported macOS Claude Code journey, but any later version requires
source and live conformance revalidation before support expands.
