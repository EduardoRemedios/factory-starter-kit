# docs/Conductor/templates/TRACEABILITY_MATRIX_TEMPLATE.md — v3

> **Legacy (0.2 line).** This document describes the stage-based process that Factory 0.3 replaced with three gates enforced by `conductorctl contract-lint`; see `docs/Conductor/onboarding/GUIDE.md`. It is kept for the archived 0.2-era runs and the golden-pack tests and will be retired after the pilot. Do not use it to run new work.

## Version
v3

## Change Log
- v3 (2026-05-09): Added verification tier column for left-shifted proof classification.
- v2 (2026-02-06): Added explicit scope tag column to prevent hidden inferred/scope-expanded requirements.

Use this template to create `pack/traceability_matrix.md`.

| Constraint ID | Severity (Critical/High/Medium/Low) | Statement (short) | Source ([SOURCE:RAW]/[SOURCE:REF]/[INFERRED]) | Scope Tag (OK / [INFERRED] / [SCOPE EXPANSION]) | Verification Tier (V0/V1/V2/V3/V4) | Verification (fixture/test/check) | Artifact Path |
|---|---|---|---|---|---|---|---|
| C-001 | Critical |  |  | OK | V2 |  |  |
