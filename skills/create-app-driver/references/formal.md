# Formal mode

A test checks the cases someone thought of. Formal verification checks every case in a stated scope: every order of steps in a model, or every input up to a bound. This mode finds where that matters most in the target repo, verifies one property there, and writes a project-local skill `prove-<area>` so the next agent can check a change against that property.

Run it after `drive-<app>` exists, when the repo has a hard zone: sync, retries, payments, locking, a protocol, a data structure invariant. Once the skill exists, `analyze-impact` runs its check whenever a change touches a covered file, in the builder's run and in the verifier's `breakage` lane.

## Steps

1. **Choose the target from the code.** A promise the code makes where a break harms users and tests rarely reach the breaking case. Take the strongest target, not the easiest. Ask the user only what the code cannot show.
   Done when: the property and the harm are each one plain sentence, and the target points at real files.
2. **Let the question pick the tool.** "Can steps happen in a bad order?" suits a model checker over a small model of the design: TLA+ by default, drawn and read as [statechart.md](../../constitution/references/statechart.md) describes. "Does this code behave for every input?" suits a verifier that runs on the code. If none runs on this language, say so.
   Done when: the tool is named with the reason, and it runs in one command at a pinned version.
3. **Stay true to the code.** Every part of the model points at code a reviewer can open. One atomic step in the model is one atomic step in the code. Names come from the repo.
   Done when: each model element has a `file:line`.
4. **Show it can fail.** Break the guarded code once on a scratch change (remove a check, reorder two steps) and watch the check catch it. Then drop the scratch change.
   Done when: the check failed on the break and is back to its starting state.
5. **Keep findings as findings.** When the current code breaks the property, report the counterexample as a short sequence of steps in the code's words. Never weaken the property or the model until it passes, and never change product code unless the user asks.
   Done when: every violation is reported, or the run passed under stated bounds.
6. **Write the skill.** `.agents/skills/prove-<area>/SKILL.md`, linked like any skill of the repo, says when a change touches the verified code, how to run the check, how to tell a real bug from a modeling error, the bounds and what is left out, and the files each check covers with the commit at which they were last confirmed. Open it as a PR in the usual format.
   Done when: the PR is open, and a cold reader could run the check from the skill alone.

## Maintain

When covered files changed after the recorded commit, `analyze-impact` reports the model as stale, and the builder opens an issue (the verifier only notes it). The user runs this pass: reread those changes, update the model or the proof, rerun the check, and move the recorded commit forward only once the model matches the code again.
