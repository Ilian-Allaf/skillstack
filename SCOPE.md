# Scope

What gets a skill changed, and what the framework will not do.

## The bar for a change

A change to a skill fits the decisions: it contradicts no accepted ADR in [`docs/adr/`](docs/adr/). To reopen one, cite it and say what changed since; a yes becomes a new ADR that supersedes it.

Size does not matter: a one-word fix and a rewrite face the same bar. A PR says why the change is worth it: an observed failure when there is one, linked to its session, PR, or issue.

## A new skill

A new skill faces the same bar as any change, and its PR says why no existing skill can absorb it. If the behavior composes from existing skills, it gets no skill of its own.

## Out of scope

| Out of scope | Why |
|---|---|
| The agent merging, in any form | [ADR 0001](docs/adr/0001-the-user-always-merges.md) |
| A trust ladder, a `.trust/` folder, a CI gate of the framework's own | [ADR 0001](docs/adr/0001-the-user-always-merges.md) |
| Tasks that start without the user: scheduled runs, crons, a queue started by a timer | [ADR 0014](docs/adr/0014-a-launched-task-runs-to-a-ready-pr.md) |
| Splitting a spec into tickets for parallel agents | [ADR 0011](docs/adr/0011-no-split-into-tickets.md) |
| Deploying | The framework stops at a PR labeled `ready`. |
| A server, a database, a message queue | The code host, the issue tracker, and the harness hold all the state. |
| Personas (tester, PM, designer) and agents that debate | Coordination comes from the shape of the work, not from roles. |
