# Domain model

The repo's own words for its domain, kept while you design, so the next agent reads one term per idea in the code, the spec, and the PRs.

## Files in the project folder

```text
~/.agents/projects/<project>/glossary.md          the domain terms of the repo
~/.agents/projects/<project>/adr/0001-<slug>.md   one file per decision worth recording
```

When the team keeps its glossary or its ADRs in the repo, these entries are routes to them, as [target-repo.md](../../constitution/references/target-repo.md) describes: read and edit the team's files. A repo with several contexts keeps a map of its glossaries, each with its own ADRs; `glossary.md` is that map, or routes to it. Create files only when you have something to write.

The glossary holds terms and nothing else: no implementation details, no spec, no scratch notes. Each entry: the term, its meaning in one or two sentences, and the words to avoid for it.

## While you design

- **Challenge against the glossary.** When the user uses a term that conflicts with the repo glossary, say so at once: "Your glossary defines cancellation as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy words.** For an overloaded word, propose one precise term: "By account, do you mean the Customer or the User?"
- **Test with scenarios.** Invent concrete edge cases that force the boundaries between concepts.
- **Check against the code.** When the user says how something works, read whether the code agrees, and surface a contradiction.
- **Write as you go.** When a term is settled, update the repo glossary right then. In the project folder, write it in place. In a file the team shares, write it on a docs branch of its own: the glossary and the ADRs land through one docs PR, linked from the spec, which the user merges like any other.

## ADRs, sparingly

Offer an ADR only when all three hold:

1. **hard to reverse**: changing your mind later costs something real;
2. **surprising without context**: a future reader would ask why;
3. **a real trade-off**: there were real alternatives, and one was picked for a reason.

An ADR is a dated record of a decision, not a description of the present. It holds:

- **Status**: `proposed`, `accepted`, `deprecated`, or `superseded by ADR-NNNN`;
- **Applies to**: the paths whose code the decision governs, such as `src/sync/`;
- the context, the decision, the alternatives rejected and why, and the consequences;
- **Enforced by**: the check that holds the decision, when one can.

Keep it true in three ways:

- **Never rewrite an accepted decision.** A new decision is a new ADR that supersedes the old one; the old one gets the status `superseded by ADR-NNNN` and stays as history, binding nothing.
- **A decision a check can hold gets the check.** Propose it through `add-guardrail` when you write the ADR: the check fails when the code drifts, and the ADR keeps only the why.
- **Read before you touch.** Work that touches a path an accepted ADR applies to reads that ADR first. To propose again what an ADR rejected, cite it and say what changed since; the user decides, and a yes becomes a superseding ADR.
