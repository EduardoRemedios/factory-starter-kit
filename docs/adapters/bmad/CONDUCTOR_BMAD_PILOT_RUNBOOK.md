# Factory BMAD Companion Pilot Runbook

Validate the complete upstream-to-Factory journey in disposable repositories
before using the companion in customer work.

## Test application

For the first trusted-colleague test, use
`ODYSSEY_V3_INITIAL_BMAD_BRIEF.md` in a disposable greenfield target. The seed
is deliberately modest so friction in the BMAD-to-Factory transition is visible
instead of hidden inside product scope.

Before team rollout, also rehearse the two brownfield states expected in team
use: one repository with neither Factory nor BMAD, and one repository with BMAD
already present but Factory absent.

Later team pilots may choose an application complex enough to exercise product
discovery, UI and API requirements, persistence, risk, and automated
verification. Application implementation remains a later Factory run; this
pilot first proves setup, intake, evidence promotion, and Factory handoff.

## Sequence

0. Run `scripts/verify_conductor_bmad_cli_rollout.py` for the marketplace root
   and each target repository. Resolve every `BLOCKED` result before a team
   starts.
1. Test three targets: empty/neither, brownfield/neither, and a brownfield
   starting state where BMAD is present and Factory is absent.
2. Install the Factory marketplace and explicitly install only `conductor-bmad`.
3. Run Doctor; complete Factory Greenfield preview and exact apply.
4. Preview and exactly approve pinned BMAD 6.10.0 Core+BMM setup.
5. Audit modules, exact version, all 46 Core+BMM skills, commands, agents,
   hooks/configuration, coverage, and reconciliation. Confirm loop is absent.
   TEA 1.21.1, if retained, is optional Stage F evidence only.
6. Apply the seed-only intake plan.
7. Use allowed BMAD discovery workflows for product/research/UX context.
8. Human-review and immutably promote selected evidence.
9. Draft `raw_brief.md` with snapshot ID and digest.
10. Use the handover map below, then run Factory A–I2 planning.
11. Verify Factory owns architecture, decomposition, risk, verification,
    execution authorization/control, and closeout.
12. Retain direct slash-command `UserPromptExpansion` evidence and run the hard
    generated-package `PreToolUse`/`Skill` contract: prohibited, unknown,
    malformed, and partial cases deny before sentinel execution; allowed
    upstream and pre-adoption BMAD-present controls remain usable. Optional model-choice
    smoke is advisory—no Skill call is inconclusive, while an emitted prohibited
    call that is not denied is a smoke failure.
13. Run the CI-callable `policy-lint`, package-current checks, full regression,
    privacy checks, and protected-state comparison.

## Handover map

- Snapshot manifest → project preflight: validates the immutable snapshot and
  human review evidence.
- Promoted `artifact.md` → Stage A recall: resolves the upstream content. Do not
  use `SNAPSHOT_MANIFEST.json` as the Stage A required reference.
- Factory intent → authoritative only after Purple Gate PASS: no BMAD artifact
  becomes downstream SDLC authority.

## Pass criteria

- Preview is zero-write and exact approval is required.
- Factory dependency and BMAD pins resolve; loop and TEA are not introduced.
- Promotion rejects stale, symlinked, traversing, or conflicting input.
- Snapshot reuse works without duplication.
- Draft citations and hash/review/authority errors fail preflight.
- Default output is concise; JSON is explicit.
- Claude profile and unrelated project files remain outside ownership.
- Existing brownfield source and BMAD content remain byte-identical.
- Unknown future `bmad-*` names fail closed with
  `CONDUCTOR_BMAD_WORKFLOW_PROHIBITED`.
- One explicit companion install resolves the protected Factory dependency.

Stop on unexpected writes, unsupported claims, or authority ambiguity.

For first-team rollout, use `CONDUCTOR_BMAD_CLI_ROLLOUT_PLAYBOOK.md` as the
operator-facing path and `CONDUCTOR_BMAD_BOOTSTRAP_RECOVERY.md` for any blocked
bootstrap receipt.

For the first trusted-colleague full-flow check, use
`CONDUCTOR_BMAD_FIRST_TESTER_HANDOFF.md`.
