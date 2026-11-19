# 0011. A spec is not split into tickets for parallel agents

- **Status**: accepted, 2026-11-19
- **Applies to**: `skills/shape-spec/`, `skills/ship/references/playbooks/bespoke.md`
- **Enforced by**: review

## Context

A common flow cuts a spec into tickets and hands them to parallel agents. Ray Amjad and Anthropic both report worse results: each agent lacks the context the others build.

## Decision

`shape-spec` produces a spec, or a map of decisions when the work is too big for one session; it produces no tickets for agents. A large spec goes through the `bespoke` playbook: one builder, a series of ordered PRs.

## Alternatives rejected

- **A `to-tickets` skill**: not adopted from Matt Pocock's set.

## Consequences

Parallel work happens inside one task, as `skills/constitution/references/parallel.md` describes, not across tickets.
