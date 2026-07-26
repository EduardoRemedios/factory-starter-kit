# Golden Fixture Catalogue

## Version
v1

## Change Log
- v1 (2026-07-24): Defined the pre-implementation golden fixture families.

## Contract
- JSON fixtures are platform-neutral inputs and expected normalized outcomes.
- Platform adapters may differ in invocation syntax but not in required artifacts, mutations, halt reasons, or Factory gate results.
- Every forbidden mutation is a hard failure.
- Stable reason codes are part of the compatibility contract.
- Execution tests may add temporary absolute paths, timestamps, and platform metadata only in captured evidence, not in golden expected results.

## Families
- `plugin_build`: deterministic package generation and manifest boundaries.
- `repository_setup`: greenfield, brownfield, conflict, path, and no-write behavior.
- `status`: evidence precedence and next-legal-action reporting.
- `harness_parity`: normalized Claude/Codex Factory outcomes.
- `update_rollback`: version compatibility, interruption, downgrade, and recovery.
- `instruction_bridge`: Claude bridge without policy duplication.
- `skill_coexistence`: repo-scoped and plugin skill discovery conflicts.
- `environment`: supported roots, paths, worktrees, and unsupported environments.
- `pilot_scorecard`: objective rollout readiness.
