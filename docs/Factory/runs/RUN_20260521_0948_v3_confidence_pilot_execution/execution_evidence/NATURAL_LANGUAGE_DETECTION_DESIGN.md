# Natural-language Detection Design

## Version
v1

## Change Log
- v1 (2026-05-21): Bounded design for future broader advisory drift detection.

## Status
Design only. This does not implement broader detection, affect required gates, or promote Factory v3.

## Purpose
Define how broader natural-language drift detection could be added without reducing trust through noisy findings.

## Recommended Shape
Use a two-layer advisory model:

1. Deterministic trigger-marker fixtures remain the regression backbone.
2. Natural-language detection runs as an advisory candidate layer with human classification before any readiness decision uses it.

## False-positive Budget
Initial pilot budget:
- scan at least 10 clean real artifacts before considering broader detection useful
- tolerate at most 1 accepted false positive across those clean artifacts
- every finding must be classified as `accepted`, `false_positive`, `needs_more_context`, or `deferred`
- no broader detection result may block work, promote V3, or change a required Factory gate during the pilot phase

## Candidate Detection Families
- local V2 deprecation claims
- local V3 promotion claims without evidence paths
- runtime-kernel authority claims
- explicit continuation after failed verification
- derived continuity overriding source artifacts
- broad dependency or abstraction language that violates SIMPLE-CODE-GATE

## Guardrails
- Prefer paragraph-local evidence over target-wide keyword matches.
- Require exact artifact path in each finding.
- Keep severity advisory-only until false-positive behavior is known.
- Do not introduce external NLP dependencies without explicit approval.
- Do not add broad semantic scoring before deterministic examples prove value.

## Exit Criteria For Future Implementation
Future implementation should be allowed only if a Factory pack approves:
- concrete matcher families
- expected false-positive budget
- fixture corpus
- manual classification workflow
- no-gate-effect guarantee
