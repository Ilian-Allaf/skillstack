# 0016. The working files live outside the repo, unless the team shares them

- **Status**: accepted, 2026-11-22
- **Applies to**: `skills/constitution/references/target-repo.md`, `skills/constitution/README.md` (rule 14), `skills/setup-repo/`, `skills/create-app-driver/`, every skill that reads the tracker file, the glossary, the ADRs, the coding standards, the rule table, or a driver
- **Enforced by**: `tools/lint_skills.py` (P006: a skill names the project folder, never the repo path of a shared entry, outside the files that write one)

## Context

`setup-repo` wrote its files into the repo it prepared: `AGENTS.md`, `docs/agents/issue-tracker.md`, `GLOSSARY.md`, `CODING_STANDARDS.md`, `docs/agent-rules.md`, `.agents/skills/drive-<app>/`, through a docs PR, plus labels on the code host. On a repo the user shares with a team, that imposes the framework on people who did not choose it. The first such repo, `Photo-Platform/photo-platform`, has four contributors and its own agent files, glossary, ADRs, and skills.

Symlinks from the repo to a folder outside it were considered and do not hold: a T3 thread starts in a fresh worktree, where untracked links are missing.

## Decision

- Each repo gets a project folder, `~/.agents/projects/<project>/`, on the user's machine and outside every repo. `<project>` comes from the `origin` remote, so every worktree finds the same folder. It holds `issue-tracker.md`, `glossary.md`, `adr/`, `coding-standards.md`, `agent-rules.md`, `drive-<app>/`, and `prove-<area>/`.
- Skills read these files at their path in the project folder, a concrete path, never an abstract role resolved elsewhere.
- Each entry is private (the default) or shared, chosen entry by entry when `setup-repo` runs. A shared entry lives in the repo, at the path the framework used before, and the project folder holds a route: a one-line file that says where the entry lives in the repo. One hop, one home per entry, and a broken route stops the skill.
- When the repo already has an entry of its own, the project folder routes to it.
- Private entries are written in place, without a PR: the project folder is the user's own. Every change to the repo still goes through a PR.
- The merge guard goes in the user's harness settings unless shared. Labels are created only when the user agrees, since the team sees them.

## Alternatives rejected

- **Every file in the repo** (the layout before this ADR): imposes the framework on the team.
- **The project folder inside this framework's repo**, as a personal skills repo would keep it: this repo ships the framework, and would ship each user's project notes with it.
- **Symlinks from the repo into the project folder**: lost in every new worktree.
- **One manifest per project, with skills naming roles such as "the tracker"**: an agent must remember a rule from another file before it can find anything; a concrete path with the route inside the file needs no prior reading.

## Consequences

- [ADR 0008](0008-a-layout-no-provider-owns.md) still governs shared entries: a shared driver lives in `.agents/skills/`, linked for the harnesses that need it.
- [ADR 0009](0009-the-issue-tracker-is-agnostic.md) is unchanged: the tracker file is still the contract, wherever it lives.
- A repo prepared before this ADR keeps its files; a rerun of `setup-repo` writes the project folder with a route to each.
- An agent that runs where the project folder is absent, such as a cloud session or CI, sees only shared entries.
- Codex's default sandbox may refuse writes outside the workspace; [harness.md](../../skills/constitution/references/harness.md) lists it as to confirm.
