# Conductor Design Pack — 04 BMAD Lane Policy

Policy is expressed by responsibility, not by enumerating each workflow's permission (agreed boundary, brief §0 and §6). Two lanes. Default deny for anything unclassified. Skill names below are the BMAD 6.10.0 names the 0.2.5 companion already knows (`SUPPORTED_BMAD_SKILLS`, `SUPPORTED_TEA_SKILLS`).

## 1. Lane definitions

**Product-context lane** — any BMAD workflow whose write set stays inside `lanes.product_context.write_roots` (default `_bmad-output/`) and that produces no delivery artifact. Its output is candidate solution context; it acquires citability only through human promotion to an immutable snapshot, and never acquires Conductor authority.

**Delivery lane** — workflows that plan, sequence, implement, review, or gate delivery. Prohibited for Conductor-bound work. Conductor is the authorized delivery-governance path; developers and their coding agents execute inside the scope Conductor has locked.

## 2. Classification of BMAD 6.10.0 workflows

| Lane | Workflows |
|---|---|
| Product-context: discovery | `bmad-brainstorming`, `bmad-forge-idea`, `bmad-product-brief`, `bmad-prfaq`, `bmad-market-research`, `bmad-domain-research`, `bmad-technical-research`, `bmad-prd`, `bmad-create-prd`, `bmad-edit-prd`, `bmad-validate-prd`, `bmad-document-project`, `bmad-help` |
| Product-context: solution-context authoring (digest-pinned profiles) | `bmad-architecture`, `bmad-spec`, `bmad-ux` |
| Product-context: **helpers** (same-lane nesting permitted) | `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`, `bmad-advanced-elicitation`, `bmad-party-mode`, `bmad-shard-doc`, `bmad-index-docs` |
| Product-context: **evidence-only** (TEA design level) | `bmad-testarch-test-design`, `bmad-testarch-nfr`, `bmad-testarch-trace`, `bmad-testarch-test-review`, `bmad-teach-me-testing` |
| Product-context: persona agents | `bmad-agent-analyst`, `bmad-agent-pm`, `bmad-agent-ux-designer`, `bmad-agent-architect`, `bmad-agent-tech-writer` — permitted only while the active workflow is product-context; the hook evaluates the workflow they invoke |
| **Delivery (prohibited)** | `bmad-create-epics-and-stories`, `bmad-create-story`, `bmad-dev-story`, `bmad-dev-auto`, `bmad-quick-dev`, `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-code-review`, `bmad-correct-course`, `bmad-check-implementation-readiness`, `bmad-retrospective`, `bmad-qa-generate-e2e-tests`, `bmad-testarch-automate`, `bmad-testarch-ci`, `bmad-testarch-atdd`, `bmad-testarch-framework`, `bmad-generate-project-context`, `bmad-create-architecture` (deprecated shim), `bmad-agent-dev`, `bmad-tea` (agent), `bmad-loop` (module; presence still blocks intake) |
| Unclassified / unknown `bmad-*` | deny (`unknown_default`) |
| Neutral tooling | `bmad-customize`, `bmad-project-settings`, `bmad-manifest`, `bmad-checkpoint-preview`: permitted, no context injected; changes to customization are caught by profile digest checks |

Decisions embedded here that a human may still change (07): `bmad-party-mode` in helpers (Eduardo: allowed, 2026-09-04); `bmad-retrospective` in delivery; the five TEA design-level workflows in evidence-only.

## 3. Hook rule: evaluate the invoked skill, not its parent

Today: "a parent workflow cannot authorize a nested skill", which breaks PRD finalization (mandatory review step) and elicitation. Conductor:

1. On every `PreToolUse(Skill)` and `UserPromptExpansion`, classify **the skill being invoked** by lane.
2. Product-context or helper → allow, inject the non-authority context block.
3. Delivery → deny with reason code `CONDUCTOR_BMAD_LANE_DELIVERY_PROHIBITED`, naming the skill and the lane.
4. Unknown → deny `CONDUCTOR_BMAD_LANE_UNKNOWN`.
5. Nesting is irrelevant to the decision: party mode may call review; review may call elicitation. Party mode cannot reach `bmad-dev-story` because step 3 fires on that invocation. This is the negative proof AC-L2 must show.

