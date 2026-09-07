# Factory 0.3.5 candidate: supported routes

Status: release preparation. The last published pilot is 0.3.4; 0.3.5 is available in this candidate branch only until publication is approved. Merging to the public marketplace main branch publishes the new package source. This document does not authorize that action.

## Existing pilot users

The plugin ids remain conductor and conductor-bmad, and the Claude companion still depends on compatible conductor 0.3.5. Existing 0.3.4 installations and the conductor-v0.3.4-pilot tag remain intact. Do not upgrade an active pilot silently; use the normal update preview, review the affected files and approve its exact plan. Project-owned brownfield files can be explicitly preserved, and ownership persists across updates and rollback.

## Codex app

Install the companion from this candidate marketplace in a qualification environment, then start a fresh task. Run conductor-bmad Doctor and audit with --harness codex. READY means repository prerequisites for guarded MCP loading. The result reports invocation_route=guarded-mcp and host_enforcement_verified=false.

Use the conductor-bmad-workflow skill to call the actual load_workflow MCP tool. Every subsequent or nested BMAD workflow must use that same tool. If the tool is absent or a load is denied, stop. Do not substitute a raw skill read or a shell loader. Delivery and unknown workflows return no instructions. Qualified UX, architecture and spec profiles are checked individually; profile drift remains a denial even when basic repository prerequisites pass.

Native BMAD invocation (--route native) and Codex bootstrap remain unsupported. This route uses an existing reviewed BMAD Core/BMM 6.10.0 installation. The pinned bootstrap installer targets Claude Code; do not relabel a Codex session as Claude to bypass its unsupported state. Intake seeds shared repository evidence and does not activate a host guard.

## Claude Code CLI

For a local candidate test, start Claude from the project with both package directories:

```bash
claude --plugin-dir /path/to/factory-starter-kit/plugins/conductor-claude --plugin-dir /path/to/factory-starter-kit/plugins/conductor-bmad-claude
```

Confirm both candidate packages loaded. Run /conductor-bmad:doctor and audit, and verify the companion hooks are active. The normal direct command and model-selected Skill routes enforce the policy. Unknown unregistered names may be rejected by the host registry before a hook runs. Local --plugin-dir loading proves that session only, not team installation.

## Common delivery contract and limits

BMAD produces candidate evidence; it cannot approve execution. Human review approves immutable promotion, then Factory G1 intent and G2 execution. Runner verification and independent review precede human G3 completion. Merge and publication remain separate decisions.

The candidate's bounded qualification covers product-brief-to-completion rehearsals and proposed spec authoring in both selected harnesses. It does not qualify every architecture/UX workflow, intentional filesystem bypass prevention, universal host activation or provider runtime. Cursor and enterprise rollout remain unqualified. Repository preflight verifies inventory and snapshot integrity without claiming a particular host is enforcing policy.
