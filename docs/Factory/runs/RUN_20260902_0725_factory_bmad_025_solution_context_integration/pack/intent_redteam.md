# Intent Red Team — Factory-BMAD 0.2.5 Integration

## Version
v1

## Change Log
- v1 (2026-09-02): Challenged version, donor, authority, compatibility, and evidence assumptions.

## Iteration
- Iteration: 1 of max 2

## Executive Verdict
- CONDITIONAL PASS to Blue hardening.
- The intent is directionally bounded, but execution would be unsafe unless Stage F/H pin complete donor states, distinguish authored versus generated files, preserve 0.2.5-only behavior, and prevent evidence from the 0.2.3 qualification being overclaimed for the integrated candidate.

## Severity-Ranked Findings
| ID | Severity | Category | Finding | Why it matters | Fix recommendation |
|---|---|---|---|---|---|
| IR-01 | Critical | Provenance | Donor paths are named but mutable working-tree bytes are not yet pinned. | Either donor can change after review, invalidating collision analysis and source authority. | Require complete path/type/mode/digest/status inventories for base, both donors, and protected roots before any integration. |
| IR-02 | Critical | Version authority | The 0.2.3 MS-05 PASS could be misread as qualifying the combined 0.2.5 candidate. | Exact-version proof is non-transitive. | Make the 0.2.3 evidence an input only; require new 0.2.5 deterministic qualification and a fresh status ceiling. |
| IR-03 | Critical | Collision semantics | Both donors modify policy/runtime and overlapping activation, capability, and enforcement tests. | Textual copy or donor precedence could erase later safeguards or reintroduce fail-open behavior. | Define a collision matrix with behavior-level resolutions and union regression cases before edits. |
| IR-04 | Critical | Generated authority | Two generated package trees differ independently. | Merging them can conceal source drift and invalidate ownership manifests. | Protect generated trees before implementation; permit replacement only by one canonical builder after authored gates pass. |
| IR-05 | Critical | Command coexistence | The solution-context donor narrows the helper that exempts Factory/companion commands, while 0.2.5 tests preserve direct Factory-command coexistence. | A BMAD marker could accidentally block Factory itself. | Preserve and explicitly test both Factory and Factory-BMAD command passthrough while still classifying BMAD commands fail closed. |
| IR-06 | Critical | Layout compatibility | The donors expose different public reason-code models for nested/unsafe layouts. | Replacing `FACTORY_BMAD_NON_CANONICAL_LAYOUT` can break operator guidance; flattening granular causes weakens remediation evidence. | Keep the stable Doctor/Audit public code, add granular subordinate cause, and retain a uniform unsafe-layout enforcement activation code. |
| IR-07 | High | Existing safeguards | “Preserve 0.2.5 safeguards” is a semantic statement without a fixed inventory. | Cache-integrity, approval labels, direct slash-command behavior, and rollout checks may regress invisibly. | Pin named 0.2.5 regression tests and exact protected source/generated counterparts. |
| IR-08 | High | Write boundary | The scope names categories but not an exact file-touch allowlist or budgets. | An agent can rationalize unrelated docs/tests as necessary. | Stage F/H must enumerate maximum authored paths, generated roots, control artifacts, and zero-touch roots. |
| IR-09 | High | Workflow proof | Exact BMAD 6.10.0 digests from the repair evidence may depend on a specific installed tree/configuration. | Different customization or reachable helpers can invalidate authoring-only claims. | Keep architecture/UX/spec default-denied until separately proven in later disposable MS-06; integration may only preserve the pinned classifier contract. |
| IR-10 | High | Indexing | Legacy archive exclusion is planned but cannot be credited from deterministic source tests alone. | Index pollution could affect AuditEdge Stage A. | Treat index exclusion code/tests as deterministic integration scope but reserve actual target proof for separately authorized MS-07. |
| IR-11 | High | Evidence hygiene | Running validation can create bytecode, caches, temp evidence, or builder calls outside the declared lifecycle. | Qualification may pass while leaving unauthorized residue. | Require `./scripts/factory-python`, invocation counting, external bounded evidence, and before/after inventories. |
| IR-12 | Medium | Housekeeping | A stale prunable worktree registration exists. | Cleanup pressure could cause scope drift. | Keep it explicitly protected and outside this run. |

## Agent Failure Modes
- Blindly apply the 0.2.3 diff → overwrite 0.2.5 version/cache/operator behavior → collision matrix and union tests block.
- Copy generated packages → source parity appears plausible but is unauditable → builder-only replacement and pre/post topology checks block.
- Treat allowed architecture/spec names as implementation permission → authority smuggling → typed evidence-only context and prohibited delivery tests block.
- Read donor state after it changes → evidence mismatch → pre-activation digest pin and immediate halt block.
- “Fix” the dirty uplift or video checkout while integrating → user work loss → external donors are read-only and complete no-touch inventories block.
- Run MS-06 to prove missing integration behavior → scope/authority bypass → status ceiling and explicit MS-06 prohibition block.

## Verification Holes
- Exact collision/allowlist fixture is not yet present.
- Exact donor/preimage schema and evidence-root budget are not yet fixed.
- Builder replacement/check-only call counts are not yet fixed.
- Full focused/regression command inventory and expected test counts are not yet pinned.
- Stable public reason and subordinate layout-cause compatibility cases are not yet enumerated.

## Minimal Hardening Required
- Add exact donor-state, collision, public-compatibility, command-coexistence, source/generated, and no-touch fixtures.
- Bind the future activation to exact hashes, commands, roots, budgets, and builder counts.
- Require semantic test union before generated replacement.
- Preserve MS-06 and AuditEdge as later gates.

## Scope Expansion Check
- Any scope expansion detected? NO.
