# Context Recall Report

## Version
v1

## Change Log
- v1 (2026-05-18): Generated recall report for profile `stage-a`.

## Report Metadata
- Profile: stage-a (Factory Stage A Preflight)
- Requested Scope: RUN_20260518_1100_factory_v3_research
- Effective Scope: docs
- Attempted Scopes: RUN_20260518_1100_factory_v3_research, docs/Factory/runs, docs/Factory/ProductOwner/phases, docs
- Fallback Applied: YES
- Coverage Verdict: SUFFICIENT
- Generated At (UTC): 2026-05-18T10:01:29Z
- Source Index: /private/tmp/factory_starter_kit_context/context.sqlite3

## Purpose
- Use this before Stage A to surface binding constraints, unresolved blockers, prior human checkpoints, and recent scope decisions tied to the new run.

## Coverage Snapshot
- Indexed sources in effective scope: 42
- Artifact types: {"canonical_doc": 41, "factory_run_root_artifact": 1}
- Focus terms: Factory v3, AEGIS, Mission Mode, stage-lint, pack-lint
- Trace IDs: None
- Required refs: docs/Factory/AEGIS_BOUNDARY.md, docs/Factory/Spec/STAGE_CONTRACTS.md, docs/Factory/ORCHESTRATION.md
- Unresolved required refs: None

## Recall Queries
### Q1. `BLOCKING`
- Result count: 47
- Evidence:
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:139` [Agent Loop Bridge > Review Result Schema]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE_MANUAL_RUNBOOK.md:56` [Agent Loop Bridge Manual Runbook > Verdict Rules]
  - `docs/Factory/Spec/DEFINITIONS.md:115` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 8. Contract-grade intent]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:21` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > Global rules (HARD)]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:129` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_A — Intent Contracting]

### Q2. `Critical`
- Result count: 27
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:207` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_F — Verification Assets]
  - `docs/Factory/Spec/DEFINITIONS.md:61` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 4. Impact rubric (verification obligations)]
  - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md:15` [docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.3 > Critical (must all be YES for PASS or CONDITIONAL PASS)]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:40` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Critical Failures (only if any Critical item is NO)]
  - `docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md:26` [docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md > Critical (must all be YES for PASS/CONDITIONAL PASS)]

### Q3. `deferral`
- Result count: 15
- Evidence:
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:44` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Deferrals Summary]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:42` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Deferrals]
  - `docs/Factory/Spec/DEFINITIONS.md:84` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 5. Bounded deferral (HARD)]
  - `docs/Factory/Spec/DEFINITIONS.md:93` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5) > 6. Conditional Pass]
  - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md:26` [docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.3 > Conditional (required for CONDITIONAL PASS)]

### Q4. `human GO`
- Result count: 42
- Evidence:
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/Harnesses/AGENT_LOOP_BRIDGE.md:55` [Agent Loop Bridge > Handoff Event Schema]
  - `docs/Factory/ProductOwner/PO_PROCESS.md:40` [Product Owner Pre-Factory Process > 0.2 Separation of Concerns (HARD)]
  - `docs/Factory/AEGIS_BOUNDARY.md:50` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Crosswalk]
  - `docs/Factory/MISSION_MODE.md:214` [docs/Factory/MISSION_MODE.md — Mission Mode (Factory Extension) > 11. Mission artifacts (minimum) > 11.3 Codex Mission Goal Continuity adapter (experimental)]

### Q5. `scope expansion`
- Result count: 32
- Evidence:
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:51` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md > Scope Expansion Check]
  - `docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md:55` [docs/Factory/templates/PACK_AUDIT_REPORT_TEMPLATE.md > Scope Expansion Summary]
  - `docs/Factory/Harnesses/CODEX.md:216` [Codex Harness Adapter > Mission Goal Continuity (Experimental)]
  - `docs/Factory/SCRATCHPAD.md:11` [Factory Scratchpad — Cross-Run Pitfalls Index > Active Pitfalls (Mandatory)]
  - `docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md:1` [docs/Factory/templates/INTENT_LOCK_REPORT_TEMPLATE.md]

