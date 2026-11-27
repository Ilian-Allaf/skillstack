# Issue trackers

The skills never name a tracker. They name an operation, such as "publish to the issue tracker" or "label it `escaped`", and `issue-tracker.md` in the project folder says how to do it there. That file is the only thing that changes from one tracker to another; the skills stay the same everywhere.

`setup-repo` writes that file from one of the templates below, then proves it with a read-only operation.

Without `setup-repo`, the tracker is the private markdown one. The first skill that needs an issue and finds no `issue-tracker.md` writes it from [local.md](local.md), as that template says, and names the file in its reply. Its first line marks it as written without `setup-repo`.

A default tracker is not a choice, so `setup-repo` offers the tracker part anyway, with the number of open issues it holds. When the user keeps the markdown tracker, remove that first line. When the user picks another, first create each open issue of `issues/` in the new tracker, with its labels and comments, then comment on the old file with the new issue's link and close it.

| Tracker | Template | Needs |
|---|---|---|
| GitHub Issues | [github.md](github.md) | the `gh` CLI, authenticated |
| GitLab Issues | [gitlab.md](gitlab.md) | the `glab` CLI, authenticated |
| Markdown files, in the project folder or the repo | [local.md](local.md) | nothing, not even a remote; the default when no tracker file exists |
| Anything else: Linear, Jira, Azure DevOps… | [other.md](other.md) | the user describes the workflow; the file records it |

Propose the tracker that matches the repo's `git remote`, and let the user change it. One tracker per repo.

## The operations

Every template, and every file written from `other.md`, answers each of these, under these headings. A skill that needs an operation the file does not answer never guesses: outside a running task it asks the user; during a task it lists the operation in its reply and the decision log, and goes on.

| Operation | Used by |
|---|---|
| Create an issue, with a title, a body, and labels | `shape-spec`, `ship`, `babysit-pr`, `analyze-impact`, `add-guardrail`, `learn-from-mistakes` |
| Read an issue, with its comments and labels | `ship`, `learn-from-mistakes`, `shape-spec` |
| List open issues by label | `shape-spec`, `learn-from-mistakes` |
| Comment on an issue | `shape-spec` |
| Add or remove a label | `shape-spec`, the user (`escaped`) |
| Create a label that does not exist yet | `setup-repo` |
| Close an issue, after a comment that says why | `shape-spec` |
| Link a child issue to its parent | `shape-spec` (a map and its decisions) |
| Mark an issue as blocked by another, and count its open blockers | `shape-spec` |
| Claim an issue, so two sessions never work the same one | `shape-spec`, `ship` |
| Link a PR to the issue it delivers, so the merge closes it | `ship` |

## The code host is separate

Pull requests, their state (the State line of the body, mirrored by the labels `ready` and `needs-human` when they exist), verdict comments, and CI live on the code host, not in the issue tracker, even when both are GitHub. The skills drive the code host with `gh` today; a GitLab code host would need the pull request side of `ship`, `verify-pr`, and `babysit-pr` adapted, which is not done yet.
