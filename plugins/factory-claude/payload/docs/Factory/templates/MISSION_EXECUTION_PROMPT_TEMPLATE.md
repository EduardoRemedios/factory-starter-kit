# docs/Factory/templates/MISSION_EXECUTION_PROMPT_TEMPLATE.md

<!--
VALIDATION:
- Create at: docs/Factory/missions/<MISSION_ID>/MISSION_EXECUTION_PROMPT.md
- Must be generated only after mission checkpoint GO.
- Must include ordered mission unit execution with stop/go gates.
- Must preserve per-unit stage contracts and guardrails.
- Must include SIMPLE-CODE-GATE v2 for Factory-controlled code-changing mission units.
- Must include HALT policy and restart constraints.
- No placeholders may remain in final artifacts.
-->

## Version
v1.1

## Change Log
- v1.1 (2026-05-19): Added SIMPLE-CODE-GATE v2 implementation guardrail for Factory-controlled code-changing mission units.
- v1 (YYYY-MM-DD): Initial mission execution prompt.

## Mission Metadata
- Mission ID:
- Created:
- Source: MISSION_MANIFEST.md + MISSION_CHECKPOINT.md

## Purpose
One paragraph defining mission execution objective and explicit out-of-scope boundaries.

## Required Read Order
1. `AGENTS.md`
2. `docs/Factory/ORCHESTRATION.md`
3. `docs/Factory/MISSION_MODE.md`
4. `docs/Factory/missions/<MISSION_ID>/MISSION_MANIFEST.md`
5. `docs/Factory/missions/<MISSION_ID>/MISSION_CHECKPOINT.md`
6. Per-unit sprint pack artifacts in mission order

## Hard Guardrails
- Preserve fail-closed behavior.
- Preserve schema-locked boundaries.
- Preserve evidence-chain integrity.
- No silent scope expansion.
- Preserve per-unit iteration caps.

## SIMPLE-CODE-GATE (v2)
Mandatory guardrail for Factory-controlled mission-unit implementation work.

For code-changing mission units:
- Implement the smallest clear, behavior-preserving change.
- Prefer direct, readable, local code over cleverness or premature abstraction.
- Avoid copy-paste chunks, awkward abstraction layers, bloated multi-purpose helpers, brittle request-path mutation, hidden side effects, dependency creep, and silent failure swallowing.
- Add abstractions only when they remove real duplication, name a stable domain concept, reduce branching or call-site complexity, and have a clear owner/boundary.
- Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection for speculative future variation.
- If future variation is uncertain, keep the code explicit and document the specific scale metric, repeated pattern, or business condition that will trigger a refactor.
- Comments must explain why, not what.

## Ordered Unit Execution
| Order | RUN_ID | SPRINT_ID | Entry Gate | Exit Gate | Stop/Go Rule |
|---:|---|---|---|---|---|
| 1 | RUN_... | SPRINT_... | checkpoint GO + unit preconditions | unit verification PASS | GO only if PASS |
| 2 | RUN_... | SPRINT_... | unit1 PASS | unit verification PASS | GO only if PASS |

If a unit pack contains `verification_manifest.yaml`, execute or satisfy those checks as part of the unit exit gate and halt on any check marked `halt_on_failure: true`.

## HALT Policy
- Halt immediately on policy violation or unit verification failure, including failed halt-on-failure manifest checks.
- When halted: mark current unit failed, remaining units skipped.

## Restart Policy
- Resume allowed only from failed unit when mission scope ledger and checkpoint remain valid.
- If invalidated, require new checkpoint.

## Final Exit Checklist
- [ ] All planned units completed OR mission halted with explicit reason.
- [ ] Mission completion report updated with evidence links.
- [ ] No unresolved BLOCKING scope expansion.
