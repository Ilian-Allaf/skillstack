# 0004. A finding blocks only when proven

- **Status**: accepted, 2026-11-18; extended to documented standards on 2026-11-19
- **Applies to**: `skills/verify-pr/references/verdict.md`, rules 3 and 4 of `skills/constitution/README.md`
- **Enforced by**: the verdict format: each FAIL carries its `run`, with observed and expected output

## Context

An untuned verifier finds problems and approves anyway, or blocks on a plausible worry nobody ran. A claim without a run reads the same whether it is true or not.

## Decision

- Only what ran counts. Every claim carries its certainty level, from 1 (said) to 5 (observed on the real app).
- A finding is a FAIL only when it is proven on the head of the PR, in the task's scope, and graded blocker or should. A breach of a documented repo standard is proven by quoting the file, the rule, and the hunk.
- `verdict.md` is the one place that defines a FAIL. Every other file points there.
- A verdict covers one patch id: a pure rebase keeps it, new code needs a new one.
- Everything else is a note. Notes stay in the verdict comment; one becomes an issue only when the user asks.

## Alternatives rejected

- **Blocking on likely problems**: every PR stalls on worries, and the user stops reading verdicts.
- **Filing every note as an issue**: the tracker fills with what nobody decided to do.

## Consequences

The verifier reproduces each FAIL itself before it posts. What the builder could not prove stays visible in the PR: under Not verified, or as a safety fact marked `unproven`.
