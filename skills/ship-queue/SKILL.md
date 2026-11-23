---
name: ship-queue
description: "Turns a list of tasks into as many ready-to-merge PRs, one owner per task, each proven and judged by its own verifier; tasks that touch the same files are stacked. Stops before every merge."
disable-model-invocation: true
argument-hint: "<the tasks or issue numbers, one per line>"
metadata:
  kind: entry
  role: coordinator
  calls: "ship"
  reads: "catch-me-up"
  consumes: "a list of tasks or issues from the user"
  produces: "one PR per task, each labeled ready or needs-human"
  budget: "2 replacements per owner, then the task is needs-human"
  hypothesis: "One task at a time leaves the user waiting on each PR, and parallel agents without one owner per PR and an independent verdict collide and ship unchecked work."
---

# Ship queue

Read [the constitution](../constitution/README.md) and [harness.md](../constitution/references/harness.md) first.

You coordinate; you never write the code. Each task gets one owner, a fresh subagent that carries it through [ship](../ship/SKILL.md) from frame to `ready`, verifier included. You decide who does what, watch what each one produces, and stop when every PR is `ready` or `needs-human`. Nobody merges: the merges are the user's.

The tasks come from the user. You do not split one task into several (ADR 0011): a task too large for one PR goes to its owner with the `bespoke` playbook.

## Steps

1. **Frame the queue.** One line per task: the task, its `done_when` in a few words, its risk class, and whether it builds on another task of the queue. Two tasks that write the same files are not independent: order them, the second stacked on the first. Show the frame and go on (rule 11 of the constitution).
   When `resume-task` hands you a queue note, frame from it: keep each task's replacements used, and add to each owner's brief the path of its own resume note.
   Done when: the frame is in your first message, with each task's base: the repo's base branch, or the task it builds on.

2. **Start one task first.** Spawn its owner, as below, and watch it through its frame and its first build. A flaw in the brief then costs one agent, not all of them.
   Done when: the first owner has pushed a build, or its flaw is fixed in the brief.

3. **Spawn the other owners.** One fresh subagent per task, each in its own worktree and branch from its base, at most three running at once; start the next as one finishes. Pick each owner's model as the harness's Model per role says. Each brief is the one [references/owner-brief.md](references/owner-brief.md) lays out. When an owner cannot spawn its own verifier, it says so, and you spawn a fresh verifier for its PR yourself.
   A task that builds on another starts once the one below has opened its PR, and branches from that PR's branch.
   Done when: every task has an owner running, or waiting on the task it builds on.

4. **Watch by side effects.** Wake on PR events, or on a periodic check while the queue runs (ADR 0014); the wake ends with the queue. On each wake, judge each owner by its pushes, its PR, and its decision log, not by its status text. An owner that errors or shows nothing new for twice its usual time is stuck: replace it with a fresh owner whose brief holds the first brief, every later directive, and the stuck owner's branch and report. After two replacements for one task, stop replacing: push the stuck owner's branch, open its PR in the PR format with what is proven and what is not, label it `needs-human` as `ship` does for a stop before its step 6, and replan the tasks that build on it. When an owner reports what a branch below needs, hand it to that branch's owner. Show the user each owner's frame as it arrives: its `done_when` and its cases. When a PR below gets a new head, tell the owner above to rebase on it, or spawn a fresh owner with its brief if that one has finished. Answer an owner that waits on you. Pass a call only the user can make to the user, with its evidence.
   Done when: every owner is running, done, or replaced, and no owner waits on you.

5. **Check what each owner hands back.** Read the PR, not the owner's summary: its coverage table, its demo, its Verdict line on the current base and head, and its label. A PR labeled `ready` without a passing verdict on its current base and head is not ready: send it back to its owner.
   Done when: every PR is `ready` with a verdict on its current base and head, or `needs-human` with its reason.

6. **Hand over.** After the handover, nobody pushes to a PR of the queue without the user's go.
   Done when: the user has the reply below.

## Reply

The shape of [catch-me-up's reply](../catch-me-up/references/reply.md): one opening sentence, the PRs' demos and screenshots, then one bullet per PR with its link, what it changes, its verdict, and its risk. Stacked PRs come in the order they must merge; independent PRs come riskiest first. Then the `needs-human` PRs with what each needs from the user.
