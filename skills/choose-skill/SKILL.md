---
name: choose-skill
description: "Tells you which skill to launch for your situation, and with what command. Launches nothing."
disable-model-invocation: true
argument-hint: "<what you want to do, in your own words>"
metadata:
  kind: entry
  consumes: "the user's situation, in their words"
  produces: "one command for the user to type"
  hypothesis: "With many skills to launch by hand, the user reaches for the wrong one, or for none."
---

# Choose skill

Read [the constitution](../constitution/README.md) first.

You are the index of this framework, so the user only has to remember you. You point; the user launches.

## Steps

1. **Restate the situation.** Say in one sentence what the user wants, and what they already have: a repo, a bug, an idea, a PR, a question.
   Done when: the user can tell from your sentence whether you understood.

2. **Match it to one row.** Use the table below. When two rows fit, ask the one question that separates them, with your recommendation. When none fits, say so and name the closest row.
   Done when: one row is chosen, or the user has your question.

3. **Give the command.** The command to type, filled in with the user's words, and in one line why this skill and what it will ask of them. Launch nothing.
   Done when: the user has one command ready to type.

## The table

| The situation | Command |
|---|---|
| the first time the framework works in this repo | `/setup-repo` |
| a bug you can reproduce, a missing feature, a refactoring, a slow path, a metric to push to a target, a UI migration, a change across many files | `/ship <the task, or an issue number>` |
| several independent tasks to turn into PRs while you do something else | `/ship-queue <the tasks, one per line>` |
| an idea with open decisions, or work too big for one session | `/shape-spec <the idea>` |
| a question about the code, a symptom you cannot reproduce, or a choice an experiment can settle | `/investigate <the question>` |
| you must stop now, or the session is about to end, and want to resume later | `/pause-task` |
| a task an earlier session left mid-way | `/resume-task <branch or PR, or nothing for the last paused task>` |
| you were away: what changed, and what waits on you | `/catch-me-up`, or `/catch-me-up video` for a short video |
| an open PR stuck on conflicts, review comments, or CI | `/babysit-pr <PR number>` |
| an independent check of a PR, yours or anyone's | `/verify-pr <PR number>`, in a fresh session |
| what a change could break before you merge it | `/analyze-impact <PR number or diff>` |
| an agent made the same mistake twice | `/add-guardrail <the mistake>` |
| what the code already enforces, before agents work on it at scale | `/add-guardrail audit` |
| the app changed and the agent drives it the old way | `/create-app-driver`, maintain mode |
| you changed a skill and want to know whether it helps before you keep it | `/test-skill-change <the skill and the change>` |
| you are about to send a prompt and want it aimed deeper | `/sharpen-prompt <your prompt>` |
| the last reply was too dense to act on | `/say-it-plainly` |
| a bug got past the checks, or a session went badly | `/learn-from-mistakes <issue, PR, or nothing for this session>` |

## Reply

Your sentence, the command, and why, in three lines.
