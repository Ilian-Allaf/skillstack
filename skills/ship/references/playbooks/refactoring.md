# Playbook: refactoring

Proof duties for a refactoring: the structure changes, the behavior does not. Each duty is met, or skipped with its reason written in the PR.

If the work reveals a bug or a missing feature, split it out: ship the structural change first, then the fix through its own playbook. A redesign that changes behavior is a feature.

`done_when` has two parts. The target structure is observable and red on the base, for example "`rg oldApi` returns nothing" or "the cycle check passes". The pin is green on the base and stays green on the head.

1. **Pin the behavior first.** Write a characterization test, a snapshot, or an equivalence script that captures what the code does today, before any structure moves. Run it green on the base. Type checks and lint are not a pin.
2. **Name the missing structure and the target shape.** Name the data shape the code lacks, then the module layout, types, and call graph you would build today, as [design.md](../design.md) describes. Sketch twice when the target crosses a boundary. The reshape follows `model-the-domain`.
3. **Subtract before you add** (`subtract-before-you-add`). Delete dead code, one-caller wrappers, redundant validators, and orphan references before the new shape goes in. A cleanup that only "might help" gets reverted.
4. **Small steps, pin green.** Each step keeps the pin green. For an API reshape, apply `migrate-callers-then-delete` in this PR. Check every rename in strings, docs, and config too; renames miss them silently. For repetitive edits, write a codemod or script (`build-the-lever`).
5. **Prove behavior is unchanged on the real artifact.** The pin passes on the head. For a larger reshape, add an equivalence run: a script that diffs old and new outputs, a recorded baseline replayed on the head, or the same journey on base and head with `drive-<app>`.
6. **Show the reader load went down** (`minimize-reader-load`). Name where the code is now easier to read: fewer layers between a question and its answer, or less state to hold. If the diff lowers it nowhere, revert it.
7. **Ordered commits.** A subtraction commit, then the reshape, then any follow-up cleanup, each one green.

The coverage table lists each case of the pin with the same result on base and head. The PR adds no behavior. The verifier runs the pin on the base and the head, treats any added behavior as a finding, and writes a note when it cannot see where reader load went down.
