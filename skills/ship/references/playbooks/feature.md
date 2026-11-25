# Playbook: feature

Proof duties for a feature. Each duty is met, or skipped with its reason written in the PR.

1. **Seams named.** The public interfaces under test are named in the frame.
2. **Integrated, not bolted on** (`redesign-from-first-principles`). When the feature lands in an existing design, the design note's Alternatives rejected names the bolt-on and why it lost. The shared types and the test harness the slices need come first (`design-the-data-first`).
3. **One vertical slice at a time.** One test at one seam, then the least code that passes it, then the next slice. Each slice responds to what the last one taught you. Never all tests first, then all code.
4. **Tests that can fail** (`test-behavior-not-implementation`). No mocks of internal collaborators. Revert the implementation once and watch each new test fail.
5. **Every entry point, every consumer.** The feature works from every entry point the feature map lists or will list; new entry points are added to the map in this PR. When it improves a shared primitive, every consumer of that primitive gets the improvement and is checked.
6. **Prove on the app.** Drive the new journey on the head with `drive-<app>`, and show the base does not have it.
7. **Refactor after green, not during.** Clean-up goes in `clean`, with tests green before and after.
8. **Close the gap to each visual target**, when the spec holds some. Read the design system of the area in the code first, and build in the spec's design mode with the rules of [ui.md](../../../constitution/references/ui.md). Lay out every target state still, then run the [target loop](../visual-loop.md), then add motion as its own slice.

The verifier reverts the implementation and checks that each new test fails, drives every entry point the feature map lists, and checks that a feature changing an existing design names the bolt-on it rejected. When the spec holds visual targets, it checks that each has a row with its side-by-side images, and that a component the design mode did not allow is not added.
