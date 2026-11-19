# Lanes

Each lane answers one question. The risk class picks the lanes (see [proof.md](../../constitution/references/proof.md)). Every lane returns each finding with a title and its run: the exact command, the output it printed, and the output the task requires. A lane that finds nothing says what it tried.

## Behavior axis

### `replay`: does the builder's proof hold?

Run every command in the PR's Proof section on the head SHA, the demo scripts included, and those of its Breakage section once your own `breakage` lane has run. Compare the output with what the PR claims. A claim whose command fails or prints something else is a finding. Check the coverage table against the evidence: a row whose evidence is missing, or a demo chapter that does not show the expected result, is a finding.

### `live`: does the app do what `done_when` says?

Drive the real app with the repo's `drive-<app>` skill, on the base and then on the head. Do not follow the builder's journey; build your own from `done_when` and the feature map. Try every entry point the map lists for the touched feature, then try what a real user would: double clicks, back navigation, reload mid-action, empty and long input, slow network.

Then test the coverage itself (see [coverage.md](../../constitution/references/coverage.md)). List the cases you would have expected from the feature map, `done_when`, and the hard zones, and drive each one the table lacks. A missing case that misbehaves is a FAIL. A missing case that behaves correctly is a coverage gap: report it with your evidence, so the builder adds it to the table.

Find the drivers as [proof.md](../../constitution/references/proof.md) describes. When no driver exists for a surface the change touches, this lane returns INCONCLUSIVE for it, with that reason. It never falls back to reading code.

### `breakage`: what does it break elsewhere?

Run [analyze-impact](../../analyze-impact/SKILL.md) on the diff yourself. Compare your safety fact with the one in the PR's Breakage section. A different fact, or a confirmed risk the PR does not list, is a finding.

### `adversarial`: can someone break it? (`high` only)

Run a swarm of three subagents racing on one brief, as [parallel.md](../../constitution/references/parallel.md) describes, from different model families when available, each in its own worktree with the head checked out. Give each this brief:

> Break this change. Prove each finding with a run against the real code: a failing test, a repro script, or command output that shows the wrong behavior. Report each finding with a title, the exact command, the output it printed, and the output the task requires. Leave out anything you did not run, including style, naming, and risks that need a future change to matter. No findings is a valid result.

Rerun each returned command yourself and keep what reproduces. Merge findings with the same root cause.

## Code axis

### `spec`: does the code do what was asked, all of it, and nothing more?

Compare the diff with the task and `done_when`. Find missing parts of the request, parts the diff adds that nobody asked for, and tests that do not test the asked behavior (tautological tests, tests coupled to internals, mocks of internal collaborators). Run the tests that claim to cover the change after reverting the fix: a test that still passes is a finding. Then check the duties of the PR's playbook, listed at the end of each [playbook](../../ship/references/frame.md#playbooks) as what the verifier checks.

### `standards`: does the code follow the repo's standards?

Read `CODING_STANDARDS.md`, `CONTRIBUTING.md`, the agent files, the repo glossary, the accepted ADRs whose Applies to covers the diff, and the [language rules](../../constitution/references/languages/typescript.md) for the languages the diff touches. Check the diff against them. Then apply the smell baseline: mysterious name, duplicated code, feature envy, data clumps, primitive obsession, repeated switches, and the signs of a skipped domain model: an if/else chain over a domain state that grew one branch, a second boolean that must stay in sync with the first, the same domain rule repeated in modules named after steps (`model-the-domain`). A documented repo standard wins over the baseline. Skip what a linter already enforces. A breach of a documented standard, quoted with its file, rule, and hunk, is a should (see [verdict.md](verdict.md)). Smells are judgment calls, so they are notes unless a repo standard makes them rules.
