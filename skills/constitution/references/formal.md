# Formal checks

A test checks the cases someone thought of. Formal verification checks every case in a stated scope: every order of steps in a model, every input up to a bound, or every input. A formal check is a project-local `prove-<area>` skill that checks one property of named code this way, so every agent that changes that code can check the change against the property.

This file holds the rules every formal check follows, the shape of `prove-<area>`, and when a check is stale. `create-formal-verification` writes a check, `maintain-formal-verification` brings one back in line with the code, and a builder whose change alters covered code updates the check in its own run. All three follow the same rules.

## Rules

- **True to the code.** Every part of the model or harness points at code a reviewer can open, with its `file:line`. What the check treats as one atomic step is one atomic step in the code. Names come from the repo.
- **Able to fail.** A check never seen failing proves nothing. After every creation and every update, break the guarded code once on a scratch change, such as a removed check or two reordered steps, and watch the check catch it. Then drop the scratch change.
- **Updated from the code, not from the result.** Write a change to the model from the code before you rerun the check, never to make a run pass.
- **Findings stay findings.** When the code breaks the property, report the counterexample. Never weaken the property, the model, or a bound until the check passes. Product code changes only when the user asks.
- **A property changes only for a promise that changed on purpose,** with evidence in the change: a doc comment, a test, the changelog, or a commit message. Record the old wording, the new wording, and the evidence.
- **Honest about scope.** State the bounds, the assumptions, and what is left out. A pass covers the model or the bound, not the whole system.
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

It lives where [target-repo.md](target-repo.md) puts `prove-<area>/`: in the project folder, or in the repo when the user shares it. It holds no placeholder, and an agent that reads it cold, mid-change, can act on it.

```markdown
---
name: prove-<area>
description: "Checks that <property, in one sentence> in <area>. Use before you change <covered files>."
---

# Prove <area>

## Property
<the property, one sentence>. Harm when it breaks: <one sentence>.

## Covered code
<each file and function the check describes>. Synced at: <commit>.

## Run
<one command>, <tool and pinned version>, about <duration>. Bounds: <bounds>. Assumptions: <assumptions>. Left out: <what the check does not cover>.

## Read the result
<what a pass means, and how to read a counterexample. Replay each step against the code: a step the code cannot take is a modeling error, so fix the model; a path the code can take is a bug.>

## When your change alters covered code
Update the model from the code before you rerun: every part keeps its `file:line`, and one atomic step in the code stays one step. Never weaken the property, the model, or a bound to make the check pass. Rerun, then break the new code once and watch the check catch it. The property changes only for a promise that changed on purpose: write the old wording, the new one, and the evidence in the PR's Proof section. Move Synced at to the new commit only once the model describes the code at that commit.
```

## Stale

A check is stale when a covered file changed after its sync commit: `git log <sync commit>..HEAD -- <covered files>` lists a commit. A stale check can keep passing on code that no longer exists, so its pass proves nothing: report the property as not verified until the model is back in line.

Move the sync commit forward only after you confirmed that the model describes the code at the new commit. A check that could not be brought back in line keeps its old sync commit.
