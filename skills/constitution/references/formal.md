# Formal checks

A test checks the cases someone thought of. Formal verification checks every case in a stated scope: every order of steps in a model, every input up to a bound, or every input. A formal check is a project-local `prove-<area>` skill that checks one property of named code this way, so every agent that changes that code can check the change against the property.

This file holds the rules every formal check follows, the shape of `prove-<area>`, when a check is stale, and what a task does with a check it touches. `create-formal-verification` writes a check, `maintain-formal-verification` brings one back in line with the code, and a builder whose change alters covered code updates the check in its own run. All three follow the same rules.

## Rules

- **True to the code.** Every part of the model or harness points at code a reviewer can open, with its `file:line`. What the check treats as one atomic step is one atomic step in the code. Names come from the repo.
- **Able to fail.** A check never seen failing proves nothing. After every creation and every update, break the guarded code once on a scratch change, such as a removed check or two reordered steps, and watch the check catch the break. A check that runs on the code runs on the broken code itself: confirm that the source it built holds the break. A model does not read the code: describe the broken code in the model by the same rules as any update, each changed part pointing at the broken code, and watch the model checker report the violation. Then drop the scratch change, in the code and in the model.
- **Updated from the code, not from the result.** Write a change to the model from the code before you rerun the check, never to make a run pass.
- **Findings stay findings.** When the code breaks the property, report the counterexample. Never weaken the property, the model, or a bound until the check passes. Product code changes only when the user asks.
- **A property changes only for a promise that changed on purpose,** with evidence in the change: a doc comment, a test, the changelog, or a commit message. Record the old wording, the new wording, and the evidence.
- **Honest about scope.** State the bounds, the assumptions, and what is left out. A pass covers the model or the bound, not the whole system. A model's pass proves the model; that the model describes the code rests on its `file:line` pointers and on the check not being stale.
- **Readable without the tool.** The property and the harm are one plain sentence each. A counterexample is a short sequence of steps in the code's words. A model of states is drawn as [statechart.md](statechart.md) describes.
- **Cheap to rerun.** One command, a pinned tool version, and a run short enough that an agent runs it on every change to covered code.

## The tool

The question picks the tool, at the lowest cost that answers it. Say which tool you chose and why.

| Question | Tool |
|---|---|
| Can steps happen in a bad order? (retries, locks, sync, a lifecycle) | a model checker over a small model of the design; TLA+ checked by TLC by default, in any language |
| Does the code behave for every input? (memory safety, overflow, a data structure invariant) | a verifier that runs on the code itself |
| No verifier runs on this language | say so, and test the real code with generated inputs, never a hand-written model of the function |
| Must it hold at every size, where a bound is not enough? | a proof |

Prefer a tool the repo's developers can install and run.

## `prove-<area>/SKILL.md`

It lives in `~/.agents/projects/<project>/prove-<area>/`, with the model, the harness, and the scripts it runs beside it. A check the team shares lives in the repo, and that folder holds a route to it, as [target-repo.md](target-repo.md) describes. The skill holds no placeholder, and an agent that reads it cold, mid-change, can act on it.

```markdown
---
name: prove-<area>
description: "Checks that <property, in one sentence> in <area>. Use before you change <covered files>."
---

# Prove <area>

## Property
<the property, one sentence>. Harm when it breaks: <one sentence>.

## Covered code
<each file and function the check describes, each file with its content id, `git rev-parse <commit>:<file>`>. Synced at: <commit>, on <date>.

## Run
<one command>, <tool and pinned version>, about <duration>. <For a private harness built with the code: how it is copied into the worktree under check, run, and removed.> Bounds: <bounds>. Assumptions: <assumptions>. Left out: <what the check does not cover>.

## Read the result
<what a pass means, and how to read a counterexample. Replay each step against the code: a step the code cannot take is a modeling error, so fix the model; a path the code can take is a bug.>

## When your change alters covered code
Update the model from the code before you rerun: every part keeps its `file:line`, and one atomic step in the code stays one step. Never weaken the property, the model, or a bound to make the check pass. Rerun, then break the new code once and watch the check catch it; for a model, describe the break in the model first. The property changes only for a promise that changed on purpose: write the old wording, the new one, and the evidence in the PR's Proof section. Once the model describes the code at a commit, record each covered file's content id at that commit and set Synced at to it; after any later change to covered code, do it again.
```

## Where the harness runs

A model checker reads its model from anywhere, so a model stays in the check's folder. A harness that must be built with the code, such as a property test or a code-level verifier's harness, runs only inside the repo:

- **Private check**: the harness lives in the check's folder. Its Run section takes the worktree under check, the head or a worktree that holds a scratch break, copies the harness into it, runs it there, and removes the copied files. The harness is never committed. Before you trust a run on a break, confirm the worktree holds the break.
- **Shared check**: the harness lives in the repo, where the repo keeps its tests, and Covered code lists it.

## Stale

A check is stale when a covered file's content differs from the content id the check records for it: `git rev-parse <commit>:<file>` prints another id, or fails because the file is gone, renamed, or moved. Content ids do not depend on history, so a squash, a rebase, or a fresh clone that lacks the commit that updated the check leaves it in sync. A stale check can keep passing on code that no longer exists, so its pass proves nothing: report the property as not verified until the model is back in line.

The sync commit and its date say where a maintenance pass starts reading history. When the commit is missing from the clone, start from the date: `git log --since=<date> -- <covered files>`.

Record new content ids only after you confirmed that the model describes the code at that commit. A check that could not be brought back in line keeps its old ids and sync commit.

## In a task

A file a formal check covers, found as [proof.md](proof.md#drivers-and-formal-checks) says, is a hard zone, so a task that touches it is never `low`, and its property is a case ([coverage.md](coverage.md)).

- **In `frame`**, check each such formal check for staleness on the base. A stale one stays stale for the whole task: its case goes under Not verified, and the builder opens an issue for the user to run `/maintain-formal-verification`. The pass itself is not part of the task.
- **In `build`**, when the change alters covered code of a check that was in sync on the base, update the check from the code, by the rules above, and record the content ids at the last commit that changes covered code. A later commit that changes no covered file, such as the one that writes the ids into a shared check, leaves the check in sync. A private check is updated in place; a shared one changes in the PR's diff.
- **In the PR's Proof**, for each updated check: the parts that changed with their `file:line`, the old and new property wording with the evidence when the property changed, the break the updated check caught, and the new sync commit.
- **A check stale on the base** stays under Not verified even when the change alters its covered code; the task does not update it.
- **The verifier judges each check that was in sync on the base** in its `breakage` lane, as [lanes.md](../../verify-pr/references/lanes.md) describes. The builder's own run of the check is evidence, never the verdict.
