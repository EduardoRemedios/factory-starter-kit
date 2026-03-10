# Onboarding Guide — Factory Starter Kit

> Audience: a contributor adopting the Factory pipeline in a repo that does not already have a governed planning framework.

## 1. What You Are Adopting

You are adopting a planning and governance framework, not a product implementation.

The Factory helps you force:
- explicit scope
- explicit constraints
- explicit verification

before coding starts.

## 2. What You Must Adapt First

Before your first run:
1. update `AGENTS.md`
2. fill in `docs/PROJECT_STATE.md`
3. fill in `docs/ROADMAP.md`
4. fill in `docs/CHANGELOG.md`
5. adapt `scripts/knowledge_lint.sh`
6. adapt `scripts/mission_lint.sh` if you plan to use Mission Mode

## 3. Single-Sprint Path

For a normal sprint:
1. write a raw brief
2. run `bash scripts/knowledge_lint.sh`
3. initialize a run
4. execute the Factory stage chain
5. review the final pack
6. decide Go or No-go

## 4. Multi-Sprint Path

Use Mission Mode only when:
- multiple sprints share one bounded mission arc
- dependencies are explicit
- you are willing to maintain the mission manifest in the same closure cycle as unit evidence

If you use Mission Mode:
1. lock the mission manifest and checkpoint
2. treat `MISSION_MANIFEST.md` as the only authored mission ledger
3. run `bash scripts/mission_lint.sh <MISSION_ID>` before advancing each already-authorized mission unit
4. keep project state docs and mission state in sync

## 5. Common Failure Modes

- scope expansion hiding inside implementation details
- verification designed too late
- stale state docs after GO
- mission ledgers drifting during longer chains
- treating planning artifacts as optional

## 6. Practical Rule

If the docs and artifacts are drifting faster than you can keep them aligned, stop and harden the process before starting another sprint.
