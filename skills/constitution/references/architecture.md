# Architecture principles

The full form of the principles that shape code. Each one says when it applies, its rule, how to apply it, the test that shows you did, and the sign that someone skipped it. [principles.md](principles.md) keeps the one-line index. The builder reads this file before it picks a shape; the verifier reads it before it judges one.

Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Every principle here serves one aim: a change that looks right from one file is right for the whole repo.

## foundational-thinking

**Apply when** a change adds logic, a type, or a module, and when you order the work.

**Rule.** Data structures first, scaffold first. Structural decisions keep options open; code-level decisions keep the code simple.

**How.**

- Define the core types before the logic. List every way the data is read and written: by id, by range, in order, by owner, all at once. Trace each one through the structure. A main path the structure serves badly means the structure is wrong now; "we will add an index later" is that sign.
- Do first what every later step benefits from: the shared types, the test harness, the check that will prove the work. Removing dead code comes before that (`subtract-before-you-add`).
- Factor the structure, not every line. Types and data models converge on one definition. Three similar statements still beat an early abstraction.
- Each increment lands one coherent abstraction, or deepens one that exists. It does not spread a new capability across callers as special-case coordination.

**Test.** For each access path, you can point to the field, the index, or the collection that serves it.

**Sign it was skipped.** A new capability travels as a flag through several callers. A lookup scans a list that should be a map. A later step recomputes what an earlier type could have held.

## model-the-domain

**Apply when** you write stateful logic, or code that branches a lot or repeats a shape assumption across files.

**Rule.** Encode the domain in a structure instead of scattered conditionals. A structure that matches the domain makes invalid states unrepresentable and deletes branches.

**How.** Reach for:

- a state machine instead of scattered booleans or phase checks;
- a typed model instead of loose parameters or repeated shape assumptions;
- a map, registry, lookup table, or tagged union instead of branches spread across files;
- a reducer or a command and event model instead of ad hoc mutations;
- a module grouped around one body of domain knowledge, not around execution order (load, validate, transform, save): execution order is not ownership;
- a small module boundary that gathers repeated behavior, ownership, or invariants;
- a queue, cache, index, graph, tree, or normalized collection, when the way the data is read calls for it.

When none fits, write what the code must never allow and how the data is read, then pick the structure that encodes exactly that.

Keep boring code when the current shape is already clear, local, and unlikely to grow.

**Test.** Name what the structure deletes: branches, duplicated rules, invalid states, or lifecycle risk. If it deletes nothing and only adds indirection, keep the boring code.

**Sign it was skipped.** A new feature grows an existing if/else chain by one branch, adds a second boolean that must stay in sync with the first, or repeats the same domain rule in modules named after steps.

## redesign-from-first-principles

**Apply when** a new requirement lands in an existing design, and when a sketch is scrapped.

**Rule.** Build as if the requirement had been an assumption from day one, instead of bolting it on.

**How.**

1. Read every affected file, and write how the current design works.
2. Answer in writing: "If we wrote this from scratch with this requirement, what would we build?"
3. Set that answer beside the bolt-on. Take the redesign when the bolt-on adds a branch, a flag, or a special case that the redesign does not need.
4. Carry the change through every reference: types, tests, docs, examples, config.
5. Think the whole redesign first, then ship it in units that each land green (`sequence-verifiable-units`).

**Test.** A reader who never saw the old design could not tell that this requirement came late.

**Sign it was skipped.** The new requirement lives in an `if` at each place it touches. A parameter is threaded through layers that never read it.

## boundary-discipline

**Apply when** you wire validation, error handling, parsing, or a framework adapter.

**Rule.** Validate at system boundaries, trust the inside, and keep business logic in pure functions.

**How.**

- Boundaries are where data enters or leaves the system: CLI arguments, config files, environment variables, network and RPC payloads, files, database rows, IPC, external APIs. There, validate, parse into a domain type, and return errors.
- Inside, the data is typed and errors propagate. Nothing is validated twice, and no null check repeats what the boundary already ruled out.
- Business logic is pure functions with no framework dependency. Parsing turns raw input into typed state; scoring turns state into a result; rendering turns structured state into a string. The shell around them is thin and mechanical, so the logic is tested without the framework.
- Across a module boundary, expose domain concepts, never the transport, storage, framework, or wire types behind them. General mechanism goes inside; special-purpose policy stays at the edge.

**Test.** For each check: is this data crossing a boundary right now? If not, the check is redundant. For each function that holds logic: could the shell call it as a pure function? If yes, extract it.

