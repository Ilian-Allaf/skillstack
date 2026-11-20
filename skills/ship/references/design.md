# Design before code

The codebase is the largest input of the next agent, and that agent copies the nearest example. A shape chosen at write time is cheap; recovering it later reads as a refactor and gets deferred. So the builder picks the shape before the code, and reads the full form of each [principle](../../constitution/references/principles.md) its sketch relies on: those the rules of [sketch.md](sketch.md) name, one file each.

## How much design the change needs

| The change | Steps |
|---|---|
| local to one function body: no new type, and nothing changes in what a function takes or returns | 1 |
| a feature, or any change that crosses a function boundary: a new or changed type, signature, or module | 1 to 5, then 7 and 8 |
| the same, through a one-way door (a public API, a schema, a storage or wire format), or when the user asked to see the design | 1 to 8 |

## 1. Name the data shape

Before any logic, name the structure that encodes the domain (`model-the-domain`), and trace every way the data is read and written through it (`design-the-data-first`).

Name the shape in the domain's words. Its types, states, and events take their names from the repo glossary, so the vocabulary settled with the user is the one the code carries. A domain concept the glossary lacks is added to it in the same PR, as `shape-spec`'s domain.md describes.

## 2. Ground

Read every module the new code touches, and write a short note on how each works today: what it owns, who calls it, which invariants it holds. Naming a file is not grounding.

When the design moves ownership or layering, read why the current shape exists: the ADRs that cover it, and the commits and PRs that introduced it (`git log --follow`, `git blame` on the load-bearing lines). Its reasons become constraints, not guesses.

Skip this step only for new code with nothing around it to integrate.

## 3. Sketch twice

Write two sketches, each as [sketch.md](sketch.md) describes (`design-it-twice`). The second differs from the first on a whole-shape axis: where the data lives and who owns it, where the boundary sits, or which structure encodes the domain. Two variants of one shape do not count. Write the second before you judge the first, so the first does not anchor it.

When a run can settle the choice between them, such as a timing, a layout, or whether an approach works at all, prototype both in the prototype mode of [investigate](../../investigate/SKILL.md) and let the observation decide.

## 4. Screen

Check both sketches against the [red flags](#red-flags) below and the Test of each principle they rely on. A red flag is a reason to revise or reject the shape.

## 5. Pick and write the note

Prefer the shape that hides more behind a smaller public surface, and where a change that looks right from one file is right for the whole repo. Take from the other sketch what is worth keeping, and fold it in by hand so the result keeps one design.

Write the design note as [design-note.md](design-note.md) shapes it; it goes in the PR's Design section. The chosen shape and the rejected one also get one line each under Decisions. The sketch can land as its own commit, before the bodies are filled.

## 6. Show the design

For a one-way door, or when the user asked to see the design, stop before any body is filled. Show the user the note's Usage, Shape, Alternatives rejected, and Questions before the merge, and ask for a go on the design through the harness's question tool. Their pushback is grounding: go back to step 2 with it.

## 7. Build against the sketch

The sketch is the contract. When the code needs something the sketch did not plan, such as a parameter, a state, or a case, ask whether the sketch, the requirement, or the code is wrong, and write the answer under Deviations in the note. Do not absorb it silently.

## 8. Scrap a wrong sketch

One deviation is information; a pattern means the shape is wrong. The tells:

- the same kind of workaround in unrelated places;
- unrelated edge cases that each need a special branch;
- types that compile only with casts, `any`, or optional fields that are always set;
- "we need a lock" when the sketch said the state was not shared;
- callers that must know the abstraction's internal rules to use it;
- two independent deviations of the same shape.

Complexity in the data is not complexity in the design: a few edge cases do not condemn a shape.

To scrap, trace what was built, then redesign as if the new constraints had been there from day one (`redesign-from-first-principles`). Cut before you grow: the new sketch is smaller than the old one before it gets bigger (`subtract-before-you-add`). Run step 3 again, with the tells in the grounding notes. A task scraps once. A second scrap means the frame was wrong: stop with `needs-human`, and give the user what the sketches taught.

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
