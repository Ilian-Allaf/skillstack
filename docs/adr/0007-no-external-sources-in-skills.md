# 0007. No external sources in the skills

- **Status**: accepted, 2026-11-19
- **Applies to**: `skills/`
- **Enforced by**: `tools/lint_skills.py` (P005)

## Context

Most skills adapt ideas from other skill sets. A line that names the original skill invites the agent to go find it and follow it, out of the framework.

## Decision

Skills name no external person, repo, or skill. Every attribution lives in [`docs/sources.md`](../sources.md), one section per file. Design docs and ADRs name their sources.

## Consequences

When a skill changes, its section in `docs/sources.md` changes in the same PR.
