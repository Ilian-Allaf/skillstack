# UI rules

Read when a prototype or a diff changes what a user sees or how it moves: as the builder, as a critic in the [target loop](../../ship/references/visual-loop.md), and as the verifier. The repo's design system and its documented standards win over this file. What a spec's Visual targets take from it can block; the rest steers the build and yields notes.

Left alone, an agent builds the safe, average page: functional, and like every other one. These rules name what to aim for and what to drop.

## The design system comes from the code

Before any screen, find where the tokens, components, and patterns of the area live: the theme or token file, the component folder, the stories, the screens nearest to the change, the durations and easings already in use. Name what exists, what the change needs, and what is missing. It is a fact: a subagent finds it, the user is never asked for it, and nobody writes it down, since the code says it and a copy goes stale.

The design mode says how to use it. The spec states it; a task without one follows.

| Mode | When | What the build does |
|---|---|---|
| `follow` | the screen belongs to the product as it is | existing tokens and components only |
| `extend` | the product needs a part it lacks | new components or variants, built from the existing tokens, in the idiom of their neighbours |
| `break away` | the look is the point and the product's own style does not fit it, such as a marketing page or a new product | a system of its own, still one system, with the rules below |

A new component that duplicates an existing one is two ways to do one task ([design.md](../../ship/references/design.md#red-flags)).

## Criteria

Grade a screen against these, not against "is it beautiful". Coherence and originality are where an agent falls short; craft and usability it mostly gets right, and when it fails them, the fundamentals are broken.

| Criterion | The question | A pass looks like |
|---|---|---|
| coherence | Does it read as one design, not a set of parts? | one button pair, one card family, one radius scale, one type scale, one spacing scale, one set of durations and easings; values from the tokens |
| originality | Are there choices made for this product? | a layout, a color, a type pairing, and a motion someone chose for this content, not a template's defaults |
| craft | Are the fundamentals sound? | a clear type hierarchy, aligned edges, even spacing, text contrast that passes, nothing cut or overlapping; motion that starts on its trigger and settles without a jump |
| usability | Can a user act without guessing? | the main action found in one look, every state drawn (empty, loading, error, focus, disabled), labels you can see; motion that shows where something came from or went, never one that makes the user wait |

## Widths

Desktop and phone at least, 1440 and 390 wide unless the spec names others, and 320 for overflow.

## Measured checks

A command can hold each of these. A spec's Visual targets take the ones that apply, with any threshold the user sets instead of the one here.

- Text contrast at least 4.5:1, and 3:1 for large text and controls.
- Nothing scrolls sideways at 320 wide.
- Tap targets at least 44px tall at the phone width.
- Every control a keyboard reaches shows its focus.
- No raw color, size, duration, or easing outside the tokens, under `follow` and `extend`.
- Each effect of a motion target happens on its trigger, with its duration within 20% of the target's.
- Under reduced motion, nothing moves and nothing stays hidden.

A check the repo needs on every change becomes a guardrail through `add-guardrail`.

## Motion

Lay out still first; motion is its own slice, built on a still that already holds up. Each effect has a reason: it shows where something came from, what changed, or what to do next. Every control a pointer reaches answers it. Effects share a few durations and easings, as a type scale shares a few sizes. A reference video is read as an effect list, as [prototype.md](../../investigate/references/prototype.md) says; take from several references, and copy none one to one.

## Generic defaults to drop

Each one alone may be fine. Together they read as a page no one designed. Use one only when the user asked for it or the design system has it.

- small uppercase labels above every heading, and monospace uppercase text as decoration;
- a serif display font picked for no reason of the content;
- purple or violet gradients, purple as the default accent, beige as the default ground;
- glowing orbs, blurred blobs, rings bursting out of things, decorative particles, long thin decorative lines;
- `01 / 02 / 03` counters on sections that have no order;
- a fade-in on every section or card as it scrolls in, parallax on text, a bounce on every button;
- a caption under each picture that explains it;
- three equal cards with an icon, a title, and two lines, as the answer to every section;
- filler text, or invented figures, reviews, or customers, in place of the product's own words and data;
- em dashes in the interface copy.
