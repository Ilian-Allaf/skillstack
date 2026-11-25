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

## The visual branch

For a heavy visual change, as step 1 of the skill detects it. Visit it once the stories are settled and before the verification branch, since its targets become cases. Every round still drafts and recommends, so a yes accepts it.

1. **Read the design system.** Spawn a fresh subagent to find, in the code, where the tokens, components, and patterns of the area live, and which screens sit nearest to the change, as [ui.md](../../constitution/references/ui.md#the-design-system-comes-from-the-code) says. It is a fact: never ask the user for it, and write none of it in the spec.
2. **Settle the design mode** (`follow`, `extend`, or `break away`, as ui.md defines them). Recommend one from what the subagent found and what the story is for, with the reason; the user confirms.
3. **Gather references.** Ask for the user's own: screenshots, sites, apps, videos for motion. With none, or too few, propose five to eight from a library of real product screens when the harness has one (see [harness.md](../../constitution/references/harness.md)), else from the web, or by driving a real site in a browser. Show each with one line on what to take from it: the layout, the color, the type, the density. The user keeps some and drops the rest.
4. **Prototype three variants** in the prototype mode of [investigate](../../investigate/SKILL.md), from the references kept, in the design mode: built from the repo's real components for `follow` and `extend`. Show them side by side, each at a desktop and a phone width.
5. **Make feedback specific.** Ask what to change, where, and how. When the user feels something is off but cannot name it, describe in plain words how you built that part: its layout, fonts, colors, spacing, so they have the words. Change the variants and show them again, until the user picks one.
6. **Fix the target.** Capture the pick at each state the stories need (empty, filled, error) and at each width. Draft the bar: the criteria of ui.md that apply, each with a score out of 10 to clear (8 when the user sets none), the generic defaults the spec bans, and the round floor and limit of the [target loop](../../ship/references/visual-loop.md), or its defaults when the user sets none.

Done when: the user picked a variant, and confirmed the design mode, the captures, and the bar.

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
