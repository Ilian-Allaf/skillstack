# Playbook: bespoke

For work no other playbook fits: a migration across many call sites, an ambitious change in several parts, or a long run the user reviews after stepping away. The first deliverable is the playbook itself, a list of phases the user can read; the code follows it.

One builder keeps the whole task in one context and lands it as an ordered series of small PRs. It does not split the work across parallel subagents by default: work that looks independent is often tangled. Fan out only across seams proven separate, each worker in its own worktree.

1. **Frame with numbers.** `done_when` as a yes-or-no check on the real product; the scope counted (call sites, files, screens) with a rough effort; the blockers found while reading; and the rigor, biased high: one-way doors and wide blast radius get more gates. This, with the phase list of step 2, is what the frame shows the user, as for any task.
2. **Design the phases** (`sequence-verifiable-units`). Units that each land green on their own, riskiest unknown first. The check comes before the work: capture the baseline from the base, so every later check reads "old value against new value". Each phase follows [design.md](../design.md) like any build; a one-way-door shape is always sketched twice. Write the phase list in the PR and in the [decision log](../../../constitution/references/decision-log.md).
3. **Wide change: expand, migrate, contract.** When one mechanical change fans across the whole codebase (rename a column, retype a shared symbol), no single slice can land green. Add the new form beside the old, so nothing breaks. Migrate callers in batches sized by blast radius, each batch its own PR, each green because the old form still exists. Delete the old form in a last PR once no caller is left. This is the one place an old path may live for a while, and only until the contract PR.
4. **Each unit is an experiment.** State the hypothesis, make the smallest change, check it on the real artifact, keep it if it moved `done_when`, revert it if not. A unit that passes too easily: suspect the check before the code. A worker that games a check: reset it and harden the brief. A check that is wrong gets fixed in its own change, never routed around.
5. **Keep the trail.** One row per decision as each unit lands, not at the end.
6. **Check the whole.** Run `done_when` on the real product, not only the harness. A correction that came back twice becomes a candidate for `/add-guardrail`.

## The flow of units

Each unit is one PR, on a branch stacked on the previous unit. For each unit, run steps 2 to 7 of `ship`: build, clean, prove, analyze impact, open, verdict. The narrow rule of `done_when` applies per unit; the whole task keeps its own `done_when`, checked in step 6 above. Do not babysit each PR as it opens: it stalls the build and spends checks on commits a later unit restacks. Run `babysit-pr` once over the stack when the last unit has its verdict. The user merges the units in order.

The coverage table of each PR lists its unit's cases. The last PR's table covers `done_when` end to end. The verifier checks that each PR is green alone, and that the contract PR leaves no caller of the old form.
