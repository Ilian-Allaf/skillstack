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

## Model per role

The user runs on one subscription, so each role takes the model of that subscription that fits the job: the strongest where judgment decides, a faster one where the work is broad and checked. A line `model for <role>: <model>` in the user's agent file overrides the table. When the harness cannot pick a subagent's model, every role runs on the session's model.

| Role | Claude subscription | Codex subscription |
|---|---|---|
| builder, coordinator | the session's model | the session's model |
| the verifier's verdict, the adversarial lane | a family other than the builder's when the harness offers one (ADR 0003 of the framework), else the session's model | the same |
| a design through a one-way door, a scrapped sketch | the strongest model, at its highest reasoning effort | the strongest model, highest reasoning effort |
| the verifier's lanes, swarm workers, the comment hunter | a mid-size model, such as Sonnet | the session's model, medium reasoning effort |
| bulk reading: a transcript, logs, a sweep of the codebase | the smallest model, such as Haiku | the session's model, low reasoning effort |

Raise the effort one step for the subtlest work, and lower it for routine work. Every role but the verifier's keeps the session's family.

## Rules

- **A fresh context means a new subagent**, not a continued one. Codex can fork the parent context; check that a Codex verifier starts empty before you trust its independence.
- **Ask through the question tool** when the user is present. A plain message is easy to miss.
- **When a subagent cannot spawn its own**, it runs the work it would have spread out one piece after another, and says so in its result.
- **When the other family is missing**, the verifier is a fresh agent of the same family. Say so in the verdict.
- **The merge hook** blocks `gh pr merge`, `gh pr merge --auto`, and merge queue commands, including variants passed through `git -c` or an alias.
