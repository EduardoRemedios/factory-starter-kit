# Factory v3 Shadow Schema Candidates

## Version
v0.1

## Change Log
- v0.1 (2026-05-18): Initial prose-only shadow schema candidates for Factory v3 research.

## Status
Research only. This document is prose, not JSON Schema, and it is not enforced by Factory v2 validators.

## Purpose
This document records possible future schema shapes without creating active contracts. The goal is to discuss field boundaries before adding any machine-readable schema files.

## Placement Rule
Future shadow schema examples, if approved later, should live under:

`docs/Factory/v3/shadow_schemas/`

They must not be placed under `docs/Factory/Spec/` until promoted by explicit release approval.

## Candidate Shapes

### mission_envelope
- Candidate fields: `mission_id`, `objective`, `repo_scope`, `execution_mode`, `allowed_paths`, `forbidden_paths`, `allowed_commands`, `verification_requirements`, `halt_conditions`, `completion_conditions`.
- Required boundary: repo coding mission only; no runtime domain action authority.
- Enforcement status: not enforced.

### authority_lease
- Candidate fields: `lease_id`, `mission_id`, `authorized_paths`, `command_classes`, `tool_permissions`, `time_limit`, `cost_limit`, `dependency_policy`, `revocation_conditions`.
- Required boundary: coding-agent authority only; no deployed-system autonomy lease.
- Enforcement status: not enforced.

### governance_profile
- Candidate fields: `profile_id`, `intensity`, `risk_triggers`, `required_reviews`, `required_validators`, `human_checkpoint_rules`.
- Required boundary: planning and review intensity only; no runtime gate decision.
- Enforcement status: not enforced.

### verification_freshness
- Candidate fields: `check_id`, `artifact_ref`, `command`, `last_run_at`, `source_revision`, `freshness_window`, `result`, `evidence_path`.
- Required boundary: delivery verification only; no production proof claim.
- Enforcement status: not enforced.

### evidence_receipt
- Candidate fields: `receipt_id`, `event_type`, `actor`, `timestamp`, `artifact_refs`, `command_refs`, `decision`, `evidence_path`.
- Required boundary: SDLC evidence pointer only; no cryptographic proof authority.
- Enforcement status: not enforced.

### escalation_event
- Candidate fields: `event_id`, `mission_id`, `trigger`, `severity`, `halt_required`, `owner`, `next_legal_action`, `evidence_path`.
- Required boundary: coding mission halt or review only; no runtime intervention.
- Enforcement status: not enforced.

### reentry_request
- Candidate fields: `request_id`, `mission_id`, `halt_event_id`, `scope_unchanged`, `evidence_validated`, `approval_ref`, `requested_next_action`.
- Required boundary: resume of coding mission only; no runtime reentry.
- Enforcement status: not enforced.

### revocation_request
- Candidate fields: `request_id`, `mission_id`, `lease_id`, `revoked_scope`, `reason`, `effective_at`, `approval_ref`.
- Required boundary: repository authority withdrawal only; no runtime lease revocation.
- Enforcement status: not enforced.

### rollback_request
- Candidate fields: `request_id`, `mission_id`, `rollback_scope`, `reason`, `affected_artifacts`, `verification_required`, `approval_ref`.
- Required boundary: code or doc rollback planning only; no production rollback execution.
- Enforcement status: not enforced.

### capability_profile
- Candidate fields: `profile_id`, `harness`, `task_class`, `observed_strengths`, `observed_failures`, `recommended_governance_profile`, `evidence_refs`.
- Required boundary: coding-agent governance tuning only; no autonomous-system readiness certification.
- Enforcement status: not enforced.

### kernel_adapter_mapping
- Candidate fields: `adapter_id`, `kernel_name`, `factory_artifact`, `factory_field`, `kernel_input`, `owner`, `non_authority_note`.
- Required boundary: mapping only; the kernel remains runtime authority.
- Enforcement status: not enforced.

### advisory_validation_report
- Candidate fields: `report_id`, `profile`, `checked_artifacts`, `findings`, `warnings`, `non_blocking_result`, `recommended_next_steps`.
- Required boundary: advisory feedback only; no blocking effect on v2 runs.
- Enforcement status: not enforced.

## Non-enforcement Rules
- No candidate field in this document is required by `knowledge_lint.sh`.
- No candidate field in this document is required by `stage-lint`.
- No candidate field in this document is required by `pack-lint`.
- No candidate schema may block a Factory v2 run until separately promoted.

## Next Step
The next safe step is an advisory validator plan that describes checks without implementing or enforcing them.

