# Premortem — MS-06 Disposable Live Qualification

## Version
v1

## Change Log
- v1 (2026-09-03): Imagined failure modes for the disposable live proof.

## Method
Assume the run failed or, worse, "passed" while proving nothing. Work backward to the causes the pack must make impossible or loudly detectable.

## Imagined Failures

1. **The proof was simulated.** The executor ran scripted checks instead of live workflows and the evidence looked identical. Cause: drivers not pinned or not enforced. Defense: only the three digest-pinned dedicated drivers produce valid live claims; driver digests are revalidated in evidence.
2. **The disposable repository was not disposable.** It was created under a donor, an existing registration, or via a symlinked path, and teardown deleted protected bytes. Defense: freshness/emptiness/non-symlink verification before seeding, symlink prohibition, and protected preimage/postimage comparison.
3. **Success destroyed its own evidence.** Teardown removed the only copy of the promoted snapshot and live logs. Defense: digest-pinned export to the external evidence root strictly before teardown; unexported evidence halts teardown.
4. **The BMAD tree drifted.** A network fetch installed a different BMAD build than the one the candidate was qualified against, invalidating every live claim. Defense: pre-existing local 6.10.0 tree pinned at activation; fetches forbidden.
5. **Live output leaked or overflowed.** Workflow output carried sensitive text into the harness transcript or blew the evidence budget. Defense: bounded-evidence rule, external full logs, secret scan before retention.
6. **Promotion happened by default.** The human was assumed to consent and a snapshot was promoted unreviewed. Defense: halt on missing review; unpromoted output stays inert.
7. **Residue survived.** Harness plugin caches or worktree registrations kept candidate state after teardown, contaminating later runs. Defense: residue inventory explicitly includes caches and registrations.
8. **A partial pass was oversold.** Authoring proofs passed, one denial proof failed, and the run claimed qualification "with notes". Defense: the partial-success rule maps any gap to `NO_GO`/`BLOCKED`; the ceiling admits no qualified-with-exceptions status.
9. **The candidate moved under the run.** The branch advanced between planning and activation, so the proof covered different bytes. Defense: activation pins commit `c23be98034215c17c9c49a7e9b6302cb2ad1f18d`; any mismatch halts.
10. **Evidence outgrew review.** Dozens of unbounded files made human review impossible and rubber-stamping likely. Defense: explicit external evidence ceiling and a bounded closeout evidence set.

## Highest-Leverage Defenses
Pinned drivers, pre-seeding containment verification, export-before-teardown sequencing, and the partial-success rule close the four failure classes that could silently produce a false qualification.
