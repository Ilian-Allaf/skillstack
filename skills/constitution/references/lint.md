# The lint pass

A language file in [languages/](languages/typescript.md) states its rules as prose, each with an id. The rules a linter can hold also ship as checks, in a pack beside the constitution: [lint/typescript/](../lint/typescript/pack.json) for TypeScript. The lint pass runs a pack's checks on the lines a change adds or edits, in any repo, whatever linter the repo already has, and writes nothing in it.

Read this before you run the pass, as the builder in `clean` or the verifier in `standards`, and before you write a decision for a repo.

## The decisions

The user decides, repo by repo, in `~/.agents/projects/<project>/lint/<language>.md`. It is an entry of the project folder like the others ([target-repo.md](target-repo.md)): private by default, or shared, and then a route.

```markdown
# TypeScript rules

Pass: private

## Rules

| Rule | Decision | Reason |
|---|---|---|
| no-unknown-returns | on | |
| no-module-mocking | off | the payment SDK cannot run locally, and its fake is the seam |

## Exceptions

| Rule | File | Reason |
|---|---|---|
| no-runtime-typeof | src/legacy/*.ts | parsed upstream, to be removed with the legacy client; approved 2026-11-25 |
```

| The entry | The pass |
|---|---|
| missing | does not run; the language was never offered, or the repo does not use it. `setup-repo` offers it |
| `Pass: off` | does not run; the user declined it |
| `Pass: private` | runs; the agent fixes what blocks |
| a route | does not run: the rules live in the repo's own linter, which its lint command and CI run |

- **Rules.** `on` blocks; `off` turns the rule off for the pass and for review, with its reason. An id the table does not list is not decided yet, such as a rule the framework added since: its findings show without blocking, and the reply lists them so the user decides. A rule with no check in the pack, such as `discriminated-unions`, takes a decision too; review then follows it.
- **Exceptions.** One rule and one file pattern, with the reason and the date the user approved it. A finding an exception covers does not show.
- **Never in the code.** A disable comment that names a rule of the pack is a blocking finding: it leaves a trace the team did not choose, and it hides the exception from the next agent. The exception goes in the table.
- **Only the user decides.** An agent proposes a decision or an exception, with the finding that motivates it; after the user's yes, it writes the line in the project folder.

## Run it

From the root of the target repo, with the task's base:

```text
python -I <constitution>/lint/lint_diff.py --base <base>
```

`<constitution>` is the folder that holds this `references/` folder. The first run installs the pack's pinned tools in `~/.agents/cache/lint/`, which needs Node.js; the pack names the versions its tools support. Later runs take seconds.

| Exit | Means | Do |
|---|---|---|
| 0 | nothing blocks | list the findings on rules not decided yet in the reply, if any |
| 1 | a finding on an `on` rule, on a line the change adds or edits | fix the code; the message says how. Only the user's decision or exception lets it stay |
| 2 | the pass could not run | the message says why and how to fix it. Put it under Not verified; the repo's own checks still decide green |

The pass reads only the files the diff touches with the pack's extensions, so a change with no such file runs nothing.

## Shared rules

When the user shares a pack, its checks join the repo's own linter through a PR, and the entry becomes a route to that linter's config. `--export <dir>` writes the built plugin and its license, and prints what to register. Oxlint and ESLint load it. Biome and other linters cannot: such a repo keeps the pass private, or shares it later through `/add-guardrail`, which can add Oxlint beside them when the team agrees. Shared, the decisions are the config's own: a rule turned off there, or an override for some files, is the team's call, made by PR.

## In review

The verifier in `standards` reads the entry. A rule turned off is not judged, in the pass or in prose. It reruns the pass on the head: a blocking finding the builder left is a should, quoted with its rule and `file:line`, since the user's decision made it this repo's standard. A finding on a rule not decided yet is a note.
