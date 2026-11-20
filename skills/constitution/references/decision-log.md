# Decision log

A trail of decisions for long or unattended work, so the user can come back and trust the result. Skills that need a trail point here instead of inventing one.

## When

- a run that lasts hours, a `bespoke` playbook, or any run the user is not watching;
- a short task needs none: the PR's Decisions section is enough.

## Format

One TSV file, one row per decision, one line per cell. Evidence is a pointer, never a paragraph.

```text
ts	phase	decision	why	evidence	result
2026-05-24T09:40:00Z	harness	took screenshots of every screen before changing anything	so old and new can be compared	scripts/snapshot.sh, baseline/	120 reference screenshots
2026-05-24T12:30:00Z	widget	threw out a subagent's work because its screenshots were blank	checked the files instead of its summary	worktree reset	reverted, brief tightened
```

- **decision**: what was chosen or done, in plain words, as you would tell a teammate.
- **why**: the reason. Name a principle in plain words if one drove it.
- **evidence**: a commit, a PR, a `file:line`, or an artifact path.
- **result**: the outcome: `tests green`, `reverted`, `pixel diff 0`, `INCONCLUSIVE`, `open`.

Log forks, units finished with their check, pivots and reverts with their trigger, blockers, and fixed gates. Skip the obvious.

## Rules

- **Append only.** A wrong call gets a new row that supersedes it. Never edit or delete a row.
- **Where.** `decisions.tsv` in the work directory, out of git. Commit it with the PR only when the reviewer needs it to trust the work; link it from Decisions.
- **A new run says so.** A run that adds to an existing log starts with a row of phase `start` that names itself.

## Before handing back

1. **Audit the log against what happened.** Every row maps to a real decision; every pointer resolves and shows what the row claims. A fork or revert that shaped the work but has no row is a gap: add it. Correct with new rows, never by editing.
2. **Have it read by another family.** Spawn a fresh subagent, from another model family when available, to read the log and flag: decisions with weak evidence, checks claimed without proof, choices that look risky in hindsight, and gaps a quick skim would miss. Its flags go in the reply under "Attention", with the reviewer's model named. "No flags" is a valid result.
