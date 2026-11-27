<img src="assets/icon.svg" width="64" height="64" alt="">

# Skillstack

Agent skills that turn a task into a pull request you can merge without worry: proven on the real app, checked for what it breaks elsewhere, and judged by a verifier that did not write it. You launch every task, and you merge every PR.

> **Status: v0.** Every skill is written and checked by the linters, and none has run on a real repo yet. Proving them on a testbed comes first ([#4](https://github.com/Ilian-Allaf/skillstack/issues/4)).

## Why these skills exist

Coding agents fail the same ways, again and again. Each skill answers one of them.

- **The agent declares done on green tests.** `ship` shows you its `done_when`, sees it fail on the base before any code, and proves it on the running app. Each journey and promise of your spec becomes a case, proven at the highest level its kind allows.
- **The change breaks something outside its diff.** `analyze-impact` finds the one fact the change is safe because of, and proves it by a run.
- **The author grades its own work.** `verify-pr` is a fresh agent, from another model family when one is available, that tries to break the PR. A finding blocks only with the run that proves it.
- **The same mistake comes back.** `add-guardrail` turns it into a check, red on the real mistake. `learn-from-mistakes` finds which layer let a bug through, and proposes the fix.
- **The agent cannot drive your app.** `create-app-driver` writes a skill that launches, drives, and observes it the way a user does. A task on a surface with no driver builds it first, and repairs a stale formal check the same way, instead of leaving the case unproven.

The choices behind them are recorded as decisions in [`docs/adr/`](docs/adr/).

## Install

Pick one route per harness: installing both gives you every skill twice.

**As a plugin**, which updates itself. In Claude Code 2.1.275 or later:

```text
/plugin install skillstack --marketplace Ilian-Allaf/skillstack
```

The skills then answer to `/skillstack:<skill>`. Codex and Copilot read the same marketplace file, `.claude-plugin/marketplace.json`; their install has not been tried yet. The repo is private, so the harness needs your GitHub access.

**From a clone**, to edit the skills as you use them:

```bash
git clone https://github.com/Ilian-Allaf/skillstack.git
cd skillstack
python -I tools/link_skills.py
```

It links every skill into `~/.agents/skills` (Codex and most other harnesses) and `~/.claude/skills` (Claude Code). The links point into the clone, so a `git pull` updates the skills, and they follow the branch you have checked out. `--dry-run` shows what would change; `--unlink` removes the links.

Skills install as whole folders beside [the constitution](skills/constitution/README.md), which they read by relative path. An installer that copies skills one at a time drops it, so it is not supported ([ADR 0005](docs/adr/0005-the-constitution-is-a-folder-not-a-skill.md)).

## Getting started

1. Run `/setup-repo` once per repo, best before the first task. It sets up the issue tracker, the labels, the glossary, the coding standards, and the app driver, and asks before each part. Each file stays private, in `~/.agents/projects/<repo>/` on your machine, unless you share it with the team in the repo ([ADR 0016](docs/adr/0016-the-working-files-live-outside-the-repo.md)).
   Skipped, the skills still work: issues go to a private markdown tracker in the project folder, and a PR's state is the State line of its body, until you pick a tracker and labels the team sees ([ADR 0023](docs/adr/0023-the-framework-works-before-setup-repo.md)). The merge guard is the one part with no default.
2. Run `/ship <task>` for each task. It shows you its frame and runs to a PR in state `ready`, stopping only for what is yours to decide. You merge.
3. Not sure which skill fits? Run `/choose-skill` and describe your situation.

Every skill on one page, the path of one task, and the loops inside `ship`, in diagrams: [`skills/GRAPH.md`](skills/GRAPH.md). How to write a prompt, prompts to copy, and the mistakes that cost the most: [`docs/guide.md`](docs/guide.md).

## Steer with principle names

Every skill applies the same principles, each with an id that says what it does: `design-the-data-first`, `validate-at-the-boundary`, `subtract-before-you-add`. The agent has read the full rule behind each id, so naming one redirects it more precisely than a paragraph of instructions:

```text
subtract-before-you-add: delete the obsolete adapters first, then design what is left.
prove-it-works: run the real import and show me the written rows, not the test output.
design-it-twice: show me a second shape before you pick this one.
```

The agent says which principle changed which choice, under Decisions in the PR. The list, one line each: [`principles.md`](skills/constitution/references/principles.md).

## Reference

Every skill is launched by you; none is picked by the model on its own. Each one reads [the constitution](skills/constitution/README.md) first: the shared rules on proof, coverage, the glossary, and the PR format.

**You launch**

- **[choose-skill](skills/choose-skill/SKILL.md)**: Tells you which skill to launch for your situation, and with what command.
- **[setup-repo](skills/setup-repo/SKILL.md)**: Prepares a repo the first time you work in it, asking before each part, and keeps each file private or shares it with the team.
- **[shape-spec](skills/shape-spec/SKILL.md)**: Turns a loose idea into a spec issue through an interview, or into a map of decisions when the work is too big for one session.
- **[shape-architecture](skills/shape-architecture/SKILL.md)**: Puts the architecture choices of a spec to you, two real shapes at a time, and records the ones you make before the build. Optional: without it, `ship` picks the shape itself.
- **[investigate](skills/investigate/SKILL.md)**: Answers a question about the code, diagnoses a runtime symptom, or settles a decision with a throwaway prototype. Opens no PR.
- **[ship](skills/ship/SKILL.md)**: Turns one task into a ready-to-merge PR, with verification tried before the build and evidence checked against recorded activity.
- **[ship-queue](skills/ship-queue/SKILL.md)**: Turns a list of tasks into as many ready-to-merge PRs, one owner per task, each with its own verifier; tasks that touch the same files are stacked. Stops before every merge.
- **[pause-task](skills/pause-task/SKILL.md)**: Stops the running task at a safe point and leaves a resume note, so a fresh session picks it up with nothing lost.
- **[resume-task](skills/resume-task/SKILL.md)**: Picks up a task an earlier session left mid-way, and carries it on without redoing what was done.
- **[recall-context](skills/recall-context/SKILL.md)**: Rebuilds where things stand on a topic from your past sessions and the repo's record, before you start or resume work.
- **[catch-me-up](skills/catch-me-up/SKILL.md)**: Tells you what changed while you were away, with the screenshots and videos the work produced, and every call waiting on you.
- **[clean-worktrees](skills/clean-worktrees/SKILL.md)**: Frees disk by removing the worktrees of finished or abandoned tasks, and never loses uncommitted work.
- **[create-app-driver](skills/create-app-driver/SKILL.md)**: Writes the repo's driver, a skill that launches, drives, and observes the app like a user, with its feature map.
- **[create-formal-verification](skills/create-formal-verification/SKILL.md)**: Proves one property of the code where a bug costs the most and tests reach the least, over every case in a stated scope, and writes the check the next agent runs on every change to that code.
- **[maintain-formal-verification](skills/maintain-formal-verification/SKILL.md)**: Brings each formal check back in line with the code after changes that skipped it, and says for each failure whether the check drifted or the code has a bug.
- **[add-guardrail](skills/add-guardrail/SKILL.md)**: Makes a repeated mistake impossible: turns it into a check, proven red on the real mistake.
- **[learn-from-mistakes](skills/learn-from-mistakes/SKILL.md)**: Reconstructs a session from recorded activity, or studies a failed PR or escaped bug, and proposes fixes to the layer that missed it.
- **[test-skill-change](skills/test-skill-change/SKILL.md)**: Tests blind whether a change to a skill makes the agent work better, old and new on the same task. Applies nothing.
- **[sharpen-prompt](skills/sharpen-prompt/SKILL.md)**: Rewrites a prompt you are about to send so it asks for deeper work, not more work.
- **[say-it-plainly](skills/say-it-plainly/SKILL.md)**: Says the agent's last reply again in plain words, shorter, with no jargon.

- **[show-me](skills/show-me/SKILL.md)**: Shows you the current topic visually, with the smallest diagram, tree, or diff that makes the key point clear.

**Inside a task** (every PR a skill opens goes through `verify-pr` and `babysit-pr`, and `ship` runs `analyze-impact` for `medium` and `high`; you can also launch them on an open PR)

- **[analyze-impact](skills/analyze-impact/SKILL.md)**: Finds what a change breaks outside its diff, and proves by a run the one fact it is safe because of.
- **[verify-pr](skills/verify-pr/SKILL.md)**: Tries to break a pull request before reading prior diagnostics, then replays the proof and gives a verdict per axis on the tested base and head, each FAIL with its run.
- **[babysit-pr](skills/babysit-pr/SKILL.md)**: Drives an open PR to ready: conflicts, review comments, CI, every fix proven again, and a new verdict when the base or head changes. Stops before the merge.

**Written in your repo** by the skills above: `drive-<app>`, the driver of each surface of your app, and `prove-<area>`, a formal check of one critical area.

## This repo

| Path | What it holds |
|---|---|
| [`skills/`](skills/) | The skills, and the constitution they share. |
| [`tools/`](tools/) | The framework's checks. `python -I tools/check.py` runs them all, tests included; CI runs the same. |
| [`docs/adr/`](docs/adr/) | Decisions, dated, superseded but never rewritten. |
| [`docs/sources.md`](docs/sources.md) | Where each skill's ideas come from. Skills name no source themselves. |
| [`resources/`](resources/README.md) | The third-party skill sets, talks, and articles the framework was designed from. |

What changes a skill, and what is out of scope: [`SCOPE.md`](SCOPE.md). What changed: [`CHANGELOG.md`](CHANGELOG.md).
