# Mode: question

For a question about the code: how something works, why it is built this way, which of two options to pick. The answer is a cited explanation or a recommendation.

## Duties

1. **How: explain from the code.** For "how does X work", spawn one fresh read-only subagent with the question and this brief: "Write an architectural explanation for a senior engineer new to this area, so they can start working in it with confidence." Read the files it cites before you trust it, then present its answer with light edits only.
2. **Why: answer from the record.** For "why is it like this", read the commits, PRs, and issues that introduced the code and each later change. Quote what the authors wrote, mark your own inferences as inferences, and say what the record does not answer.
3. **Which: compare by running.** For a choice between options, check each claim about an option by running something when a run can check it: a benchmark, a script, a spike outside the source tree.

## Shape of the answer

- An explanation: overview, key concepts, how it works, where things live, gotchas.
- A choice: a table of options and tradeoffs, then your recommendation and why.
- An "are we sure?" question: your judgment and its reasons. If the premise of the question is wrong, say so.
