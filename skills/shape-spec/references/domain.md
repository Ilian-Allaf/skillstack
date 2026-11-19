# Domain model

The repo's own words for its domain, kept while you design, so the next agent reads one term per idea in the code, the spec, and the PRs.

## Files in the target repo

```text
GLOSSARY.md          the domain terms of the repo
docs/adr/0001-<slug>.md   one file per decision worth recording
```

A repo with several contexts has a `GLOSSARY-MAP.md` at the root pointing at a `GLOSSARY.md` and a `docs/adr/` per context. Create files only when you have something to write.

`GLOSSARY.md` holds terms and nothing else: no implementation details, no spec, no scratch notes. Each entry: the term, its meaning in one or two sentences, and the words to avoid for it.

## While you design

- **Challenge against the glossary.** When the user uses a term that conflicts with `GLOSSARY.md`, say so at once: "Your glossary defines cancellation as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy words.** For an overloaded word, propose one precise term: "By account, do you mean the Customer or the User?"
- **Test with scenarios.** Invent concrete edge cases that force the boundaries between concepts.
- **Check against the code.** When the user says how something works, read whether the code agrees, and surface a contradiction.
- **Write as you go.** When a term is settled, update `GLOSSARY.md` right then, on a docs branch of its own. `GLOSSARY.md` and the ADRs land through one docs PR, linked from the spec, which the user merges like any other.

## ADRs, sparingly

Offer an ADR only when all three hold:

1. **hard to reverse**: changing your mind later costs something real;
2. **surprising without context**: a future reader would ask why;
3. **a real trade-off**: there were real alternatives, and one was picked for a reason.

An ADR states the context, the decision, the alternatives rejected and why, and the consequences. Later work reads the ADRs of the area it touches and does not propose again what an ADR rejected.
