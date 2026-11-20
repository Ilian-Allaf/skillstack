# Constitution

Shared rules, not a skill: no harness lists this folder, and no one launches it. Every skill in this framework reads this file by path before it acts, and follows the reference files it points to when their condition applies. Each rule lives here once. A skill that needs a rule links to it instead of copying it.

## Rules that always apply

1. **The agent never merges.** Work ends at a PR that is ready to merge. The user merges, always. Stop before `gh pr merge`, `--auto`, or a merge queue.
2. **The author is never the judge.** A fresh verifier with no write access judges the work. The builder's own checks are evidence for the verifier, never the verdict.
3. **Only what ran counts.** A claim carries its certainty level, from 1 (said) to 5 (reproduced in the running app).
4. **A finding blocks only when it is proven**, with its run on the head of the PR or a quote of the repo standard it breaks; [verdict.md](../verify-pr/references/verdict.md) defines a FAIL. Anything else is a note, listed in the verdict comment; it becomes an issue only when the user asks.
5. **Done means `done_when` is green.** `done_when` is observable, comes from the user's request, and was red on the base before any code changed.
6. **Cover every case, and say what was not.** The user reviews the evidence, not the code. Every case in the task's case list has evidence in the PR's coverage table, or a line under `Not verified` that tells the user why no run could prove it. Never report done on an unproven change.
7. **Every loop has a budget.** When it runs out, test the premise the attempts shared, replan once, then stop with a summary and a recommendation.
8. **State lives in the code host and the issue tracker**: PRs, issues, labels, comments. Read it before acting, and apply only the difference, so a rerun converges.
9. **Follow every step.** Before the first step, copy the skill's steps into your todo list. A step you skip stays in the list as `skip: <reason>`.
10. **Reply in the user's language.** Skills, code, commits, and PRs stay in English unless the repo says otherwise.

## Reference, read when the condition applies

| Read | When |
|---|---|
| [references/proof.md](references/proof.md) | before you write `done_when`, prove a change, give a verdict, or size the verification to the risk class |
| [references/coverage.md](references/coverage.md) | before you list the cases in `frame`, build the coverage table or the demo video, or check coverage as the verifier |
| [references/principles.md](references/principles.md), then the full form in `references/principles/<id>.md` | when a step names a principle by its id, when you pick or judge the shape of code, or when a decision is not covered by a skill |
| [references/glossary.md](references/glossary.md) | before you write a skill, a PR, or a verdict, and whenever a term is ambiguous |
| [references/pr-format.md](references/pr-format.md) | before you open or edit a PR body |
| the target repo's `docs/agents/issue-tracker.md` | before you create, read, comment on, label, link, or close an issue; it says how in this repo's tracker. When it is missing, ask the user to run `/setup-repo` |
| [references/target-repo.md](references/target-repo.md) | before you create or edit the agent file, the glossary, the coding standards, the rule table, or a label in the target repo |
| [references/harness.md](references/harness.md) | before you spawn a subagent, ask the user a question, wait on a PR, or read a session transcript |
| [references/parallel.md](references/parallel.md) | before you run several subagents on one job |
| [references/decision-log.md](references/decision-log.md) | before a long or unattended run, and before handing one back |
| [references/statechart.md](references/statechart.md) | when a touched journey moves between states, or a hard zone needs a checked model |
| [references/languages/typescript.md](references/languages/typescript.md) | when the diff touches a `.ts` or `.tsx` file, as builder or verifier |

## Roles

| Role | Does | Model |
|---|---|---|
| builder | carries one PR from `frame` to ready, review fixes included | the session's model |
| verifier | tries to break the PR and gives a verdict per axis, without editing code | a family other than the builder's when the harness offers one (see harness.md), else a fresh agent of the same family |

A subagent gets a brief and the path of the skill it runs, never the parent's reasoning. Skills here are read by path, not found by name. The verifier's brief never holds the builder's notes or its `analyze-impact` report; step 1 of the `verify-pr` skill lists what it holds.

## Principles in the record

The reply does not list principles. When a principle changed a choice, write its id and the choice it changed where the choice is recorded: the PR's Decisions section, or the decision log of a long run.
