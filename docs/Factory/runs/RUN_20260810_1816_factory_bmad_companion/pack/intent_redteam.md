# Intent Red Team — Factory BMAD Companion

## Version

v1

## Change Log

- v1 (2026-08-10): Adversarial review of intent v1.

## Iteration

Iteration: 1 of max 2

## Verdict

CONDITIONAL PASS pending the minimal hardening below.

## Findings

| ID | Severity | Finding | Why it matters | Fix recommendation |
|---|---|---|---|---|
| IR-01 | Critical | “Recoverable rollback” is underspecified for a third-party installer | Blind cleanup could delete user-owned BMAD or Claude state | Permit automatic cleanup only for exact transaction-created unchanged paths; otherwise halt with recovery evidence |
| IR-02 | Critical | Installing BMM necessarily exposes downstream workflows | Module presence cannot prove Factory-bound work avoided competing authority | Treat usage as a routing/citation boundary; never invoke downstream workflows and fail preflight on prohibited authority/citations |
| IR-03 | High | Dependency 0.2.x semantics may depend on current Claude tag resolution | A syntactically valid manifest could install but disable the companion | Revalidate strict manifest plus positive/absent/disabled/version-unsatisfied live cases before package completion |
| IR-04 | High | Companion-owned project files lack an overwrite contract | Setup could silently replace a project policy or preflight adapter | Add ownership manifest, seed-only-when-absent rules, exact conflict halt, and receipt coverage |
| IR-05 | High | Concise output could hide evidence needed for audit | Users need low friction while validators need full fidelity | Define a stable summary schema and explicit JSON/evidence mode sourced from the same result |
| IR-06 | High | Claude local settings are volatile during commands | Self-measurement can itself create permission rules and noisy false defects | Exclude the file from ownership and avoid commands whose only purpose is hashing it |
| IR-07 | Medium | Codex packaging could enlarge the pilot | It could distract from the only live enterprise harness | Allow mechanical package generation only; exclude Codex live-support claims and live gates |

## Agent Failure Modes

- Sees `_bmad-output/architecture.md` and cites it directly; preflight blocks the draft path.
- Treats TEA automation as a passing Factory gate; policy marks it evidence only.
- Calls BMAD sprint planning because BMM is installed; companion exposes no such route.
- Upstream install partially fails; runtime preserves evidence and halts instead of deleting uncertain state.
- Emits full JSON to a first-time user; summary contract makes JSON opt-in.

## Verification Holes

- Exact upstream install change-prefix and partial-failure fixtures.
- Existing-policy conflict and ownership migration fixtures.
- Live dependency negative cases.
- Stable concise-output golden files.

## Scope Expansion Check

- None. All recommendations refine raw-brief constraints.
