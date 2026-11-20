# 0001. The user always merges

- **Status**: accepted, 2026-11-18
- **Applies to**: every skill; rule 1 of `skills/constitution/README.md`
- **Enforced by**: rule 1 of the constitution today; the merge guard of issue #9 once built

## Context

Version 2 of the design let the agent merge on its own once it had earned trust: a `.trust/` folder, a CI gate of the framework's own, and a ladder of trust levels N0 to N5. Every rung was one more thing to prove, and one more way to merge something nobody read.

## Decision

The agent never merges, in any form: no `gh pr merge`, no `--auto`, no merge queue. It stops at a PR labeled `ready`, which lacks nothing but the user's decision. The user reads the PR and merges.

## Alternatives rejected

- **A trust ladder** (N0 to N5) that grants merge rights per risk class: removed with `.trust/`.
- **A CI gate owned by the framework**: the repo's own CI and the user's reading of the PR are enough.
- **A separate GitHub account for the agent**: it only served approvals at level N3. The agent works under the user's name, and the guard stops it from merging.

## Consequences

- The framework's effort goes into verification instead: what the agent proves, and what the verifier tries to break.
- A rule that lives only in a sentence can be broken, so the guard of issue #9 is a hook in the harness, not a line in a skill.
