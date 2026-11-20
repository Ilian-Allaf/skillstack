---
name: pause-task
description: "Stops the running task at a safe point and leaves a resume note, so a fresh session picks it up with nothing lost."
disable-model-invocation: true
argument-hint: "<nothing, or why you stop>"
metadata:
  kind: entry
  calls: "resume-task"
  consumes: "a task running in this session"
  produces: "a wip commit whose body is the resume note; the note on the PR when one is open"
  hypothesis: "A session that ends mid-task, on a usage limit, a full context, or a closed laptop, loses what lived only in the conversation, and the next agent redoes or contradicts it."
---

# Pause task

Read [the constitution](../constitution/README.md) first.

You stop cleanly so that an agent with none of this conversation can resume. Run this when the user says pause, stop for now, or that they are going offline, and on your own when your context or the usage limit is about to run out. "Keep going" or "I am going to bed, keep going" is not a pause: do not run this.

## Steps

1. **Stop at a safe point.** Finish the current atomic step, or back out of it. Start nothing new, and stop the subagents you spawned, noting what each was doing.
   Done when: no step is half done, and no subagent of yours is running.

2. **Make the work durable.** Commit every uncommitted edit as one commit on the current branch, titled `wip: <task in a few words>`. If the tree does not build or the tests fail, say so in one line of the body. Take no irreversible action to pause: push only a branch that was already pushed, and open no PR.
   Done when: `git status` is clean, and the branch holds the `wip:` commit.

3. **Write the resume note** in the body of that commit, for an agent that has none of this conversation:
   - the goal, in the user's words, and `done_when`;
   - the skill and the step you stopped at, and the playbook;
   - what is done and verified, each with its evidence: a commit, a run, a file;
   - what is in progress, and what you were about to try next;
   - the decisions made so far, and the questions still open for the user;
   - the key files, and the gotchas you learned the hard way.

   When a decision log exists, point to it instead of copying it. When a PR is open, post the same note as a PR comment headed `Paused`.
   Done when: the note answers "what next, and why" without the conversation.

## Reply

Where you stopped, what is on disk and on the PR, whether the tree is green, and the command to resume: `/resume-task <branch or PR>`, as [resume-task](../resume-task/SKILL.md) describes. This is a pause, not a final report.
