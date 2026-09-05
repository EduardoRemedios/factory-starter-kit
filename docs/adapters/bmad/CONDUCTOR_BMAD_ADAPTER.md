# Factory BMAD Companion Adapter

## Purpose

`conductor-bmad` is a separate, customer-neutral companion plugin for teams that
use BMAD but want Factory to remain their SDLC. It does not extend or replace
Factory Core. It safely turns selected BMAD 6.10.0 upstream discovery output
into reviewed, immutable evidence that a Factory brief can cite.

## Authority boundary

Factory owns intent locking, architecture, decomposition, risk, verification
governance, execution authorization/control, and closeout. BMAD may help with
discovery and context, but its output is non-binding until a human promotes an
immutable evidence snapshot. BMAD solutioning and implementation workflows are
not routed by this companion.

TEA is not missing functionality: Factory owns test strategy and evidence
governance. If a team later keeps TEA to generate API/UI automation assets,
those assets enter Factory Stage F as optional evidence; TEA does not become a
gate. `bmad-loop` is incompatible with Factory-bound intake and blocks it.

## Five starting states

| State | Companion action |
|---|---|
| Neither system, otherwise new target | Run Factory Greenfield preview first. |
| Neither system, existing project | Run Factory Brownfield preview first. |
| Factory only | Preview pinned BMAD Core+BMM setup. |
| BMAD present, Factory absent | Run Factory Brownfield preview. This is an adoption starting state only, not an approved operating mode. |
| Both | Audit modules and authority before intake. |

Partial or contradictory state blocks for human repair.

## Single-repository enforcement candidate

The I2-passed `SPRINT_20260811_001` pack retains one explicit user-scope install:

```bash
claude plugin install conductor-bmad@factory-starter-kit
```

Claude resolves the separate Factory package automatically; users do not run a
second install. `/conductor-bmad:doctor` remains the only adoption front door.

The 0.3.x Claude Code CLI pilot candidate includes plugin-bundled guards for
direct slash-command expansion and model-initiated Skill invocation.
Enforcement activates only when Factory and present/partial BMAD coexist in the
current Git worktree. Approved upstream `bmad-*` names are explicitly
allowlisted; every other or unknown name is denied by default. Capability audit
and brownfield reconciliation preserve existing code and BMAD files while
preventing legacy downstream artifacts from becoming binding Factory authority.

The implementation, focused suites, deterministic packages, and disposable
repository journeys are present. Runtime policy loading activates no-bytecode
protection before dynamic import, and the live verifier now has a zero-Claude
preflight for its binary/version, permission, isolated-config, evidence, and
protected-root contracts. The hard hook proof loads the generated
package's exact `PreToolUse`/`Skill` command, submits the production event schema,
and proves denial prevents downstream sentinel execution. Retained direct
expansion evidence and optional model-choice smoke are reported separately; a
model choosing not to call a Skill is inconclusive, not a release failure. The
0.2 line passed isolated Claude Code CLI live requalification and added the
first-team rollout preflight, cache-integrity protection, and approval-plan
labels that 0.3.x keeps. 0.3 expresses policy by lane, supports a declared
non-root BMAD installation, and seeds its contracts independently of intake.
None of that grants publication or organization rollout by itself.

## Evidence flow

1. Work in `_bmad-output/` using an allowed upstream workflow.
2. Review a selected artifact and preview promotion.
3. Approve the exact promotion plan.
4. The companion creates `docs/upstream/bmad/<SNAPSHOT_ID>/` with artifact,
   provenance, review evidence, hashes, and a stable aggregate digest.
5. Draft from `docs/adapters/bmad/RAW_BRIEF_TEMPLATE.md` and cite only the
   snapshot ID plus aggregate digest.
6. Factory's existing project-preflight seam re-runs the shared policy lint and
   validates policy version, capability coverage, reconciliation evidence,
   authority, provenance, and citation before
   the Intent Pack cites it. In 0.3 a promoted snapshot enters a run as an
   `upstream_snapshot` source and freezes at G1 Intent Lock (the 0.2-era
   equivalent was Stage A recall and Brief Purple PASS).

Snapshots are product-level, immutable, and reusable by multiple Factory runs.
Receipts make setup and rollback auditable without silently touching user files.

## Supported boundary

- Technical pilot: Claude Code CLI, with the rollout preflight and first-team
  playbook applied before adopter use.
- Mechanically generated portability package: Codex; not yet live-supported.
- Unsupported in this release candidate until separately validated: Claude
  Desktop, Cursor, organization rollout, TEA delivery, and downstream BMAD
  execution.
- User-scope installation is the pilot boundary. Project-scope installation is
  deferred because its target metadata would recreate Greenfield friction.
- Local hooks are defense against normal and accidental misuse; protected CI,
  branch policy, or managed settings are needed against intentional bypass.
