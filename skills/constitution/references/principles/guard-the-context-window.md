# guard-the-context-window

**Apply when** output is large, reads repeat, or a phase plans to read many files.

**Rule.** Send bulk work to subagents or scripts, and keep summaries in the main thread. A full context reasons worse and loses what it read first.

## How

- A subagent gets file paths, not pasted content, and returns pointers and a short summary, not a dump.
- A script filters a large output before you read it: the failing lines, the count, the diff.
- Size each phase: how many files it reads, how long it runs.
- Write down what must survive a long run, such as decisions and open questions, in the decision log or the PR, not only in the conversation.

## Test

Is anything in the main thread there only because it was never summarized?

## Sign it was skipped

A whole log pasted into the conversation. The same file read three times.
