# 0005. The constitution is a folder, not a skill

- **Status**: accepted, 2026-11-19
- **Applies to**: `skills/constitution/`
- **Enforced by**: `tools/lint_skills.py` (F016: a shared folder's `README.md` has no frontmatter, so no harness lists it as a skill)

## Context

Every skill obeys the same rules: proof, coverage, glossary, PR format, harness capabilities. Copied into each skill, they drift. Made into a skill, they show in the harness's menu, where the user could launch rules that do nothing alone.

## Decision

`skills/constitution/` holds `README.md` and `references/`, with no `SKILL.md`. Every skill reads it first, by its relative path (`../constitution/README.md`).

## Alternatives rejected

- **A skill other skills call through the harness's Skill tool**: our skills are all launched by the user (ADR 0006), and a user-invoked skill cannot be reached that way. Reading a file works in every harness.
- **Rules copied into each skill**: one meaning, one home.

## Consequences

The constitution must sit beside the skills, at the same level, for `../constitution/` to resolve. An install that keeps the whole `skills/` folder works: a plugin, or a symlink per skill into this repo. An installer that copies skills one at a time drops it, so it is not supported.
