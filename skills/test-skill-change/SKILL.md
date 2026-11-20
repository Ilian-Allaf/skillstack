---
name: test-skill-change
description: "Tests blind whether a change to a skill makes the agent work better, by running the old and the new skill on the same task and judging both. Applies nothing."
disable-model-invocation: true
argument-hint: "<the skill, and the change: a diff, a branch, or a PR>"
metadata:
  kind: meta
  consumes: "a skill and a change to it"
  produces: "a verdict on the change, with each run's output and a recommendation"
  hypothesis: "A skill edit written after one bad session overfits that session, and an agent that knows it is tested behaves differently."
---

# Test skill change

Read [the constitution](../constitution/README.md) first.

You run an experiment, not a review. The same task goes to agents with the old skill and with the new one; a judge scores both without knowing which is which; you read everything and recommend. You apply nothing: the change ships through its own PR, or not.

Every run spends the user's quota. Say the number of runs and their rough cost in your first message.

## Steps

1. **Frame.** Name the variant under test, the behavior that counts as success, and the task that exercises it: one a user would really give. Write 3 to 6 criteria the judge scores; the agents never see them. Pick the number of runs per variant, two by default, all on the session's model (see [harness.md](../constitution/references/harness.md)).
   Done when: the variant, the task, the criteria, and the run count are written.

2. **Blind the setup.** One working copy per run, each in its own directory with a name a user might pick, holding the project and the skill version of its variant. No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, or `candidate` in any path, file, or prompt an agent sees.
   Done when: each run has its own copy, and a search for those words in the copies finds nothing.

3. **Write one prompt** that reads like a real request: the goal, never what is measured. Do not ask the agent to list the skills, principles, or files it used.
   Done when: the same prompt is ready for every run.

4. **Run.** Spawn one fresh subagent per run, at the same moment, each in its own copy, with the same prompt. No agent knows the others exist.
   Done when: every run finished, or its dropout is noted.

5. **Judge blind.** Spawn one fresh subagent as the judge. It gets the criteria and every output under a neutral label, never the variant, and scores all of them in one pass on one scale.
   Done when: the judge scored every output on every criterion.

6. **Check what each agent did, not what it said.** When the harness keeps transcripts, read which files each run opened and which steps it took. Otherwise judge from the shape of its output. A skill that was never read did not help.
   Done when: for each run, you know whether it read and followed the skill under test.

7. **Read every output yourself** and compare with the judge. A disagreement means a biased judge or a vague criterion: read both before you decide.
   Done when: you have a verdict: better, worse, no difference, or inconclusive, with its reason.

## Reply

The variant, the criteria, one line per run, the judge's scores, your verdict and why, and a recommendation: keep the change, revise it in a named way, or drop it. Two runs per variant show a direction, not a proof; say so.
