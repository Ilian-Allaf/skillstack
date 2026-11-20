---
name: add-guardrail
description: "Makes a repeated mistake impossible: turns it into a check, proven red on the real mistake. Also audits what the code enforces."
disable-model-invocation: true
metadata:
  kind: kit
  produces: "one PR per mistake class, and a row in the repo's rule table"
  hypothesis: "Agents copy the nearest example and take the shortest path that compiles, so a rule written only in prose gets broken again."
---

# Add guardrail

Read [the constitution](../constitution/README.md) first.

Change the repo so the next agent cannot make the same mistake. Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles.

Three modes:

- **a correction** (`/add-guardrail <what went wrong>`): the user just corrected an agent, or `learn-from-mistakes` traced an escaped bug to the code. Run the steps below on that one mistake.
- **history** (`/add-guardrail` with no argument): find the mistake classes in the repo's history, then run the steps on the most frequent ones. A class counts once it happened twice.
- **audit** (`/add-guardrail audit`): measure the foundations of the code, without changing them. Follow [references/audit.md](references/audit.md).

## Steps

1. **Name the class.** State the mistake as a class, not an instance: "a component reads the store directly" rather than "line 40 of `Editor.tsx`". Find every occurrence in the repo, and the past commits, reverts, and review comments where it appeared.
   Done when: the class is one sentence, with its occurrences counted and two real examples cited by commit or `file:line`; in a correction, one real occurrence is enough, or a recreated one when the mistake was caught before it landed.

2. **Pick the highest level that works.** Try each in order, and stop at the first that makes the mistake impossible or loud. See [references/levels.md](references/levels.md).
   Done when: you chose a level, and you wrote why each higher level does not work for this class.

3. **Build the check.** Write it so its error message names the right file, type, or function to use. When the pattern is already common, fail only on new occurrences and keep a list of the existing ones, each with a reason. Run the same command locally and in CI.
   Done when: the check runs in CI, and its error message alone tells an agent what to write instead.

4. **Prove it on the real mistake.** Check out or recreate one real past occurrence and run the check: it must fail with its message. Then run it on the fixed code: it must pass.
   Done when: the PR shows both runs, red on the real mistake and green on the fix (certainty level 4).

5. **Update the rule table.** `docs/agent-rules.md` holds a table pairing each rule with what enforces it; `AGENTS.md` points to it in one line and holds no rules itself. Add the row. When the rule was already in the table with no enforcer, this was a repeat: say so in the PR. Remove rules whose mistake can no longer happen.
   Done when: the table has the row, and no row says "nothing" in its enforcer column without an open issue.

6. **Open the PR.** One PR per class, in [the PR format](../constitution/references/pr-format.md). Judgment calls that no check can hold go to `CODING_STANDARDS.md`, which the verifier's `standards` lane reads.
   Then get a verdict and run `babysit-pr`, as rule 2 of the constitution says.
   Done when: the PR is open with both runs from step 4 as its proof, and carries `ready` or `needs-human`.

## Reply

Each class with its evidence, the level chosen and why a higher level did not work, and the proof runs.
