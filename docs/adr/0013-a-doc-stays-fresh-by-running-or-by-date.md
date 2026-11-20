# 0013. A doc stays fresh by running or by its date

- **Status**: accepted, 2026-11-19
- **Applies to**: every doc of this repo, and the feature maps and ADRs the framework writes in target repos
- **Enforced by**: `tools/check_refs.py` (R006: the skills map lists every skill); the entry-point check that `create-app-driver` writes beside each feature map

## Context

A description of the present goes stale the day the code moves, and an agent trusts it anyway. This repo's 7,500-word design document described skills that had since changed, and repeated what the skills say.

## Decision

A doc is kept only if it is one of two things:

- **executed**: a check fails when it disagrees with the code, as with the skills map in `skills/README.md` and the "Declared in" column of a feature map;
- **dated and immutable**: an ADR, superseded but never rewritten, or a frozen note in `docs/history/`.

How the framework works lives in the skills and in `skills/README.md`. Decisions live in `docs/adr/`. The roadmap lives in the issue tracker.

## Alternatives rejected

- **A living design document**: nothing tells when it goes wrong.

## Consequences

Design documents 01, 02, and 03 are frozen in `docs/history/`, in French, and bind nothing.
