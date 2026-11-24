# Principles

The index of the principles this framework applies. Skills name a principle by its id. When a principle changes a choice, its id goes with that choice in the PR's Decisions section; in a decision log, the principle is said in plain words.

Each row gives when the principle applies and its rule in one line. Its full form is `principles/<id>.md`: how to apply it, the test that shows you did, the sign that someone skipped it, and an example when it shapes code. Read the full form of a principle before you apply it or judge someone else's work by it. Examples are in TypeScript; their shape carries to any language.

## Design and structure

| Id | Apply when | Rule |
|---|---|---|
| `design-the-data-first` | a change adds logic, a type, or a module, and when you order the work | Define the core types and trace every read and write through them before any logic; build first what every later step needs. [Full form](principles/design-the-data-first.md). |
| `model-the-domain` | you write stateful logic, or code that branches a lot or repeats a shape assumption | Encode the domain in a structure, such as a state machine, a typed model, or a table, that deletes branches and invalid states. [Full form](principles/model-the-domain.md). |
| `design-for-the-consumer` | you design an interface someone else uses | Write the consumer's usage first, and choose their experience over the implementation's convenience. [Full form](principles/design-for-the-consumer.md). |
| `design-it-twice` | a change adds a feature, or adds or changes a type, a signature, or a module boundary | Sketch two structurally different shapes, screen both, then pick one. [Full form](principles/design-it-twice.md). |
| `redesign-from-first-principles` | a new requirement lands in an existing design, and when a sketch is scrapped | Build as if the requirement had been there from day one, instead of bolting it on. [Full form](principles/redesign-from-first-principles.md). |
| `make-illegal-states-unrepresentable` | you design a type or a signature | Tagged unions, branded primitives, types derived from the owning schema, exhaustive switches: the compiler rejects what must never happen. [Full form](principles/make-illegal-states-unrepresentable.md). |
| `validate-at-the-boundary` | you wire validation, error handling, parsing, or a framework adapter | Validate where data enters, trust it inside, and keep business logic in pure functions. [Full form](principles/validate-at-the-boundary.md). |
| `minimize-reader-load` | you shape code, add a layer or state, or review a diff | Fewer layers between a question and its answer, less state to hold; a change that lowers neither is reverted. [Full form](principles/minimize-reader-load.md). |
| `migrate-callers-then-delete` | an internal API changes shape | Move every caller and delete the old API in the same PR; no shim. A wide change uses expand, migrate, contract. [Full form](principles/migrate-callers-then-delete.md). |
| `make-operations-idempotent` | an operation or a skill step can be retried or crash halfway | Read the current state and apply only the difference, so a rerun converges. [Full form](principles/make-operations-idempotent.md). |
| `separate-before-serializing-shared-state` | concurrent actors or parallel runs could write the same thing | Remove the sharing first; serialize only what cannot be separated, by structure. [Full form](principles/separate-before-serializing-shared-state.md). |

## Scope and change size

| Id | Apply when | Rule |
|---|---|---|
| `make-the-smallest-change` | you size a diff, or are tempted to add a layer, an option, or an abstraction | Prefer deletion and the smallest change that meets `done_when`. [Full form](principles/make-the-smallest-change.md). |
| `subtract-before-you-add` | you sequence an addition, a refactoring, or a rewrite | Remove dead code and redundant checks first, then build on the simpler base. [Full form](principles/subtract-before-you-add.md). |
| `sequence-verifiable-units` | the work has several steps, commits, or PRs | Cut it into small units that each end on a check, in an order that proves itself. [Full form](principles/sequence-verifiable-units.md). |
| `scope-stays-put` | something outside the task turns up | Open an issue for it; the PR stays on its task. [Full form](principles/scope-stays-put.md). |
| `keep-the-codebase-clean` | before you open a PR | The next agent copies what you leave: remove slop, stale comments, and workarounds. [Full form](principles/keep-the-codebase-clean.md). |

## Debugging

| Id | Apply when | Rule |
|---|---|---|
| `build-a-tight-loop` | you start a bug fix or a feature | First build one fast, deterministic command that goes red on this exact problem. [Full form](principles/build-a-tight-loop.md). |
| `fix-root-causes` | you debug | Fix the first place the system went wrong, not where the symptom surfaced; a guard is a fix only when the state it handles is legitimate. [Full form](principles/fix-root-causes.md). |
| `attack-the-premise` | two fixes that share a premise failed the same check | Write the premise down and test it before a third fix. [Full form](principles/attack-the-premise.md). |

## Evidence and verification

| Id | Apply when | Rule |
|---|---|---|
| `prove-it-works` | before you report done, or trust an output | Check the real artifact, not a proxy, a self-report, or "it compiles". [Full form](principles/prove-it-works.md). |
| `test-behavior-not-implementation` | you write, change, or keep a test | Assert what users of the code observe, so the test fails when behavior breaks and survives a refactoring. [Full form](principles/test-behavior-not-implementation.md). |
| `explain-the-number` | before you report or act on a measured number | Say what produced it, what limits it, and what would make it wrong. [Full form](principles/explain-the-number.md). |
| `verify-at-the-edge` | you size verification | Spend it where the model is weakest: hard zones and high risk. [Full form](principles/verify-at-the-edge.md). |

## Tools and lessons

| Id | Apply when | Rule |
|---|---|---|
| `build-the-lever` | the work is not trivial | Build the script, codemod, or check that does the work or proves it. [Full form](principles/build-the-lever.md). |
| `encode-lessons-in-structure` | the same correction comes back, or you are about to write a decision or a rule in a doc | Turn it into architecture, a type, a check that names the fix, or a test, and docs last. An ADR keeps only what the code cannot say. [Full form](principles/encode-lessons-in-structure.md). |

## Running agents

| Id | Apply when | Rule |
|---|---|---|
| `guard-the-context-window` | output is large or reads repeat | Send bulk work to subagents or scripts; keep summaries in the main thread. [Full form](principles/guard-the-context-window.md). |
| `never-block-on-the-human` | you are about to ask "should I?" on reversible work | Decide, note it under `Decisions`, and move on; a run settles facts, the user settles product calls and irreversible steps. [Full form](principles/never-block-on-the-human.md). |
