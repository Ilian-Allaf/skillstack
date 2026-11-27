---
name: resume-task
description: "Picks up a task an earlier session left mid-way, or a PR you answered after it stopped, and carries it on without redoing what was done."
disable-model-invocation: true
argument-hint: "<branch, PR number, issue, or nothing for the last paused task>"
metadata:
  kind: entry
  calls: "ship, investigate, shape-spec, babysit-pr, ship-queue"
  consumes: "a branch, a PR, or a paused task"
  produces: "the task carried on by the skill that owns it"
  hypothesis: "A new session distrusts the work it inherits and redoes it, or trusts a summary and skips what was never verified."
---

# Resume task

Read [the constitution](../constitution/README.md) first.

The earlier session's trail is your input, and it is authoritative: you continue it, you do not redo it. You also do not trust a claim you have not seen evidence for.

## Steps

1. **Find the trail.** Without an argument, take the most recent resume note `pause-task` left: a branch whose last commit starts with `wip:`, or a file `<repo>-*-resume.md` in the system's temporary folder, whichever is newer. Read, in this order: the resume note, the PR or the issue and its comments, the decision log, and the session transcript when the harness keeps one (see [harness.md](../constitution/references/harness.md)). Read a long transcript in a subagent and keep only its timeline of decisions and open points.
   Done when: you can state the goal, the skill, and the step the earlier session stopped at.

2. **Rebuild the state.** The branch and its worktree, what landed against the base (`git log`, `git diff`), the PR's checks, State line, labels, and threads, the decisions made, and the questions still open.
   Done when: you have a list of what is done, each with its evidence, and of what is pending.

3. **Check what the next step relies on.** Rerun only the cheap checks the next step builds on, such as `done_when` and the build. A claim with no evidence is pending, not done. Do not rerun what has its evidence.
   Done when: each claim the next step relies on is confirmed, or moved back to pending.

4. **Hand over and continue.** On a `needs-human` PR, the user's answer, in the session or in the PR's latest comments, is a new directive: set the State line back to `in progress`, remove the `needs-human` label if it carries one, and the loop that stopped starts again with a fresh budget (rule 11 of the constitution). Undo the `wip:` commit into the working tree if the tree was broken, or keep it; when it was pushed, push the undo with `git push --force-with-lease`, since the branch is yours. Then continue in the skill that owns the task, at its first step whose Done when fails: [ship](../ship/SKILL.md), [investigate](../investigate/SKILL.md), [shape-spec](../shape-spec/SKILL.md), [babysit-pr](../babysit-pr/SKILL.md) for a PR that only needs to reach `ready`, or [ship-queue](../ship-queue/SKILL.md) for a queue note, which resumes each task through its own note.
   Done when: the owning skill is running from its resume point.

## Reply

First, where the earlier session stopped, what you inherited, and what you redid (ideally nothing), and the resume point. Then the reply of the skill that took over.
