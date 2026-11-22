# Template: GitLab Issues

Copy the block below into `~/.agents/projects/<project>/issue-tracker.md`, or into the repo at `docs/agents/issue-tracker.md` when the user shares it, with a route to it in the project folder.

```markdown
# Issue tracker: GitLab

Issues live in this project's GitLab Issues. Use the `glab` CLI; it finds the project from `git remote`. GitLab calls comments "notes".

## Create an issue
`glab issue create --title "..." --description "..." --label "..."`

## Read an issue
`glab issue view <n> --comments -F json`

## List open issues by label
`glab issue list --label "<label>" -O json`

## Comment on an issue
`glab issue note <n> --message "..."`

## Add or remove a label
`glab issue update <n> --label "<label>"`, or `--unlabel "<label>"`

## Create a label
`glab label create --name "<label>"`. Check first with `glab label list` whether it exists.

## Close an issue
`glab issue close <n>` takes no comment: post the reason with `glab issue note` first.

## Link a child issue to its parent
Create the child with `--linked-issues <parent> --link-type relates_to`, and put `Part of #<parent>` at the top of its description.

## Blocking
Post the quick action `/blocked_by #<blocker>` as a note on the child. Native blocking links need a paid tier; without them, put `Blocked by: #<n>` at the top of the description. The issue can start once every blocker is closed.

## Claim an issue
`glab issue update <n> --assignee @me`, as the session's first write on it.

## Link a PR to the issue it delivers
In the merge request description, `Closes #<n>` on the one that completes the issue, and `Part of #<n>` on an earlier one of a stack; GitLab closes the issue when it merges into the default branch. When the code lives on another host, post the PR's link as a comment on the issue instead, and the user closes the issue when they merge.
```

Prove the file with the read-only list command before you save it. The blocking and label commands are the least tested; run each once on a throwaway issue when the user agrees.
