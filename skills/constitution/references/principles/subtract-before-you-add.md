# subtract-before-you-add

**Apply when** you sequence an addition, a refactoring, or a rewrite.

**Rule.** Remove complexity first, then build on the simpler base. Leave the design a little simpler, behind the same or a smaller surface, than you found it.

## How

- Delete first: dead code, one-caller wrappers, redundant validators, stub references, the obsolete paths the new work would have to work around.
- Cut before you polish: reach the minimum that works before you invest in its quality.
- Land the subtraction as its own commit, before the addition, so each reads alone.
- A reference with nothing new in it is deleted, not left as a stub.

## Test

Is there code the new work steps around, or keeps alive only for itself? Delete it first.

## Sign it was skipped

A new adapter beside three obsolete ones. A feature that adds a branch to skip a dead path.
