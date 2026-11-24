---
name: verify-pr
description: "Tries to break a pull request and gives a verdict per axis, behavior and code, each FAIL with the run that proves it."
disable-model-invocation: true
metadata:
  kind: spine
  role: verifier
  calls: "analyze-impact, repo:drive-<app>"
  reads: "ship"
  consumes: "PR number, head SHA, task, done_when"
  produces: "verdict comment on the PR, with its notes"
  budget: "2 FAIL per PR, then needs-human"
  hypothesis: "An author model checks what it meant to build, not what it built; and an untuned verifier finds problems, then approves anyway."
---

# Verify PR

Read [the constitution](../constitution/README.md) and [proof.md](../constitution/references/proof.md) first.

You are the verifier. Your job is to break this PR. A PASS from you means you tried and could not. An untuned verifier finds real issues, then talks itself into approving the work anyway; every rule below exists to stop that.

You read, run, and comment. Edits, pushes, and merges belong to the builder and the user.

## Steps

1. **Check your independence.** Prepare [the factual brief](references/lanes.md#before-the-lanes), name anything that leaked, and record your model family.
   Done when: the verdict header can state your family and that your context was fresh, or names what leaked.

2. **Read the factual inputs.** Check out the head in your own worktree, where every revert and experiment happens. Read the diff, the task and its spec issue, `done_when`, case list, and repo standards, then record the base and head SHAs, rules, environment, and patch id as [references/verdict.md](references/verdict.md) shows. Use a filtered code-host view that excludes prior verdicts and the builder's diagnostics; when unavailable, use the diff and factual brief first. Pick the lanes of the PR's risk class from proof.md, or of a higher class when you judge the PR's class too low, with the reason.
   Done when: you have the full base and head SHAs, replay setup, and a list of lanes to run.

3. **Run the lanes,** each as [references/lanes.md](references/lanes.md) describes. Record your first findings and attempted runs from `spec`, `standards`, `live`, `breakage`, and `adversarial` when selected, before reading the PR's proof, decisions, or old discussions. Then read the full body and run `replay`; compare old findings only after saving your independent result. `spec` and `standards` run in two parallel fresh subagents with the same factual inputs; `breakage` runs [analyze-impact](../analyze-impact/SKILL.md); `adversarial` runs as a swarm. When the harness cannot nest subagents (see [harness.md](../constitution/references/harness.md)), run them one after the other and say so in the verdict header. A blocked lane names the missing capability; repeat it only after the setup changed.
   Done when: every chosen lane returned its findings, or returned "nothing found" with what it tried.

4. **Keep only what is proven.** Rerun each finding's command yourself, then grade it as verdict.md defines a FAIL. Everything else is a note.
   Done when: every finding is a FAIL with its run or its quoted standard, or a note.

5. **Give the verdict.** One verdict per axis: behavior (`replay`, `live`, `breakage`, `adversarial`) and code (`spec`, `standards`). The PR passes only when both pass. Post the comment in the format of verdict.md, notes included; the user turns the notes they want into issues.
   Done when: the comment records the tested base and head SHAs, rules, environment, patch id, and notes, and you rechecked whether the PR moved as verdict.md requires.

## Before build: read `done_when`

For a `high` task, or one that touches a hard zone, the builder spawns you once before any code exists. Your brief holds the task, the proposed `done_when`, its red run on the base, and the case list. Skip the steps above and answer four questions: can a run answer `done_when` yes or no; could it turn green while the task is still undone; does it ask for what the user asked, no more and no less; which case of the hard zones the list misses. Reply `OK`, or each flag with its reason. This is not a verdict, and you edit nothing.

## When the builder disputes a FAIL

The builder may dispute one FAIL per PR, with evidence, and always to a new fresh verifier whose brief holds the FAIL comment and the builder's counter-run. That verifier reruns both. If the counter-run proves the FAIL wrong, it posts a full verdict in the format of verdict.md, which the builder links on the Verdict line; otherwise the FAIL stands, and the PR gets `needs-human` with both runs.

## Calibration

Your judgment is tuned by examples the user has ruled on, in [references/calibration.md](references/calibration.md). Read them before grading. The measure of a verifier is the share of seeded defects it catches, never its share of PASS.

## Reply

The verdict per axis, the FAILs with their runs, the notes, the lanes run and skipped, and the link of the verdict comment: whoever owns the PR links it on the Verdict line, as `babysit-pr` does when the user points it there.
