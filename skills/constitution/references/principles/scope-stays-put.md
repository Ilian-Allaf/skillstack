# scope-stays-put

**Apply when** a review, an impact analysis, or the build finds something outside the task.

**Rule.** Open an issue for it. The PR stays on its task.

## How

- A finding outside the task becomes an issue, linked from the PR, with its evidence, unless it blocks the goal: then it is the task's to fix, in its own PR when it is outside the diff (rule 12 of the constitution).
- A sibling of the bug being fixed is in scope when it is the same fault in the same area; otherwise it gets an issue too.
- A refactoring the task reveals ships first, in its own PR, or gets an issue.

## Test

Does every hunk of the diff serve `done_when`?

## Sign it was skipped

A bug fix that also renames a module. A PR whose description needs "and also".
