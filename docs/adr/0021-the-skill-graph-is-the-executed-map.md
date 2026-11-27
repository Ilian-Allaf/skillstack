# 0021. The skill graph is the executed map

- **Status**: accepted, 2026-11-27. Supersedes [0013](0013-a-doc-stays-fresh-by-running-or-by-date.md).
- **Applies to**: every doc of this repo, and the feature maps and ADRs the framework writes in target repos; `skills/GRAPH.md`
- **Enforced by**: `tools/check_refs.py` (R006: every skill has its row in the table of `skills/GRAPH.md`; R012: each row's Runs and Run by match the skills' `calls:` frontmatter); the entry-point check that `create-app-driver` writes beside each feature map

## Context

ADR 0013 keeps a doc only if a check fails when it disagrees with the code, or if it is dated and never rewritten. Its executed map of the skills was `skills/README.md`, checked only for naming every skill: the edges, the flow of a task, and most of its prose were trusted, not checked. `skills/GRAPH.md` then showed the same graph and the same flow, more readably, so the repo held two descriptions of the present to keep in line by hand.

## Decision

A doc is kept only if it is one of two things, as in 0013:

- **executed**: a check fails when it disagrees with the code, as with the skill table of `skills/GRAPH.md` and the "Declared in" column of a feature map;
- **dated and immutable**: an ADR, superseded but never rewritten, a changelog entry, or a frozen note in `docs/history/`.

`skills/GRAPH.md` replaces `skills/README.md`, which is removed. Its table names every skill with the skills it runs and the skills that run it, and `tools/check_refs.py` checks both columns against the frontmatter. Its diagrams and its walk through `ship` follow the skills by hand: they repeat what the table and the skills already say, so a drift shows against a checked source.

How the framework works lives in the skills and in `skills/GRAPH.md`. Decisions live in `docs/adr/`. The roadmap lives in the issue tracker.

## Alternatives rejected

- **Keep both pages**: two descriptions of the same flow, with nothing to tell which one went stale.
- **Check every diagram edge**: the diagrams name nodes by short ids and cut the graph by question, so a parser would be harder to trust than the table it duplicates.

## Consequences

A dated doc may still name `skills/README.md`: `tools/check_refs.py` lists it under `REMOVED` and allows it only in the changelog, `docs/sources.md`, and the ADRs. Design documents 01, 02, and 03 stay frozen in `docs/history/`, in French, and bind nothing.
