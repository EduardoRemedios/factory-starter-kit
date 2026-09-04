# Conductor Invariants

Read this file and `docs/PROJECT_STATE.md` before any Conductor-governed work. Everything else is on demand. This file states what Conductor governs and the rules that never bend; it does not tell you how to sequence your work.

## 0) Governing principle

Conductor governs **authority, outcomes, and write boundaries**. It does not govern steps.

| Constraint | Question it answers | Hard mechanism |
|---|---|---|
| Authority | Who may authorize what, against which exact artifact digest? | Human countersign files, hash-pinned intent and snapshots, default-deny adapter policies |
| Proof | What evidence proves a claim? | Runner-produced receipts, Statement of Completion lint, fresh-context verifier |
| Write boundary | Where may writes land? | Protected roots, protected-postimage compare, adapter workspace containment, hooks |

Instruction prose (this file, skills, guides) is soft: user instructions override it in every harness. Only schemas, validators, hooks, and CI are hard. A rule that must hold lives in the hard layer and is merely explained here.

## 1) Three gates

- **G1 Intent Lock** (human): the Intent Pack validates and a human countersigns its digest. Effort and model are declared.
- **G2 Governed Execution** (autonomous): work proceeds end to end inside the locked intent. Every declared check gets a runner-produced receipt. No write lands outside declared boundaries.
- **G3 Adversarial Review and Completion**: a fresh-context verifier audits every claim against its receipt; the Statement of Completion lint derives the closeout state; a human countersigns. Merge authorization follows `MERGE_PROTOCOL.md` unchanged.

Humans are involved at exactly two points per run: G1 and G3 (plus G2 entry when execution is enabled). Nothing else pauses for a human.

## 2) Autonomy contract

Loaded for every G2 run through the AGENTS.md managed block:

> You are operating under Conductor governance. The Intent Pack sets the scope and the scope is the deliverable: do not narrow, widen, or swap it. For reversible actions inside the locked intent, proceed without asking. Stop only for a destructive action, a genuine scope change, or input only a human can provide; record such a stop as a Gap Request, not as a question in chat. Before reporting progress, audit each claim against a receipt from this run; report only what a receipt proves, and say explicitly what is not yet verified. Before ending your turn, check your last paragraph: if it is a plan, a question, or a promise, do that work now. Implement the smallest clear change (SIMPLE-CODE-GATE v2 applies). Do not write tests for reversible, low-impact changes beyond what the verification manifest requires.

## 3) Hard Guardrails
- Preserve fail-closed behavior for regulated and consequential actions.
- Do not expand scope implicitly; new scope must be explicit and approved.
- Keep schema-locked boundaries intact.
- Keep deterministic ordering and evidence-chain integrity in reports and artifacts.
- Run Factory-controlled Python verification through `./scripts/conductor-python`; do not bypass its bytecode guard with a raw interpreter command.
- Keep complete high-volume evidence in an explicitly authorized file and emit only bounded summaries through the harness. Never make conversational output the evidence store.
- Do not create a second authored source of truth for mission state when Mission Mode is active.
- Keep continuity artifacts as evidence aids, not as replacement authority for the underlying source documents.
- If an adopting repo has a separate autonomy governance kernel, do not duplicate kernel authority, policy, evidence, lease, or runtime-action behavior inside Factory.

## 3.1) SIMPLE-CODE-GATE (v2)
Availability:
- Mandatory implementation guardrail for Factory-controlled code-changing work.
- Applies to planning, execution, and review wherever Factory controls implementation scope.

Core Directive:
- Implement the smallest clear, behavior-preserving change.
- Prefer direct, readable, local code over cleverness or premature abstraction.

Banned List:
- No Code Bloat: avoid copy-paste chunks, awkward abstraction layers, and bloated multi-purpose helpers.
- No Spooky Action: avoid brittle request-path mutation, hidden side effects, or passing unvalidated junk through middleware/boundary layers.
- No Dependency Creep: use the standard library and existing repo utilities first. Do not introduce external packages unless explicitly authorized and justified.
- No Silent Failures: do not swallow exceptions or return ambiguous `None`/empty fallbacks just to keep a path limping along. Fail fast for invalid config/init/state. In runtime policy paths, fail closed explicitly with reason codes, evidence, and tests.

Abstraction Firewall:
- Add an abstraction or helper only when it passes all four checks:
  1. Removes real, existing duplication.
  2. Names a stable domain concept.
  3. Reduces branching or call-site complexity.
  4. Has a clear owner/boundary in the current architecture.

Future-Proofing and Context:
- Do not add generic frameworks, registries, strategy layers, plugin seams, or broad indirection just because future variation is possible.
- If future variation is uncertain, keep the code explicit and document the specific scale metric, repeated pattern, or business condition that will trigger a refactor.
- Comments must explain why, not what. No line-by-line narration of obvious logic.

## 4) Upstream lanes

Upstream product-context tools (installed through an adapter) author candidate context in their own workspace. Their output has no Conductor authority until a human promotes it to an immutable, hash-pinned snapshot, and even then it is evidence that G1 may accept, reject, or defer. Delivery-lane workflows of upstream tools are prohibited for Conductor-bound work. Each adapter's policy file enumerates its lanes; unknown workflows are denied by default. The hook that enforces this is an invocation gate, not a filesystem sandbox: write containment is proven separately by the protected-postimage compare.

## 5) AGENTS.md composition

Conductor owns exactly one block in `AGENTS.md`, delimited by `<!-- conductor:managed:start ... -->` and `<!-- conductor:managed:end -->`. The start marker records the Conductor version and the SHA-256 of the block body. Everything outside the block is project-owned and is preserved byte for byte by adoption and update. A managed block whose recorded digest does not match its body is a validation error.

## 6) Known pitfalls (short list)

- A countersign whose subject digest no longer matches its subject file is stale and grants nothing.
- A claim in a Statement of Completion without a receipt is not `verified`, whatever the prose says.
- `REVIEW_READY` is never merge approval; only the merge protocol produces `MERGE_READY`.
- Legacy upstream installations are inert evidence under the adapter's legacy namespace, never a second active root.
