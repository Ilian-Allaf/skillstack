# Technical decisions

The section of the spec issue that this skill writes, and that `ship` and `verify-pr` read. It replaces the section `shape-spec` left.

```markdown
## Technical decisions
Grounded on: <full SHA of the base>, <date>, for <the modules the decisions touch, by name>. Sketches: `sketches/<spec>/` in the project folder of the machine that ran it.
- **D1. <the decision, in one sentence in the repo glossary's terms>.** Why: <the reason, with the principle id when one decided it>. Rejected: <the other shape, and why it lost>. ADR: <link, when one records it>.
- **D2. ...**
Left to the builder: <each decision left open, one line each>, and everything else.
```

## Rules

- **No file paths and no code**, as in the rest of the spec: they go stale. The exception is the spec's: a type, a state machine, or a schema from a sketch that pins a decision better than prose, trimmed to the decision. The paths live in the saved sketches.
- **Each decision can be checked against a diff**: a reader of the PR can say whether it holds. "Keep it simple" is not one.
- **Only the user's decisions are numbered.** What the user left open goes under Left to the builder.
- **A decision the spec already held**, stated by the user in the grill, keeps its id. A decision that replaces another, in a rerun or on the user's answer to a stop of `ship`, takes a new id, names the one it replaces, which leaves the list, and quotes the user's answer or links where it lives.
- **When the user left everything to the builder**, the section keeps the default line of the spec, and the sketches stay in the project folder for the record.
- **An ADR, sparingly**, by the three tests of `shape-spec`'s [domain.md](../../shape-spec/references/domain.md#adrs-sparingly). The decision links it; the ADR keeps the why and the alternatives rejected.
