# 0018. A verdict covers the tested base and head

- **Status**: accepted, 2026-11-23. Supersedes only the patch-id reuse clause of [0004](0004-a-finding-blocks-only-when-proven.md).
- **Applies to**: `skills/verify-pr/`, `skills/babysit-pr/`, `skills/ship/`, `skills/ship-queue/SKILL.md`, `skills/constitution/references/glossary.md`, `skills/constitution/references/pr-format.md`
- **Enforced by**: `skills/ship/scripts/check_evidence.py` rejects a recorded verdict whose base or head differs from the current values supplied by the caller; `tools/test_check_evidence.py` exercises a conflict-free rebase that keeps the patch id but breaks behavior. The code-host freshness check, rule and environment record, and removal of `ready` remain instructions checked by review.

## Context

ADR 0004 let a pure rebase retain a verdict when the stable patch id was unchanged. Our reproduction changes a dependency on the target branch and then rebases a patch touching another file. Git reports no conflict and the patch id stays the same, but the program prints 40 instead of the previously verified 20. The patch id describes edits, not their interaction with the base. The executable reproduction is `EvidenceTest.test_conflict_free_rebase_keeps_patch_but_breaks_behavior` in `tools/test_check_evidence.py`; the example and decision are ours.

## Decision

A verdict covers the exact base and head commits checked, identified by full SHAs. Base means the tip of the PR's target branch at verification time, not the merge base. The verdict records the rule revisions and replay environment used. The patch id remains a description of the diff, never permission to reuse a verdict.

A changed base or head requires fresh proof and a new verdict, including after a conflict-free rebase or a target-branch update without a push to the PR. A missing identity in an older verdict also requires a new verdict. Remove `ready` while the current pair lacks a valid verdict. The verifier rechecks the code host before posting, and babysitting checks again before marking ready. Old results remain historical. Even with the same commits, changed rules or setup require checking whether the recorded verification still applies.

Keep the record in the existing verdict comment and CI artifacts. The local evidence index remains outside git. No database, runtime state in the application, or committed per-run file is introduced. This decision records which rules were used; a policy for freezing private tools or adjudicating proposed rule changes is a separate decision.

## Alternatives rejected

- **Reuse by patch id**: misses the executed counterexample.
- **Reuse by head alone**: misses target-branch changes that affect integration and the comparison against the base.
- **Reuse by tree identity or dependency analysis**: may save runs, but requires proving which rules, dependencies, and environments are equivalent. Start with the conservative rule.
- **Persist every run in the source repo or a new service**: existing PR comments and artifacts already hold the evidence.

## Consequences

Rebases and target-branch updates cost a new verification, even when harmless. A metadata-only commit does too. Every affected PR in a stack follows the same rule. Older evidence records containing only a patch id fail the local check until a new verdict supplies both SHAs. The check validates the index, not the truth of a PASS, the caller's current SHAs, or the replay environment. The rest of ADR 0004, including proof and grading of findings, stands.
