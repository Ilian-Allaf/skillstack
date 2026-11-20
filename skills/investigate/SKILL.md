---
name: investigate
description: "Answers a question about the code, diagnoses a runtime symptom, or settles a decision with a throwaway prototype. Opens no PR."
disable-model-invocation: true
argument-hint: "<question, symptom, or decision>"
metadata:
  kind: entry
  calls: "repo:drive-<app>"
  consumes: "a question, a runtime symptom or a capture, or a decision to make"
  produces: "a cited answer, a diagnosis, or a decision with its throwaway artifact; a proposed task when a change is due"
  hypothesis: "A model answers from the source it read instead of from what runs, and turns a question into a code change nobody asked for."
---

# Investigate

Read [the constitution](../constitution/README.md) and [proof.md](../constitution/references/proof.md) first.

You answer; you do not change the product. No branch, no commit, no PR. Scratch work lives outside the source tree. When the answer calls for a change, you propose it as a task and the user decides whether to launch it.

## Steps

1. **Restate and pick the mode.** Say the question back in your own words, and pick one mode:

   | The user brings | Mode |
   |---|---|
   | a question about the code: how, why, or which option | [question](references/question.md) |
   | a runtime symptom with an unknown cause, or a capture | [diagnosis](references/diagnosis.md) |
   | a decision a quick experiment can settle | [prototype](references/prototype.md) |

   A request to change behavior is a task for `ship`: say so and stop. Nothing here changes the product, so no go is needed before you start.
   Done when: the user has the restated question, the mode, and what the answer will look like.

2. **Gather the evidence.** Meet the duties of the mode's file. Prefer a run to a reading: when a claim can be checked by running something, run it and keep the command.
   Done when: every duty of the mode is met, or skipped with its reason.

3. **Grade every claim.** Give each claim its certainty level from proof.md. A claim at level 4 or 5 shows its command and output; an inference is marked as one.
   Done when: every claim in the draft answer carries a level, and the claims the answer rests on reached level 3 or more, or are named as open.

4. **Answer.** In the shape the mode's file gives. Say what the evidence does not answer.
   Done when: every part of the question restated in step 1 is answered, or named as open with what would answer it.

5. **Propose the change, if one is due.** Write it as a task the user can launch with `/ship`: the goal, the `done_when` the evidence suggests, the playbook, and the evidence to reuse. Launch nothing yourself.
   Done when: the user has the proposed task, or the reply says no change is needed.

## Reply

The mode, the answer with each claim's level, the evidence paths and commands, what stays open, the scratch path, and the proposed task.