### Q6. `Factory v3`
- Result count: 19
- Evidence:
  - `docs/Factory/Spec/DEFINITIONS.md:1` [docs/Factory/Spec/DEFINITIONS.md — Doc Factory (v3.5)]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/raw_brief.md:6` [Raw Brief - Factory v3 Research Track > Context]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/raw_brief.md:26` [Raw Brief - Factory v3 Research Track > Constraints]
  - `docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md:1` [docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md — v3.3]
  - `docs/Factory/templates/TRACEABILITY_MATRIX_TEMPLATE.md:1` [docs/Factory/templates/TRACEABILITY_MATRIX_TEMPLATE.md — v3]

### Q7. `AEGIS`
- Result count: 17
- Evidence:
  - `docs/Factory/AEGIS_BOUNDARY.md:40` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Strategic Rule]
  - `docs/Factory/runs/RUN_20260518_1100_factory_v3_research/raw_brief.md:6` [Raw Brief - Factory v3 Research Track > Context]
  - `docs/Factory/AEGIS_BOUNDARY.md:1` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary]
  - `docs/Factory/AEGIS_BOUNDARY.md:9` [docs/Factory/AEGIS_BOUNDARY.md - Factory v3 / AEGIS Boundary > Purpose]
  - `docs/Factory/ARCHITECTURE.md:93` [Factory Architecture > Layer Model > 6. External Governance Kernels]

### Q8. `Mission Mode`
- Result count: 46
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:346` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > MISSION_WRAPPER (additive, optional — not a replacement stage chain)]
  - `docs/Factory/ORCHESTRATION.md:143` [docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit) > 2. Run Initialization]
  - `docs/Factory/templates/MISSION_EXECUTION_PROMPT_TEMPLATE.md:27` [docs/Factory/templates/MISSION_EXECUTION_PROMPT_TEMPLATE.md > Required Read Order]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:129` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_A — Intent Contracting]
  - `docs/Factory/templates/MISSION_CHECKPOINT_TEMPLATE.md:1` [docs/Factory/templates/MISSION_CHECKPOINT_TEMPLATE.md]

### Q9. `stage-lint`
- Result count: 13
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:108` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > STAGE_VALIDATION — Stage Lint]
  - `docs/Factory/Harnesses/CODEX.md:65` [Codex Harness Adapter > Codex CLI Terminal Flow]
  - `docs/Factory/ORCHESTRATION.md:188` [docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit) > 4. Stage Flow]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:21` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > Global rules (HARD)]
  - `docs/Factory/ARCHITECTURE.md:46` [Factory Architecture > Layer Model > 3. Validators]

### Q10. `pack-lint`
- Result count: 20
- Evidence:
  - `docs/Factory/ORCHESTRATION.md:213` [docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit) > 5. Human Decision]
  - `docs/Factory/Spec/STAGE_CONTRACTS.md:305` [docs/Factory/Spec/STAGE_CONTRACTS.md — Factory Stage Contracts (v4.11) > POST_I2_VALIDATION — Pack Lint]
  - `docs/Factory/Harnesses/CODEX.md:65` [Codex Harness Adapter > Codex CLI Terminal Flow]
  - `docs/Factory/ORCHESTRATION.md:6` [docs/Factory/ORCHESTRATION.md — Factory Pipeline Runner Guide (Starter Kit) > Change Log]
  - `docs/Factory/ARCHITECTURE.md:46` [Factory Architecture > Layer Model > 3. Validators]

## Trace Queries
## Required Reference Checks
### R1. `docs/Factory/AEGIS_BOUNDARY.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/AEGIS_BOUNDARY.md` (canonical_doc)

### R2. `docs/Factory/Spec/STAGE_CONTRACTS.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/Spec/STAGE_CONTRACTS.md` (canonical_doc)

### R3. `docs/Factory/ORCHESTRATION.md`
- Status: RESOLVED
- Resolution Type: path
- Evidence:
  - `docs/Factory/ORCHESTRATION.md` (canonical_doc)

## Operator Notes
- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.
