# Sketch

How to write one sketch. [design.md](design.md) says when to sketch and what to do with the two you write.

## What a sketch holds

1. **The usage, written first.** The quickstart a consumer of the code reads, and two or three call sites in the repo's own code: what they import, what they call, what comes back, how they handle a failure.
2. **The shape, derived from the usage.** Types, signatures, and module layout. Bodies stay `not implemented`; tricky logic is pseudocode; each public symbol has one doc comment stating its intent and its invariant. A reader traces data from input to output by reading types and signatures alone.

## Rules

Each rule names its principle. Before your sketch relies on a rule, read the full form of its principle, with its test and its example, as [principles.md](../../constitution/references/principles.md) says; read only those your sketch relies on.

1. **The usage is the spec** (`design-for-the-consumer`). When the shape and the usage disagree, change the shape.
2. **Data structures first** (`design-the-data-first`). Trace each main read and write through the structure. "We will add a map, an index, or a cache later" means the structure is wrong now.
3. **Encode the domain** (`model-the-domain`). Pick the structure that deletes branches and invalid states. Name it in the words of the repo glossary.
4. **Integrate, do not bolt on** (`redesign-from-first-principles`). When the change lands in an existing design, sketch what you would build if the requirement had always been there.
5. **A deep interface.** Prefer the smallest public surface that hides the most capability. Pull complexity into the callee. No transport, storage, or wire type on the public surface.
6. **Invariants in types** (`make-illegal-states-unrepresentable`). Types first, runtime checks second, comments last.
7. **Validate at the boundary, pure inside** (`validate-at-the-boundary`). Business logic in pure functions; the shell stays thin.
8. **One source of truth.** One owner per piece of state, one definition per rule. Derive, never sync.
9. **Shared state** (`separate-before-serializing-shared-state`). When two actors can write the same thing, ask what happens. If the answer is not "nothing", give each its own state and merge where it is read.
10. **Idempotent transitions** (`make-operations-idempotent`). Say what happens when an operation runs twice, or crashes halfway.
11. **Short paths** (`minimize-reader-load`). Following one flow takes three files at most.
12. **Nothing speculative** (`make-the-smallest-change`). No option, layer, or extension point that the usage does not need.
