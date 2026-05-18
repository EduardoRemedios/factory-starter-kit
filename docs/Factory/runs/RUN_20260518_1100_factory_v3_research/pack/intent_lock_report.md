# Intent Lock Report

## Version
v1

## Change Log
- v1 (2026-05-18): Initial Purple intent lock for Factory v3 research planning.

## Verdict
- PASS

## Reasons
- The intent is contract-grade and source-tagged.
- The v2 operating core is preserved as authoritative.
- Factory v3 is explicitly research and design only.
- AEGIS compatibility is required without making AEGIS a dependency.
- Runtime-kernel behavior is excluded from Factory.
- No scope expansion remains unresolved.

## Locked Scope
- Plan v3 research documents.
- Plan shadow schema candidates without enforcement.
- Plan advisory validators without wiring them into v2 required gates.
- Plan eval and promotion criteria.
- Plan README language for the v2 and v3 split.

## Bounded Deferrals
- None.

## Conditions
- Future implementation must not modify v2 stage contracts, `stage-lint`, `pack-lint`, or required knowledge-lint behavior unless a separate approved Factory run authorizes that scope.

