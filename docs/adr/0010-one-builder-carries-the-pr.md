# 0010. One builder carries the PR from frame to ready

- **Status**: accepted, 2026-11-18; to settle on the testbed (issue #6)
- **Applies to**: `skills/ship/`, `skills/babysit-pr/`
- **Enforced by**: review

## Context

Two practices exist. A fresh agent for each review round sees the code without the builder's assumptions (Matt Pocock, pstack). The same builder keeps its context, and Ray Amjad measured it better and 38% cheaper over about ten PRs.

## Decision

The same builder carries a PR from `frame` to `ready`, review fixes included. Independence comes from the verifier (ADR 0003), not from changing builders.

## Alternatives rejected

- **A fresh builder per round**: kept as the comparison to run on the testbed's PRs.

## Consequences

If the testbed's PRs show the fresh builder doing better, a new ADR supersedes this one.
