# Questions on the shape

The grill of `shape-spec`, as its [grill.md](../../shape-spec/references/grill.md) describes it, applied to the shape of the code. Its rounds, its frontier, and "facts are yours, decisions are the user's" hold as they are. What changes is below.

## Think in code, ask in decisions

The sketches are code; the questions are not. From the two sketches, take the decisions that carry the shape, the ones a design note's Shape names: who owns each piece of state, where the boundary sits, which structure encodes the domain, what the public surface hides, and what crosses a one-way door. Word each one in the repo glossary's terms, never in file paths.

```text
Q1. <the decision>
  A. <the shape>. <what it exposes, what it hides, the red flag or the promise it touches>
  B. <the shape>. <the same>
  Recommended: <A or B>, because <the reason, with the principle id>. <what would make the other one right>.
  Or: leave it to the builder.
```

When the user asks to see the shape, show the sketch behind the question.

## Ask only what carries the shape

- **Ask**: the choice between whole shapes, each one-way door, and each trade-off between them. When a shape has a consequence for the product the spec does not settle, such as working offline, ask it as a product question and record the answer under the spec's Decisions.
- **Do not ask**: an inner detail a later change undoes cheaply. It goes to Left to the builder, unasked (`never-block-on-the-human`).

## Every question can be left open

"Leave it to the builder" is an option of every question, written in each one as the format above shows. A decision the user makes, a yes to your recommendation included, becomes a technical decision that binds `ship`. One left open goes to Left to the builder, and `ship` designs it as if this skill had not run.

## The order of the rounds

Data first (`design-the-data-first`). The first round settles the whole shape: where the data lives and who owns it. The next rounds take the boundaries and the interfaces that hang off that answer, then the rest of what carries the shape. Each answer moves the frontier, as in the grill.

## Done

The frontier is empty: each decision made or left open. Ask the user to confirm the whole before you write it.
