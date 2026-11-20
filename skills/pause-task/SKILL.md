---
name: pause-task
description: "Stops the running task at a safe point and leaves a resume note, so a fresh session picks it up with nothing lost."
disable-model-invocation: true
argument-hint: "<nothing, or why you stop>"
metadata:
  kind: entry
  consumes: "a task running in this session"
  produces: "a resume note: in a wip commit when the task has its branch, else in a file outside the repo; also on the PR or issue when there is one"
  hypothesis: "A session that ends mid-task, on a usage limit, a full context, or a closed laptop, loses what lived only in the conversation, and the next agent redoes or contradicts it."
---

# Pause task

Read [the constitution](../constitution/README.md) first.

You stop cleanly so that an agent with none of this conversation can resume. Run this when the user says pause, stop for now, or that they are going offline, and on your own when your context or the usage limit is about to run out. "Keep going" or "I am going to bed, keep going" is not a pause: do not run this.

## Steps

1. **Stop at a safe point.** Finish the current atomic step, or back out of it. Start nothing new, and stop the subagents you spawned, noting what each was doing. A `ship-queue` coordinator first has each owner pause its own task by these steps, then writes one queue note: the frame, and for each task its owner's state, branch, PR, and replacements used.
   Done when: no step is half done, and no subagent of yours is running.

2. **Make the work durable.** When the task has its own branch (a `ship` task from its step 2 on, a unit of a stack, or `shape-spec` once it opened its docs branch), commit every uncommitted edit as one commit on that branch, titled `wip: <task in a few words>`; if the tree does not build or the tests fail, say so in one line of the body. When it has none (`investigate`, `shape-spec` before its docs branch, a `ship` task still in its frame), commit nothing: the note goes to a file outside the repo, in the system's temporary folder, named `<repo>-<task in a few words>-resume.md`. Take no irreversible action to pause: push only a branch that was already pushed, and open no PR. When the branch's PR carries `ready`, remove the label before you push: a `wip:` head is not ready.
   Done when: the edits are in the `wip:` commit, or the task had no branch and the note file is named; nothing of yours is left uncommitted on a task branch.

3. **Write the resume note** in the body of that commit, or in that file, for an agent that has none of this conversation:
   - the goal, in the user's words, and `done_when`;
   - the skill and the step you stopped at, and the playbook;
   - what is done and verified, each with its evidence: a commit, a run, a file;
   - what is in progress, and what you were about to try next;
   - the decisions made so far, and the questions still open for the user;
   - the key files, and the gotchas you learned the hard way.

   When a decision log exists, copy its rows of this session into the note: the log lives out of git, and the next session may run on another machine. When a PR is open, post the same note as a PR comment headed `Paused`; when the task has an issue and no PR, post it on the issue.
   Done when: the note answers "what next, and why" without the conversation.

## Reply

Where you stopped, what is on disk and on the PR, whether the tree is green, and the command to resume: `/resume-task <branch, PR, or issue>`. This is a pause, not a final report.
