# Odyssey v3 Initial BMAD Brief

## Working Name

Triage Desk

## Goal

Build a small local-first web app that lets a solo operator review a short list
of incoming support or operations notes and classify them into action buckets.

This is a regression pilot for the BMAD-to-Factory transition. The application
must stay deliberately modest; the test target is workflow quality, evidence
quality, and handoff discipline, not product ambition.

## Initial Product Slice

The first version should support only:

1. A seeded list of 8 to 12 notes loaded from a local JSON fixture.
2. Three classification buckets:
   - Needs Reply
   - Needs Investigation
   - No Action
3. A detail panel for the selected note showing title, source, received time,
   body, and current bucket.
4. A simple way to move a note between buckets.
5. A summary count by bucket.
6. A local export button that downloads the current classifications as JSON.

## Explicit Exclusions

- No authentication.
- No database.
- No external APIs.
- No AI features.
- No notifications.
- No team collaboration.
- No mobile app.
- No backend unless the selected scaffold already requires one.
- No analytics, billing, CRM, inbox integration, or automation rules.

## BMAD Brainstorming Boundary

BMAD may help clarify:

- user persona and operating context;
- note fields and classification language;
- one fast-path workflow;
- one or two UX risks;
- what should be intentionally excluded from the Factory implementation brief.

BMAD must not expand the scope into a helpdesk, CRM, ticketing system,
collaboration suite, automation engine, or AI assistant.

## Factory Handoff Target

The BMAD output should become a bounded Factory raw brief with:

- a promoted immutable BMAD artifact citation;
- the local JSON fixture requirement;
- the three buckets and export behavior;
- clear exclusion list;
- acceptance criteria for classify, recount, select, and export flows;
- verification expectations suitable for deterministic local tests.

## Success Criteria

- A user can open the app, classify every note, see counts update, and export the
  result.
- The BMAD handoff produces a bounded implementation brief with clear exclusions.
- Factory produces deterministic verification evidence for the implemented
  slice.
- No Odyssey v2 state is reused as an authority for Odyssey v3.
