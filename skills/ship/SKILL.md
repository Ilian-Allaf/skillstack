---
name: ship
description: "Turns one task into a ready-to-merge PR, proven on the real app and judged by an independent verifier. Stops before the merge."
disable-model-invocation: true
argument-hint: "<task, or an issue number>"
metadata:
  kind: entry
  role: builder
  calls: "investigate, analyze-impact, verify-pr, babysit-pr, repo:drive-<app>"
  consumes: "a task from the user, or an issue"
  produces: "one PR labeled ready, or needs-human"
  budget: "3 build attempts; 2 FAIL verdicts"
  hypothesis: "Without a fixed path, a model declares done on green tests, sets its own bar, and grades its own work."
---

# Ship

Read [the constitution](../constitution/README.md) and [proof.md](../constitution/references/proof.md) first.

You are the builder. Carry this task to a PR the user can assess in two minutes, review fixes included. The merge is the user's.

A question goes to [investigate](../investigate/SKILL.md) instead, which opens no PR. Inside a task you call it and go on: diagnosis for a symptom you cannot reproduce, prototype for a choice a run can settle. A diagnosis with no trigger that fires stops the task, with what would make it reproduce and no PR. Several open decisions are the user's: stop, and propose `/shape-spec`.

The light path: for a `low` task, keep step 1 to the restatement and `done_when`, and keep the proof short.

When the build budget runs out or a second sketch is scrapped, still open the PR as step 6 does, with the summary, labeled `needs-human` (rule 8).

## Steps

1. **Frame.** Restate the task, fix `done_when`, list the cases, and name the risk class, the hard zones, and the playbook, as [references/frame.md](references/frame.md) describes. Try [the verification setup](references/verification.md) and show `done_when` red on the base. Show the frame and go on: launching was the go (rule 11). Claim an issue task first, as the tracker file says.
   Done when: the frame is in your first message, `done_when` ran red on the base, an issue task is claimed, its missing proof is built first, and verification can start or its limits are disclosed.

2. **Build.** In a worktree and a branch of your own, made from the base (see [harness.md](../constitution/references/harness.md)). Design before any logic, as [references/design.md](references/design.md) describes: name the data shape, and for a feature or a change that crosses a function boundary, ground, sketch twice, write the design note, show it when the table there asks, and build against the sketch. Follow the playbook from [the list](references/frame.md#playbooks). The budget is 3 attempts; after the second failure, write the premise your attempts share and test it before the third.
   Done when: `done_when` is green, every playbook duty is met, each altered [formal check](../constitution/references/formal.md#in-a-task) describes the head, and a sketched change has its design note, Deviations filled; or the budget ran out and the PR is open and `needs-human`.

3. **Clean.** Remove slop, then spawn the comment hunter and fix each `MUST KILL` at the root, as [references/clean.md](references/clean.md) describes. A mistake you made twice in this task, and each constraint comment, goes to the user as a candidate for `/add-guardrail`.
   Done when: lint, types, and tests are green, and every `MUST KILL` is fixed or has an issue.

4. **Prove every case.** Script each case and run it on the base and the head through the user's path, with the driver of each touched surface (see proof.md). Fill the coverage table with the best evidence per case. Record the demo and draw the state chart when [coverage.md](../constitution/references/coverage.md) asks for them, and update the feature map file of any journey the change alters.
   Done when: every case has replayable evidence in the table or a line under Not verified, and `done_when` reached the level proof.md requires.

5. **Analyze impact.** For `medium` and `high`, run [analyze-impact](../analyze-impact/SKILL.md) on your diff. Add its catching test to the PR, and any new case it finds to the coverage table. Fix confirmed risks that are in scope; open issues for the others.
   Done when: the safety fact is at level 4 or marked `unproven`, and every confirmed risk is fixed or has an issue.

6. **Open the PR.** [Audit activity and check evidence](references/verification.md), then push and open in [the PR format](../constitution/references/pr-format.md), linking an issue task.
   Done when: the formatted PR is open and the evidence check passes, or discrepancies are attached to a draft labeled `needs-human`.

7. **Get a verdict.** Spawn a fresh verifier (see Roles in the constitution) to run [verify-pr](../verify-pr/SKILL.md) with the brief its step 1 lists, and write the outcome on the PR's Verdict line. On a FAIL, go back to step 2 with its run, or dispute it as verify-pr describes, once per PR. An axis INCONCLUSIVE means `needs-human`, with what would make the lane runnable: for a surface with no driver, `/create-app-driver`. The budget is 2 FAIL verdicts.
   Done when: both axes pass on the current base and head, or the PR is `needs-human`: budget spent, FAIL upheld, or an axis INCONCLUSIVE.

8. **Hand over to babysit-pr.** Run [babysit-pr](../babysit-pr/SKILL.md) on the PR until it is `ready` or `needs-human`. Before handback, [refresh and check evidence](references/verification.md) against the final activity and verdict; unresolved discrepancies mean `needs-human`.
   Done when: the PR carries `ready` or `needs-human`, and the user has the link and a three-line summary: what changed, how it was proven, what was not verified.

## Reply

The PR link, its state, the proof and verdict in one line each, what was not verified, and the decisions made without the user.
