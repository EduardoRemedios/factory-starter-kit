# Raw Brief - Factory v3 Research Track

## Request
Use the existing Factory v2 process to plan the Factory v3 research and design track.

## Context
- Factory v2 remains the current usable operating process in this starter kit.
- The v2 core is the `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2` planning pipeline.
- Mission Mode, Mission Cursor, task memory, Repo Cartographer, Agent Loop Bridge, verification manifests, pack-lint, stage-lint, and merge protocol are v2-compatible or generalized improvements.
- Factory v3 is future mission-governed autonomous execution research.
- Factory v3 must be AEGIS-compatible but not AEGIS-dependent.
- Factory v3 must not duplicate AEGIS or any lower-level runtime governance kernel.

## Goal
Create a planning pack for introducing Factory v3 research and design artifacts without changing Factory v2 behavior.

## Required Answers
1. What new docs should exist for Factory v3?
2. Which docs should be explicitly marked strategic or research-only?
3. What should be kept out of v3 to avoid duplicating AEGIS?
4. What concepts from v3 should be schema candidates later, but not enforced yet?
5. What is the staged path from v2 core intact to strategy notes, shadow schemas, advisory validators, pilot profile, and eventual runtime integration?
6. What verification or lint rules should protect v2 from accidental v3 overwrite?
7. What public README language is needed so users understand the v2 and v3 split?

## Constraints
- Planning only.
- Preserve Factory v2 as the current source of truth for execution.
- Treat v3 as research and design until explicitly promoted.
- Do not introduce runtime kernel behavior into Factory.
- Do not make AEGIS a dependency of the starter kit.
- Prefer lightweight, portable, public-repo-friendly docs.
- Identify exact file paths for proposed artifacts.
- Include risks, open questions, and a recommended first small implementation slice.

