# 0006. Skills are launched by the user, and route by path

- **Status**: accepted, 2026-11-19
- **Applies to**: every `SKILL.md`: its frontmatter, `metadata.calls`, and `metadata.reads`
- **Enforced by**: `tools/lint_skills.py` (F014 and F015: a link to another skill has a declared edge, and a declared call has its link by path)

## Context

A model picks a skill from its description, and picks wrong or not at all. Inside a task, `ship` must run `analyze-impact`, `verify-pr`, and `babysit-pr` every time, not when a description happens to match.

## Decision

- Every skill has `disable-model-invocation: true`: the user launches it, and its description is one line written for the user.
- A skill reaches another by reading its `SKILL.md` at a relative path, declared in `metadata.calls` (it runs the other) or `metadata.reads` (it reads a part of it).
- `choose-skill` tells the user which skill to launch; it launches nothing.

## Alternatives rejected

- **Inner skills the model can invoke, called through the harness's Skill tool**: the model could fire `verify-pr` or `babysit-pr` outside a task the user launched (ADR 0002), and not every harness has a Skill tool.

## Consequences

Each harness needs its own way to keep the model away from a skill: `disable-model-invocation` for Claude Code, `agents/openai.yaml` with `allow_implicit_invocation: false` for Codex. `learn-from-mistakes` checks in transcripts that the expected nodes were read.
