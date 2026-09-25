# AI-native SDLC implementation roadmap

Original direction: 2026-09-19. Status update: 2026-09-25.

Status: planning only. Phase 0 is the immediate priority; later phases are
proposed increments, to be refined before execution. No dates or delivery
commitments are assigned.

## Purpose and priority

Extend Factory/Conductor and its BMAD integration into a more complete, usable
AI-native software delivery system. Anthropic's
[AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook)
is a reference for the broader lifecycle, evaluation, operational and adoption
capabilities. This roadmap proposes our implementation of relevant capabilities;
it does not imply that the playbook itself supplies a complete implementation.

**The pilot team must be able to use the qualified work without waiting for this
roadmap to be completed.** Its first real delivery slice is the immediate
priority. Broader capability development follows evidence from actual use.

The starting position includes working delivery governance and BMAD intake,
promotion and reconciliation mechanisms. The BMAD 6.12.1 and TEA work is integrated in 0.3.10.
Publication, installation and successful pilot delivery remain distinct;
integration does not establish that the pilot's real delivery slice is complete.

## Phase 0 — Unblock the pilot with one real delivery slice

**Outcome:** the team can take one agreed Spec through the existing Factory path
and repeat the process from written instructions.

**Entry:** confirm the team's selected Spec and current branch before continuing
the real delivery slice. Use the latest written handoff and team feedback; do not
assume a previously reviewed branch or example remains current. This roadmap
does not restart or supersede the existing pilot handoff.

Work:

- Confirm the exact BMAD, Factory and harness versions and the project's local
  configuration. Resolve only incompatibilities that affect this delivery path;
  preserve legitimate project customisations.
- Prepare a written walkthrough using that Spec: BMAD Spec and companion context
  → Factory intake → hardening/questions → BMAD reconciliation → approval →
  implementation → review. Show the actual command or action, responsible role,
  expected result and next legal action at every handoff.
- Explain which material is authoritative at each point. BMAD owns upstream
  authoring; promoted context supplies frozen evidence; approved Factory intent
  governs delivery. Reconciled requirements must not silently change locked intent.
- Exercise the walkthrough within separately approved project scope. Record actual
  results, human stops and any friction. Completion, merge and release remain
  distinct decisions.
- Fix reproducible blockers narrowly, verify the repairs and return to the slice.
  Record broader improvements for later phases.

**Exit evidence:** one real slice has completed the agreed lifecycle, including
independent review and human completion acceptance; the team has a usable written
guide and has confirmed whether it can repeat the handoffs. Any remaining
unproven steps and limitations stay explicit. A maintainer-only rehearsal does
not prove unaided team adoption.

**Not required:** a workshop, company-wide rollout, new dashboards, broad
automation or completion of any later phase. Work may begin on the approved
slice before the entire Phase 0 learning cycle is complete.

## Phase 1 — Make the handoffs repeatable and easy to use

**Outcome:** an adopter can understand and advance the existing workflow without
repeated maintainer interpretation.

Use Phase 0 friction to choose the smallest improvements: clearer next-action
guidance, role-specific examples, complete context intake, actionable questions,
reconciliation and safe resume behaviour. Reduce manual copying of paths and
identities while keeping explicit human approval and evidence binding intact.
Advance automatically only where an existing approval and valid state permit it.

**Entry:** real friction is recorded and prioritised; the pilot continues on its
working path. **Exit evidence:** a team member repeats the agreed journey from
the instructions, including one requirements correction and one interrupted
resume, with no lost context or bypassed authority.

**Decide before execution:** supported harnesses, exact user actions and which
friction warrants code rather than clearer documentation. Do not build a new
orchestrator merely to wrap commands that already work.

## Phase 2 — Measure delivery and evaluate agent behaviour

**Outcome:** changes to models, instructions, skills and integrations can be
assessed against representative work and observed delivery results.

Build a small, permissioned set of real-task evaluation cases from pilot work,
including successful delivery, ambiguous requirements, reconciliation and unsafe
or out-of-scope requests. Keep deterministic contract tests and agent behaviour
evaluations distinct. Record configuration, outcomes, limitations and cost for
each comparison.

Establish a lightweight baseline for elapsed delivery time, human review effort,
rework, recurring blockers and defects found after acceptance. Separate waiting
time from work time and measured values from estimates. Use findings to propose
reviewed changes to instructions, examples and evaluation cases.

**Entry:** representative evidence and permission to reuse it exist. **Exit
evidence:** a repeatable baseline and a comparison after one controlled change,
using agreed criteria, plus one measured improvement cycle. No claims of general
agent reliability from a small sample.

