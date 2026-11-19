# Template: markdown files in the repo

For a solo project, or a repo with no remote. Pick it instead of a hosted tracker, never beside one. Copy the block below into the target repo at `docs/agents/issue-tracker.md`.

```markdown
# Issue tracker: markdown files

Issues live as markdown files under `.scratch/`, committed with the code.

## Create an issue
A new file `.scratch/<effort>/issues/<NN>-<slug>.md`, numbered from `01`. Its first lines are `Status: open` and `Labels: <labels>`; the body follows.

## Read an issue
Read the file. Comments are under its `## Comments` heading.

## List open issues by label
Search `.scratch/` for files with `Status: open` whose `Labels:` line holds the label.

## Comment on an issue
Append to the file's `## Comments` heading, with the date.

## Add or remove a label
Edit the `Labels:` line.

## Create a label
Nothing to do: a label exists once a file uses it.

## Close an issue
Append the reason under `## Comments`, then set `Status: closed`.

## Link a child issue to its parent
Put the child under `.scratch/<effort>/issues/` with `Part of: <parent file>` on its third line. A map is `.scratch/<effort>/map.md`.

## Blocking
A `Blocked by: <NN>, <NN>` line near the top. The issue can start once every listed file is closed or resolved.

## Claim an issue
Set `Status: claimed` and save, before any other work on it.
```
