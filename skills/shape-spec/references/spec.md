# Spec

Synthesize what the interview settled; do not interview again.

## Before writing

1. Read the code the spec touches, the repo glossary, and the ADRs of the area. Use the glossary's terms throughout.
2. Choose the seams the feature will be tested at: existing seams before new ones, the highest seam possible, as few as possible; one is ideal. For a feature with a user-facing surface, the journeys' surfaces are its seams; name only seams beyond them, such as a library's API. Check them with the user.

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
S1. As a <actor>, I want <feature>, so that <benefit>.
   Journey: on <surface>, <steps>, then <the result the user expects>.
(A long list that covers every part of the feature, edge cases included. Every story has its journey, confirmed with the user.)

## Promises
- **P1. <what must never break, in one product sentence>.** Harm: <what the user loses when it breaks>.
(Each one confirmed with the user. Write "none" when the grill found none.)

## Visual targets
Only for a heavy visual change; otherwise "none".
Design mode: <follow, extend, or break away>, because <reason>.
- **V1. <screen and state, such as the empty inbox>.** Still, at <the widths of the UI rules, or others>. Captures: <their files in the project folder's `targets/`, and a link when the tracker hosts them>. Serves: <S1>.
- **V2. <what moves, such as a card opening>.** Motion, at <a width>. Recording: <its file, as for captures>. Effects: <its effect list, one line each: the trigger, what moves, the duration, the easing, the direction>. Serves: <S1>.
Checks: <the measured checks of the UI rules this design takes, with any threshold the user set>.
Banned: <the generic defaults this design must not use, and the user's own bans>.
(Each target confirmed with the user, who picked it from the prototypes.)

## Not verifiable
What no run can prove, and why, agreed in the grill. Write "nothing" when everything can be.

## Seams
The public interfaces the tests will use beyond the journeys' surfaces, agreed with the user.

## Decisions
Modules built or changed, their interfaces, schema changes, API contracts, architecture choices, and the ADRs they rest on.
No file paths and no code: they go stale. Exception: a snippet from a prototype that pins a decision better than prose (a state machine, a type, a schema), trimmed to the decision.

## Testing decisions
What a good test is here (external behavior only), which modules get tests, and the existing tests to copy.

## Out of scope
What this spec will not do.
```

## From spec to proof

Each journey, promise, and visual target becomes a case in `frame` (see [coverage.md](../../constitution/references/coverage.md)), so the coverage table of the final PR answers the spec story by story and promise by promise. The template numbers them, `S1`, `S2` for stories, `P1`, `P2` for promises, and `V1`, `V2` for visual targets, so the evidence record names each one; a second journey of a story takes the next letter, `S1b`. A journey, a promise, or a visual target no case covers goes under Not verified.
