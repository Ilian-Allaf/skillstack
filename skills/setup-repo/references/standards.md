# Coding standards

The standards of a repo come from what its code and its reviews already do, not from a generic list. Each one ends in one of two places: a check, when a tool can hold it, or the coding standards, when only judgment can: `coding-standards.md` in the project folder, or `CODING_STANDARDS.md` when the user shares it. See [target-repo.md](../../constitution/references/target-repo.md).

## Find them

- **The tools' settings**: the linter and type checker config, the formatter, the rules turned on and off. What they already enforce needs no line anywhere.
- **The code's habits**: how errors are handled, where validation happens, how modules are split, how state is owned, how tests are written and where they live. A habit counts when most of the code follows it; cite three places that do.
- **The reviews**: recent review comments and reverts, which show what the team corrects again and again.
- **The repo's docs**: a contributing guide or a style guide already written by the team.

## Sort each one

| It is | Example | Goes to |
|---|---|---|
| mechanical: a tool can fail on it | "components never import the store directly" | the report, as a candidate for `add-guardrail` |
| a judgment call: two good engineers could disagree on a given diff | "prefer a new module over growing a file past one responsibility" | the coding standards |
| already enforced by a tool | "no unused imports" with the lint rule on | nowhere |
| what the code does not do yet | "every endpoint validates its input" when half of them do not | the report, as a gap, never as a standard |

## Write a judgment call

One line for the rule, then one real example from this repo with its `file:line`, and when the rule does not apply. A standard the verifier cannot recognize in a diff is not a standard.

## Languages

The constitution has diff rules per language in its `languages/` folder. Name each language of the repo that has no file there yet; the report lists it as a gap to fill in the framework, in its own PR.
