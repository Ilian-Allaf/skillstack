# Language rules

The constitution's language files state rules with ids, and a pack holds the checks for those a linter can hold ([lint.md](../../constitution/references/lint.md)). This part asks the user, once per language, whether the lint pass applies them in this repo, and writes the answer to `~/.agents/projects/<project>/lint/<language>.md`.

## Offer only the languages of the code

A language is offered when it is a language of the repo's code, and the constitution has a pack for it.

| The repo has | TypeScript |
|---|---|
| a `tsconfig.json`, or `.ts`, `.tsx`, `.mts`, `.cts` files in its source | offered |
| TypeScript only in tooling: `vite.config.ts`, `*.d.ts`, scripts the build does not ship | not offered |
| JavaScript only | not offered: most rules are about type annotations, which JavaScript does not have |
| several languages, such as Go and TypeScript | offered for TypeScript; the pass reads only TypeScript files |

A language of the code with no language file is a gap, as [standards.md](standards.md) says. One with a file but no pack has nothing to offer: its rules are read in review only.

## Propose a decision per rule

Run the pack on the whole repo, from its root: `python -I <constitution>/lint/lint_diff.py --all --language <language>`. It counts the findings per rule; it needs the Node.js versions the pack names, and when it cannot run, the plan says so and proposes every rule on.

Every id of the language file starts `on`, except:

- **The repo's linter already holds it.** Its config turns on a rule that catches the same code. Propose `off`, with that rule as the reason: one check per mistake.
- **The repo's code does the opposite on purpose.** Most files where the rule applies break it, as a habit of [standards.md](standards.md) counts. Propose `off`, with the count, so the user sees what the rule would fight.

Findings in a few files are not a reason: the pass reads only the lines a change adds or edits, so old code never blocks a task.

## Ask once

The plan of step 3 holds one question per language, with the recommended answer first:

```text
TypeScript rules (this repo lints with ESLint)
  ● Private (recommended): the agent applies them, nothing enters the repo
  ○ Shared: a PR adds them to your ESLint config, and CI applies them
  ○ No
  Proposed off: no-runtime-typeof (the code uses typeof in 41 of 52 files).
  Every other rule on.
```

Offer Shared only when the repo lints with Oxlint or ESLint, which can load the pack; with another linter, the choices are Private and No. The user can flip any rule in the same answer. A rerun of `setup-repo` asks again only about ids the entry does not list yet, the rules the framework added since.

## Write the answer

- **Private.** Write the entry with `Pass: private`, a Rules table with every id of the language file and its decision, and the reason of each `off`.
- **No.** Write the entry with `Pass: off` and nothing else, so a rerun does not ask again.
- **Shared.** In the docs PR of step 7: run `lint_diff.py --export <dir>` with a folder the repo's tooling layout suggests, add the printed dependency at its exact version, and register the plugin and the rules decided `on` in the repo's lint config, by the smallest diff. A rule with findings on the base starts off in that config, listed in the PR as a candidate for `/add-guardrail`, so CI stays green on the day it merges. The project folder holds a route to the lint config: `This lives in the repo at <config path>. Read it there instead.`

Done when the entry exists for each language offered, private, off, or a route, and the report lists each rule proposed off with its reason.
