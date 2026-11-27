# Architecture

How to shape code before it is written: the data shape, the grounding, two sketches, and the screen. It has two readers. `ship` follows it to pick a shape itself, as its [design.md](../../ship/references/design.md) says. `shape-architecture` follows it to put the choice to the user before the build.

The codebase is the largest input of the next agent, and that agent copies the nearest example. A shape chosen before the code is cheap; recovering it later reads as a refactor and gets deferred. Before a sketch relies on a [principle](principles.md), read its full form: those the rules of [sketch.md](sketch.md) name, one file each.

## 1. Name the data shape

Before any logic, name the structure that encodes the domain (`model-the-domain`), and trace every way the data is read and written through it (`design-the-data-first`).

Name the shape in the domain's words. Its types, states, and events take their names from the repo glossary, so the vocabulary settled with the user is the one the code carries. A domain concept the glossary lacks is added to it, as `shape-spec`'s domain.md describes; inside a task, in the task's PR.

## 2. Ground

Read every module the new code touches, and write a short note on how each works today: what it owns, who calls it, which invariants it holds. Naming a file is not grounding. For a change to what a user sees, ground the design system as [ui.md](ui.md#the-design-system-comes-from-the-code) says.

When the design moves ownership or layering, read why the current shape exists: the ADRs that cover it, and the commits and PRs that introduced it (`git log --follow`, `git blame` on the load-bearing lines). Its reasons become constraints, not guesses.

Skip this step only for new code with nothing around it to integrate.

## 3. Sketch twice

Write two sketches, each as [sketch.md](sketch.md) describes (`design-it-twice`). The second differs from the first on a whole-shape axis: where the data lives and who owns it, where the boundary sits, or which structure encodes the domain. Two variants of one shape do not count. Write the second before you judge the first, so the first does not anchor it.

When a run can settle the choice between them, such as a timing, a layout, or whether an approach works at all, prototype both in the prototype mode of [investigate](../../investigate/SKILL.md) and let the observation decide.

## 4. Screen

Check both sketches against the [red flags](#red-flags) below and the Test of each principle they rely on. A red flag is a reason to revise or reject the shape.

The screen favors the shape that hides more behind a smaller public surface, and where a change that looks right from one file is right for the whole repo. It keeps both sketches: `ship` picks one by it, and `shape-architecture` recommends one by it.

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
