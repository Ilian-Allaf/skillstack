---
name: learn-from-mistakes
description: "Learns from a session, a failed PR, or a bug found after merge, and proposes fixes to the layer that missed it. Applies nothing before you approve."
disable-model-invocation: true
argument-hint: "<nothing for this session, a PR number, or an issue labeled escaped>"
metadata:
  kind: meta
  calls: "add-guardrail, create-app-driver"
  reads: "ship, verify-pr"
  consumes: "a session transcript, a PR, or an issue labeled escaped"
  produces: "an approved list of changes, each in its own PR, and issues for the backlog"
  hypothesis: "Without a structured retro, the same mistake comes back, and the fix lands as one more line of rules instead of a check."
---

# Learn from mistakes

Read [the constitution](../constitution/README.md) first, and `~/.agents/projects/<project>/issue-tracker.md`: this skill reads escaped bugs and files backlog issues, so without that file it stops and asks the user to run `/setup-repo`.

A mistake that reached the user is a hole in one layer of the system. You find the layer, and you make the hole smaller. You change nothing before the user approves: a skill change affects every future run, and the user stays in charge of what gets launched.

## Steps

1. **Gather what happened.** By argument:
   - nothing: this session's transcript, found through the harness (see [harness.md](../constitution/references/harness.md));
   - a PR: its body, verdict comments, review threads, commits, and the decision log if one exists;
   - an issue labeled `escaped`: the bug, the PR that shipped it, and that PR's coverage table and verdict.

   For a session, reconstruct required reads, actions, and outputs from activity before reading its final summary; use [decision-log.md](../constitution/references/decision-log.md#before-handing-back) to distinguish an observed action from a claim. Name missing activity rather than treating absence of a trace as proof an action never ran. Skip a session that was trivial or already went by the book. A one-off is not a lesson.
   Done when: every source is listed with its path or link, or the reason to stop is given.

2. **Spawn three reviewers, for a session only.** A swarm of three read-only fresh subagents, one per lens, as [references/reviewers.md](references/reviewers.md) describes. With a PR or an `escaped` issue, skip this step: the layer of step 3 is the finding, and step 4 sorts it alone.
   Done when: three lists came back, each finding with its evidence, a dropout is reported, or the step was skipped for a PR or an issue.

3. **Find the layer.** For an `escaped` bug or a failed PR, name the layer that should have caught it and why it did not, using the table in [references/routes.md](references/routes.md). Run the case again where you can: the proof command that missed it, the lane that passed it.
   Done when: the layer is named with a run or a `file:line`, at certainty level 3 or more.

4. **Synthesize.** For a session, one fresh subagent sorts the three lists into Accepted, Rejected, and Backlog with the criteria in [references/synthesis.md](references/synthesis.md). For a PR or an issue, apply those criteria to the layer yourself. A lesson a check could enforce goes to `add-guardrail`: a check beats a sentence.
   Done when: every finding is in one of the three lists, with its route or its reason.

5. **Ask the user.** Show the three lists through the harness's question tool. The user approves rows, drops them, or changes their route.
   Done when: the user answered for every Accepted row.

6. **Apply the approved rows,** each in its own PR outside any task, by the route routes.md gives it: a check through [add-guardrail](../add-guardrail/SKILL.md), a feature map gap through [create-app-driver](../create-app-driver/SKILL.md) in maintain mode, a verifier miss through [calibration.md](../verify-pr/references/calibration.md) and its replay. A change to a file of this framework, a calibration example included, goes to the framework's own repo, as a PR when you can reach it or an issue with the proposed diff, never as an edit of the installed copy; offer `/test-skill-change` on it before it is kept. Every PR goes through a verdict and `babysit-pr`, as rule 2 of the constitution says. Backlog rows become issues.
   Done when: each approved row has a PR or an issue, linked in the reply, and a verifier change shows its replayed FAIL.

## Reply

The sources read, the layer that failed and why, the approved changes with their PR links, the backlog issues, and the rejected lessons with one reason each.
