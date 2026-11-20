# make-the-smallest-change

**Apply when** you size a diff, or are tempted to add a layer, an abstraction, an option, or a parameter threaded through calls.

**Rule.** Prefer deletion and the smallest change that meets `done_when`. Fewer lines beat elegant boilerplate.

## How

- Consolidate a decision. When the same choice is made in several places, make it once, behind one source of truth, and pass the result.
- Build for the usage you observed, not for the one you imagine. No speculative option, validator, parser, or extension point.
- An abstraction earns its place by removing duplication that exists today, not duplication that might come.
- A change that "might help" is a hypothesis. It does not ship.
- The smallest change is not the smallest diff at any cost: when the right fix is a redesign, the redesign is the smallest change that solves the problem (`redesign-from-first-principles`).

## Test

For each added line, name the part of `done_when` it serves. A line that serves none is removed.

## Sign it was skipped

A generic helper with one caller. An option no caller sets. An interface with one implementation and no second one planned.
