# separate-before-serializing-shared-state

**Apply when** concurrent actors could write the same file, row, key, branch, or object: threads, processes, requests, jobs, or parallel subagents.

**Rule.** Remove the sharing first. Serialize only what cannot be separated, and then by structure, never by convention.

## How

1. List the shared mutable state: what two actors both write, or one writes while another reads.
2. Ask whether they need one canonical object or are publishing independent facts. Give each actor its own file, key, row, worktree, or branch, and merge where the data is read. Two workers writing their own field into one shared file still share it; one file per worker does not.
3. Only when one shared target is a real invariant, serialize access by structure: a single writer, sequential phases, a lock, or an atomic compare-and-swap. "We need a lock" is a smell to check first, not the default answer.

## Test

For each piece of shared state: what happens if another actor changes it right now? The answer is "nothing", or a named structure prevents it.

## Sign it was skipped

A lock added after a flaky test. A rule in a comment ("call this only from the main thread") instead of a structure that enforces it. Two subagents in one worktree.

## Example

```ts
// Skipped: every worker rewrites one shared object; the last write wins.
const state = JSON.parse(await fs.readFile("state.json", "utf8"));
state.lastIndexedAt = now;
await fs.writeFile("state.json", JSON.stringify(state));

// Applied: each worker owns its file; the reader merges.
await writeAtomic(`state/${workerId}.json`, { lastIndexedAt: now });
const status = mergeStatus(await readAll("state/"));
```
