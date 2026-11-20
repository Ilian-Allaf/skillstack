# build-the-lever

**Apply when** the work is not trivial: edits across many files, a migration, an analysis, a check, anything a reviewer would otherwise have to redo by hand to trust.

**Rule.** Build the tool that does the work or proves it, instead of working by hand. A script does the work the same way every time, reruns for free, and turns "trust me" into "run this".

## How

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning it on that unit and diffing against your hand-made version. Make it safe to rerun (`make-operations-idempotent`).
- A codemod or script for edits, a generator for repetitive files, a query for analysis, a rerunnable check for verification.
- A deterministic tool beats fan-out. If a script can process every unit in one pass, run it; do not spread subagents to apply by hand what a script can do.
- When you do fan work out, write the recipe, the check, and the files not to touch in one file every subagent reads, outside their write scope.
- Build the smallest script that does the job, never a framework (`make-the-smallest-change`). Commit it when the work outlives the session.

The bar is triviality, not repetition: a one-off still earns a tool when the tool is what makes the work checkable.

## Test

Applying this principle produces a file. If it is cited and the diff holds no script, codemod, generator, or check, it was not applied.

## Sign it was skipped

Forty files edited by hand with the same change. A claim of "checked every caller" with no command to replay it.
