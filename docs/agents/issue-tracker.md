# Issue tracker: GitHub

Issues live in this repo's GitHub Issues. Use the `gh` CLI; it finds the repo from `git remote`. Before the first write of a session, check the target with `gh repo view --json nameWithOwner`: in a fork, `gh` can default to the upstream repo.

## Create an issue
`gh issue create --title "..." --body-file <file> --label "..."`. Write long bodies to a file first.

## Read an issue
`gh issue view <n> --json number,title,body,labels,comments,state`

## List open issues by label
`gh issue list --state open --label "<label>" --json number,title,labels`

## Comment on an issue
`gh issue comment <n> --body-file <file>`

## Add or remove a label
`gh issue edit <n> --add-label "<label>"`, or `--remove-label "<label>"`

## Create a label
`gh label create "<label>"`, without `--force`, which would overwrite an existing label's color and description. When the label already exists, the command fails and the label stays as it is.

## Close an issue
Comment with the reason first, then `gh issue close <n>`.

## Link a child issue to its parent
`gh issue edit <parent> --add-sub-issue <child>`. Without sub-issues, put `Part of #<parent>` at the top of the child's body.

## Blocking
`gh issue edit <child> --add-blocked-by <blocker>`. Open blockers: `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by`; 0 means the issue can start. Without native dependencies, put `Blocked by: #<n>` at the top of the body; the issue can start once every listed issue is closed.

## Claim an issue
`gh issue edit <n> --add-assignee @me`, as the session's first write on it.
