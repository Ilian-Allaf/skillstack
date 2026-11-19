# 0003. The author is never the judge

- **Status**: accepted, 2026-11-18
- **Applies to**: `skills/verify-pr/`, `skills/ship/SKILL.md`, rule 2 of `skills/constitution/README.md`
- **Enforced by**: the verdict comment records the verifier's model family and whether its context was fresh

## Context

A model checks what it meant to build, not what it built. Tuning a separate evaluator to be skeptical works far better than making a generator critical of its own work (Anthropic, *harness design*).

## Decision

The verifier is a fresh agent, with no write rights, from another model family when the harness offers one. It reads, runs, and comments. It sees the task, `done_when`, and the PR, not the builder's reasoning.

## Alternatives rejected

- **Self-review by the builder**: it grades the intent, not the result.
- **A verifier of the builder's family**: kept only as the fallback when no other family is available. Seeded defects measure how much weaker it is.

## Consequences

The verdict comment states the family and the freshness of the context (`skills/verify-pr/references/verdict.md`), so the user can see when a verdict is weaker.
