# Onboarding Guide — Factory Starter Kit

> Audience: a contributor adopting the Factory pipeline in a repo that does not already have a governed planning framework.

## 1. What You Are Adopting

You are adopting a planning and governance framework, not a product implementation.

The Factory helps you force:
- explicit scope
- explicit constraints
- explicit verification
- explicit continuity recall

before coding starts.

## 2. What You Must Adapt First

Before your first run:
1. update `AGENTS.md`
2. fill in `docs/PROJECT_STATE.md`
3. fill in `docs/ROADMAP.md`
4. fill in `docs/CHANGELOG.md`
5. adapt `scripts/knowledge_lint.sh`
6. review the default recall source patterns in `scripts/factory_context_index.py`
7. adapt `scripts/mission_lint.sh` if you plan to use Mission Mode

## 3. Single-Sprint Path

For a normal sprint:
1. write a raw brief
2. run `bash scripts/knowledge_lint.sh`
3. run `./scripts/factoryctl context-index`
4. generate the run recall artifact
5. initialize a run
6. execute the Factory stage chain
7. review the final pack
8. decide Go or No-go

## 4. Multi-Sprint Path

Use Mission Mode only when:
- multiple sprints share one bounded mission arc
- dependencies are explicit
- you are willing to maintain the mission manifest in the same closure cycle as unit evidence

If you use Mission Mode:
1. lock the mission manifest and checkpoint
2. treat `MISSION_MANIFEST.md` as the only authored mission ledger
3. refresh `MISSION_CONTEXT_RECALL_REPORT.md` before checkpointing or authorizing the next unit
4. run `bash scripts/mission_lint.sh <MISSION_ID>` before advancing each already-authorized mission unit
5. keep project state docs and mission state in sync

## 5. Optional Product Owner Path

Use the Product Owner lane when:
- you want a governed phase-level planning layer upstream of Factory runs
- you want sprint-budget tracking and brief review before a brief enters Stage A

If you use the PO lane:
1. lock the Phase Intent
2. check budget in `PHASE_STATE.md`
3. generate the brief-cycle recall artifact
4. run the brief review cycle
5. only then hand the passed brief into the Factory as `raw_brief.md`

## 6. Common Failure Modes

- scope expansion hiding inside implementation details
- verification designed too late
- stale state docs after GO
- mission ledgers drifting during longer chains
- PO briefs drifting from locked phase intent
- recall artifacts treated as optional or generated too narrowly
- treating planning artifacts as optional

## 7. Practical Rule

If the docs and artifacts are drifting faster than you can keep them aligned, stop and harden the process before starting another sprint.
