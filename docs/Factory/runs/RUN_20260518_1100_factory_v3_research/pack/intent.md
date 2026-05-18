# Factory v3 Research Track Intent

## Version
v1

## Change Log
- v1 (2026-05-18): Initial intent for a planning-only Factory v3 research track governed by Factory v2.

## Purpose
Plan Factory v3 as a research and design track while preserving Factory v2 as the current operating process. [SOURCE:RAW]

## Goal
Produce a planning pack that defines the initial v3 research artifacts, advisory validation path, evaluation evidence, promotion criteria, and README language needed before any v3 release claim. [SOURCE:RAW]

## Non-goals
- Do not replace, reorder, or weaken the `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2` v2 planning pipeline. [SOURCE:RAW]
- Do not change `stage-lint`, `pack-lint`, execution authorization, Mission Mode, Mission Cursor, verification manifests, or merge protocol behavior. [SOURCE:RAW]
- Do not introduce runtime kernel behavior, production action mediation, cryptographic proof authority, persistent world-model memory, or a second AEGIS-style ledger. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- Do not make AEGIS a starter-kit dependency. [SOURCE:RAW]

## Principles
- Factory v3 must be built through Factory v2 governance until explicitly promoted by evidence. [SOURCE:RAW]
- Factory v3 should be AEGIS-compatible but not AEGIS-dependent. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- v3 artifacts start as lightweight public-repo-friendly documents and optional advisory checks. [SOURCE:RAW]
- Shadow schemas are candidates only until promotion criteria make them enforceable. [SOURCE:RAW]
- Factory owns SDLC mission governance for coding work; lower-level kernels own runtime authority and proof. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]

## Roles
- Root Planner: preserve v2 read order, preflight evidence, and stage progression. [SOURCE:REF:docs/Factory/ORCHESTRATION.md]
- Research Author: draft v3 strategy, concept, and non-goal documents. [SOURCE:RAW]
- Boundary Reviewer: check AEGIS and runtime-kernel separation. [SOURCE:REF:docs/Factory/AEGIS_BOUNDARY.md]
- Verification Specialist: define advisory validators, eval fixtures, and promotion evidence. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]
- Purple Gate: decide whether this planning pack is safe to use as the first v3 research slice. [SOURCE:REF:docs/Factory/Spec/STAGE_CONTRACTS.md]

## Acceptance Criteria
- The pack identifies exact proposed v3 document paths. [SOURCE:RAW]
- The pack marks which v3 documents are strategic or research-only. [SOURCE:RAW]
- The pack lists runtime-kernel and AEGIS-owned behaviors excluded from Factory v3. [SOURCE:RAW]
- The pack lists schema candidates that remain non-enforcing. [SOURCE:RAW]
- The pack defines a staged path from v2 intact to strategy notes, shadow schemas, advisory validators, pilot profile, and eventual runtime integration. [SOURCE:RAW]
- The pack defines lint or verification rules that protect v2 from accidental v3 overwrite. [SOURCE:RAW]
- The pack recommends public README language for the v2 and v3 split. [SOURCE:RAW]
- The pack includes risks, open questions, and a first small implementation slice. [SOURCE:RAW]

## Open Questions
### BLOCKING
- None.

### NON-BLOCKING
- Should v3 research docs live under `docs/Factory/v3/` or `docs/Factory/research/v3/`?
- Should shadow schemas begin as prose-only candidates or JSON Schema examples?
- What minimum eval count is enough before a release candidate can claim v3 readiness?

## Go Or No-Go Rule
- GO if the final pack preserves v2 behavior, keeps v3 research-only, excludes runtime-kernel duplication, and provides a verifiable staged research path.
- NO-GO if any artifact implies v3 replaces v2, makes AEGIS required, or adds runtime authority to Factory.

