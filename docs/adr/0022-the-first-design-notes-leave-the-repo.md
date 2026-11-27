# 0022. The first design notes leave the repo

- **Status**: accepted, 2026-11-27. Amends [0021](0021-the-skill-graph-is-the-executed-map.md), whose last consequence kept them.
- **Applies to**: `docs/`, `AGENTS.md`, `README.md`
- **Enforced by**: `tools/check_refs.py` (R001 fails on a link to a file that does not exist)

## Context

`docs/history/` held the first design notes, in French, frozen since the repo was standardized. ADR 0021 kept them as one kind of dated doc. They bind nothing: what they decided that still holds is in the ADRs and the skills, and the rest describes skills that have since changed. In the repo, they cost a language exception, a rule for agents not to update them, and a folder a reader must learn to skip.

## Decision

`docs/history/` is removed. The git history keeps the notes for anyone who needs them. The dated docs are now the ADRs and the changelog; ADR 0021's decision is otherwise unchanged.

## Alternatives rejected

- **Keep them, frozen**: a cost on every reader, for notes no decision relies on.

## Consequences

Every file of this repo is in English, except `resources/`. An attribution in `docs/sources.md` that linked a note now names it without a link.
