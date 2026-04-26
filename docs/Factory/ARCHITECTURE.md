# Factory Architecture

## Version
v0.1

## Change Log
- v0.1 (2026-04-26): Initial portable architecture model for Factory Core, harness adapters, validators, extension packs, and project adapters.

## Purpose

Factory is an AI-first SDLC workflow for drift-resistant software delivery. It helps a product or domain owner turn rough intent into a bounded, testable execution contract before an AI coding agent writes code.

This starter kit is the reusable process layer. It should stay generic enough to work across many repositories, domains, and coding harnesses.

## Layer Model

### 1. Factory Core

Factory Core is the portable kernel:
- stage contracts
- artifact templates
- execution-mode rules
- Mission Mode rules
- context recall contract
- Product Owner lane contract
- pack audit requirements

Factory Core must not contain private project state, product-specific run history, customer-specific constraints, or domain-specific implementation assumptions.

### 2. Harness Adapters

Harness adapters describe how the same Factory stages run in different AI coding tools.

Examples:
- Codex App/Desktop
- Codex CLI
- Claude Code
- Cursor
- GitHub code review

Harness adapters may define model routing, reasoning effort, tool availability, skill/plugin usage, and automation hooks. They must not change the stage contracts.

### 3. Validators

Validators are deterministic checks that reduce manual policing.

Examples:
- knowledge lint
- mission lint
- context recall coverage checks
- pack lint
- closeout lint

Validators should enforce file presence, placeholder rules, size caps, checklist consistency, execution-mode consistency, and evidence completeness. They should not make subjective product decisions.

Use validators at two levels:
- `stage-lint` after each stage handoff, before the next stage starts
- `pack-lint` after Stage I2, before human review

### 4. Extension Packs

Extension packs are optional accelerators around the core workflow.

Examples:
- role-specific skills for Root Planner, Purple Gate, Pack Consolidator, and Execution Closeout
- Codex hook examples
- GitHub PR review helpers
- Slack or email status helpers
- browser QA helpers
- domain-specific research packs

Extension packs must be optional. A repo should still be able to run Factory Core without them.

### 5. Project Adapters

Each adopting repository owns its project adapter:
- `AGENTS.md`
- project state, roadmap, and changelog
- project-specific lint and test commands
- domain invariants
- source allowlists
- external signal feeds
- project-specific skills or plugins

Project adapters are allowed to be opinionated. Factory Core should remain neutral.

## Source-Of-Truth Rule

Generic Factory improvements should be authored in the starter-kit repository first, then imported into downstream projects.

Downstream projects may adapt their local project adapter, but they should not silently fork the core stage contracts, templates, or validators. If a downstream project discovers a reusable process improvement, promote it back into this starter kit before copying it elsewhere.

## Non-Goals

Factory is not:
- a code generator
- a replacement for testing
- a project management suite
- a private run-history archive
- a product-specific compliance framework

Factory can support high-compliance domains, but it is not limited to them.

## Improvement Roadmap

Near-term portable improvements:
1. Add optional Codex hook examples that run validators at useful lifecycle points.
2. Add generic Factory role skills.
3. Add `RUN_METRICS` guidance for stage timing, model/harness usage, drift indicators, and validator outcomes.
4. Add a domain-owner operating guide for users who are not developers but need to direct AI coding agents safely.
