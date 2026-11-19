# 0008. A layout no AI provider owns

- **Status**: accepted, 2026-11-19
- **Applies to**: `skills/constitution/references/target-repo.md`, `skills/setup-repo/`, every skill's frontmatter
- **Enforced by**: `tools/lint_skills.py` (the frontmatter fields of the Agent Skills specification)

## Context

Each harness reads skills and instructions from its own place: `.claude/skills/` and `CLAUDE.md` for Claude Code, `.agents/skills/` and `AGENTS.md` for Codex and most others. Writing for one locks the framework to it.

## Decision

- Skills follow the Agent Skills specification (agentskills.io).
- In a target repo, each skill lives in `.agents/skills/<name>/`. A harness that reads only its own folder gets a symlink per skill, never a copy. On Windows without symlinks, it gets a junction, never committed.
- `AGENTS.md` is the canonical agent file. An existing `CLAUDE.md` gets the line `@AGENTS.md`.
- Skills name capabilities, never tools. `skills/constitution/references/harness.md` maps each capability to each harness.
- The default model of each role is a family, not a pinned model.

## Consequences

A harness-specific file, such as Codex's `agents/openai.yaml`, sits beside the `SKILL.md` and says the same thing as its frontmatter.
