# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-18): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260518_1235_v3_advisory_lint_impl_plan
- Effective Scope: docs
- Attempted Scopes: RUN_20260518_1235_v3_advisory_lint_impl_plan, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-18T11:36:06Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 107
- Artifact types: {"canonical_doc": 50, "factory_run_pack_artifact": 52, "factory_run_root_artifact": 5}
- Focus terms: advisory lint, implementation, Factory v3
- Trace IDs: None
- Required refs: docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_AUDIT_REPORT.md, docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md, docs/Factory/v3/evals/EVAL_20260518_001.md, docs/Factory/Spec/STAGE_CONTRACTS.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 142
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:24` [SPRINT_20260518_002 Envelope > Advisory Report Shape]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:139` [Agent Loop Bridge > Review Result Schema]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE_MANUAL_RUNBOOK.md:56` [Agent Loop Bridge Manual Runbook > Verdict Rules]
  - `docs/Factory/Spec/DEFINITIONS.md:115` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 8. Contract-grade intent]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:21` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > Global rules (HARD)]

### Q2. `Critical`
- Result count: 55
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:207` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_F — Verification Assets]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/Spec/DEFINITIONS.md:61` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 4. Impact rubric (verification obligations)]
  - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md:15` [docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.3 > Critical (must all be YES for PASS or CONDITIONAL PASS)]

### Q3. `deferral`
- Result count: 28
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:44` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Deferrals Summary]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:42` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Deferrals]
  - `docs/Factory/Spec/DEFINITIONS.md:84` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 5. Bounded deferral (HARD)]

### Q4. `human GO`
- Result count: 53
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]
  - `docs/Factory/MISSION_MODE.md:214` [docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension) > 11. Mission artifacts (minimum) > 11.3 Codex Mission Goal Continuity adapter (experimental)]

### Q5. `scope expansion`
- Result count: 44
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:51` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Scope Expansion Check]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:55` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Scope Expansion Summary]
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]

### Q6. `advisory lint`
- Result count: 43
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/premortem.md:15` [Premortem > Failure Scenarios > PM-002 - advisory validators become accidental required gates]
  - `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md:15` [Factory v3 Advisory Validator Plan > Non-blocking Rule]
  - `docs/Factory/ORCHESTRATION.md:86` [docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit) > 0.7 Support Helpers (Optional, Advisory)]
  - `docs/Factory/v3/evals/EVAL_20260518_001.md:46` [Factory v3 Eval 20260518 001 > Profile Results > P2 - v2 Drift Shadow Check]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/SPRINT_20260518_001_ENVELOPE_REDTEAM.md:24` [SPRINT_20260518_001 Envelope Red Team > Findings > EF-003 - High - v2 protection lint candidates need non-blocking posture]

### Q7. `implementation`
- Result count: 73
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/micro_sprints.md:41` [Micro-sprints > MS-05 - Implementation Readiness Gate]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_AUDIT_REPORT.md:29` [Pack Audit Report > Approved Planning Output]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md:78` [SPRINT_20260518_002 Envelope > Criteria Before Writing Validator Code]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/intent_lock_report.md:29` [Intent Lock Report > Conditions]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/intent_redteam.md:14` [Intent Red Team > Findings > F-001 - Critical - Advisory design can become implementation by drift]

### Q8. `Factory v3`
- Result count: 212
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/HANDOFF/HANDOFF_STAGE_F.md:30` [Stage F Handoff > Outputs Produced (paths)]
  - `docs/Factory/v3/evals/EVAL_20260518_001.md:12` [Factory v3 Eval 20260518 001 > Eval Scope]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/SPRINT_20260518_001_ENVELOPE.md:29` [SPRINT_20260518_001 Envelope > Proposed Files]
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_AUDIT_REPORT.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/PACK_AUDIT_REPORT.md` (factory_run_pack_artifact)

### R2. `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/pack/SPRINT_20260518_002_ENVELOPE.md` (factory_run_pack_artifact)

### R3. `docs/Factory/v3/evals/EVAL_20260518_001.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/evals/EVAL_20260518_001.md` (canonical_doc)

### R4. `docs/Factory/Spec/STAGE_CONTRACTS.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md` (canonical_doc)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
