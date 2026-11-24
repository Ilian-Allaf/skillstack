# encode-lessons-in-structure

**Apply when** the same correction comes back, you catch yourself writing the same instruction a second time, or you are about to write a decision or a rule in a doc: an ADR, the agent file, a coding standard.

**Rule.** Turn the lesson into structure, in this order of preference: architecture that removes the wrong way, a type that rejects it, a lint or check whose message names the fix, a test, and docs last. Nothing fails when an agent skips a doc.

## How

- Architecture first: one owner per piece of state, one way per task, internals that cannot be imported, one list from which the others derive.
- A check proves itself by failing on a real past mistake before it is trusted.
- When the structural fix exists, use only it. The instruction was the symptom.
- When the lesson needs judgment and cannot be encoded, make the instruction prominent and add an example of the failure.
- A decision follows the same order. What the code holds needs no doc. An ADR keeps only what the code cannot say: the why, and the alternatives rejected.
- `/add-guardrail` does this for a whole class of mistakes.

## Test

If an agent made the same mistake tomorrow, what would fail?

## Sign it was skipped

A rule written in a doc, a comment, or a prompt, and nothing that fails when it is broken. Or an ADR that says nothing the code does not already say.
