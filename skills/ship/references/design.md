# Design before code

The builder picks the shape before the code, with the method of [architecture.md](../../constitution/references/architecture.md), and within the technical decisions the spec holds.

## How much design the change needs

| The change | Steps |
|---|---|
| local to one function body: no new type, and nothing changes in what a function takes or returns | 1 |
| a feature, or any change that crosses a function boundary: a new or changed type, signature, or module | 1 to 5, then 7 and 8 |
| the same, through a one-way door (a public API, a schema, a storage or wire format), or when the user asked to see the design | 1 to 8 |

## The spec's technical decisions

A spec issue can hold Technical decisions, numbered `D1`, `D2`: the user made them, through `shape-architecture` or in the grill. Build within them as within an accepted ADR. A spec whose section says the shape is left to the builder holds none.

- **Fresh.** At step 2, check that each decision still holds. The Grounded on line names a commit and the modules the decisions touch. When one of them changed since that commit, or the line is missing, as for a decision stated in the grill, ground those modules again. Sketches saved in the project folder, when this machine has them, are input to the grounding, never a draft: your sketches start from the code.
- **Within.** Both sketches keep every decision and differ only on what the section leaves to the builder. When it leaves nothing open that crosses a boundary, write the one sketch the decisions give, and skip the second.
- **A decision the code contradicts** is evidence against what the user asked for (rule 11 of the constitution): stop, with the decision's id, the file or run that contradicts it, and the replacement you recommend. Found before any body is filled, the stop costs only the frame. Found during the build, write it under Deviations with the decision's id, and open the PR as `needs-human`, as `ship` does when its build budget runs out.
- **The user's answer replaces the decision.** Write it into the spec's Technical decisions with the tracker's Edit an issue, under a new id that names the one it replaces and quotes the answer or links the comment that holds it, as `shape-architecture`'s [decisions.md](../../shape-architecture/references/decisions.md) shapes it. When the replaced decision links an ADR, the PR carries the ADR that supersedes it. Then build within the new decision, and name it on the Deviations line.
- **A decision you would rather change**, with no evidence against it, stays: make your case under Questions before the merge.

## 1 to 4. Name the data shape, ground, sketch twice, screen

Follow steps 1 to 4 of [architecture.md](../../constitution/references/architecture.md).

## 5. Pick and write the note

Pick the shape the screen favors. Take from the other sketch what is worth keeping, and fold it in by hand so the result keeps one design. Write the design note as [design-note.md](design-note.md) shapes it; it goes in the PR's Design section. The chosen shape and the rejected one also get one line each under Decisions. The sketch can land as its own commit, before the bodies are filled.

## 6. Show the design

For a one-way door, or when the user asked to see the design, stop before any body is filled. A one-way door a technical decision of the spec already settled needs no stop: the user made that call. Show the user the note's Usage, Shape, Alternatives rejected, and Questions before the merge, and ask for a go on the design through the harness's question tool. Their pushback is grounding: go back to step 2 with it.

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

To scrap, trace what was built, then redesign as if the new constraints had been there from day one (`redesign-from-first-principles`). Cut before you grow: the new sketch is smaller than the old one before it gets bigger (`subtract-before-you-add`). Run step 3 again, with the tells in the grounding notes, and within the spec's technical decisions: a scrap whose tells point at one of them is a decision the code contradicts, as above. A task scraps once. A second scrap means the frame was wrong: stop with `needs-human`, as `ship` says for a stop before its step 6, and give the user what the sketches taught.
