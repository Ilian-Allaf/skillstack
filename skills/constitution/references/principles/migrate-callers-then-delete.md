# migrate-callers-then-delete

**Apply when** an internal API changes shape, or a new way replaces an old one.

**Rule.** Move every caller and delete the old API in the same PR. No shim, no parallel old and new path: the next agent copies whichever it finds first.

## How

- Find every caller, including the ones in strings, config, docs, tests, and generated code. Spot-check each rename against the files; renames miss usages silently.
- Use a codemod or a script when the callers are many (`build-the-lever`).
- Update the tests to assert the new contract, and delete the tests that only protected the old implementation.
- When a shared primitive improves, every consumer gets the improvement in the same change, and each one is checked.
- One exception: a wide change that cannot land green in one PR uses expand, migrate, contract (the `bespoke` playbook). The old form lives only until the contract PR.
- This holds while no external user depends on the old API. A public API with outside users needs a deprecation path, which is a one-way door.

## Test

After the change, a search for the old name returns nothing.

## Sign it was skipped

A `legacy`, `old`, or `v1` symbol beside its replacement. A function that only forwards to its replacement. Two ways to do one task.
