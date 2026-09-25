# Governed TEA automation (0.3.9 candidate)

TEA stays the team's test strategy, NFR and QA-review tool. This candidate adds
one bounded way to use TEA **automation** inside Factory-approved work. It does
not give TEA any Factory authority.

## What is allowed, and why only this

The behaviour below was established by reading the installed BMAD 6.12.1-next.0 /
TEA workflow files.

| Workflow | What it actually does | Factory status |
|---|---|---|
| `bmad-testarch-test-design`, `-nfr`, `-trace`, `-test-review`, `bmad-teach-me-testing` | Write reports under the test-artifacts folder; trace computes PASS/CONCERNS/FAIL | Allowed as evidence, as before. Their verdicts are advisory. |
| `bmad-testarch-automate` | Writes test files, fixtures and a summary. It can dispatch subagents, may widen coverage on its own, and may drive a browser. | **Admitted only under run-scoped authority (below)** |
| `bmad-testarch-atdd` | Writes deliberately skipped red-phase tests from story acceptance criteria | Prohibited. Skipped tests inside a delivery change are claims that no receipt can prove. It could join this lane later if test-first work is needed. |
| `bmad-testarch-framework` | Installs npm packages and merges PreToolUse/PostToolUse/Stop hooks into `.claude/settings.json` | Prohibited. It changes how the agent itself is governed. Run it, if needed, as its own reviewed change outside a Factory run. |
| `bmad-testarch-ci` | Writes CI workflow YAML and defines its own quality gates | Prohibited |
| `bmad-tea` (agent menu) | Dispatches other workflows. Its `prompt` items bypass the guarded Skill invocation. | Prohibited |

An approved parent never authorises a child. Each Skill invocation is checked on
its own. Subagents and step files that `automate` loads are not visible to the
hook, which is why containment is checked by the write-window compare, not by the hook.

## The lifecycle inside one run

1. **G1 pins the authority.** The run directory holds `bmad_automation_authority.json`:

   ```json
   {"schema_version": 1, "run_id": "RUN_20260925_1100_spec-042",
    "workflow": "bmad-testarch-automate",
    "inputs": ["bmad/_bmad-output/specs/spec-042-example/SPEC.md"],
    "write_roots": ["apps/e2e/tests", "bmad/_bmad-output/test-artifacts/automation-summary.md"]}
   ```

   The Intent Pack cites it as a `spec` source with its SHA-256, and
   `verification_definitions.json` includes a check that runs
   `automation-compare --run <RUN_ID>`. A human countersigns `INTENT_LOCK` and `EXECUTION_GO`.

   Write roots may not be, contain, or sit inside any of these:
   - `.claude`, `.agents`, `.codex`, `.github`, `.husky`, `.tea`
   - `docs/Conductor`, `docs/upstream`, `docs/adapters`, `scripts`
   - `AGENTS.md`, `CLAUDE.md`
   - the BMAD installation or skill tree
   - the repository root

2. **Open the window** (one per run), after the implementation edits are in place:
   `"$FACTORY_PY" "$COMPANION" --root . --json automation-capture --run <RUN_ID>`.
   It records the approved write roots and the digest of every watched file in
   `automation/window-001/preimage.json`. Watched files are:
   - every Git-visible file;
   - `.claude/settings.local.json` (at the root and in the BMAD install), `.git/config` and `.git/hooks`, even when ignored;
   - the run's own records, apart from the runner-owned `automation/`, `receipts/` and `postimage/` folders.
3. **Invoke** `bmad-testarch-automate`. The hook admits it only while the window is
   open. It adds context naming the inputs and write roots, and forbids:
   - package installs, manifest or lockfile edits, Pact and CI files, and hooks;
   - ATDD, framework, CI and `bmad-tea`;
   - treating TEA gate or approval text as authority.
4. **Close and check:** the pinned VM check (or a manual run of `automation-compare`)
   recomputes the whole window every time and writes `compare.json`. An existing
   `compare.json` is never trusted. It fails if any change since the capture is:
   - outside the write roots;
   - a dependency manifest or lockfile, even inside a root;
   - in a governance path, including the run's own intent, authority, countersigns or gaps.

   A failed compare fails the check. Record it as a Gap Request, not a waiver.
5. **Verification stays Factory's.** Generated tests count only through the run's
   pinned checks (for example the project's Playwright and precommit commands). TEA's
   summary is evidence for the independent G3 reviewer. It cannot change scope,
   waive a check or grant completion.

Admission also requires:
- exact pinned TEA bytes;
- inert per-skill overrides (no activation steps or `on_complete` callback);
- exactly one run holding authority;
- no completion countersign on that run.

A closed window admits nothing, and a run has only one. Another automation pass needs a new run.

## Limits

- **Trust boundary.** The compare detects TEA writing outside its folders by accident or
  misdirection. It is not tamper-proof against an agent that deliberately edits Factory's own
  evidence: the window's `preimage.json`, `receipts/` and `postimage/` sit in the repository and are
  not watched. Anything that can write the repository could rewrite them. Receipts and the protected-file compare share this
  boundary; checksums establish consistency, not independent authentication.
- **Records during the window.** Refreshing `review-packet` or re-running `receipts run` while the
  window is open rewrites watched run files, so the pinned compare then fails. Run the compare check first.

- **What it cannot see.** Apart from the watched governance files above, writes to
  ignored paths (for example `node_modules/`, `.env`), `/tmp` or outside the
  repository are not detected. That includes writes through a symlink that points
  outside. Their absence is not proven.
- **Order matters.** The pinned check recomputes against the current tree, so any
  out-of-root change after capture fails it, even a legitimate implementation edit.
  Implement first, then capture and run TEA. The compare cannot tell who wrote a file.
- **Write roots** may not be symlinks or case variants of a forbidden path.
- **6.10.0 is not covered.** The TEA version paired with 6.10.0 has no pinned
  profile, so `automate` stays denied there.
