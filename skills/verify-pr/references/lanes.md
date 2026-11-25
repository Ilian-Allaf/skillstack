# Lanes

Each lane answers one question. The risk class picks the lanes (see [proof.md](../../constitution/references/proof.md)). Every lane returns each finding with a title and its run: the exact command, the output it printed, and the output the task requires. A lane that finds nothing says what it tried.

## Before the lanes

Your brief holds the task, the spec issue when the task comes from one, `done_when`, the case list, risk class, playbook, the PR number, the head SHA, the path of the verifier's SKILL.md, driver paths (`~/.agents/projects/<project>/drive-*/SKILL.md`, or the repo files their routes name), the paths of the formal checks that cover a touched file (`~/.agents/projects/<project>/prove-*/SKILL.md`, or the repo files their routes name), and safe startup and access instructions. Keep it factual: the builder's reasoning, notes, impact report, and prior verdicts stay out. Name anything that leaked, including diagnostic text exposed by the code host, and record your model family.

When the user launched you with a PR number alone, build that brief yourself: extract the task, `done_when`, case list, risk class, and playbook from the PR body through a filtered view, the spec issue from its `Part of` line, and the head SHA from the code host. If the view exposes diagnoses, record the leak. Missing startup or access instructions stay an explicit limit. A PR with no `done_when` or no risk class, such as a colleague's, gets its task inferred from its title and description and the class `medium`, both said in the verdict header; `replay` then runs only what the PR claims.

## Behavior axis

### `replay`: does the builder's proof hold?

Run every command in the PR's Proof section on the head SHA, the demo scripts included, and those of its Breakage section: after your own `breakage` lane when you run it, at the end of this lane when you do not. Compare the output with what the PR claims. A claim whose command fails or prints something else is a finding. Check the coverage table against the evidence: a row whose evidence is missing, or a demo chapter that does not show the expected result, is a finding.

### `live`: does the app do what `done_when` says?

Drive the real app with the repo's `drive-<app>` skill, on the base and then on the head. When the brief holds a spec issue, read it yourself and start from its journeys and promises: drive each story's journey and each promise, by its id. Do not follow the builder's journey; build the rest of yours from `done_when` and the feature map. Try every entry point the map lists for the touched feature, then try what a real user would: double clicks, back navigation, reload mid-action, empty and long input, slow network.

List and drive the cases you would have expected from the spec, the feature map, `done_when`, and the hard zones. Save those results before reading the coverage table, then test the coverage itself (see [coverage.md](../../constitution/references/coverage.md)). A spec story, promise, or visual target missing from the table is a missing case like any other. A missing case that misbehaves is a FAIL. A missing case that behaves correctly is a coverage gap: report it with your evidence, so the builder adds it to the table.

When the spec holds visual targets, capture the head yourself at each still target's state and width, and record it at each motion target, side by side with the target, before you look at the builder's images. A finding is one of: a measured check the Visual targets take that fails, an effect of a motion target missing or outside its tolerance, or a ban they take that a command detects on the head; [verdict.md](verdict.md) grades it. Any other judgment of taste is a note, against the criteria of [ui.md](../../constitution/references/ui.md).

Find the drivers as [proof.md](../../constitution/references/proof.md) describes. When no driver exists for a surface the change touches, this lane returns INCONCLUSIVE for it, with that reason. It never falls back to reading code.

### `breakage`: what does it break elsewhere?

Run [analyze-impact](../../analyze-impact/SKILL.md) on the diff yourself and save the result. After the independent lanes finish, compare your safety fact with the one in the PR's Breakage section. A different fact, or a confirmed risk the PR does not list, is a finding.

Judge each formal check made or repaired in the task, and each one in sync on the base whose covered code the change alters, as it now stands, against the rules of [formal.md](../../constitution/references/formal.md). Each part the PR changed points at the head's code by its `file:line`. Break the guarded code once in your worktree, as formal.md's Able to fail rule says for a model and for a harness, and run the check: a break it misses is a FAIL graded should, since the coverage row of its property no longer shows its case. A property reworded without evidence that the promise changed on purpose, or a bound reduced without a line in Proof, is a finding. Such a check left stale at the head is a FAIL graded should. Compare a repaired check with its base version, from git for a shared check and from the copy the builder saved for a private one ([formal.md](../../constitution/references/formal.md#in-a-task)): a property weakened, a bound cut, or an assumption added that the PR's Proof does not justify is a finding. A check stale on the base that the task left unrepaired is a finding, unless its case sits under Not verified with the reason the repair failed.

### `adversarial`: can someone break it? (`high` only)

Run a swarm of three subagents racing on one brief, as [parallel.md](../../constitution/references/parallel.md) describes, from different model families when available, each in its own worktree with the head checked out. Give each this brief:

> Break this change. Prove each finding with a run against the real code: a failing test, a repro script, or command output that shows the wrong behavior. Report each finding with a title, the exact command, the output it printed, and the output the task requires. Leave out anything you did not run, including style, naming, and risks that need a future change to matter. No findings is a valid result.

Rerun each returned command yourself and keep what reproduces. Merge findings with the same root cause.

## Code axis

### `spec`: does the code do what was asked, all of it, and nothing more?

Compare the diff with the task and `done_when`, and with the spec issue when the brief holds one. Find missing parts of the request, parts the diff adds that nobody asked for, and behavior the spec's Out of scope excludes, and tests that do not test the asked behavior (tautological tests, tests coupled to internals, mocks of internal collaborators). Run the tests that claim to cover the change after reverting the fix: a test that still passes is a finding. With visual targets, a new component the spec's design mode does not allow is a part nobody asked for. Then check the duties of the PR's playbook, listed at the end of each [playbook](../../ship/references/frame.md#playbooks) as what the verifier checks.

### `standards`: does the code follow the repo's standards?

Read `coding-standards.md` in the project folder, `CONTRIBUTING.md`, the agent files, the repo glossary, the accepted ADRs whose Applies to covers the diff, and the [language rules](../../constitution/references/languages/typescript.md) for the languages the diff touches. Check the diff against them. When the diff changes what a user sees, read [ui.md](../../constitution/references/ui.md) too: its rules yield notes, since what a spec took from it is for `live` to check. Then apply the smell baseline: mysterious name, duplicated code, feature envy, data clumps, primitive obsession, repeated switches, and the signs of a skipped domain model: an if/else chain over a domain state that grew one branch, a second boolean that must stay in sync with the first, the same domain rule repeated in modules named after steps (`model-the-domain`). Check the shape of the diff against the [red flags](../../ship/references/design.md#red-flags). Then read the full form of each principle the PR's Decisions and Design section cite, and of each principle whose Apply when in [principles.md](../../constitution/references/principles.md) matches the diff, and check the diff against its Sign it was skipped. A principle cited under Decisions that the diff contradicts is a note. When the PR has a Design section, compare the diff with its Shape: a departure that Deviations does not list is a note. A documented repo standard wins over the baseline. Skip what a linter already enforces. A breach of a documented standard, quoted with its file, rule, and hunk, is a should (see [verdict.md](verdict.md)). Smells are judgment calls, so they are notes unless a repo standard makes them rules.
