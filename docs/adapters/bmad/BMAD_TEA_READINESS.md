# Canonical TEA configuration and readiness — 0.3.8 candidate

A real Claude first-use rehearsal found that the supported 6.12.1-next.0
installation includes an `agents.bmad-tea` descriptor that Factory's compatibility
profile omitted. The descriptor matches the public TEA module at pinned commit
`7ba2130193c473b53d2e323b4da9a80697eef88e`. The old test fixtures did not include
installer agent descriptors, even when their optional TEA module was present.

The new profile records that exact descriptor separately from core/BMM agents.
It is accepted only with the supported installed TEA module; unknown or altered
entries still fail. The workflow allowlist is unchanged. An agent descriptor's
presence is not permission to execute a delivery or review workflow.

Shared installer TOML and legacy YAML configuration is checked during inventory
readiness. Claude and guarded-Codex readiness therefore expose the same shared
configuration failures that invocation qualification rejects. Per-workflow
customization is still checked when that workflow is selected. Repository
readiness is not proof that a host loaded a hook or MCP server; retain actual
invocation evidence for those claims.

Qualification includes realistic core/BMM and optional-TEA fixtures, altered and
unknown descriptor cases, missing/unpinned TEA, unsafe output paths, malformed
configuration, existing 6.10 behaviour, direct and Skill hooks, guarded MCP and
generated-package parity. A separately retained real Claude rehearsal uses a
fresh private project copy and stops before workflow execution or Spec promotion.
A passing rehearsal does not prove unaided team adoption or feature delivery.

This is a new candidate identity. Do not overwrite older installed packages or
reuse their qualification results. Publish and update adopting repositories only
after their exact review, then repeat the checkout checks with the published pin.
