# Sketch brief

The brief of each runner in the design arena. The builder gives it with the task, `done_when`, the case list, the grounding notes, and the runner's own output path. The builder passes the path of this file; it does not paraphrase it.

You produce one candidate design. You are one of several runners, each on its own model. Make the best design your model can, not a safe middle: the differences between candidates are what the builder picks and grafts from.

## What you hand back

1. **The usage, written first.** The quickstart a consumer of the code reads, and two or three call sites in the repo's own code: what they import, what they call, what comes back, how they handle a failure.
2. **The sketch, derived from the usage.** Types, signatures, and module layout. Bodies stay `not implemented`; tricky logic is pseudocode; each public symbol has one doc comment stating its intent and its invariant. A reader traces data from input to output by reading types and signatures alone.
3. **The design note**, shaped as [design-note.md](design-note.md) describes, without its Synthesis section, which the builder writes.

## How to design

Each rule names the principle behind it; the full form, with its test, is in [architecture.md](../../constitution/references/architecture.md).

1. **The usage is the spec.** When the sketch and the usage disagree, change the sketch.
2. **Data structures first** (`foundational-thinking`). Trace each main read and write through the structure. "We will add a map, an index, or a cache later" means the structure is wrong now.
3. **Encode the domain** (`model-the-domain`). Pick the structure that deletes branches and invalid states. Name it in the words of the repo glossary.
4. **Integrate, do not bolt on** (`redesign-from-first-principles`). When the change lands in an existing design, sketch what you would build if the requirement had always been there.
5. **A deep interface.** Prefer the smallest public surface that hides the most capability. Pull complexity into the callee, even when its implementation gets harder. No transport, storage, or wire type on the public surface.
6. **Invariants in types** (`type-system-discipline`). Types first, runtime checks second, comments last.
7. **Validate at the boundaries, pure inside** (`boundary-discipline`). Business logic in pure functions; the shell stays thin.
8. **One source of truth.** One owner per piece of state, one definition per rule. Derive, never sync.
9. **Shared state** (`separate-before-serializing-shared-state`). When two actors can write the same thing, ask what happens. If the answer is not "nothing", give each its own state and merge where it is read.
10. **Idempotent transitions** (`make-operations-idempotent`). Say what happens when an operation runs twice, or crashes halfway.
11. **Short paths** (`minimize-reader-load`). Following one flow takes three files at most.
12. **Screen your own sketch** against the [red flags](design.md#red-flags) before you hand it back, and fix each one you find.

Name at least one whole other shape you rejected, and why.
