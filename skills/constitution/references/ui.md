# UI rules

Read when a prototype or a diff changes what a user sees: as the agent in `shape-spec`'s visual branch, as the builder, as a critic in the [target loop](../../ship/references/visual-loop.md), and as the verifier in `live` and `standards`. The repo's design system and its documented standards win over this file. What the spec takes from it is the contract; the rest steers and makes notes.

Left alone, an agent builds the safe, average page: functional, and like every other one. These rules name what to aim for and what to drop.

## The design system comes from the code

Before any screen, find where the tokens, components, and patterns of the area live: the theme or token file, the component folder, the stories, the screens nearest to the change. Name what exists, what the change needs, and what is missing. Never write the design system down: the code says it, and a copy goes stale.

The spec's design mode says how to use it:

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
| coherence | Does it read as one design, not a set of parts? | one button pair, one card family, one radius scale, one type scale, one spacing scale; values from the tokens |
| originality | Are there choices made for this product? | a layout, a color, and a type pairing someone chose for this content, not a template's defaults |
| craft | Are the fundamentals sound? | a clear type hierarchy, aligned edges, even spacing, text contrast that passes, nothing cut or overlapping |
| usability | Can a user act without guessing? | the main action found in one look, every state drawn (empty, loading, error, focus, disabled), labels you can see |

## Every screen, every width

- Desktop and phone at least, such as 1440 and 390 wide; nothing scrolls sideways at 320.
- Every control a pointer can reach answers it; every control a keyboard can reach shows its focus.
- Tap targets 44px tall on a phone.
- Under reduced motion, everything rests and nothing stays hidden.
- Real content: the product's own words and data, never filler text or invented figures, reviews, or customers.

## Generic defaults to drop

Each one alone may be fine. Together they read as a page no one designed. Use one only when the user asked for it or the design system has it.

- small uppercase labels above every heading, and monospace uppercase text as decoration;
- a serif display font picked for no reason of the content;
- purple or violet gradients, purple as the default accent, beige as the default ground;
- glowing orbs, blurred blobs, rings bursting out of things, decorative particles, long thin decorative lines;
- `01 / 02 / 03` counters on sections that have no order;
- a fade-in on every section or card as it scrolls in, parallax on text;
- a caption under each picture that explains it;
- three equal cards with an icon, a title, and two lines, as the answer to every section;
- em dashes in the interface copy.

## Motion after layout

Get the screen right still first; add motion as its own step. Motion from a reference video is analyzed frame by frame into a list of each effect, its timing, and its easing; take from several references, and copy no element one to one.

## Measured or judged

A number a command produced is measured: contrast ratios, overflow at a width, tap sizes, a raw color outside the tokens, a color delta per region against the target. Anything a person or a model judged is level 1, whatever its score. Each rule above that a command can hold becomes a check through `add-guardrail` when the repo needs it.
