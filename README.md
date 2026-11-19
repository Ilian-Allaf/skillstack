<img src="assets/icon.svg" width="64" height="64" alt="">

# Software AI skills framework

Agent skills that turn a task into a pull request you can merge without worry: proven on the real app, checked for what it breaks elsewhere, and judged by a verifier that did not write it. You launch every task, and you merge every PR.

> **Status: v0.** Every skill is written and checked by the linters, and none has run on a real repo yet. Proving them on a testbed comes first ([#4](https://github.com/Ilian-Allaf/software-ai-skills-framework/issues/4)).

## Why these skills exist

Coding agents fail the same ways, again and again. Each skill answers one of them.

- **The agent declares done on green tests.** `ship` sets a `done_when` you approve, sees it fail on the base before any code, and proves it on the running app.
- **The change breaks something outside its diff.** `analyze-impact` finds the one fact the change is safe because of, and proves it by a run.
- **The author grades its own work.** `verify-pr` is a fresh agent, from another model family when one is available, that tries to break the PR. A finding blocks only with the run that proves it.
- **The same mistake comes back.** `add-guardrail` turns it into a check, red on the real mistake. `learn-from-mistakes` finds which layer let a bug through, and proposes the fix.
- **The agent cannot drive your app.** `create-app-driver` writes a skill that launches, drives, and observes it the way a user does.

The choices behind them are recorded as decisions in [`docs/adr/`](docs/adr/).

## Install

Pick one route per harness: installing both gives you every skill twice.

**As a plugin**, which updates itself. In Claude Code 2.1.275 or later:

```text
/plugin install software-ai-skills-framework --marketplace Ilian-Allaf/software-ai-skills-framework
```

The skills then answer to `/software-ai-skills-framework:<skill>`. Codex and Copilot read the same marketplace file, `.claude-plugin/marketplace.json`; their install has not been tried yet. The repo is private, so the harness needs your GitHub access.

**From a clone**, to edit the skills as you use them:

```bash
git clone https://github.com/Ilian-Allaf/software-ai-skills-framework.git
cd software-ai-skills-framework
python -I tools/link_skills.py
```

It links every skill into `~/.agents/skills` (Codex and most other harnesses) and `~/.claude/skills` (Claude Code). The links point into the clone, so a `git pull` updates the skills, and they follow the branch you have checked out. `--dry-run` shows what would change; `--unlink` removes the links.

Skills install as whole folders beside [the constitution](skills/constitution/README.md), which they read by relative path. An installer that copies skills one at a time drops it, so it is not supported ([ADR 0005](docs/adr/0005-the-constitution-is-a-folder-not-a-skill.md)).

## Getting started

1. Run `/setup-repo` once per repo. It sets up the issue tracker, the labels, the glossary, the coding standards, the agent file, and the app driver, and asks before each part.
2. Run `/ship <task>` for each task. You say go before any code, and you merge the PR it labels `ready`.
3. Not sure which skill fits? Run `/choose-skill` and describe your situation.

The map of every skill and the path of one task, in a diagram: [`skills/README.md`](skills/README.md).

## Reference

Every skill is launched by you; none is picked by the model on its own. Each one reads [the constitution](skills/constitution/README.md) first: the shared rules on proof, coverage, the glossary, and the PR format.

**You launch**

- **[choose-skill](skills/choose-skill/SKILL.md)**: Tells you which skill to launch for your situation, and with what command.
- **[setup-repo](skills/setup-repo/SKILL.md)**: Prepares a repo the first time you work in it, asking before each part.
- **[shape-spec](skills/shape-spec/SKILL.md)**: Turns a loose idea into a spec issue through an interview, or into a map of decisions when the work is too big for one session.
- **[investigate](skills/investigate/SKILL.md)**: Answers a question about the code, diagnoses a runtime symptom, or settles a decision with a throwaway prototype. Opens no PR.
- **[ship](skills/ship/SKILL.md)**: Turns one task into a ready-to-merge PR, proven on the real app and judged by an independent verifier.
- **[create-app-driver](skills/create-app-driver/SKILL.md)**: Writes the repo's driver, a skill that launches, drives, and observes the app like a user, with its feature map.
- **[add-guardrail](skills/add-guardrail/SKILL.md)**: Makes a repeated mistake impossible: turns it into a check, proven red on the real mistake.
- **[learn-from-mistakes](skills/learn-from-mistakes/SKILL.md)**: Learns from a session, a failed PR, or a bug found after merge, and proposes fixes to the layer that missed it.

**Inside a task** (`ship` runs them; you can also launch them on an open PR)

- **[analyze-impact](skills/analyze-impact/SKILL.md)**: Finds what a change breaks outside its diff, and proves by a run the one fact it is safe because of.
- **[verify-pr](skills/verify-pr/SKILL.md)**: Tries to break a pull request and gives a verdict per axis, behavior and code, each FAIL with the run that proves it.
- **[babysit-pr](skills/babysit-pr/SKILL.md)**: Drives an open PR to ready: conflicts, review comments, CI, every fix proven again. Stops before the merge.

**Written in your repo** by the skills above: `drive-<app>`, the driver of each surface of your app, and `prove-<area>`, a formal check of one critical area.

## This repo

| Path | What it holds |
|---|---|
| [`skills/`](skills/) | The skills, and the constitution they share. |
| [`tools/`](tools/) | The framework's checks. `python -I tools/check.py` runs them all, tests included; CI runs the same. |
| [`docs/adr/`](docs/adr/) | Decisions, dated, superseded but never rewritten. |
| [`docs/sources.md`](docs/sources.md) | Where each skill's ideas come from. Skills name no source themselves. |
| [`docs/history/`](docs/history/) | The first design notes, in French, frozen. |
| [`evals/`](evals/) | Cases the verifier must catch. |
| [`knowledge/`](knowledge/README.md) | The third-party skill sets, talks, and articles the framework was designed from. |

What changes a skill, and what is out of scope: [`SCOPE.md`](SCOPE.md). What changed: [`CHANGELOG.md`](CHANGELOG.md).
