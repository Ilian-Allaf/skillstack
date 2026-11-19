# Design before code

The codebase is the largest input of the next agent, and that agent copies the nearest example. A shape chosen at write time is cheap; recovering it later reads as a refactor and gets deferred. So the builder picks the shape before the code, with the [architecture principles](../../constitution/references/architecture.md) as its method.

## How much design the change needs

| The change | Steps |
|---|---|
| local to one function body | 1 |
| adds or changes a type, a signature, or a module boundary that other code calls | 1 to 7 |
| the same, through a one-way door: a public API, a schema, a storage or wire format | 1 to 7, with three runners in step 3, and the door on the PR's Risk line |

An open question that a run can settle, such as a timing, a layout, or whether an approach works at all, is settled before step 3, in the prototype mode of [investigate](../../investigate/SKILL.md). The sketch starts from its result, not from a guess.

## 1. Name the data shape

Before any logic, name the structure that encodes the domain, as [`model-the-domain`](../../constitution/references/architecture.md#model-the-domain) describes, and trace every way the data is read and written through it (`foundational-thinking`).

Name the shape in the domain's words. Its types, states, and events take their names from the repo glossary, so the vocabulary settled with the user is the one the code carries. A domain concept the glossary lacks is added to it in the same PR, as `shape-spec`'s domain.md describes.

## 2. Ground

Read every module the new code touches, and write a short note on how each works today: what it owns, who calls it, which invariants it holds. Naming a file is not grounding.

When the design moves ownership or layering, read why the current shape exists: the ADRs that cover it, and the commits and PRs that introduced it (`git log --follow`, `git blame` on the load-bearing lines). Its reasons become constraints, not guesses.

Skip this step only for new code with nothing around it to integrate.

## 3. Sketch twice

Run an arena of two runners, or three for a one-way door, as [parallel.md](../../constitution/references/parallel.md) describes, from two model families when the harness offers them (see [harness.md](../../constitution/references/harness.md)). Each runner's brief holds the task, `done_when`, the case list, your grounding notes, its own output path, and the path of [sketch-brief.md](sketch-brief.md), which it follows.

Ask for structurally different shapes: whole-shape alternatives, not point fixes inside one shape. The arena's criteria are the 3 to 6 rules of the sketch brief that matter most for this change.

## 4. Screen

Check each candidate against the [red flags](#red-flags) below and the Test of each principle it cites. A red flag is a reason to revise or reject the shape.

## 5. Pick, graft, and write the note

Prefer the shape that hides more behind a smaller public surface, and where a change that looks right from one file is right for the whole repo. Graft by hand, as the arena describes, so the result keeps one design.

Write the design note as [design-note.md](design-note.md) shapes it; it goes in the PR's Design section. The chosen shape and the main rejected one also get one line each under Decisions. The sketch can land as its own commit, before the bodies are filled.

## 6. Build against the sketch

The sketch is the contract. When the code needs something the sketch did not plan, such as a parameter, a state, or a case, ask whether the sketch, the requirement, or the code is wrong, and write the answer under Deviations in the note. Do not absorb it silently.

## 7. Scrap a wrong sketch

One deviation is information; a pattern means the shape is wrong. The tells:

- the same kind of workaround in unrelated places;
- unrelated edge cases that each need a special branch;
- types that compile only with casts, `any`, or optional fields that are always set;
- "we need a lock" when the sketch said the state was not shared;
- callers that must know the abstraction's internal rules to use it;
- two independent deviations of the same shape.

Complexity in the data is not complexity in the design: a few edge cases do not condemn a shape.

To scrap, trace what was built, then redesign as if the new constraints had been there from day one (`redesign-from-first-principles`). Cut before you grow: the new sketch is smaller than the old one before it gets bigger (`subtract-before-you-add`). Run step 3 again, with the tells in the grounding notes. A task scraps once. A second scrap means the frame was wrong: stop with `needs-human`, and give the user what the two sketches taught.

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
