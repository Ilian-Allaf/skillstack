# 0012. Principles go in the record, not in the reply

- **Status**: superseded by [0015](0015-principle-ids-in-the-pr-plain-words-in-the-log.md), 2026-11-20; accepted 2026-11-19
- **Applies to**: `skills/constitution/README.md` ("Principles in the record"), `skills/constitution/references/principles.md`
- **Enforced by**: review

## Context

Listing the principles applied at the end of every reply adds words the user skips, and turns the principle ids into decoration.

## Decision

A principle id appears only next to the choice it changed: in the Decisions section of the PR, or in the decision log.

## Consequences

`learn-from-mistakes` finds which principles mattered by reading Decisions, not replies.
