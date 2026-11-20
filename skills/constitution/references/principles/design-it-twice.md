# design-it-twice

**Apply when** a change adds a feature, or adds or changes a type, a signature, or a module boundary that other code calls.

**Rule.** The first shape that comes to mind is a guess. Sketch two structurally different shapes, screen both, then pick one.

## How

- The second sketch differs from the first on a whole-shape axis: where the data lives and who owns it, where the boundary sits, or which structure encodes the domain. Two variants of one shape do not count.
- Write the second sketch before you judge the first, so the first does not anchor it.
- Screen both against the red flags in `ship/references/design.md`, and the Test of each principle they rely on.
- Prefer the shape that hides more behind a smaller public surface.
- When a run can settle the choice, such as a timing, a layout, or whether an approach works, prototype both and observe instead of arguing.
- Write the losing shape and why it lost in the design note, under Alternatives rejected.

## Test

Could someone tell the two sketches apart from their module layout alone? If not, they are one shape.

## Sign it was skipped

The design note names no alternative, or names a variant of the chosen shape. The first sketch shipped unchanged.
