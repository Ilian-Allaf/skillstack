# A stack

A stack is a chain of open PRs, each based on the branch of the one below.

When each PR of the stack has its own owner, as in a `ship-queue`, each owner babysits only its own PR, and the rules below apply to its branch alone. When the PR below gets a new head, the owner rebases its own branch on it and pushes with `git push --force-with-lease`. A fix or a rebase that a branch it does not own needs goes to the coordinator, which hands it to that branch's owner.

Otherwise, one babysitter per stack: before you start, check the lowest PR's comments for a `Babysitting this stack` comment from another session in the last hour. If there is one, another babysitter is on it: stop and report. Otherwise post yours, and post it again each round so it stays fresh.

- **Work the lowest PR that is not `ready`.** It is the only one whose checks matter until it is ready. Read the threads of the PRs above and batch their fixes, but push nothing to them while the lowest PR's checks run.
- **A fix goes in the PR that owns the code**, never in the top PR.
- **Keep the stack's shape.** Never retarget a base, reorder the stack, or squash across PRs: the order is the builder's. The one exception: when the PR below merged, retarget the PR above onto the branch it merged into, then rebase it there. When the lowest PR is rebased on its base, rebase each PR above on the new head of the one below. Each PR whose base or head changed goes back to `verify-pr`, even when its patch id is unchanged, as [verdict.md](../../verify-pr/references/verdict.md#verdict-validity) requires.
- **Stop at the line.** The stack is done when every PR is `ready` or `needs-human`. The user merges from the bottom.
