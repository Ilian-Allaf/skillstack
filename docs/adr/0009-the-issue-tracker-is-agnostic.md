# 0009. The issue tracker is agnostic; the code host is GitHub for now

- **Status**: accepted, 2026-11-19
- **Applies to**: every skill that reads or writes issues; `skills/setup-repo/references/trackers/`
- **Enforced by**: review

## Context

Teams track work in GitHub Issues, GitLab, Linear, Jira, or local files. A skill that runs `gh issue create` works for only one of them.

## Decision

Skills name an operation ("publish to the issue tracker", "add the label `escaped`"). The target repo's `docs/agents/issue-tracker.md` says how to do each one. `setup-repo` writes it from a template (GitHub, GitLab, local markdown), or from the user's description of another tool and the tools really available. This is the split of Matt Pocock's `setup-matt-pocock-skills`.

## Alternatives rejected

- **A tracker abstraction in code**: an agent follows a short file of commands just as well, and the user can edit it.

## Consequences

PRs, CI, and PR labels still assume GitHub. Issue #10 extends the split to the code host.
