# Nectar — Claude Code verification

Dated analysis, 2026-11-23. Source: [Addy Osmani](SOURCE.md); [reading notes](content.md).

## What this adds to our research

Our interpretation: verification needs its own evaluation loop. A passing application check and a trustworthy verifier are separate claims. A useful research exercise would replay the same historical changes before and after a verifier change, keeping both missed bugs and false alarms visible.

The article's distinction between generated-input testing and comparison against an old implementation gives us two different questions to ask: which invariant must hold, and which existing behavior must remain? Neither question alone determines the right check for a task.

## Framework questions, not adopted changes

These are our questions as of the collection date, not descriptions of current skill behavior:

- Could a verifier evaluation report distinguish bugs found initially from bugs retained in its final verdict?
- Could a review-rule change be evaluated separately from the application change it judges?
- When a rule is added after an incident, which known clean change demonstrates that it does not over-report?

Any proposal must still meet [SCOPE.md](../../../../SCOPE.md). The article's gates do not reopen [ADR 0001](../../../../docs/adr/0001-the-user-always-merges.md), and its protected-rule practice needs reconciliation with [ADR 0017](../../../../docs/adr/0017-a-formal-check-guards-every-task-that-touches-its-code.md), which allows a builder to update covered checks and requires independent verification of that update.
