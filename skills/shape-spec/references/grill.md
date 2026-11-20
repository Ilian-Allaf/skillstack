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

## Facts are yours, decisions are the user's

When a question needs a fact from the code, the docs, or a tool, spawn a fresh subagent to find it. Never ask the user for something you could look up. Do not wait for it: only the questions downstream of that fact wait; ask the rest now.

When an answer is something you could observe by running a small experiment, prototype instead of asking.

## Done

The frontier is empty: every branch visited, nothing silently assumed. Ask the user to confirm the shared understanding before you act on it.
