# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-18): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260518_1155_v3_advisory_validator_design
- Effective Scope: docs
- Attempted Scopes: RUN_20260518_1155_v3_advisory_validator_design, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-18T10:56:26Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 79
- Artifact types: {"canonical_doc": 50, "factory_run_pack_artifact": 26, "factory_run_root_artifact": 3}
- Focus terms: Factory v3, advisory validator, Level 0 research, AEGIS
- Trace IDs: None
- Required refs: docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md, docs/Factory/v3/evals/EVAL_20260518_001.md, docs/Factory/Spec/STAGE_CONTRACTS.md, docs/Factory/AEGIS_BOUNDARY.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 85
- Evidence:
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:139` [Agent Loop Bridge > Review Result Schema]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE_MANUAL_RUNBOOK.md:56` [Agent Loop Bridge Manual Runbook > Verdict Rules]
  - `docs/Factory/Spec/DEFINITIONS.md:115` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 8. Contract-grade intent]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:21` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > Global rules (HARD)]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:129` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_A — Intent Contracting]

### Q2. `Critical`
- Result count: 42
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:207` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_F — Verification Assets]
  - `docs/Factory/Spec/DEFINITIONS.md:61` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 4. Impact rubric (verification obligations)]
  - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md:15` [docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.3 > Critical (must all be YES for PASS or CONDITIONAL PASS)]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/PACK_CHECKLIST.md:13` [Pack Checklist > Critical]

### Q3. `deferral`
- Result count: 21
- Evidence:
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:44` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Deferrals Summary]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:42` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Deferrals]
  - `docs/Factory/Spec/DEFINITIONS.md:84` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 5. Bounded deferral (HARD)]
  - `docs/Factory/Spec/DEFINITIONS.md:93` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 6. Conditional Pass]

### Q4. `human GO`
- Result count: 51
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]
  - `docs/Factory/MISSION_MODE.md:214` [docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension) > 11. Mission artifacts (minimum) > 11.3 Codex Mission Goal Continuity adapter (experimental)]

### Q5. `scope expansion`
- Result count: 39
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:67` [Context Recall Report > Recall Queries > Q5. `scope expansion`]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:51` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Scope Expansion Check]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:55` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Scope Expansion Summary]
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/SCRATCHPAD.md:11` [Factory Scratchpad — Cross-Run Pitfalls Index > Active Pitfalls (Mandatory)]

### Q6. `Factory v3`
- Result count: 161
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/HANDOFF/HANDOFF_STAGE_F.md:30` [Stage F Handoff > Outputs Produced (paths)]
  - `docs/Factory/v3/evals/EVAL_20260518_001.md:12` [Factory v3 Eval 20260518 001 > Eval Scope]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/SPRINT_20260518_001_ENVELOPE.md:29` [SPRINT_20260518_001 Envelope > Proposed Files]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:49` [Context Recall Report > Recall Queries > Q3. `deferral`]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:40` [Context Recall Report > Recall Queries > Q2. `Critical`]

### Q7. `advisory validator`
- Result count: 43
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1155_v3_advisory_validator_design/raw_brief.md:25` [Raw Brief - Factory v3 Advisory Validator Design > Required Answers]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/verification_plan.md:32` [Verification Plan > Checks > V1-CHECK-002 - Required Validator Isolation]
  - `docs/Factory/v3/PILOT_PROFILE_PLAN.md:37` [Factory v3 Pilot Profile Plan > Pilot Profiles > Profile P2 - v2 Drift Shadow Check]
  - `docs/Factory/v3/PROMOTION_CRITERIA.md:45` [Factory v3 Promotion Criteria > Promotion Levels > Level 1 - Advisory]
  - `docs/Factory/v3/evals/EVAL_20260518_001.md:12` [Factory v3 Eval 20260518 001 > Eval Scope]

### Q8. `Level 0 research`
- Result count: 11
- Evidence:
  - `docs/Factory/AEGIS_BOUNDARY.md:102` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Governance Intensity Guidance]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/raw_brief.md:6` [Raw Brief - Factory v3 Research Track > Context]
  - `docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md:1` [docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md]
  - `docs/Factory/v3/NON_GOALS_AND_BOUNDARIES.md:12` [Factory v3 Non-goals And Boundaries > Core Boundary]
  - `docs/Factory/v3/PROMOTION_CRITERIA.md:40` [Factory v3 Promotion Criteria > Promotion Levels > Level 0 - Research]

### Q9. `AEGIS`
- Result count: 65
- Evidence:
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/CONTEXT_RECALL_REPORT.md:85` [Context Recall Report > Recall Queries > Q7. `AEGIS`]
  - `docs/Factory/v3/README.md:37` [Factory v3 Research > Relationship To AEGIS]
  - `docs/Factory/AEGIS_BOUNDARY.md:40` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Strategic Rule]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/intent.md:21` [Factory v3 Research Track Intent > Principles]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/pack/premortem.md:19` [Premortem > Failure Scenarios > PM-003 - AEGIS compatibility becomes AEGIS dependency]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/ADVISORY_VALIDATOR_PLAN.md` (canonical_doc)

### R2. `docs/Factory/v3/evals/EVAL_20260518_001.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/v3/evals/EVAL_20260518_001.md` (canonical_doc)

### R3. `docs/Factory/Spec/STAGE_CONTRACTS.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md` (canonical_doc)

### R4. `docs/Factory/AEGIS_BOUNDARY.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/AEGIS_BOUNDARY.md` (canonical_doc)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
