# Scope

What gets a skill changed, and what the framework will not do.

## The bar for a change

A change to a skill clears both parts:

1. **An observed failure.** It names something that went wrong in a real session: what was run, what the skill did, what was expected. Link the session, the PR, or the issue. "It would be better if..." does not clear this part.
2. **It fits the decisions.** It contradicts no accepted ADR in [`docs/adr/`](docs/adr/). To reopen one, cite it and say what changed since; a yes becomes a new ADR that supersedes it.

Size does not matter: a one-word fix and a rewrite face the same bar. A broken reference, a failing check, or an attribution in [`docs/sources.md`](docs/sources.md) is fixed without one.

## A new skill

A new skill enters only when the same failure was seen twice and no existing skill can absorb it. If the behavior composes from existing skills, it gets no skill of its own.

## Out of scope

| Out of scope | Why |
|---|---|
| The agent merging, in any form | [ADR 0001](docs/adr/0001-the-user-always-merges.md) |
| A trust ladder, a `.trust/` folder, a CI gate of the framework's own | [ADR 0001](docs/adr/0001-the-user-always-merges.md) |
| Tasks that start without the user: scheduled runs, crons, a queue worked overnight | [ADR 0002](docs/adr/0002-nothing-starts-without-the-user.md) |
| Splitting a spec into tickets for parallel agents | [ADR 0011](docs/adr/0011-no-split-into-tickets.md) |
| Deploying | The framework stops at a PR labeled `ready`. |
| A server, a database, a message queue | The code host, the issue tracker, and the harness hold all the state. |
| Personas (tester, PM, designer) and agents that debate | Coordination comes from the shape of the work, not from roles. |
