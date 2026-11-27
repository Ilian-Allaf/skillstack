# Template: markdown files

The default tracker, and the one for a solo project or a repo with no remote. Pick it instead of a hosted tracker, never beside one.

- **Private**, the default. The issues live in the project folder, at `~/.agents/projects/<project>/issues/`, and never reach the repo. Copy the block below into `~/.agents/projects/<project>/issue-tracker.md`, with `<issues>` replaced by that folder, `<project>` named as [target-repo.md](../../../constitution/references/target-repo.md) says.
- **Shared.** The issues live in the repo at `.scratch/issues/`, committed with the code. Copy the block into the repo at `docs/agents/issue-tracker.md`, with `<issues>` replaced by `.scratch/issues/`, and write a route to it in the project folder.

**Written without setup-repo.** When a skill needs an issue and the project folder has no `issue-tracker.md`, it writes the private file itself, keeping the block's first line, and says so in its reply. That line tells `setup-repo` nobody chose this tracker yet, as [README.md](README.md) says.

Issues are numbered across the repo, as a hosted tracker numbers them, so `/ship 7` names one issue. A map is an issue like any other.

````markdown
Default tracker, written without setup-repo.

# Issue tracker: markdown files

Issues live as markdown files in `<issues>`, one per issue, named `<NNNN>-<slug>.md`. An issue's number is the `NNNN` of its file, and a number is never reused. A file reads:

    # <title>
    Status: open
    Labels: <labels, comma-separated>
    Part of: <number>, for a child only
    Blocked by: <number>, <number>, while blocked
    PR: <link>, once a PR delivers it

    <body>

    ## Comments

## Create an issue
A new file `<issues>/<NNNN>-<slug>.md`, numbered one above the highest number in the folder, from `0001`, with the folder created on the first issue. The title, `Status: open`, and `Labels:` come first, then the body, then an empty `## Comments` heading.

## Read an issue
Read the file whose name starts with its number. Comments are under `## Comments`.

## List open issues by label
Search `<issues>` for files with `Status: open` whose `Labels:` line holds the label.

## Comment on an issue
Append `- <date>: <comment>` under `## Comments`.

## Add or remove a label
Edit the `Labels:` line.

## Create a label
Nothing to do: a label exists once an issue uses it.

## Close an issue
Append the reason under `## Comments`, then set `Status: closed`.

## Link a child issue to its parent
A `Part of: <parent number>` line in the child, and the child's number and title in the parent's body.

## Blocking
A `Blocked by: <number>, <number>` line. The issue can start once every issue it lists is closed.

## Claim an issue
Set `Status: claimed` and save, before any other work on it.

## Link a PR to the issue it delivers
A `PR: <link>` line in the issue, with `(part)` after the link for an earlier PR of a stack. The user sets `Status: closed` when they merge the PR that completes it. In the PR body, the issue line is `Issue: <issues>/<file>` when `<issues>` is in the repo; when it is in the project folder, the PR names no issue, since its readers cannot open it.
````
