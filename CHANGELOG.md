# Changelog

One entry per merged PR that changes what a skill does, or how the framework is installed or checked. Newest first. A rename or a removal names what replaced it.

## Unreleased (v0)

- Every list of the skills is checked: `plugin.json` lists exactly the skills (R007), the README links each one (R008), and `choose-skill` names each one as a command (R009).
- Install routes: a plugin (`.claude-plugin/plugin.json` and `marketplace.json`, version 0.1.0), or `tools/link_skills.py` from a clone. Every skill carries `agents/openai.yaml`, so Codex keeps it for the user to launch too; the linter checks both harnesses (F017, F018). `setup-repo` installs the merge guard as `harness.md` describes, instead of an `install.py` that was never built.
- Repo standardized: English README, `SCOPE.md`, this changelog, decisions as ADRs in `docs/adr/`, the first design notes frozen in `docs/history/`, attribution moved to `docs/sources.md`, an issue template for a skill failure, and the roadmap moved to issues #4 to #12.
- Feature maps and ADRs stay fresh: "Declared in" with its check, ADR status and supersession, the skills map in `skills/README.md` checked by R006 (#3).
- This repo prepared with its own `setup-repo`: `AGENTS.md`, `CODING_STANDARDS.md`, `docs/agents/issue-tracker.md` (#2).
- First version of the framework: 11 skills, the constitution, `tools/check.py` (#1).
