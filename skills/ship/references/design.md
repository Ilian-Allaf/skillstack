# Design before code

The codebase is the largest input of the next agent, and that agent copies the nearest example. A shape chosen at write time is cheap; recovering it later reads as a refactor and gets deferred. So the builder picks the shape before the code.

## 1. Name the data shape

Before any logic, name the structure that encodes the domain:

- a state machine instead of scattered booleans or phase checks;
- a typed model instead of loose parameters or repeated shape assumptions;
- a map, registry, lookup table, or discriminated union instead of branches spread across files;
- a reducer or command and event model instead of ad hoc mutations;
- a module grouped around one body of domain knowledge, not around execution order (load, validate, transform, save);
- a small module boundary that gathers repeated behavior, ownership, or invariants;
- a queue, cache, index, graph, tree, or normalized collection, when the way the data is read calls for it.

When none fits, write what the code must never allow and how the data is read, then pick the structure that encodes exactly that.

Keep boring code when the current shape is already clear, local, and unlikely to grow. A structure earns its place by deleting branches, duplicated rules, invalid states, or lifecycle risk, never by adding indirection.

Name the shape in the domain's words. Its types, states, and events take their names from the repo glossary, so the vocabulary settled with the user is the one the code carries. A domain concept the glossary lacks is added to it in the same PR, as `shape-spec`'s domain.md describes.

The sign this step was skipped: a new feature grows an existing if/else chain by one branch, adds a second boolean that must stay in sync with the first, or repeats the same domain rule in modules named after steps.

## 2. Sketch twice when the code crosses a boundary

Sketch when the change adds or changes a type, a signature, or a module boundary that other code calls. Skip it for a change local to one function body.

1. **Ground.** Read every module the new code touches and write a short explanation of how each works today. Naming a file is not grounding.
2. **Two sketches.** Run an arena of two or three runners, as [parallel.md](../../constitution/references/parallel.md) describes, from two model families when the harness offers them (see [harness.md](../../constitution/references/harness.md)). Give each the task, `done_when`, and your grounding, and ask for a sketch: the caller's usage first, then types, signatures, and module layout, with bodies left `not implemented`. Ask for structurally different shapes, not two variants of one.
3. **Screen.** Check each sketch against the red flags below. A red flag is a reason to revise or reject the shape.
4. **Pick.** Prefer the shape that hides more behind a smaller public surface, and where a change that looks right from one file is right for the whole repo. Write the choice and the rejected shape in one line each under Decisions in the PR.

The sketch is the contract for `build`. When the code needs something the sketch did not plan, ask whether the sketch, the requirement, or the code is wrong; do not absorb it silently. When the same kind of workaround keeps coming back, or types need casts and escape hatches to compile, throw the sketch out and sketch again, smaller.

## Red flags

Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles.

| Red flag | Sign | Fix |
|---|---|---|
| shallow module | callers coordinate several methods for one operation; options expose internal stages | a simple interface over substantial behavior |
| information leakage | one representation, policy, or wire type appears in several modules | parse external data into domain types behind the interface |
| temporal decomposition | modules named after steps repeat one representation and its rules | group code by the knowledge it owns |
| pass-through method | a method forwards the same arguments to another of the same shape | remove it, or give it real policy |
| split ownership | several modules write the same state or keep copies | one owner per piece of state; others read or ask |
| two ways to do one task | the design offers two paths to the same result | keep one; move callers and delete the other in this change |
| importable internals | a caller can import a module's internals | make them unreachable, so an outside import fails the build |
| hand-synced list | adding an item means editing several lists | keep one list and derive the rest, or fail the build when they differ |
