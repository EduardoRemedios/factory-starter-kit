# Intent Synthesis

## Version
v1

## Change Log
- v1 (2026-05-18): Initial synthesis of red-team findings into the Factory v3 research intent.

## Iteration
- Iteration: 1 of max 2

## Synthesis
- The intent remains valid because it already keeps Factory v3 research subordinate to Factory v2 governance.
- The pack must explicitly separate research docs, shadow schema candidates, advisory validators, and promoted v3 contracts.
- The pack must recommend README language that distinguishes Factory document versions from Factory v2 and future Factory v3 product posture.
- The pack must include v2-protection lint rules as advisory candidates before any enforcement.

## Hardened Requirements
- New v3 docs should live outside `docs/Factory/Spec/` until promotion.
- Shadow schemas should not be imported by existing validators.
- AEGIS compatibility language must say optional compatibility target, not dependency.
- Promotion criteria must include eval evidence and human release approval.

## Critical Findings Resolution
- F-001 is resolved by requiring public README split language and research-only banners.
- F-002 is resolved by isolating shadow schemas under the v3 research namespace.
- F-003 is resolved by preserving the AEGIS boundary as a non-duplication contract.
- F-004 is resolved by adding evaluation and promotion criteria to later artifacts.

## Scope Expansion Review
- No net-new requirement expands scope beyond the raw brief.