**Sign it was skipped.** The same null check at three depths. A function that mixes a network call with a business rule. A database row type in a public signature.

## type-system-discipline

**Apply when** you design a type or a signature, in any typed language. The rules of each language are in `languages/`, such as [typescript.md](languages/typescript.md).

**Rule.** Make the compiler reject impossible states, mixed-up primitives, and unhandled variants. Define errors and special cases out of existence instead of adding handlers.

**How.**

- Model variants as a tagged union with one tag field, not a bag of optional fields.
- Brand semantic primitives. A `UserId` and an `OrderId` are both strings, but not interchangeable: give each its own type, a branded type or a newtype, made once by a function that checks it.
- External data is untyped until a parse function at the boundary turns it into the model (`boundary-discipline`).
- Derive types from the schema that owns the shape: protocol buffers, OpenAPI, GraphQL, a migration, a design-token file. Never hand-write a parallel type.
- Make every switch over a variant exhaustive, so a new variant fails the build.
- Build the shape so the illegal value cannot be built: a non-empty list type, a start and a duration instead of two dates that must stay ordered.

**Test.** List the states the code must never reach. For each, say what rules it out: a type, then a runtime check, then a comment, in that order of preference (`encode-lessons-in-structure`). A state ruled out only by a comment is a finding.

**Sign it was skipped.** Optional fields that are always set in practice. Casts. Two parameters of the same primitive type that a caller can swap. A "should never happen" throw.

## minimize-reader-load

**Apply when** you shape code, add a layer or a piece of state, or review a diff.

**Rule.** The cost of code is the work a reader does to understand it, on two axes: the layers between a question and its answer, and the state the reader must hold in their head. Lines of code and complexity scores are proxies.

**How.**

- Collapse a layer that costs more than it saves: a wrapper with one caller, an adapter with one implementation, an indirection added for a need that never came.
- Each layer changes the abstraction. A layer that repeats the methods and arguments of the next one is a pass-through: remove it.
- Prefer a small interface that hides real decisions over a wide one the reader must learn on top of the implementation.
- Shrink the scope of state: a return value over a mutation, a local over a field, a field over module state, module state over a global. Derive a value instead of keeping two copies in sync.
- Name an invariant once, at the boundary that holds it, not in every consumer.
- Following one flow takes three files at most. If it takes more, flatten.
- Before you add a layer or a piece of state, check that it removes at least as much reader load elsewhere.

**Test.** A new reader answers "where does X come from?" and "what can change X?" in under 30 seconds.

**Sign it was skipped.** A chain of functions that pass the same arguments down. A flag set in one module and read in another. A cache kept in sync by hand.

## make-operations-idempotent

**Apply when** you design a command, a lifecycle step, a migration, or a loop that runs amid crashes and retries.

**Rule.** An operation converges to the same end state however many times it runs and wherever the last run stopped.

**How.**

- Derive each step from the state that exists, not from what the last run meant to do: read the current state, compare it with the goal, and apply only the difference. A repeat then finds nothing left to do.
- Anything a run leaves behind, such as a lock, a temporary file, a half-written record, or a claimed job, must be recognizable as stale by the next run, from evidence that holds wherever the last run stopped. Write to a temporary path and rename it into place. Compare artifacts by content, not by creation order.

**Test.** What happens if it runs twice in a row? What happens if the last run crashed at each possible point? If an answer is "it depends on what was left behind", the operation needs a reconciliation step.

**Sign it was skipped.** A rerun fails on "already exists". A crash needs a manual cleanup before the next run.

## separate-before-serializing-shared-state

**Apply when** concurrent actors could write the same file, row, key, branch, or object: threads, processes, requests, jobs, agents.

**Rule.** Remove the sharing first. Serialize only what cannot be separated, and then by structure, never by convention.

**How.**

1. List the shared mutable state: what two actors both write, or one writes while another reads.
2. Ask whether they need one canonical object or are publishing independent facts. Give each actor its own file, key, row, or branch, and merge where the data is read. Two workers writing their own field into one shared file still share it; one file per worker does not.
3. Only when one shared target is a real invariant, serialize access by structure: a single writer, sequential phases, a lock, or an atomic compare-and-swap. "We need a lock" is a smell to check first, not the default answer.

**Test.** For each piece of shared state: what happens if another actor changes it right now? The answer is "nothing", or a named structure prevents it.

**Sign it was skipped.** A lock added after a flaky test. A rule in a comment ("call this only from the main thread") instead of a structure that enforces it.
