# Harness capabilities

Skills name a capability, never a tool. This table maps each capability to the tool that provides it in each harness. "To confirm" means nobody has tested it yet. Confirm it and update this file before a skill depends on it.

| Capability | T3 Code | Claude Code alone | Codex |
|---|---|---|---|
| spawn a fresh subagent, same family | `Agent` tool | `Agent` tool | to confirm |
| spawn a subagent of another family | `delegate_task` | to confirm | to confirm |
| isolate a run | git worktree | git worktree | git worktree |
| a subagent spawns its own subagents (the verifier's lanes, swarms) | to confirm | to confirm | to confirm |
| wake up when a PR changes | `watch_pull_request` | to confirm (REST polling fallback) | to confirm |
| find a project skill | `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex), by the agent it runs | `.claude/skills/` only: link each skill from `.agents/skills/` | `.agents/skills/`, from the working directory up to the repo root |
| read the agent file | as the agent it runs | `AGENTS.md` when no `CLAUDE.md` exists; otherwise `CLAUDE.md`, which imports it with `@AGENTS.md` | `AGENTS.md` |
| ask the user a question | `AskUserQuestion` | `AskUserQuestion` | `request_user_input` |
| read a session transcript | to confirm | `~/.claude/projects/<project>/<session>.jsonl` | to confirm |
| attach a video or image to a PR so it plays in the page | to confirm (`gh` has no upload command; CI artifact or branch link as fallback) | to confirm | to confirm |
| block the merge | a `PreToolUse` hook | a `PreToolUse` hook | to confirm |
| cap the cost of a run | to confirm | to confirm | to confirm |

## Rules

- **A fresh context means a new subagent**, not a continued one. Codex can fork the parent context; check that a Codex verifier starts empty before you trust its independence.
- **Ask through the question tool** when the user is present. A plain message is easy to miss.
- **When a subagent cannot spawn its own**, it runs the work it would have spread out one piece after another, and says so in its result.
- **When the other family is missing**, the verifier is a fresh agent of the same family. Say so in the verdict.
- **The merge hook** blocks `gh pr merge`, `gh pr merge --auto`, and merge queue commands, including variants passed through `git -c` or an alias.
