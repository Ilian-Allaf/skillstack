# Principles

The principles this framework applies, each with when it applies. Skills name a principle by its id. When a principle changes a choice, its id goes with that choice in the PR's Decisions section or the decision log.

Each rule is a short summary, so every skill can read it.

## Evidence and verification

| Id | Apply when | Rule |
|---|---|---|
| `prove-it-works` | before you report done | Check the real artifact: run the feature, read the stored value, inspect the diff. A proxy, a self-report, or "it compiles" is not a check. |
| `tight-loop` | before you fix a bug or build a feature | First build a signal that goes red on this exact problem, then make it fast and deterministic. With no loop, stop and ask for access or an artifact instead of guessing. |
| `test-behavior-not-implementation` | when you write, change, or keep a test | Assert what users of the code can observe. The expected value comes from a source independent of the code: a known literal, a worked example, the spec. |
| `explain-the-number` | before you report or act on a measured number | Say what produced it, what controls it, and what would make it wrong. |
| `verify-at-the-edge` | when you size verification | Spend verification where the model is weakest: hard zones and high risk. Below that edge, a verifier confirms and costs. |

## Root causes and structure

| Id | Apply when | Rule |
|---|---|---|
| `fix-root-causes` | when debugging | Trace the symptom to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. |
| `attack-the-premise` | when two fixes that share a premise failed the same check | Write the premise down and test it directly before a third fix. |
| `encode-lessons-in-structure` | when the same correction comes back | Turn it into structure, in this order of preference: architecture, a type, a lint whose message names the fix, a test, and docs last. |
| `build-the-lever` | before repetitive or error-prone work | Build the script, codemod, or check that does it or proves it. |
| `model-the-domain` | before writing logic or stateful code | Name the data structure that encodes the domain first: a state machine, a typed model, a table. It must delete branches or invalid states, not add indirection. |
| `design-it-twice` | when a change adds or changes a type, a signature, or a module boundary | Sketch two structurally different shapes, screen both against the red flags in `ship/references/design.md`, then pick one. |
| `migrate-callers-then-delete` | when an API changes shape | Move every caller and delete the old API in the same PR. No shim; the next agent would copy the old path. One exception: a wide change that cannot land green in one PR uses expand, migrate, contract (the `bespoke` playbook), and the old form lives only until the contract PR. |
| `minimize-reader-load` | when shaping or reviewing code | Count the layers between a question and its answer, and the state a reader must hold. A change that lowers neither is reverted. |
| `type-system-discipline` | when designing types or signatures | Make illegal states unrepresentable. |
| `boundary-discipline` | when wiring validation or error handling | Guard at system boundaries: CLI, config, network, external APIs. Trust the inside. |

## Scope and change size

| Id | Apply when | Rule |
|---|---|---|
| `laziness-protocol` | when tempted to add a layer or an abstraction | Prefer deletion and the smallest change that meets `done_when`. |
| `subtract-before-you-add` | before an addition or a refactor | Remove dead code and redundant checks first, then build on the simpler base. |
| `sequence-verifiable-units` | for multi-step work and stacked PRs | Cut the work into small units that each end on a check. |
| `scope-stays-put` | when a review or an impact analysis finds something outside the task | Open an issue. The PR stays on its task. |

## Running agents

| Id | Apply when | Rule |
|---|---|---|
| `guard-the-context-window` | when output is large or reads repeat | Send bulk work to subagents or scripts and keep summaries in the main thread. |
| `make-operations-idempotent` | for every step that can be retried | Read the current state and apply only the difference, so a rerun converges. |
| `separate-before-serializing-shared-state` | when parallel runs could write the same file, branch, or key | Remove the sharing first. Serialize only what cannot be separated. |
| `never-block-on-the-human` | on reversible work | Make the reversible choice, note it under `Decisions`, and move on. Irreversible choices and merges stay with the user. |
| `keep-the-codebase-clean` | before you open a PR | The next agent copies what you leave. Remove slop, stale comments, and workarounds. |