**Decide before execution:** dataset ownership, sensitive-data handling, metrics,
evaluation budget and what result blocks an upgrade. Begin manual measurement
during Phase 0 if useful; dashboards are not a dependency.

## Phase 3 — Integrate team review and managed execution controls

**Outcome:** the qualified delivery path fits normal team repositories and their
security controls, with less manual review administration.

Deliver two separately scoped increments:

1. Connect pull-request review, bounded repair and re-verification to Factory
   evidence. Preserve independent review and human merge authority. Define retry
   limits, failure escalation and treatment of changes after approval.
2. Define and verify a supported team execution profile using existing harness,
   repository and IT controls: permissions, sandboxing, credentials, approved
   tools and branch protection. Document what those controls enforce and what
   remains policy only.

**Entry:** a target team, repository and supported tool configuration are chosen.
**Exit evidence:** a real PR completes the review/repair/check loop and relevant
negative cases demonstrate the stated access boundaries in that configuration.

**Decide before execution:** review responsibilities, permitted repairs and
central control ownership. Factory is the authorised delivery path; assess
third-party workflows by their behaviour and authority effects. Do not promise
universal blocking or rebuild the harness's security infrastructure.

## Phase 4 — Connect completion to safe release

**Outcome:** an accepted change can follow the project's approved deployment path
with verifiable release and recovery evidence.

Integrate with one project's existing CI/CD: environment-specific authority,
release checks, post-deployment validation, stop conditions and recovery actions.
Keep application rollback distinct from plugin installation rollback. Include
data migration and irreversible effects where relevant; a rollback command alone
does not establish recoverability.

**Entry:** the project's release owner and deployment controls are identified.
**Exit evidence:** a representative deployment and recovery rehearsal in an
approved environment, with results bound to the reviewed change. Production
execution remains separately authorised.

**Decide before execution:** environments, release approvals, health criteria and
recovery objectives. Project-specific DevOps mechanisms remain project-owned.

## Phase 5 — Close the operational feedback loop

**Outcome:** production experience creates prioritised, evidence-backed work and
improves subsequent delivery.

Connect a bounded source of operational feedback—such as an incident, defect or
scheduled scan—to triage, diagnosis and a proposed new delivery slice. Reconcile
requirement changes with BMAD context where applicable. Link the resulting
approved work to its originating signal and verify the outcome after release.

**Entry:** a project has suitable operational signals, access controls and an
accountable triage owner. **Exit evidence:** one traceable cycle from observed
signal through prioritisation, approved fix and outcome verification; recurring
lessons produce a reviewed update to guidance or evaluations.

**Decide before execution:** signal quality, triage ownership, notification rules
and permitted automation. An alert grants no authority for production writes or
unattended repair.

## Sequencing and scope rules

- Phase 0 takes precedence over broader roadmap work. Phases 1–5 are not
  prerequisites for pilot adoption or continued delivery.
- Bring a change into Phase 0 only when evidence shows that the chosen slice
  cannot proceed correctly, safely or understandably without it. Nice-to-have
  automation and generalisation stay in the backlog.
- Necessary fixes retain the existing governance boundaries. Do not bypass a
  failed check, discard evidence or silently widen approval to remove friction.
- Later phases are incremental capabilities, not a single platform replacement.
  Existing project practices continue. A project need may justify bringing
  forward a bounded release or operational integration without completing every
  earlier phase; record the reason and actual prerequisites.
- Before activating an increment, define the observed problem, smallest useful
  deliverable, acceptance evidence, write boundaries, responsible roles,
  dependencies and capacity. Then obtain the applicable implementation authority.
  Roadmap inclusion is not a locked intent or execution approval.
- Prefer existing harness, GitHub and DevOps capabilities. Factory owns delivery
  authority and evidence; it should integrate with those systems rather than
  duplicate their responsibilities.
- Revisit priorities after the first pilot slice and subsequent measured
  feedback. Track published versions, qualified candidates, installed versions
  and completed project outcomes separately.

## Coverage of the identified gaps

| Gap | Primary increment |
| --- | --- |
| Connected BMAD-to-Factory handoffs | Phase 0 practical example; Phase 1 repeatability |
| Real-task agent evaluations | Phase 2 |
| Continuous PR review and bounded repair | Phase 3, first increment |
| Organisation-wide runtime controls | Phase 3, second increment |
| Deployment and application recovery | Phase 4 |
| Operational feedback and maintenance | Phase 5 |
| Delivery measurement and continuous learning | Phase 2 baseline; feedback throughout |

Supporting authority: [Conductor invariants](INVARIANTS.md) and
[merge protocol](MERGE_PROTOCOL.md). This document changes neither.
