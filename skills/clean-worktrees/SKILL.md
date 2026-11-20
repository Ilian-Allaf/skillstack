---
name: clean-worktrees
description: "Frees disk by removing the git worktrees of finished or abandoned tasks, and never loses uncommitted work."
disable-model-invocation: true
argument-hint: "<nothing, or the repo path>"
metadata:
  kind: kit
  consumes: "a repo whose worktrees have piled up"
  produces: "the worktrees removed, the ones kept with their reason, and the disk freed"
  hypothesis: "Agents leave a worktree per task and never remove it, and a cleanup by hand deletes the one that held unsaved work."
---

# Clean worktrees

Read [the constitution](../constitution/README.md) first.

This is the one skill that deletes the user's local state with no PR to review it, so the gates below are the review. A worktree removed with its branch kept loses nothing; an uncommitted edit removed is gone.

## Steps

1. **Take stock.** Record the free disk space. List the worktrees from `git worktree list --porcelain`, never from paths typed by hand: worktrees live in several places. For each one, collect its path, branch, size, age of its last commit and of its last changed file, the state of its branch's PR (open, merged, closed, none), whether its branch is merged into the base, its uncommitted tracked edits (`git -C <path> status --porcelain`), its untracked files, and any process running in it.
   Done when: every worktree has each field filled, or "unknown".

2. **Sort each worktree** into one group:

   | Group | When | Action |
   |---|---|---|
   | in use | the current session's worktree, a task still running, an owner of a running `ship-queue`, a file changed in the last 24 hours, or a process running in it | keep |
   | open | its PR is open and not merged | keep |
   | unsaved | it holds uncommitted tracked edits, or untracked files that git does not ignore | ask the user, showing the diff and the files |
   | paused | its branch is not merged, has no PR, and its last commit starts with `wip:` | keep: `/resume-task` picks it up |
   | safe | its branch is merged or its PR closed, and the tree is clean | remove |
   | abandoned | its branch is not merged, has no PR, its last commit is not `wip:`, and the tree is clean | remove the worktree, keep the branch |

   The main checkout is never a candidate.
   Done when: every worktree has one group, with the fact that put it there.

3. **Ask about the unsaved ones.** For each, show the diff and the untracked files, and ask through the harness's question tool whether to commit it to its branch, keep the worktree, or drop the edits. This is an irreversible choice: it is the user's.
   Done when: every unsaved worktree has the user's answer.

4. **Remove.** For each worktree to remove, run `git worktree remove --force <path>`; if the folder survives on ignored build files, delete it. Then `git worktree prune`. Keep every branch: its commits stay reachable.
   Done when: `git worktree list` no longer shows the removed ones, and the free space is measured again.

## Reply

The free space before and after, the worktrees removed, and each one kept with its one-line reason: in use by what, an open PR, or unsaved work the user chose to keep.
