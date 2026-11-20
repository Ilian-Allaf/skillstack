# Playbook: feature

Proof duties for a feature. Each duty is met, or skipped with its reason written in the PR.

1. **Seams agreed.** The public interfaces under test were named in `frame` and the user said go.
2. **One vertical slice at a time.** One test at one seam, then the least code that passes it, then the next slice. Each slice responds to what the last one taught you. Never all tests first, then all code.
3. **Tests that can fail** (`test-behavior-not-implementation`). No mocks of internal collaborators. Revert the implementation once and watch each new test fail.
4. **Every entry point.** The feature works from every entry point the feature map lists or will list. New entry points are added to the map in this PR.
5. **Prove on the app.** Drive the new journey on the head with `drive-<app>`, and show the base does not have it.
6. **Refactor after green, not during.** Clean-up goes in `clean`, with tests green before and after.

The verifier reverts the implementation and checks that each new test fails, and drives every entry point the feature map lists.
