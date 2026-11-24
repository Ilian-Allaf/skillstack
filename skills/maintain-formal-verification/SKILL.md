---
name: maintain-formal-verification
description: "Brings each formal check back in line with the code after changes that skipped it, reruns it, and says for each failure whether the check drifted or the code has a bug."
disable-model-invocation: true
argument-hint: "<a prove-<area> skill, or nothing for every check>"
metadata:
  kind: kit
  consumes: "the repo's prove-<area> skills and the commits since each sync commit"
  produces: "one outcome per check (in sync, updated, bug, blocked); the updated prove-<area>, in place or in one PR when shared; each bug with its counterexample"
  hypothesis: "A check that still describes code that is gone keeps passing, and a stale pass reads like a proof."
---

# Maintain formal verification

Read [the constitution](../constitution/README.md) and [formal.md](../constitution/references/formal.md) first. The rules in formal.md hold at every step.

A builder that changes covered code updates the check in its own run. This pass catches the changes that skipped the check: merges, refactors, edits made without it. It runs after them, on a stale-check issue, or for a task whose base has a stale check.

Edit only the verification: models, harnesses, property files, and `prove-<area>` itself. Product code changes only when the user asks.

## Outcomes

Give each check one outcome, or both `updated` and `bug`:

| Outcome | Means |
|---|---|
| `in sync` | nothing since the sync commit alters what the check describes, and it passes |
| `updated` | the check now describes the changed code, and it passes |
| `bug` | the check describes the current code, and the code breaks the property |
| `blocked` | the check could not be brought back in line, or could not run; say why |

## Steps

1. **Find the checks.** Read each `~/.agents/projects/<project>/prove-*/SKILL.md`, following routes into the repo, or the one the user named, and any verifier the repo already runs against named code. Collect each check's property, covered code, bounds and assumptions, command, and sync commit. Without a recorded sync commit, use the last commit changing the verification files, and say so. With no check at all, stop and point at `/create-formal-verification`.
   Done when: every check has these five facts, or you stopped.

2. **Run each check as it is,** before any edit. A pass only says the old description holds; judge no failure yet.
   Done when: each check has its recorded result.

3. **Read every change to covered code** since the sync commit, with its commit message. Follow renamed, split, or moved code, and new code writing the guarded state. Sort each change against the model, not the message:
   - **no effect**: formatting, comments, or paths the check does not describe;
   - **the model no longer describes the code**: a step split, a check moved, a new path reaches the guarded state;
   - **the promise changed on purpose**, with the evidence formal.md asks;
   - **the promise may be broken**: the code changed and nothing says the promise did.
   Done when: every commit since the sync commit sits in one group, and each promise changed on purpose cites its evidence.

4. **Update from the code.** Change the model or the harness so each changed part points at code again, before you rerun. Change a property only for a promise changed on purpose; keep the bounds unless the change makes them wrong.
   Done when: every changed part has its `file:line`; each property change has its old wording, new wording, and evidence; each reduced bound is listed.

5. **Rerun and judge.** On a pass, break the new code once and watch the check catch it, as formal.md says, then drop the break. On a failure, replay the counterexample on the code. A step the code cannot take means the check is wrong: fix it and say what was wrong. A path the code can take is a bug: find the commit that introduced it, and tell the path in the code's words with its harm. A cheap repro is evidence, never product code.
   Done when: each check has its outcome, with its run and, for a pass, the break it caught.

6. **Update `prove-<area>`:** covered code with its content ids, command, bounds, assumptions, and the sync commit you checked; a `blocked` check keeps its old ones. Then follow it once as the next agent would.
   Done when: the skill describes the check as it now is, and its own command ran from it.

7. **Hand it over.** A private check is updated in place. A shared one goes in one PR in [the PR format](../constitution/references/pr-format.md), holding only verification changes, through a verdict and `babysit-pr` (rule 2), which a task runs once over its stack. Each bug becomes an issue with its counterexample, harm, and introducing commit; the user fixes it through `/ship`. Close or link the issue that asked for this pass.
   Done when: every check has its outcome reported, each bug has its issue, and the verification changes are in place or in an open PR labeled `ready` or `needs-human`.

## Reply

For each check: the outcome and the commits you read; each change to the verification and why, with its evidence; the rerun and the break it caught; each bug as steps in the code's words, with its harm and introducing commit; what the check still does not cover. Say which failures were drift in the check and which were bugs in the code. When a check passed before the update and fails after, say the old pass was on a stale description.
