# sequence-verifiable-units

**Apply when** the work has several steps: a sweep, a migration, a run of similar edits, a stack of commits or PRs.

**Rule.** Cut the work into small units that each end on a check, verify each before the next, and order the delivery so the sequence proves itself to a reviewer.

## How

- Each unit is a bracket: a known-good state, one change, the check, then the next unit. A break caught at the unit that caused it is cheap to locate; a break found after a batch is buried.
- Start from a clean base, so every check measures against the real baseline.
- Order the commits as an argument: the failing test, then the fix; the subtraction, then the reshape; the baseline, then the change; the scaffold, then the feature.
- Each commit and each PR lands green on its own.

## Test

Could a reviewer replay the commits in order and watch each one go from red to green?

## Sign it was skipped

One commit with every change. Checks run only at the end of a long run.
