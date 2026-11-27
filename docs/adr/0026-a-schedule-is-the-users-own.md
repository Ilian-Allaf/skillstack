# 0026. A schedule is the user's own, outside the framework

- **Status**: accepted, 2026-11-28. Amends [0014](0014-a-launched-task-runs-to-a-ready-pr.md): its rule against scheduled runs binds the framework, not the user.
- **Applies to**: every skill, `SCOPE.md`, rule 11 of `skills/constitution/README.md`
- **Enforced by**: `tools/lint_skills.py` keeps every skill for the user to launch (F017 for Claude Code, F018 for Codex); the rest by review

## Context

ADR 0014 keeps ADR 0002's "nothing starts without the user": no cron, no scheduled run, and it rejects "a daily driver audit" started by a timer. `maintain-app-driver` keeps the feature map honest only if it runs often, and the user wants to run it daily, by hand now and from a cron later. That cron is set up outside this repo, by the user, in a system the framework neither ships nor knows.

## Decision

- The framework ships no scheduler, no cron, no timer, and no skill starts another task on its own. That part of 0014 stands.
- A schedule the user sets up outside the framework is the user launching the skill. What it launches runs as if the user had typed it, under the same rules: a task still ends at a PR the user merges (ADR 0001).
- A skill may say how often it is worth running; it never sets up the schedule.

## Alternatives rejected

- **Keep 0014 as written**: it would forbid the user's own cron, a choice that is the user's and lies outside this repo.
- **Ship a scheduler in the framework**: the state of a schedule needs a server, which `SCOPE.md` leaves out.

## Consequences

Rule 11 of the constitution says the user starts every task, by hand or from a schedule of their own. `SCOPE.md` names what stays out of scope: a schedule the framework itself sets up or starts.
