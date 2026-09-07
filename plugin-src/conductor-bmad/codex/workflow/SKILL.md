---
name: conductor-bmad-workflow
description: Load a named BMAD discovery, helper, or qualified solution workflow through the Factory guarded MCP tool in Codex. Deny delivery and unknown workflows before loading their instructions. Readiness is scoped to this route and requires an available MCP tool.
---

# Factory BMAD guarded workflow

Use the conductor-bmad MCP `load_workflow` tool with the current project's absolute root and the exact requested `bmad-*` name. If the name is missing, use `bmad-help`.

Do not read a BMAD `SKILL.md` directly or invoke a Claude Skill command. Every nested, recommended, or subsequent BMAD workflow must be loaded through the same MCP tool. A permitted parent grants no permission to its child. If the tool is unavailable or denies a workflow, stop and report the reason; do not substitute a shell loader or infer permission from its allowlist.

On a successful load, retain its authority context and route constraint while following its instructions. Resolve relative skill resources against the returned `skill_root`; resolve project paths against `root`. Loading does not authorize running scripts or writing files beyond the user's current request. If asked only to smoke-test loading, report the name, reason code and digest, then stop without following the workflow.

BMAD output is candidate context. It cannot approve Factory intent, execution, delivery, a merge or completion. Promotion needs human review and the existing immutable promotion contract. Factory G1/G2/G3 remain authoritative.

Codex audit reports repository prerequisites for this explicit guarded route. Intake may seed repository evidence for an existing reviewed installation; bootstrap remains Claude-specific. An audit READY result is not proof the current host loaded the MCP tool. Raw filesystem access is outside this loader's enforcement boundary and must not be presented as covered by it. Claude retains its separately tested direct and model-initiated Skill hooks.
