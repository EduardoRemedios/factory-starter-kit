# Factory And BMAD Routing Matrix

Factory-only adoption remains the default path. Factory-BMAD is an optional
companion for teams that want BMAD upstream discovery while Factory remains the
downstream SDLC authority.

This matrix applies to Claude Code CLI now. Reuse the same decision logic for
Claude Desktop only after a separate Desktop validation lane passes.

| Starting state | Desired outcome | First command path |
|---|---|---|
| New or empty target | Factory only | Install `factory`, then run `/factory:greenfield`. |
| New or empty target | Factory plus BMAD | Install `factory-bmad` from the companion marketplace, let its Factory dependency resolve, then follow `/factory-bmad:doctor`. |
| Existing repository, neither Factory nor BMAD | Factory only | Install `factory`, run `/factory:doctor`, then `/factory:brownfield`. |
| Existing repository, neither Factory nor BMAD | Factory plus BMAD | Adopt Factory first with Brownfield, then run the companion Doctor and BMAD bootstrap. |
| Existing repository, BMAD only | Factory plus BMAD | Install the companion, run `/factory-bmad:doctor`; Factory Brownfield is the first mutation before audit/intake. |
| Existing repository, Factory only | Add BMAD upstream discovery | Install the companion, run `/factory-bmad:doctor`, then bootstrap/audit/intake as directed. |
| Existing repository, both present | Govern handoff | Run `/factory-bmad:audit`, then intake, promote reviewed evidence, and cite only promoted snapshots in Factory briefs. |

## Boundaries

- Installing `factory` must never require BMAD.
- Installing `factory-bmad` may depend on Factory, but it must not duplicate or
  replace Factory Core.
- BMAD output is upstream evidence only; Factory owns intent lock, architecture,
  risk, verification, execution authorization, and closeout.
- Desktop, WSL, cloud sessions, and Cowork are unsupported until independently
  validated.
