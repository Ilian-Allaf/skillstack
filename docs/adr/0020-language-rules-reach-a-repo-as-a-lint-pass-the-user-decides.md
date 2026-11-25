# 0020. Language rules reach a repo as a lint pass the user decides, rule by rule

- **Status**: accepted, 2026-11-25
- **Extends**: [0016](0016-the-working-files-live-outside-the-repo.md), with one more entry of the project folder, `lint/<language>.md`, whose shared form is the repo's own lint config. The rest of 0016 stands.
- **Applies to**: `skills/constitution/references/languages/`, `skills/constitution/references/lint.md`, `skills/constitution/lint/`, `skills/constitution/references/target-repo.md`, `skills/setup-repo/` (steps 3, 6, 7, 10, `references/language-rules.md`), `skills/ship/references/clean.md`, `skills/verify-pr/references/lanes.md` (`standards`)
- **Enforced by**: `skills/constitution/lint/lint_diff.py`, which blocks a finding on a rule decided `on` and a disable comment naming a rule of the pack, with its tests in `tools/test_lint_diff.py`; each check of the TypeScript pack has a rule test, run by `tools/run_lint_packs.py` in `tools/check.py`. The rest by review.

## Context

The TypeScript rules were prose, read by the builder and the verifier when a diff touched a `.ts` file. Prose is the weakest level of [add-guardrail's levels](../../skills/add-guardrail/references/levels.md): nothing fails, and an agent may skip it. On 2026-11-25 the user asked for TypeScript good practice out of the box, applied only where the repo uses TypeScript, so that another language can follow the same way, such as Go. They want one coherent system with the project folder of 0016, where they decide at a fine grain, and a setup that stays simple.

A third-party rule set of Oxlint checks (see `docs/sources.md`) holds many rules of the kind we want. Tried on 2026-11-25:
- A config and a plugin stored outside the repo lint it, with no file in the repo, and ignore the repo's own ESLint, Biome, or Oxlint config.
- The same plugin, built to one JavaScript file, loads in a repo's ESLint 9.
- Oxlint runs it on Node 20.19+ or 22.12+; on Node 20.10, npm skips its native binary without an error.
- A disable comment in the code silences a check of the pass, and Oxlint has no flag to ignore such comments.

## Decision

- **Ids, decided per repo.** Each rule of a language file has an id. The user decides `on` or `off` per id in `~/.agents/projects/<project>/lint/<language>.md`. One decision governs both the pass and review, so a rule turned off is not judged in prose either.
- **A pack beside the constitution.** The checks of the rules a linter can hold ship in `skills/constitution/lint/<language>/`. The pass runs them on the lines a change adds or edits, never on code the change did not touch. Their tools install once in `~/.agents/cache/lint/`, so nothing is written in the repo.
- **Offered only for a language of the code.** TypeScript counts with a `tsconfig.json` or TypeScript source. It does not count when TypeScript appears only in tooling files. A JavaScript-only repo is not offered the pack. The pass reads only the files of its language.
- **Private by default.** Shared means the checks join the repo's own linter through a PR, and the entry is a route to its config. This is offered only where that linter loads the plugin: Oxlint or ESLint. A repo linted by Biome or another linter keeps the pass private or off.
- **New rules wait for the user.** An id the entry does not list shows its findings without blocking, until the user decides it. A rerun of `setup-repo` asks only about those ids.
- **Exceptions live in the entry.** An exception is a rule, a file pattern, and the reason. A disable comment that names a rule of the pack blocks.
- **Two levels, as in 0016.** The framework's defaults, then the project's decisions. There is no user-wide layer.
- **The first pack copies 15 rules of that set.** Three of its general rules stay out: one is about a word in names, one is about blank lines, which the repo's formatter owns, and one is a performance preference whose fix depends on the runtime. Its rules for one library stay out too: a pack is per language. Two of its rules contradicted our prose, so the prose changed. `typeof` now narrows only inside a type guard, and a schema is called at the boundary instead of a helper that takes `unknown`.

## Alternatives rejected

- **The type-aware preset the rule set's author recommends instead.** It reads the repo's types and installed packages, needs a beta backend and Node 22.18+, and runs only in Oxlint. It cannot run outside the repo, nor in a repo's ESLint.
- **Installing Oxlint in every TypeScript repo.** That imposes a tool on a team that did not choose it (0016).
- **Prose only.** Nothing fails.
- **Linting whole files.** Old code would block every task, and the user would have to turn rules off to work at all.
- **New framework rules on at once.** A PR would turn red on a rule the user never chose.
- **A user-wide layer, `~/.agents/defaults/`.** It would add a third home for every decision, glossary and standards included. We will add it on the first real need.

## Consequences

- The pass needs Node.js in the versions the pack names. Otherwise it exits 2 with the fix, and the builder lists it under Not verified. CI sets up Node 22. On a laptop without a supported Node, `tools/check.py` skips the rule tests with a warning, and CI still runs them.
- The copied rules change only by hand. The upstream commit is in `docs/sources.md`, so an update can diff against it.
- Another language follows the same way: a language file with ids, then a pack whose tool the runner learns to call.
