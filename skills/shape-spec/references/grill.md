# Grill

A relentless interview until you and the user share one understanding.

## The design tree

Every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are settled: the questions you can ask now without guessing answers you have not heard.

## Rounds

Ask the whole frontier in one round, through the harness's question tool when it fits, otherwise as a numbered message:

```text
Q1. <title>: <the question, with the options when there are some>
Recommended: <your answer>

Q2. <title>: <the question>
Recommended: <your answer>
```

- Word each question so "yes" accepts your recommendation.
- A question whose answer depends on another open question in this round waits for a later round.
- Each round of answers moves the frontier. Recompute it and ask the next round.

## The verification branch

The design tree of every spec has this branch; visit it once the stories are settled. A map's decisions skip it, and its destination's spec takes it. Draft each answer and ask in one round, so a yes accepts it:

- **A journey per story**: the surface, the steps, and the result the user expects. One per story is the minimum and usually enough; a story in a hard zone adds its edge cases.
- **Promises**, as the [glossary](../../constitution/references/glossary.md) defines them, each with the harm when it breaks.
- **What cannot be verified**, and why, so the user knows it before the build.

The means of proof are facts: look up the drivers and formal checks of the area as [proof.md](../../constitution/references/proof.md#drivers-and-formal-checks) says, stale or not. For a touched surface with no driver, ask the user for what only they can give, the account, the access, and where the secret lives, and write it to `~/.agents/projects/<project>/access/<app>.md`, never the secret itself. Nothing technical goes in the spec.

## Facts are yours, decisions are the user's

When a question needs a fact from the code, the docs, or a tool, spawn a fresh subagent to find it. Never ask the user for something you could look up. Do not wait for it: only the questions downstream of that fact wait; ask the rest now.

When an answer is something you could observe by running a small experiment, prototype instead of asking.

## Done

The frontier is empty: every branch visited, the verification branch included, nothing silently assumed. Ask the user to confirm the shared understanding before you act on it.
