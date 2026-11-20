# keep-the-codebase-clean

**Apply when** you are about to open a PR, and on every file you leave behind.

**Rule.** The next agent copies what you leave. Remove slop, stale comments, and workarounds before anyone reads the diff.

## How

- Remove dead code, debug output, commented-out code, comments that narrate the change, and guards that only "might help".
- A comment survives only for a non-obvious why the code cannot show. A comment that explains a surprise in our own code means the code should change instead.
- A test or check script states its steps in its assertions and log strings, not in phase comments.
- `ship`'s clean step runs the comment hunter for this.

## Test

Would you want the next agent to copy every hunk of this diff?

## Sign it was skipped

A `// Phase 1` comment. A `console.log` left in. An `IMPORTANT: do not remove` with no check behind it.
