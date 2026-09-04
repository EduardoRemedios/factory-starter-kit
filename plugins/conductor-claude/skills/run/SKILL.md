---
name: run
description: Continue a Factory run through the next legal planning or execution action while preserving stage order and human Go gates.
---

# Factory Run

Continue Factory only through the next legal action.

## Workflow

1. Run Factory diagnosis and progress inspection before selecting an action.
2. Preserve the canonical sequence `A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> I2`.
3. Load the authoritative repository instructions and stage inputs for the next action.
4. Run the required deterministic validator after each handoff and halt on failure.
5. After I2, stop for human Go unless explicit execution authorization is already recorded.
6. After approved execution, use the repository's `conductor-execution-closeout`
   skill and canonical `conductorctl execution-closeout` command; do not let the
   validator choose or upgrade the authored outcome.

## Guardrails

- Do not expand scope implicitly.
- Do not treat plugin instructions as a replacement for Factory Core.
- The selected session model serves Red, Blue, and Purple roles unless separate routing is explicitly configured.
- `REVIEW_READY` is a review handoff, never commit, merge, tag or release authority.
