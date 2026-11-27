# 0014. A launched task runs to a ready PR

- **Status**: accepted, 2026-11-20; amended by [0026](0026-a-schedule-is-the-users-own.md). Supersedes [0002](0002-nothing-starts-without-the-user.md).
- **Applies to**: every skill; `skills/ship/` (frame, design, the long-run rules), `skills/constitution/README.md` (rules 7, 11, 12, 13)
- **Enforced by**: `tools/lint_skills.py` keeps every skill for the user to launch (F017 for Claude Code, F018 for Codex); the rest by review

## Context

ADR 0002 made `ship` wait for the user's go before any code, on every task, and removed `autopilot`, `ketchup`, and `eval` because they started work on their own. On 2026-11-20 the user restated the goal: the agent as autonomous as possible up to a ready PR, never a merge, and no cron that starts agents alone. The source the framework follows (pstack) restates the goal and does not wait: it stops only for an irreversible step, a product call no experiment can settle, or a dead end. What ADR 0002 got right was who starts the work; what it cost was a pause on every task, after the user had already asked for it.

## Decision

The user starts every task. Once started, the task runs to a ready PR without asking.

- **Nothing starts without the user.** No cron, no scheduled run, no work picked from a tracker alone, no PR outside a task the user launched. This part of ADR 0002 stands.
- **Launching is the go.** `ship` shows its frame (goal, `done_when` red on the base, cases, risk, design) in its first message and goes on without waiting.
- **The agent stops only for**: a one-way door, where it shows the design before code (`ship/references/design.md` step 6); a product or preference call no run can settle; evidence that rules out what the user asked for; a dead end after the budget and one replan. Everything else is decided, recorded under Decisions, and reported.
- **A periodic wake inside a launched run is allowed**, such as a queue checking on its owners. It lives only as long as the run the user launched, and ends with it.
- **User-launched skills may run long**: a queue of tasks, a catch-up, a blind test of a skill change.
- **The merge stays the user's** (ADR 0001).

## Alternatives rejected

- **Keep the go on every task**: one pause per task after the user already asked for it; the frame is still shown, so the user can stop a misread task at once.
- **A go only for `high` tasks**: the risk class is the agent's own judgment; the one-way door is the observable case, and it keeps its stop.
- **Scheduled runs and automations** (a daily driver audit, an overnight queue started by a timer): the user wants to decide what starts.

## Consequences

- `ship` step 1 shows the frame and continues; the user can say "show me the design" in the task to get the design stop on any change.
- `learn-from-mistakes` still applies nothing before the user approves each line: it changes the framework itself.
- `ship-queue`, `catch-me-up`, and `test-skill-change` can enter the catalog as user-launched skills.
