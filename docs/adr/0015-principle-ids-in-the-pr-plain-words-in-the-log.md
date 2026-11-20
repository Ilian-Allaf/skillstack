# 0015. Principle ids in the PR, plain words in the decision log

- **Status**: accepted, 2026-11-20. Supersedes [0012](0012-principles-go-in-the-record.md).
- **Applies to**: `skills/constitution/README.md` ("Reading a principle", "Principles in the record"), `skills/constitution/references/decision-log.md`
- **Enforced by**: review

## Context

ADR 0012 put a principle's id next to the choice it changed, in the PR's Decisions section and in the decision log. The decision log's own format, taken from pstack's `show-me-your-work`, says the opposite: "If a principle drove it, say it plainly, not as a jargon tag." An audit of the skills on 2026-11-20 found the contradiction, and the user chose pstack's rule for the log.

## Decision

- The reply does not list principles (this part of ADR 0012 stands).
- In the PR's Decisions section, a principle that changed a choice is named by its id, next to that choice. An id cited there is one whose full form the builder read in the session.
- In a decision log, the principle is said in plain words, as the reason for the row: the log is read by a person catching up after a long run, who should not need the index.

## Alternatives rejected

- **Ids in both places** (ADR 0012): the log reads as jargon to the person it is written for.
- **Plain words in both places**: `learn-from-mistakes` and the verifier find the principles a PR relied on by their ids under Decisions.

## Consequences

`learn-from-mistakes` reads principle ids from the PR's Decisions section only, not from decision logs.
