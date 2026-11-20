# 0002. Nothing starts without the user

- **Status**: accepted, 2026-11-19
- **Applies to**: every skill; `skills/ship/SKILL.md` (the go), `skills/create-app-driver/references/maintain.md`
- **Enforced by**: `tools/lint_skills.py` keeps every skill for the user to launch (F017 for Claude Code, F018 for Codex); the rest by review

## Context

The design once had skills that started work on their own: `autopilot` worked a queue of issues overnight, `ketchup` wrote a morning report, `eval` ran A/B tests of skills, and the driver's `maintain` mode and `ratchet` ran on a schedule. Each one opened PRs or spent tokens the user had not asked for.

## Decision

The user launches every task.

- No scheduled run, no cron, no queue worked alone, no planned PR.
- `ship` asks for a go before any code, on every task, whatever its risk class.
- What stays automatic happens inside a task the user launched: subagents, the verifier, `babysit-pr` up to `ready`.
- `maintain` and `ratchet` run on demand. `frame` reports the feature map's freshness from its "Last driven" commit.

## Alternatives rejected

- **The go only for high-risk tasks**: a low-risk task still spends the user's tokens and opens a PR in their name.
- **`autopilot`, `ketchup`, `eval`**: removed from the catalog. A change to a skill is judged on the next PRs of the testbed instead of an A/B run.

## Consequences

`learn-from-mistakes` applies nothing before the user approves each line. A large spec goes through the `bespoke` playbook: one builder, a series of ordered PRs, all inside the task the user gave.