Write-boundary containment remains a separate check (postimage compare over `write_roots`), not a hook responsibility. The hook is an invocation gate, not a sandbox, exactly as BMAD_POLICY v1.1 states.

## 4. Layout rule: unsafe layouts block authority actions only

| Layout state (existing `assess_bmad_layout`) | Today | Conductor |
|---|---|---|
| `canonical_root` or `declared_root` (new) | enforce normally | enforce normally |
| `nested`, `partial`, `multiple_roots`, `manifest_ambiguous`, any symlink state | deny **every** BMAD skill | deny `intake`, `promote`, solution-context authoring (`unsafe_layout_blocks`); **allow discovery and helpers with a warning context** naming the layout finding |
| `legacy_archive_inert`, `absent` | inactive | inactive |

## 5. Declared root

`PROJECT_CONFIG.json → bmad.declared_root`. Exactly one. Constraints enforced by `assess_bmad_layout`: repo-relative, no symlink components, contains `_config/manifest.yaml`, not under `docs/`, not equal to the legacy evidence root. Every digest, version, override-inertness, and files-manifest check that applies at `_bmad` applies unchanged at the declared root. A canonical `_bmad` **and** a differing declared root is `multiple_roots` (unsafe). This satisfies "split installations" without a free-form path.

## 6. Legacy trees

Preserved only under `docs/adapters/bmad/legacy-evidence/`. Never under `docs/upstream/` (the context index scans it). The AuditEdge clone's `docs/upstream/bmad-legacy-spike-1/` is therefore non-compliant and is the "update from non-compliant layout" fixture in 06 §4. Audit's zero-write remediation preview remains the only path that proposes a move; the move itself needs exact-plan approval.

## 7. Deny message specification

Replace the constant "Doctor was not run; /factory-bmad:doctor is only the suggested next action." with:

```
<REASON_CODE>: <skill> is <lane> for Conductor-bound work.
Layout: <layout state> (<layout reason code>).
Allowed here: <discovery|helpers|none>. Next: <one concrete command>.
```

The existing test `test_denial_says_doctor_was_not_run` is inverted to assert this shape.

## 8. Promotion, supersession, feedback

Unchanged from 0.2.5: human promotes selected `_bmad-output/` content to `docs/upstream/bmad/<SNAPSHOT_ID>/` with `SNAPSHOT_MANIFEST.json`, aggregate digest, `EVIDENCE_ONLY` authority, optional supersession pair. New: a Gap Request (03 §4) is the only artifact that carries a question from a Conductor run back to the product-context lane. A resolution that introduces a new snapshot with `supersession_impact = active_scope` reopens G1.

## 9. Acceptance criteria → qualification step

| AC | Statement | Proven by (06 §4) |
|---|---|---|
| AC-L1 | PRD flow ending in `bmad-review-*` with `bmad-advanced-elicitation` completes under the hook | Disposable adoption, Claude Code harness; hook decision log shows allow for each nested invocation |
| AC-L2 | `bmad-party-mode` cannot reach a delivery-lane skill | Same run; scripted party-mode session attempts `bmad-dev-story`; hook log shows `CONDUCTOR_BMAD_LANE_DELIVERY_PROHIBITED`; packaged-hook sentinel matrix extended with PT-09 |
| AC-L3 | Declared non-root BMAD root passes doctor and intake | Disposable repo with BMAD at `tools/bmad/_bmad` and matching Project Config |
| AC-L4 | Nested legacy tree blocks only authority actions | Spike-1 rehearsal pass two (update from non-compliant layout): discovery allowed with warning, promote denied |
| AC-L5 | TEA design output promotable as EVIDENCE_ONLY; `bmad-testarch-automate` denied | Disposable adoption with TEA 1.21.1 installed |
| AC-L6 | Gap Request round-trips to a new snapshot with a supersession decision | Spike-1 pass one: PLANNING_ONLY run emits one Gap Request; human resolves; lint shows G1 reopened |

Every AC produces receipts and appears as a row in the qualification Statement of Completion.
