---
name: sharpen-prompt
description: "Rewrites a prompt you are about to send so it asks for deeper work, not more work. Does not do the task."
disable-model-invocation: true
argument-hint: "<the prompt you want to send>"
metadata:
  kind: entry
  consumes: "a prompt the user is about to send"
  produces: "a rewritten prompt, ready to send"
  hypothesis: "A user asks for what they already know to ask for, and the agent does exactly that, short of what an expert would have done."
---

# Sharpen prompt

Read [the constitution](../constitution/README.md) first.

You make the prompt deeper, not bigger. You do not do the task.

## Steps

1. **Answer four questions** about the task, in a few lines each:
   - What would a top professional in this field do here that the prompt does not ask for?
   - What is the rawest material they would start from, instead of what has already been digested for the user?
   - Which methods and tools would they use?
   - What, other than the agent or the user, would show that the result is right?
   Done when: each question has a concrete answer for this task, not a general one.

2. **Rewrite the prompt** to ask for exactly that: the depth and the evidence an expert would reach, with their methods named as the bar the result must meet, not as steps the agent must follow. The rewrite asks the agent to settle by a prototype any choice an experiment can settle, and to recommend from what it observed. It leaves to the user the product and preference choices no experiment can settle. It keeps the user's goal and words where they were precise.
   Done when: the rewritten prompt can be sent as it is.

## Reply

The four answers in a few lines, then the rewritten prompt in a code block, then the command to send it with, such as `/ship`.
