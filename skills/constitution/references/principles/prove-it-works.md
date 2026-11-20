# prove-it-works

**Apply when** you are about to report a task done, or to trust an output.

**Rule.** Check the real artifact: run the feature, read the stored value, inspect the diff. A proxy, a self-report, or "it compiles" is not a check.

## How

- Check the real thing, not a sign of it: the process itself, not a derived state; the stored value, not a cached copy; the running app, not a screenshot from before.
- Script the check when you can. A script reruns the same comparison and leaves an artifact a reviewer can replay; a one-time look does not. The certainty levels are in [proof.md](../proof.md).
- When a check fails, suspect the way you observed before you suspect the system. When it passes too easily, suspect it too.
- A subagent's report is a claim until you open what it produced.

## Test

Could the user replay your evidence and see the same thing?

## Sign it was skipped

"Tests pass" as the only evidence of a user-facing change. A report that quotes a subagent's summary without its artifact.
