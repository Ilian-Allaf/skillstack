# Spec

Synthesize what the interview settled; do not interview again.

## Before writing

1. Read the code the spec touches, the repo glossary, and the ADRs of the area. Use the glossary's terms throughout.
2. Choose the seams the feature will be tested at: existing seams before new ones, the highest seam possible, as few as possible; one is ideal. Check them with the user.

## Template

Publish it to the issue tracker, labeled `spec`.

```markdown
## Problem
The user's problem, from the user's side.

## Solution
The solution, from the user's side.

## Done when
The observable condition that says the whole spec is delivered, agreed with the user in the grill: a command, a test, or an app journey that answers yes or no. `ship` takes it as the task's `done_when`.

## User stories
1. As a <actor>, I want <feature>, so that <benefit>.
(A long list that covers every part of the feature, edge cases included.)

## Seams
The public interfaces the tests will use, agreed with the user.

## Decisions
Modules built or changed, their interfaces, schema changes, API contracts, architecture choices, and the ADRs they rest on.
No file paths and no code: they go stale. Exception: a snippet from a prototype that pins a decision better than prose (a state machine, a type, a schema), trimmed to the decision.

## Testing decisions
What a good test is here (external behavior only), which modules get tests, and the existing tests to copy.

## Out of scope
What this spec will not do.
```

## From spec to proof

Each user story becomes at least one case in `frame` (see [coverage.md](../../constitution/references/coverage.md)), so the coverage table of the final PR answers the spec story by story. A story no case covers goes under Not verified.
