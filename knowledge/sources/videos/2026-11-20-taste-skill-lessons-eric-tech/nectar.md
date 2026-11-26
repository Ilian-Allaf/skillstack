# Nectar — 8 Taste Skill Lessons

Dated analysis, 2026-11-25. Source: [Eric Tech, condensing Leon Lin](SOURCE.md); [transcript](transcript.md); [timestamped notes](notes.md).

## The idea in one line

Taste comes less from the wording of a prompt than from three inputs the agent cannot invent: **a target to match** (references, then a chosen mockup), **a bar it is told it has not reached**, and **a judge that did not build it**. Cook's tagline says it: a target, a bar, and time.

## Corroboration

The Anthropic [harness design article](../../articles/2026-03-24-harness-design-long-running-apps/content.md), an independent source, reached two of the same lessons on frontend design: generation and grading separated (lesson 8), and criteria that penalize generic "AI slop" patterns (lesson 5). It adds what the video lacks: "Is this design beautiful?" is hard to grade consistently, but "does this follow our principles for good design?" is gradable; the evaluator was calibrated with few-shot examples, and it drove the live page with Playwright instead of scoring a screenshot. It also warns that the wording of the criteria steers the output ("museum quality" made designs converge) and that the last iteration was not always the best.

The other claims rest on one practitioner's demos, reported through a second person.

## The lessons against the framework

Our reading, as of 2026-11-25. "Covered" names the file that already does it; nothing here is adopted.

| Lesson | Already in the framework | What is missing |
|---|---|---|
| 1. References carry the quality | `investigate` prototype mode, duty 2: gather references when the design space is open | References are not a durable input: the spec does not hold them, and neither the builder nor the verifier receives them |
| 2. Make the target first | Prototype mode: variants behind one switch, each screenshotted; `shape-spec` sends a question of look or feel to a prototype the user picks from | The picked variant ends as a decision in prose. It does not become the target the build is checked against; no phone width is required |
| 3. A number to hit | `done_when` must be observable and red on the base; `hillclimb` pairs a target with an attempt floor | A self-reported "99% match" is a level 1 claim. Only a measured number fits ADR 0004: an image diff against the target, a count of breaches |
| 4. Give it time | Attempt budgets and the hillclimb attempt floor keep a run from stopping at "it works" | A minimum duration is not adopted: it spends usage without proof that it helps, and the token budget is tight |
| 5. Ban the slop | `clean` step 1 removes code slop | No list of UI defaults to avoid. A list in a prompt only stops what it names; a detector is the `add-guardrail` form of the same lesson |
| 6. Build in steps | `feature` builds one vertical slice at a time | Nothing says layout before motion, or motion from reference videos analyzed frame by frame |
| 7. Specific feedback | `shape-spec` grills until decisions are explicit; the glossary carries the user's words | No design vocabulary: when the user cannot name what is wrong, the agent's description of what it built would give the words |
| 8. Another judge | ADR 0003: the verifier is fresh, from another family when available | No lane judges how the UI looks: `live` checks that journeys work, `standards` reads code, `visual-parity` checks exact sameness only |

## Where the source conflicts with our decisions

- **A judge's score as the bar** ("don't stop before 9.2 out of 10"). A score from a model is a claim, not a run, so under [ADR 0004](../../../../docs/adr/0004-a-finding-blocks-only-when-proven.md) it can only be a note. The Anthropic article points to the reconciliation: grade against written criteria. A breach of a documented design standard, quoted with the rule and a screenshot, can block; a taste score cannot.
- **A folder inside the project** (Cook writes its brief and rounds there). [ADR 0016](../../../../docs/adr/0016-the-working-files-live-outside-the-repo.md) keeps working files outside the repo.
- **A designer role.** [SCOPE.md](../../../../SCOPE.md) puts personas out of scope; the gap is a kind of evidence and a review question, not a role.
- **Long unattended runs** are compatible with [ADR 0014](../../../../docs/adr/0014-a-launched-task-runs-to-a-ready-pr.md) only when the user launched them, and stop at a PR.

## Questions for later work

Research questions, not adopted changes:

- Can the user's pick in a look-or-feel prototype become a target the spec holds (screens at desktop and phone width), so `frame` makes it a case and `live` compares the head with it?
- Where does a UI slop list live so that a breach is a documented standard: a principle with a "Sign it was skipped", or a project file next to `coding-standards.md` that `setup-repo` seeds and `learn-from-mistakes` extends?
- Is a look-and-feel review a check inside `live` (it already drives the app and takes screenshots), or a lane of its own?
- Does a target-matching loop fit `hillclimb` with a measured metric, or does it need a playbook of its own?
- Does a design with references and a target, judged against criteria, beat the same task without them, in a blind `test-skill-change` run? That is the proof the video does not give.
- What do the primary sources say? Cook and the Taste Skill are now imported ([cook](../../repos/leonxlnx-cook/SOURCE.md), [taste-skill](../../repos/leonxlnx-taste-skill/SOURCE.md)); Lin's article and the Impeccable detector are not.
