# Grill

A relentless interview until you and the user share one understanding.

## The design tree

Every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are settled: the questions you can ask now without guessing answers you have not heard.

## Rounds

Ask the whole frontier in one round, as a numbered message that ends your turn. The user answers in their own words, all the questions at once or a few, and can push back on any of them. A form of buttons turns the interview into a pick among your options; use the harness's question tool only for a round of one question between named options.

```text
Open: <each branch still open, one line each>

Q1. <title>
<the question, with the options when there are some, and what each one costs>
Recommended: <your answer, with its reason>

Q2. <title>
<the question>
Recommended: <your answer, with its reason>
```

- Open each round with the branches still open, so the user sees how far the interview is and what comes next.
- Word each question so "yes" accepts your recommendation.
- A question whose answer depends on another open question in this round waits for a later round.
- Dig into each answer. An answer that opens a branch, names a case you had not seen, or hesitates gets its follow-up in the next round, until the branch is settled, not only the question answered.
- Each round of answers moves the frontier. Recompute it and ask the next round.

## A heavy visual change

When step 1 of the skill found one, two decisions hang off the stories. Visit them once the stories are settled and before the verification branch, since the targets become cases.

- **The design mode.** Ground the area's design system first: a fact a subagent finds, as [ui.md](../../constitution/references/ui.md#the-design-system-comes-from-the-code) says. Recommend a mode from what it found and what the story is for, with the reason; the user confirms.
- **The pick.** Run [investigate](../../investigate/SKILL.md) in prototype mode on the visual decision, in the confirmed design mode, until the user picks a variant. Draft the spec's Visual targets from the pick: a capture of each state the stories need at each width, a recording with its effect list for each part that moves, and the measured checks and bans of ui.md that apply. Save their files to `~/.agents/projects/<project>/targets/<spec>/`, outside the repo, and link them from the issue when the tracker can host files. The user confirms them, or sets other thresholds.

Done when: the user confirmed the design mode, picked a variant, and confirmed its visual targets.

## The verification branch

The design tree of every spec has this branch; visit it once the stories are settled. A map's decisions skip it, and its destination's spec takes it. Draft each answer and ask in one round, so a yes accepts it:

- **A journey per story**: the surface, the steps, and the result the user expects. One per story is the minimum and usually enough; a story in a hard zone adds its edge cases.
- **Promises**, as the [glossary](../../constitution/references/glossary.md) defines them, each with the harm when it breaks.
- **What cannot be verified**, and why, so the user knows it before the build.

The means of proof are facts: look up the drivers and formal checks of the area as [proof.md](../../constitution/references/proof.md#drivers-and-formal-checks) says, stale or not. For a touched surface with no driver, ask the user for what only they can give, the account, the access, and where the secret lives, and write it to `~/.agents/projects/<project>/access/<app>.md`, never the secret itself. The means of proof stay out of the spec.

## Facts are yours, decisions are the user's

When a question needs a fact from the code, the docs, or a tool, spawn a fresh subagent to find it. Never ask the user for something you could look up. Do not wait for it: only the questions downstream of that fact wait; ask the rest now.

When an answer is something you could observe by running a small experiment, prototype instead of asking.

A decision on the shape of the code that the user states unasked, such as a storage or a library, is theirs: keep it for Technical decisions, and ask nothing more about the shape.

## Done

The frontier is empty: every branch visited, the verification branch included, nothing silently assumed. Ask the user to confirm the shared understanding before you act on it.
