# model-the-domain

**Apply when** you write stateful logic, or code that branches a lot or repeats a shape assumption across files.

**Rule.** Encode the domain in a structure instead of scattered conditionals. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Choosing it at write time is cheap; recovering it later reads as a refactor and gets deferred.

## How

Reach for:

- a state machine instead of scattered booleans or phase checks;
- a typed model instead of loose parameters or repeated shape assumptions;
- a map, registry, lookup table, or tagged union instead of branches spread across files;
- a reducer or a command and event model instead of ad hoc mutations;
- a module grouped around one body of domain knowledge, not around execution order (load, validate, transform, save): execution order is not ownership;
- a small module boundary that gathers repeated behavior, ownership, or invariants;
- a queue, cache, index, graph, tree, or normalized collection, when the way the data is read calls for it.

When none fits, write what the code must never allow and how the data is read, then pick the structure that encodes exactly that. Name it in the words of the repo glossary.

Keep boring code when the current shape is already clear, local, and unlikely to grow.

## Test

Name what the structure deletes: branches, duplicated rules, invalid states, or lifecycle risk. If it deletes nothing and only adds indirection, keep the boring code.

## Sign it was skipped

A new feature grows an existing if/else chain by one branch, adds a second boolean that must stay in sync with the first, or repeats the same domain rule in modules named after steps.

## Example

```ts
// Skipped: three booleans allow eight states; the domain has four.
type Upload = { started: boolean; done: boolean; failed: boolean; error?: string };
if (u.started && !u.done && !u.failed) showSpinner();

// Applied: a state machine; each state carries only its own data.
type Upload =
  | { state: "idle" }
  | { state: "sending"; progress: number }
  | { state: "done"; url: string }
  | { state: "failed"; error: string };
```

A rule that varies by kind becomes a table, not a branch in every caller:

```ts
// Skipped: the limit is decided in each module that needs it.
const limit = plan === "free" ? 3 : plan === "team" ? 20 : 100;

// Applied: one table owns the rule; a new plan is one row.
const LIMITS: Record<Plan, { seats: number }> = { free: { seats: 3 }, team: { seats: 20 }, enterprise: { seats: 100 } };
```
