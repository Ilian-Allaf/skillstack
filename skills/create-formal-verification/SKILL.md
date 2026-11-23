---
name: create-formal-verification
description: "Proves one property of the code where a bug costs the most and tests reach the least, over every case in a stated scope, and writes the check the next agent runs on every change to that code."
disable-model-invocation: true
argument-hint: "<an area or a property, or nothing to let the code choose>"
metadata:
  kind: kit
  consumes: "the repo, and an area or a property when the user names one"
  produces: "repo:prove-<area> skill, in the project folder or in one PR when shared; each counterexample found, in the code's words"
  hypothesis: "Tests check the orders of steps someone thought of; the race, the retry, or the lock that expires mid-write is the order nobody wrote, and it ships."
---

# Create formal verification

Read [the constitution](../constitution/README.md) and [formal.md](../constitution/references/formal.md) first. The rules in formal.md hold at every step.

Find the part of the repo where a broken promise harms users and tests rarely reach the case that breaks it, check one property of it in every case within a stated scope, and leave a `prove-<area>` skill so the next agent can check a change against that property. The user must be able to trust the result and act on it without learning the tool.

## Steps

1. **Choose the target from the code.** Start where the user pointed, if they named an area, a bug, or a property. Otherwise look in the hard zones of [proof.md](../constitution/references/proof.md) and the data structure invariants. Take the strongest target, not the easiest to check. Ask the user only what the code cannot show.
   Done when: the property and the harm are each one plain sentence, and the target points at real files and functions.

2. **Pick the tool.** Use the table in formal.md. Install it at a pinned version.
   Done when: the tool is named with the reason, and one command runs it.

3. **Write the model or the harness.** Keep it true to the code, with the repo's names.
   Done when: each part of the model has its `file:line`, and each atomic step of the model is one atomic step in the code.

4. **Run it on the current code.** For each counterexample, replay every step against the code. A step the code cannot take is a modeling error: fix the model and say what was wrong. A path the code can take is a finding: keep the property, and tell the path as steps in the code's words.
   Done when: the check passes under stated bounds, or every violation is a finding replayed against the code.

5. **Show it can fail.** Break the guarded code once on a scratch change, watch the check catch it, then drop the change.
   Done when: the check failed on the break, and it is back where it started: passing, or failing only on the findings of step 4.

6. **Write `prove-<area>`.** Write `~/.agents/projects/<project>/prove-<area>/SKILL.md`, with the model, the harness, and its scripts in that folder, as formal.md describes. When the user shares it, write it in the repo at `.agents/skills/prove-<area>/` instead, with the links and the route [target-repo.md](../constitution/references/target-repo.md) asks for. Use the shape in formal.md, with this repo's real commands, paths, and names. Set Synced at to the commit you checked.
   Done when: the skill holds no placeholder, every command in it ran once, and it lists every file and function the check covers.

7. **Follow it cold.** Spawn a fresh subagent, as [harness.md](../constitution/references/harness.md) describes, with only the path of `prove-<area>` and a scratch change that breaks the property in the real code. It follows the skill and reports what the check said. When the subagent misses the break or a step does not run, fix the skill or the model, never the scratch change, and run this step again.
   Done when: the subagent caught the break from the skill alone, the scratch change is dropped, and the check is back where step 5 left it.

8. **Hand it over.** A private check is done once step 7 passed. A shared one goes in a PR in [the PR format](../constitution/references/pr-format.md), which also runs the check in the repo's CI, so a change made without an agent is checked too: its Proof holds the runs of steps 4, 5, and 7. Then get a verdict and run `babysit-pr`, as rule 2 of the constitution says. A finding stays out of product code unless the user asks; to fix it, the user runs `/ship` with the counterexample.
   Done when: the private check's path is reported with its runs; or the PR is open with its runs, and carries `ready` or `needs-human`.

## Reply

- what you checked: the property and the harm, one sentence each;
- the tool and why, the bounds and the assumptions;
- what the check found: each counterexample as steps in the code's words, or the pass and its scope;
- how to run it, and where `prove-<area>` lives;
- what it does not cover;
- a second target, only if you found a close one.

When code it covers changes without the check, through a merge, a refactor, or an edit made without `prove-<area>`, `/maintain-formal-verification` brings it back in line.
