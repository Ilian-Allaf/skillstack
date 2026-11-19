# Playbook: visual parity

Proof duties when the UI must look exactly the same after a change: a component migrated to a new library, a styling system replaced, two implementations matched. The baseline is the spec, and an image diff judges equivalence, not the eye. Each duty is met, or skipped with its reason written in the PR.

`done_when` has two parts, as for a refactoring: the migration target is red on the base (for example "no import of the old library in `src/ui/`"), and the image diff against the baseline is zero on the head.

1. **Baseline first.** Before anything moves, write a visual harness that screenshots each component in each of its states: empty, filled, error, hover, focus, each theme and size it supports. No baseline, no parity claim. This blocks the work; it is not a follow-up.
2. **Never touch the spec.** No edit to the harness, no new baseline images, no reshaping a component so a diff passes. If the baseline looks wrong, stop and ask the user.
3. **Shared primitives first.** Migrate the primitives other components use, then one component at a time. Parallel runs get one component each, in separate worktrees.
4. **Diff each component.** A nonzero diff is a FAIL. Find the cause of each changed pixel and fix it, then diff again, until zero.
5. **One PR per component or safe batch.** The coverage table lists each component and state with its diff result.

The verifier reruns the harness on the head, and checks that the baseline files and the harness did not change in the diff.
